"""第 10 章: 1 テープ決定性チューリング機械のシミュレータ。

遷移関数は (状態, 読んだ記号) -> (次の状態, 書く記号, ヘッドの移動) の辞書で
与える。遷移が定義されていない組に出会ったら拒否状態に移ったものとみなす。

例として、言語 { 0^n 1^n | n >= 0 } を判定する機械を動かす。

実行例::

    python ch10_turing_machine.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

BLANK = "_"
ACCEPT = "q_accept"
REJECT = "q_reject"

Transition = dict[tuple[str, str], tuple[str, str, str]]


@dataclass
class TuringMachine:
    """1 テープ決定性チューリング機械。移動は "L" (左) か "R" (右)。"""

    delta: Transition
    start: str
    tape: dict[int, str] = field(default_factory=dict)
    head: int = 0
    state: str = ""

    def run(self, word: str, max_steps: int = 10_000,
            trace: bool = False) -> bool:
        """word を入力として動かし、受理なら True、拒否なら False を返す。"""
        self.tape = dict(enumerate(word))  # 書かれていないマスは空白
        self.head = 0
        self.state = self.start
        for _ in range(max_steps):
            if trace:
                print(self.snapshot())
            if self.state in (ACCEPT, REJECT):
                return self.state == ACCEPT
            symbol = self.tape.get(self.head, BLANK)
            key = (self.state, symbol)
            if key not in self.delta:
                self.state = REJECT
                continue
            self.state, written, move = self.delta[key]
            self.tape[self.head] = written
            self.head += 1 if move == "R" else -1
            self.head = max(self.head, 0)  # 左端より左には動かない
        raise RuntimeError(f"{max_steps} ステップ以内に停止しなかった")

    def snapshot(self) -> str:
        """現在の様相 (テープの内容、状態、ヘッド位置) を文字列にする。"""
        right = max([self.head, *self.tape.keys()]) + 1
        cells = [self.tape.get(i, BLANK) for i in range(right + 1)]
        cells.insert(self.head, f"[{self.state}]")
        return " ".join(cells)


# 0 を X に、対応する 1 を Y に書き換えることを繰り返す。
ZERO_N_ONE_N: Transition = {
    ("q0", "0"): ("q1", "X", "R"),     # 未処理の 0 を X にする
    ("q0", "Y"): ("q3", "Y", "R"),     # 0 が残っていなければ検査へ
    ("q0", BLANK): (ACCEPT, BLANK, "R"),  # 空列 (n = 0)
    ("q1", "0"): ("q1", "0", "R"),     # 右へ進んで最初の 1 を探す
    ("q1", "Y"): ("q1", "Y", "R"),
    ("q1", "1"): ("q2", "Y", "L"),     # 対応する 1 を Y にする
    ("q2", "0"): ("q2", "0", "L"),     # 左へ戻る
    ("q2", "Y"): ("q2", "Y", "L"),
    ("q2", "X"): ("q0", "X", "R"),     # X の右隣から繰り返す
    ("q3", "Y"): ("q3", "Y", "R"),     # 残りが Y だけか確かめる
    ("q3", BLANK): (ACCEPT, BLANK, "R"),
}


def main() -> None:
    tm = TuringMachine(ZERO_N_ONE_N, "q0")
    print("入力 0011 の動作:")
    tm.run("0011", trace=True)
    print()
    for word in ["", "01", "0011", "000111", "001", "0101", "10"]:
        result = "受理" if tm.run(word) else "拒否"
        print(f"{word!r:>9}: {result}")


if __name__ == "__main__":
    main()
