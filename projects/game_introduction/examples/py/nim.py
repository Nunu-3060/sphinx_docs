"""ニムの必勝法を使う AI と対戦する（5 章、8 章）。

ルール: 2 人が交互に、1 つの山から 1 個以上の石を取る。最後の石を取った方が勝ち。

実行方法:
    py nim.py            山 3, 4, 5 で対戦する（あなたが先手）
    py nim.py 1 3 5 7    山の大きさを指定して対戦する
"""

import random
import sys
from functools import reduce
from operator import xor


def nim_sum(heaps: list[int]) -> int:
    """すべての山の石の数の排他的論理和（ニム和）を返す。"""
    return reduce(xor, heaps, 0)


def winning_move(heaps: list[int]) -> tuple[int, int] | None:
    """ニム和を 0 にする手（山の番号, 取る個数）を返す。無ければ None を返す。"""
    s = nim_sum(heaps)
    if s == 0:
        return None
    for i, h in enumerate(heaps):
        target = h ^ s
        if target < h:
            return i, h - target
    return None  # s != 0 なら必ず上で見つかるので、ここには来ない


def ai_move(heaps: list[int]) -> tuple[int, int]:
    """必勝の手があればそれを選び、無ければ 1 個だけ取って相手の失敗を待つ。"""
    move = winning_move(heaps)
    if move is not None:
        return move
    i = random.choice([i for i, h in enumerate(heaps) if h > 0])
    return i, 1


def read_move(heaps: list[int]) -> tuple[int, int]:
    while True:
        parts = input("山の番号と取る個数 > ").split()
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            i, n = int(parts[0]), int(parts[1])
            if 0 <= i < len(heaps) and 1 <= n <= heaps[i]:
                return i, n
        print("例: 0 2（0 番の山から 2 個取る）")


def main() -> None:
    heaps = [int(a) for a in sys.argv[1:]] or [3, 4, 5]
    player_turn = True
    while sum(heaps) > 0:
        print("山: " + "  ".join(f"[{i}] {h}" for i, h in enumerate(heaps)) + f"  （ニム和 {nim_sum(heaps)}）")
        if player_turn:
            i, n = read_move(heaps)
        else:
            i, n = ai_move(heaps)
            print(f"AI: {i} 番の山から {n} 個取る")
        heaps[i] -= n
        player_turn = not player_turn
    print("あなたの勝ち" if not player_turn else "AI の勝ち")


if __name__ == "__main__":
    main()
