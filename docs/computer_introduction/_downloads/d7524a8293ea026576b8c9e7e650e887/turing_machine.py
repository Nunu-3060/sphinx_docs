"""チューリングマシンのシミュレータ。

テープに書かれた 2 進数に 1 を足すチューリングマシンを動かし、
1 ステップごとの状態とテープの様子を表示します。

実行方法::

    python turing_machine.py
"""

# 空白を表す記号
BLANK = "_"
# 停止状態の名前
HALT = "halt"

# 遷移規則: (現在の状態, 読んだ記号) -> (書く記号, ヘッドの移動, 次の状態)
# ヘッドの移動は +1 が右、-1 が左を表す。
Rules = dict[tuple[str, str], tuple[str, int, str]]

INCREMENT_RULES: Rules = {
    # right: 右端までヘッドを進める
    ("right", "0"): ("0", +1, "right"),
    ("right", "1"): ("1", +1, "right"),
    ("right", BLANK): (BLANK, -1, "carry"),
    # carry: 右端から 1 を足し、繰り上がりを左へ伝える
    ("carry", "1"): ("0", -1, "carry"),
    ("carry", "0"): ("1", -1, HALT),
    ("carry", BLANK): ("1", -1, HALT),
}


def show(tape: dict[int, str], head: int) -> str:
    """テープの内容を文字列にし、ヘッドの位置を [ ] で囲んで示す。"""
    left = min(min(tape), head)
    right = max(max(tape), head)
    cells = []
    for position in range(left, right + 1):
        symbol = tape.get(position, BLANK)
        cells.append(f"[{symbol}]" if position == head else f" {symbol} ")
    return "".join(cells)


def run(rules: Rules, text: str, state: str, max_steps: int = 100) -> str:
    """text を書いたテープでチューリングマシンを動かし、結果を返す。"""
    # テープは位置 -> 記号 の辞書で表す (書かれていない位置は空白)
    tape = dict(enumerate(text))
    head = 0

    for step in range(max_steps):
        print(f"{step:>2}: {state:<5} {show(tape, head)}")
        if state == HALT:
            break
        symbol = tape.get(head, BLANK)
        write, move, state = rules[(state, symbol)]
        tape[head] = write
        head += move
    else:
        raise RuntimeError(f"{max_steps} ステップ以内に停止しませんでした")

    # 空白を除いた部分を結果とする
    cells = (tape[position] for position in sorted(tape))
    return "".join(cells).strip(BLANK)


def main() -> None:
    """1011 (10 進数の 11) に 1 を足す。"""
    result = run(INCREMENT_RULES, "1011", "right")
    print(f"結果: {result} (10 進数の {int(result, 2)})")


if __name__ == "__main__":
    main()
