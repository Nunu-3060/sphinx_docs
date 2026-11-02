"""ゲームループの最小の例（4 章）。

落ちてくる果物をかごで受け止める端末上のゲーム。
1 回のループで「入力 → 更新 → 描画」を順に行う。
入力を待つ手番制のループなので、1 回の入力が 1 フレームに当たる。

実行方法: py game_loop.py
操作: a で左、d で右、何も入力せずに Enter で待機、q で終了
"""

import random
from dataclasses import dataclass

WIDTH = 7   # 横のマス数
HEIGHT = 6  # 縦のマス数
LIVES = 3   # 受け止めそこねてよい回数


@dataclass
class State:
    """ゲームの状態。ループのたびに更新される。"""

    basket_x: int
    fruit_x: int
    fruit_y: int
    score: int = 0
    misses: int = 0


def read_input() -> str:
    """入力: プレイヤーの操作を 1 つ読む。"""
    return input("a/d/Enter/q > ").strip().lower()


def update(state: State, command: str) -> None:
    """更新: 操作とルールに従って状態を 1 段階進める。"""
    if command == "a":
        state.basket_x = max(0, state.basket_x - 1)
    elif command == "d":
        state.basket_x = min(WIDTH - 1, state.basket_x + 1)
    state.fruit_y += 1
    if state.fruit_y == HEIGHT - 1:  # 果物がかごの高さに着いた
        if state.fruit_x == state.basket_x:
            state.score += 1
        else:
            state.misses += 1
        state.fruit_x = random.randrange(WIDTH)
        state.fruit_y = 0


def draw(state: State) -> None:
    """描画: 状態を画面（端末）に表示する。"""
    for y in range(HEIGHT):
        row = ["."] * WIDTH
        if y == state.fruit_y:
            row[state.fruit_x] = "o"
        if y == HEIGHT - 1:
            row[state.basket_x] = "U"
        print("".join(row))
    print(f"score={state.score} misses={state.misses}/{LIVES}")


def main() -> None:
    state = State(basket_x=WIDTH // 2, fruit_x=random.randrange(WIDTH), fruit_y=0)
    draw(state)
    while state.misses < LIVES:
        command = read_input()
        if command == "q":
            break
        update(state, command)
        draw(state)
    print(f"game over: score={state.score}")


if __name__ == "__main__":
    main()
