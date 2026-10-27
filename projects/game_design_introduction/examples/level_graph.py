"""レベルをグラフとして表し、鍵と扉の配置が破綻していないか調べる。

部屋をノード、通路をエッジとし、通路には「開けるのに必要な鍵」を付けられる。
スタートから行ける部屋を探索し、拾った鍵で開く扉が増えたら探索をやり直す、
という手順を繰り返して、最終的にゴールへ到達できるかを判定する。
鍵は何度でも使える（色の付いた鍵のように、対応する扉をすべて開けられる）ものとする。

実行例:
    python level_graph.py
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Passage:
    """2 つの部屋をつなぐ通路。lock が None でなければ、その鍵が必要である。"""

    a: str
    b: str
    lock: str | None = None


@dataclass
class Level:
    start: str
    goal: str
    passages: list[Passage]
    keys: dict[str, str] = field(default_factory=dict)  # 部屋の名前 → その部屋にある鍵

    def neighbors(self, room: str, held: set[str]) -> list[str]:
        """手持ちの鍵 held で通れる通路の先にある部屋を返す。"""
        result: list[str] = []
        for p in self.passages:
            if p.lock is not None and p.lock not in held:
                continue
            if p.a == room:
                result.append(p.b)
            elif p.b == room:
                result.append(p.a)
        return result


def reachable(level: Level, held: set[str]) -> list[str]:
    """手持ちの鍵で行ける部屋を、幅優先探索で見つけた順に返す。"""
    visited = [level.start]
    queue = deque([level.start])
    while queue:
        room = queue.popleft()
        for nxt in level.neighbors(room, held):
            if nxt not in visited:
                visited.append(nxt)
                queue.append(nxt)
    return visited


def check(level: Level) -> bool:
    """鍵を拾いながら探索を繰り返し、ゴールに着けるかを表示して返す。"""
    held: set[str] = set()
    step = 1
    while True:
        rooms = reachable(level, held)
        new_keys = {level.keys[r] for r in rooms if r in level.keys} - held
        print(f"  段階 {step}: 行ける部屋 = {', '.join(rooms)}")
        if level.goal in rooms:
            print(f"  → ゴール「{level.goal}」に到達できる")
            return True
        if not new_keys:
            all_rooms = {p.a for p in level.passages} | {p.b for p in level.passages}
            stuck = sorted(all_rooms - set(rooms))
            print(f"  → 新しい鍵が無く、先に進めない（行けない部屋: {', '.join(stuck)}）")
            return False
        print(f"           拾った鍵 = {', '.join(sorted(new_keys))}")
        held |= new_keys
        step += 1


def sample_level(blue_key_room: str) -> Level:
    return Level(
        start="入口",
        goal="ボス部屋",
        passages=[
            Passage("入口", "広間"),
            Passage("広間", "東の通路"),
            Passage("東の通路", "倉庫"),
            Passage("広間", "北の塔", lock="赤の鍵"),
            Passage("広間", "地下", lock="青の鍵"),
            Passage("地下", "ボス部屋"),
        ],
        keys={"倉庫": "赤の鍵", blue_key_room: "青の鍵"},
    )


def main() -> None:
    print("正しい配置（青の鍵は北の塔にある）")
    check(sample_level(blue_key_room="北の塔"))
    print()
    print("破綻した配置（青の鍵が、青の扉の向こうの地下にある）")
    check(sample_level(blue_key_room="地下"))


if __name__ == "__main__":
    main()
