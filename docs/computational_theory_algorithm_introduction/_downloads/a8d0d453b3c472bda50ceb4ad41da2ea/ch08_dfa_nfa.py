"""第 8 章: DFA と NFA のシミュレータ、および部分集合構成法。

* DFA: 決定性有限オートマトン。各状態と入力記号に対し遷移先がちょうど 1 つ。
* NFA: 非決定性有限オートマトン。遷移先は状態の集合で、空列 (EPS) による
  遷移も許す。
* subset_construction: NFA を、同じ言語を受理する DFA に変換する。

実行例::

    python ch08_dfa_nfa.py
"""

from __future__ import annotations

from dataclasses import dataclass

EPS = ""  # 空列による遷移を表す記号


@dataclass(frozen=True)
class DFA:
    """決定性有限オートマトン。状態は任意のハッシュ可能な値で表す。"""

    states: frozenset[object]
    alphabet: frozenset[str]
    delta: dict[tuple[object, str], object]
    start: object
    accepting: frozenset[object]

    def accepts(self, word: str) -> bool:
        """word を先頭から 1 文字ずつ読み、受理状態で終われば True。"""
        state = self.start
        for symbol in word:
            state = self.delta[(state, symbol)]
        return state in self.accepting


@dataclass(frozen=True)
class NFA:
    """空列遷移付き非決定性有限オートマトン。"""

    states: frozenset[object]
    alphabet: frozenset[str]
    delta: dict[tuple[object, str], frozenset[object]]
    start: object
    accepting: frozenset[object]

    def eps_closure(self, states: frozenset[object]) -> frozenset[object]:
        """states から空列遷移だけでたどり着ける状態の集合を返す。"""
        closure = set(states)
        stack = list(states)
        while stack:
            q = stack.pop()
            for r in self.delta.get((q, EPS), frozenset()):
                if r not in closure:
                    closure.add(r)
                    stack.append(r)
        return frozenset(closure)

    def step(self, states: frozenset[object],
             symbol: str) -> frozenset[object]:
        """現在の状態集合から symbol を読んだ後の状態集合を返す。"""
        moved: set[object] = set()
        for q in states:
            moved |= self.delta.get((q, symbol), frozenset())
        return self.eps_closure(frozenset(moved))

    def accepts(self, word: str) -> bool:
        """取りうる状態をすべて同時に追跡し、受理状態を含めば True。"""
        current = self.eps_closure(frozenset({self.start}))
        for symbol in word:
            current = self.step(current, symbol)
        return bool(current & self.accepting)


def subset_construction(nfa: NFA) -> DFA:
    """NFA の状態の集合を DFA の 1 つの状態とみなして DFA を作る。"""
    start = nfa.eps_closure(frozenset({nfa.start}))
    delta: dict[tuple[object, str], object] = {}
    seen = {start}
    stack = [start]
    while stack:  # 開始状態から到達できる状態集合だけを作る
        current = stack.pop()
        for symbol in sorted(nfa.alphabet):
            target = nfa.step(current, symbol)
            delta[(current, symbol)] = target
            if target not in seen:
                seen.add(target)
                stack.append(target)
    accepting = frozenset(s for s in seen if s & nfa.accepting)
    return DFA(frozenset(seen), nfa.alphabet, delta, start,
               frozenset(accepting))


def divisible_by_3_dfa() -> DFA:
    """2 進数として読んだ値が 3 の倍数である文字列を受理する DFA。

    状態 r は「ここまで読んだ値を 3 で割った余りが r」であることを表す。
    値 x の後ろに 1 ビット b を付けると値は 2x + b になる。
    """
    delta: dict[tuple[object, str], object] = {}
    for r in range(3):
        for b in "01":
            delta[(r, b)] = (2 * r + int(b)) % 3
    return DFA(frozenset({0, 1, 2}), frozenset("01"), delta, 0,
               frozenset({0}))


def third_from_last_is_1_nfa() -> NFA:
    """後ろから 3 文字目が 1 である 0/1 の文字列を受理する NFA。

    状態 0 で読み進め、「ここが後ろから 3 文字目だ」と推測した 1 で
    状態 1 に移り、残り 2 文字を読んで受理状態 3 に至る。
    """
    delta: dict[tuple[object, str], frozenset[object]] = {
        (0, "0"): frozenset({0}),
        (0, "1"): frozenset({0, 1}),
        (1, "0"): frozenset({2}),
        (1, "1"): frozenset({2}),
        (2, "0"): frozenset({3}),
        (2, "1"): frozenset({3}),
    }
    return NFA(frozenset({0, 1, 2, 3}), frozenset("01"), delta, 0,
               frozenset({3}))


def main() -> None:
    dfa = divisible_by_3_dfa()
    for n in range(10):
        word = format(n, "b")
        print(f"{word:>4} ({n}): {'受理' if dfa.accepts(word) else '拒否'}")

    nfa = third_from_last_is_1_nfa()
    converted = subset_construction(nfa)
    print("NFA の状態数:", len(nfa.states))
    print("変換後の DFA の状態数:", len(converted.states))
    for word in ["100", "0100", "1011", "0011", "11"]:
        print(f"{word}: NFA {nfa.accepts(word)},"
              f" DFA {converted.accepts(word)}")


if __name__ == "__main__":
    main()
