"""2 進数に 1 を加えるチューリングマシンのシミュレータ。

第 6 章「計算理論」のサンプルである。テープ、ヘッド、状態、
遷移関数だけで「1 を加える」計算を行う様子を、1 ステップずつ表示する。

実行方法::

    python ch06_turing_machine.py
"""

BLANK = "_"

# 遷移関数 δ: (状態, 読んだ記号) -> (次の状態, 書く記号, ヘッドの移動)
# 移動は "L"（左）または "R"（右）で表す。
Transition = dict[tuple[str, str], tuple[str, str, str]]

INCREMENT: Transition = {
    # right: 右端まで移動する
    ("right", "0"): ("right", "0", "R"),
    ("right", "1"): ("right", "1", "R"),
    ("right", BLANK): ("carry", BLANK, "L"),
    # carry: 下位の桁から 1 を加え、繰り上がりを左へ伝える
    ("carry", "1"): ("carry", "0", "L"),
    ("carry", "0"): ("done", "1", "L"),
    ("carry", BLANK): ("done", "1", "L"),
}


def show(tape: dict[int, str], head: int, state: str) -> str:
    """テープの内容とヘッドの位置を 1 行の文字列にする."""
    left = min(min(tape), head)
    right = max(max(tape), head)
    cells = []
    for i in range(left, right + 1):
        symbol = tape.get(i, BLANK)
        # ヘッドの位置の記号を [ ] で囲む
        cells.append(f"[{symbol}]" if i == head else f" {symbol} ")
    return f"{state:>5}: {''.join(cells)}"


def run(
    delta: Transition, text: str, start: str, halt: str, verbose: bool
) -> str:
    """チューリングマシンを停止状態まで動かし、テープの内容を返す."""
    # テープは両方向に無限に続くので、書かれたマスだけを辞書で持つ
    tape = {i: c for i, c in enumerate(text)}
    head = 0
    state = start
    steps = 0
    while state != halt:
        if verbose:
            print(show(tape, head, state))
        symbol = tape.get(head, BLANK)
        state, write, move = delta[(state, symbol)]
        tape[head] = write
        head += 1 if move == "R" else -1
        steps += 1
    if verbose:
        print(show(tape, head, state))
        print(f"{steps} ステップで停止")
    cells = [tape[i] for i in sorted(tape)]
    return "".join(cells).strip(BLANK)


def main() -> None:
    """1011 に 1 を加える過程を表示し、他の入力も検算する."""
    result = run(INCREMENT, "1011", "right", "done", verbose=True)
    print(f"結果: {result}")

    print("検算:")
    for text in ["0", "1", "111", "1001", "11111"]:
        out = run(INCREMENT, text, "right", "done", verbose=False)
        assert int(out, 2) == int(text, 2) + 1
        print(f"  {text} + 1 = {out}")


if __name__ == "__main__":
    main()
