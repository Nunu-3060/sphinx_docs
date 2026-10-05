"""2 相コミット（2PC：Two-Phase Commit）の動作を示すサンプル。

1 つのコーディネーターと 3 つの参加者からなる 2 相コミットを、1 つの
プロセスの中でシミュレーションします。ネットワークは使わず、メッセージ
の送受信はメソッド呼び出しで表します。次の 3 つのシナリオを実行し、
それぞれのログを表示します。

1. 全員が Yes と投票し、コミットされる
2. 1 人が No と投票し、アボートされる
3. 全員が準備完了（Yes）と投票した後、コーディネーターが決定を送る前に
   故障する。参加者は自分だけではコミットもアボートも決められず、
   ロックを保持したまま待ち続ける（阻塞）

時刻は模擬時計の値（ms）で、実際の時間は経過しません。

実行方法:
    python two_phase_commit.py
"""

import unicodedata
from enum import Enum


class Clock:
    """模擬時計。advance() を呼んだときだけ時刻が進む。"""

    def __init__(self) -> None:
        self.now = 0

    def advance(self, ms: int) -> None:
        self.now += ms


class PState(Enum):
    """参加者の状態。"""

    INIT = "初期"
    PREPARED = "準備完了"
    COMMITTED = "コミット済み"
    ABORTED = "アボート済み"


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として、表示幅が width になるよう空白で埋める。"""
    shown = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
                for c in text)
    return text + " " * max(width - shown, 0)


class Logger:
    """時刻付きでログを表示する。"""

    def __init__(self, clock: Clock) -> None:
        self.clock = clock

    def log(self, who: str, message: str) -> None:
        print(f"  [{self.clock.now:5d} ms] {pad(who, 16)}: {message}")


class Participant:
    """2PC の参加者（例えば、1 つのデータベースのシャード）。"""

    def __init__(self, name: str, vote_yes: bool, logger: Logger) -> None:
        self.name = name
        self.vote_yes = vote_yes  # 準備が成功するかどうか
        self.state = PState.INIT
        self.locked = False
        self.logger = logger

    def prepare(self) -> bool:
        """フェーズ 1：準備要求を受け、投票する。"""
        if self.vote_yes:
            # 変更内容とロックを永続化してから Yes と答える。
            # Yes と答えた後は、自分の判断でアボートできない。
            self.locked = True
            self.state = PState.PREPARED
            self.logger.log(self.name, "変更をログに記録、ロック取得 → Yes")
            return True
        self.state = PState.ABORTED
        self.logger.log(self.name, "制約違反のため準備失敗 → No")
        return False

    def commit(self) -> None:
        """フェーズ 2：コミットの決定を受ける。"""
        self.state = PState.COMMITTED
        self.locked = False
        self.logger.log(self.name, "コミットしてロック解放")

    def abort(self) -> None:
        """フェーズ 2：アボートの決定を受ける。"""
        if self.state != PState.ABORTED:
            self.state = PState.ABORTED
            self.locked = False
            self.logger.log(self.name, "変更を取り消してロック解放")

    def wait_for_decision(self, others: list["Participant"],
                          first: bool) -> None:
        """決定が届かないときの振る舞い（タイムアウト後）。"""
        if self.state != PState.PREPARED:
            return
        if not first:
            self.logger.log(self.name, "まだ決定が届かない（ロック保持中）")
            return
        # 他の参加者に結果を問い合わせる（協調終了プロトコル）。
        # 誰かがコミット済みかアボート済みならその結果に従えばよく、
        # 未投票（INIT）の参加者がいればコミットは決定されていない
        # のでアボートしてよい。ただし、このサンプルのシナリオ 3 では
        # 全員が準備完了なので、この分岐には入らない。
        self.logger.log(self.name, "タイムアウト。他の参加者に問い合わせ")
        for other in others:
            if other.state in (PState.COMMITTED, PState.ABORTED,
                               PState.INIT):
                return
        # 全員が準備完了：コーディネーターがどちらに決めたか誰も知らない
        self.logger.log(self.name, "全員が準備完了で結果不明 → 待つしかない")


class Coordinator:
    """2PC のコーディネーター。"""

    def __init__(self, participants: list[Participant], logger: Logger,
                 clock: Clock, crash_after_votes: bool = False) -> None:
        self.participants = participants
        self.logger = logger
        self.clock = clock
        self.crash_after_votes = crash_after_votes
        self.decision_log: str | None = None  # 永続化された決定

    def run(self) -> None:
        name = "コーディネーター"
        # フェーズ 1：準備（投票）
        self.logger.log(name, "フェーズ 1：全参加者に PREPARE を送信")
        self.clock.advance(10)
        votes = [p.prepare() for p in self.participants]
        self.clock.advance(10)
        self.logger.log(name, "投票結果 " + ", ".join(
            "Yes" if v else "No" for v in votes))

        if self.crash_after_votes:
            # 決定をログに書く前に故障する
            self.logger.log(name, "*** 故障（決定を送る前に停止）***")
            return

        # フェーズ 2：決定（決定を先に永続化するのが重要）
        if all(votes):
            self.decision_log = "COMMIT"
            self.logger.log(name, "決定 COMMIT をログに記録して送信")
            self.clock.advance(10)
            for p in self.participants:
                p.commit()
        else:
            self.decision_log = "ABORT"
            self.logger.log(name, "決定 ABORT をログに記録して送信")
            self.clock.advance(10)
            for p in self.participants:
                p.abort()

    def recover(self) -> None:
        """再起動後の回復。決定の記録がなければアボートする。"""
        name = "コーディネーター"
        self.logger.log(name, "*** 再起動 *** ログを読み込む")
        if self.decision_log is None:
            self.decision_log = "ABORT"
            self.logger.log(name, "決定の記録なし → ABORT を記録して送信")
            self.clock.advance(10)
            for p in self.participants:
                p.abort()


def show_states(participants: list[Participant]) -> None:
    states = ", ".join(
        f"{p.name}={p.state.value}{'(ロック中)' if p.locked else ''}"
        for p in participants)
    print(f"  最終状態: {states}")


def run_scenario(title: str, votes: list[bool],
                 crash: bool = False) -> None:
    print(f"=== {title} ===")
    clock = Clock()
    logger = Logger(clock)
    participants = [
        Participant(f"参加者 {i + 1}", vote, logger)
        for i, vote in enumerate(votes)
    ]
    coordinator = Coordinator(participants, logger, clock,
                              crash_after_votes=crash)
    coordinator.run()

    if crash:
        # 参加者はタイムアウトしても待つしかない
        for elapsed in (1000, 5000):
            clock.advance(elapsed)
            for p in participants:
                others = [o for o in participants if o is not p]
                p.wait_for_decision(others, first=(elapsed == 1000))
        show_states(participants)
        clock.advance(30000)
        coordinator.recover()
    show_states(participants)
    print()


def main() -> None:
    run_scenario("シナリオ 1：全員 Yes", [True, True, True])
    run_scenario("シナリオ 2：参加者 2 が No", [True, False, True])
    run_scenario("シナリオ 3：準備完了後にコーディネーターが故障",
                 [True, True, True], crash=True)


if __name__ == "__main__":
    main()
