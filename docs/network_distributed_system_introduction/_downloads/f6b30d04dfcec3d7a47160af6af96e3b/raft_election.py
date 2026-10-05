"""Raft のリーダー選出を離散イベントシミュレーションで示すサンプル。

5 つのノードからなる Raft クラスターについて、次の流れを時刻付きの
ログで表示します。

* 各ノードはフォロワーとして起動し、ランダムな選挙タイムアウト
  （150〜300 ms）を設定する
* 最初にタイムアウトしたノードが term を 1 増やして候補者になり、
  他のノードに RequestVote を送る
* 過半数（5 台中 3 票）を得た候補者がリーダーになり、ハートビート
  （中身が空の AppendEntries）を定期的に送る
* 複数のノードが同時に候補者になって票が割れ、誰も過半数を得られない
  場合は、次にタイムアウトしたノードが term を増やして再選挙する
* リーダーが故障すると、フォロワーはハートビートが届かなくなって
  タイムアウトし、新しいリーダーが選ばれる
* 故障したノードが復帰すると、より大きな term を知ってフォロワーに戻る

簡単にするため、ログ複製は省略しています。そのため、RequestVote で
候補者のログが十分に新しいかどうかを確かめる条件も省いています。
また、メッセージの紛失はなく、遅延は 2〜10 ms のランダムな値です。
乱数のシードを固定しているので、実行結果は毎回同じになります。

時刻は模擬時計の値（ms）で、実際の時間は経過しません。

実行方法:
    python raft_election.py
"""

import heapq
import itertools
import random
from dataclasses import dataclass, field
from functools import partial
from enum import Enum
from typing import Callable

NUM_NODES = 5
MAJORITY = NUM_NODES // 2 + 1
ELECTION_TIMEOUT = (150, 300)  # ms
HEARTBEAT_INTERVAL = 50  # ms
NETWORK_DELAY = (2, 10)  # ms
END_TIME = 1500  # ms
CRASH_TIME = 500  # リーダーを故障させる時刻
RECOVER_TIME = 1000  # 故障したノードを復帰させる時刻


class Role(Enum):
    FOLLOWER = "フォロワー"
    CANDIDATE = "候補者"
    LEADER = "リーダー"


@dataclass(order=True)
class Event:
    """時刻順に処理するイベント。"""

    time: int
    seq: int
    action: Callable[[], None] = field(compare=False)


class Simulator:
    """イベントを時刻順に取り出して実行する。"""

    def __init__(self) -> None:
        self.now = 0
        self._queue: list[Event] = []
        self._seq = itertools.count()

    def schedule(self, delay: int, action: Callable[[], None]) -> None:
        heapq.heappush(self._queue,
                       Event(self.now + delay, next(self._seq), action))

    def run(self, until: int) -> None:
        while self._queue and self._queue[0].time <= until:
            event = heapq.heappop(self._queue)
            self.now = event.time
            event.action()


