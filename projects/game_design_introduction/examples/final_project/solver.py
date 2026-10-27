"""『宝石と見張り』のレベルを幅優先探索で解き、最短手数を求める。

盤面（プレイヤーの位置、残りの宝石、見張りの位置と向き）を頂点、1 手を辺とするグラフを
幅優先探索するので、最初に見つかったクリア手順が最短手順になる。
レベルを作ったら、このスクリプトで「解けること」と「最短手数」を確かめる。

実行例:
    python solver.py                    # levels フォルダのすべてのレベルを解く
    python solver.py levels/level2.txt  # 指定したレベルだけを解く
"""

from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from game_logic import DOWN, LEFT, MOVES, RIGHT, UP, WAIT, Guard, Level, Pos, State, Status, load_levels

MOVE_SYMBOLS: dict[Pos, str] = {UP: "↑", DOWN: "↓", LEFT: "←", RIGHT: "→", WAIT: "・"}
# 同じ手数の手順が複数あるときに「その場で待つ」手順が選ばれるよう、待機を先に試す。
SEARCH_ORDER: tuple[Pos, ...] = (WAIT, *[m for m in MOVES if m != WAIT])

# ターン数を除いた盤面。ターン数が違っても同じ盤面なら、その先の展開は同じである。
Key = tuple[Pos, frozenset[Pos], tuple[Guard, ...]]


@dataclass(frozen=True)
class Solution:
    moves: list[Pos] | None  # 解けないときは None
    explored: int  # 調べた盤面の数


def key_of(state: State) -> Key:
    return state.player, state.gems, state.guards


def solve(level: Level) -> Solution:
    start = level.initial
    parents: dict[Key, tuple[Key, Pos] | None] = {key_of(start): None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for move in SEARCH_ORDER:
            nxt = level.step(state, move)
            if nxt is None or nxt.status is Status.CAUGHT:
                continue
            key = key_of(nxt)
            if key in parents:
                continue
            parents[key] = (key_of(state), move)
            if nxt.status is Status.CLEARED:
                return Solution(reconstruct(parents, key), len(parents))
            queue.append(nxt)
    return Solution(None, len(parents))


def reconstruct(parents: dict[Key, tuple[Key, Pos] | None], goal: Key) -> list[Pos]:
    moves: list[Pos] = []
    entry = parents[goal]
    while entry is not None:
        previous, move = entry
        moves.append(move)
        entry = parents[previous]
    return moves[::-1]


def describe(moves: list[Pos]) -> str:
    return "".join(MOVE_SYMBOLS[m] for m in moves)


def main() -> None:
    here = Path(__file__).parent
    levels = [Level.load(Path(arg)) for arg in sys.argv[1:]] or load_levels(here / "levels")
    for level in levels:
        result = solve(level)
        if result.moves is None:
            print(f"{level.name}: 解けない（調べた盤面 {result.explored}）")
        else:
            waits = result.moves.count(WAIT)
            print(f"{level.name}: 最短 {len(result.moves)} 手（待機 {waits} 回、調べた盤面 {result.explored}）")
            print(f"  {describe(result.moves)}")


if __name__ == "__main__":
    main()
