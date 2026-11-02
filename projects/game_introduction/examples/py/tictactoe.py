"""三目並べの局面を数え、ミニマックス法の AI と対戦する（5 章、8 章）。

実行方法:
    py tictactoe.py          局面数とゲームの値を表示する
    py tictactoe.py play     AI と対戦する（あなたが先手の X）
"""

import sys
from functools import cache

Board = str  # 9 文字の文字列。"X"、"O"、" " で 3×3 のマスを左上から表す

EMPTY: Board = " " * 9
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 横
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 縦
    (0, 4, 8), (2, 4, 6),             # 斜め
]


def winner(board: Board) -> str | None:
    """勝者（"X" か "O"）を返す。まだ決まっていなければ None を返す。"""
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_over(board: Board) -> bool:
    return winner(board) is not None or " " not in board


def turn(board: Board) -> str:
    """次に打つ側を返す。X が先手。"""
    return "X" if board.count("X") == board.count("O") else "O"


def moves(board: Board) -> list[int]:
    return [i for i, cell in enumerate(board) if cell == " "]


def play(board: Board, square: int) -> Board:
    return board[:square] + turn(board) + board[square + 1:]


def count_games(board: Board = EMPTY) -> int:
    """終局までの手順の数（ゲーム木の葉の数）を数える。"""
    if is_over(board):
        return 1
    return sum(count_games(play(board, m)) for m in moves(board))


def reachable_positions(board: Board = EMPTY) -> set[Board]:
    """初期局面から到達できる局面の集合を返す（初期局面を含む）。"""
    found = {board}
    stack = [board]
    while stack:
        current = stack.pop()
        if is_over(current):
            continue
        for m in moves(current):
            nxt = play(current, m)
            if nxt not in found:
                found.add(nxt)
                stack.append(nxt)
    return found


@cache
def value(board: Board) -> int:
    """ミニマックス法による局面の値。X の勝ちが +1、引き分けが 0、O の勝ちが -1。"""
    w = winner(board)
    if w is not None:
        return 1 if w == "X" else -1
    if " " not in board:
        return 0
    values = [value(play(board, m)) for m in moves(board)]
    return max(values) if turn(board) == "X" else min(values)


def best_move(board: Board) -> int:
    """手番の側にとって最もよい手を返す。"""
    pick = max if turn(board) == "X" else min
    return pick(moves(board), key=lambda m: value(play(board, m)))


def show(board: Board) -> None:
    cells = [c if c != " " else str(i) for i, c in enumerate(board)]
    for row in range(3):
        print(" " + " | ".join(cells[row * 3:row * 3 + 3]))


def play_against_ai() -> None:
    board = EMPTY
    while not is_over(board):
        show(board)
        if turn(board) == "X":
            text = input("マスの番号 > ").strip()
            if not text.isdigit() or int(text) not in moves(board):
                print("空いているマスの番号を入力する")
                continue
            board = play(board, int(text))
        else:
            board = play(board, best_move(board))
    show(board)
    print(f"勝者: {winner(board) or '引き分け'}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "play":
        play_against_ai()
        return
    positions = reachable_positions()
    print(f"終局までの手順の数: {count_games()}")
    print(f"到達できる局面の数: {len(positions)}")
    print(f"初期局面の値: {value(EMPTY)}（0 は双方が最善を尽くすと引き分け）")


if __name__ == "__main__":
    main()