class Node:
    """Raft のノード（リーダー選出の部分だけ）。"""

    def __init__(self, node_id: int, sim: Simulator,
                 rng: random.Random) -> None:
        self.id = node_id
        self.sim = sim
        self.rng = rng
        self.peers: list[Node] = []
        self.alive = True
        self.role = Role.FOLLOWER
        self.term = 0
        self.voted_for: int | None = None
        self.votes = 0
        # タイマーの世代番号。リセットのたびに増やし、古いタイマーを無効化
        self.timer_gen = 0

    def log(self, message: str) -> None:
        print(f"[{self.sim.now:5d} ms] ノード {self.id} "
              f"(term {self.term}, {self.role.value}): {message}")

    # ---- タイマー ----
    def reset_election_timer(self) -> None:
        self.timer_gen += 1
        gen = self.timer_gen
        timeout = self.rng.randint(*ELECTION_TIMEOUT)
        self.sim.schedule(timeout, lambda: self.on_election_timeout(gen))

    def on_election_timeout(self, gen: int) -> None:
        if not self.alive or gen != self.timer_gen:
            return  # 故障中、またはタイマーがリセット済み
        if self.role == Role.LEADER:
            return
        self.start_election()

    # ---- 選挙 ----
    def start_election(self) -> None:
        self.term += 1
        self.role = Role.CANDIDATE
        self.voted_for = self.id  # 自分に投票
        self.votes = 1
        self.log("選挙タイムアウト。候補者になり RequestVote を送信")
        self.reset_election_timer()  # 票が割れたら再選挙するため
        term = self.term
        for peer in self.peers:
            self.send(partial(peer.on_request_vote, term, self))

    def on_request_vote(self, term: int, candidate: "Node") -> None:
        if not self.alive:
            return
        self.observe_term(term)
        granted = (term == self.term
                   and self.voted_for in (None, candidate.id))
        if granted:
            self.voted_for = candidate.id
            self.reset_election_timer()
            self.log(f"ノード {candidate.id} に投票")
        elif term == self.term:
            self.log(f"ノード {candidate.id} への投票を拒否"
                     f"（ノード {self.voted_for} に投票済み）")
        cur = self.term
        self.send(lambda: candidate.on_vote_reply(cur, granted))

    def on_vote_reply(self, term: int, granted: bool) -> None:
        if not self.alive:
            return
        self.observe_term(term)
        if self.role != Role.CANDIDATE or term != self.term:
            return  # 古い選挙への返事は無視
        if granted:
            self.votes += 1
            if self.votes == MAJORITY:
                self.become_leader()

    def become_leader(self) -> None:
        self.role = Role.LEADER
        self.log(f"{self.votes} 票を得て過半数。リーダーに当選")
        self.send_heartbeats(first=True)

    # ---- ハートビート ----
    def send_heartbeats(self, first: bool = False) -> None:
        if not self.alive or self.role != Role.LEADER:
            return
        if first:
            self.log(f"ハートビートの送信を開始（{HEARTBEAT_INTERVAL} ms ごと）")
        term = self.term
        for peer in self.peers:
            self.send(partial(peer.on_heartbeat, term, self))
        self.sim.schedule(HEARTBEAT_INTERVAL, self.send_heartbeats)

    def on_heartbeat(self, term: int, leader: "Node") -> None:
        if not self.alive or term < self.term:
            return  # 古いリーダーからのものは無視
        if term > self.term:
            self.log(f"リーダー {leader.id} のハートビートで新しい "
                     f"term {term} を知る")
        self.observe_term(term)
        if self.role == Role.CANDIDATE:
            self.role = Role.FOLLOWER
            self.log(f"リーダー {leader.id} のハートビートを受信。"
                     "フォロワーに戻る")
        self.reset_election_timer()

    # ---- 共通 ----
    def observe_term(self, term: int) -> None:
        """自分より大きな term を見たら、その term のフォロワーになる。"""
        if term > self.term:
            old_role = self.role
            self.term = term
            self.voted_for = None
            self.role = Role.FOLLOWER
            if old_role != Role.FOLLOWER:
                self.log(f"より大きな term {term} を知り、フォロワーに戻る")

    def send(self, deliver: Callable[[], None]) -> None:
        """ネットワーク遅延の後にメッセージを届ける。"""
        if self.alive:
            self.sim.schedule(self.rng.randint(*NETWORK_DELAY), deliver)

    def crash(self) -> None:
        self.log("*** 故障 ***")
        self.alive = False

    def recover(self) -> None:
        # term と投票先は永続化されているので、故障前の値のまま再開する
        self.alive = True
        self.role = Role.FOLLOWER
        self.log("*** 復帰。フォロワーとして再開 ***")
        self.reset_election_timer()


def find_leader(nodes: list[Node]) -> Node | None:
    for node in nodes:
        if node.alive and node.role == Role.LEADER:
            return node
    return None


def main() -> None:
    rng = random.Random(11)
    sim = Simulator()
    nodes = [Node(i, sim, rng) for i in range(1, NUM_NODES + 1)]
    for node in nodes:
        node.peers = [n for n in nodes if n is not node]
        node.reset_election_timer()

    crashed: list[Node] = []

    def crash_leader() -> None:
        leader = find_leader(nodes)
        if leader is not None:
            leader.crash()
            crashed.append(leader)

    def recover_crashed() -> None:
        for node in crashed:
            node.recover()

    sim.schedule(CRASH_TIME, crash_leader)
    sim.schedule(RECOVER_TIME, recover_crashed)
    sim.run(until=END_TIME)

    print()
    print(f"[{END_TIME} ms 時点の状態]")
    for node in nodes:
        print(f"  ノード {node.id}: term {node.term}, {node.role.value}")


if __name__ == "__main__":
    main()
