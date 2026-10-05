"""2 進数が 3 の倍数かどうかを判定する決定性有限オートマトン（DFA）。

第 6 章「計算理論」のサンプルである。状態を「これまでに読んだ
2 進数を 3 で割った余り」とすると、3 つの状態だけで判定できる。

実行方法::

    python ch06_dfa.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DFA:
    """決定性有限オートマトンを表すクラス.

    states: 状態の集合 Q
    alphabet: 入力記号の集合（アルファベット）Σ
    delta: 遷移関数 δ を (状態, 記号) -> 状態 の辞書で表したもの
    start: 開始状態 q0
    accepts: 受理状態の集合 F
    """

    states: frozenset[str]
    alphabet: frozenset[str]
    delta: dict[tuple[str, str], str]
    start: str
    accepts: frozenset[str]

    def run(self, text: str) -> list[str]:
        """入力 text を読み、通過した状態の列を返す."""
        state = self.start
        path = [state]
        for symbol in text:
            if symbol not in self.alphabet:
                raise ValueError(f"アルファベットに無い記号: {symbol!r}")
            # 現在の状態と入力記号だけで次の状態が 1 つに決まる
            state = self.delta[(state, symbol)]
            path.append(state)
        return path

    def accepts_input(self, text: str) -> bool:
        """入力 text を受理するなら True を返す."""
        return self.run(text)[-1] in self.accepts


def make_multiple_of_three_dfa() -> DFA:
    """2 進数が 3 の倍数かを判定する DFA を作る.

    状態 q0, q1, q2 は、それまでに読んだ数を 3 で割った余り 0, 1, 2
    を表す。余り r の数の後ろにビット b を付けると値は 2r + b になる
    ので、次の状態は (2r + b) mod 3 となる。
    """
    delta: dict[tuple[str, str], str] = {}
    for r in range(3):
        for b in range(2):
            delta[(f"q{r}", str(b))] = f"q{(2 * r + b) % 3}"
    return DFA(
        states=frozenset({"q0", "q1", "q2"}),
        alphabet=frozenset({"0", "1"}),
        delta=delta,
        start="q0",
        accepts=frozenset({"q0"}),
    )


def main() -> None:
    """遷移表を表示し、いくつかの入力を判定する."""
    dfa = make_multiple_of_three_dfa()

    print("遷移表:")
    for state in sorted(dfa.states):
        row = [dfa.delta[(state, s)] for s in sorted(dfa.alphabet)]
        print(f"  {state}: 0 -> {row[0]}, 1 -> {row[1]}")

    print("判定:")
    for text in ["0", "11", "110", "1001", "1010", "1111", "10010"]:
        path = " -> ".join(dfa.run(text))
        result = dfa.accepts_input(text)
        # 組み込みの int で検算する
        assert result == (int(text, 2) % 3 == 0)
        mark = "受理" if result else "拒否"
        print(f"  {text:>5} ({int(text, 2):2d}): {mark}  {path}")


if __name__ == "__main__":
    main()
