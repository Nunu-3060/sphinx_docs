"""第 9 章: CYK 法による文脈自由言語の所属判定。

チョムスキー標準形の文法 G と文字列 w が与えられたとき、w が G から
導出できるかを動的計画法で O(n^3 |G|) 時間で判定する。

例として、言語 { a^n b^n | n >= 1 } を生成する次の文法を使う。

    S -> A B | A C
    C -> S B
    A -> a
    B -> b

実行例::

    python ch09_cyk.py
"""

from __future__ import annotations

# 生成規則: 左辺 -> 右辺の候補のリスト。右辺は (変数, 変数) か (終端記号,)。
Grammar = dict[str, list[tuple[str, ...]]]

AN_BN: Grammar = {
    "S": [("A", "B"), ("A", "C")],
    "C": [("S", "B")],
    "A": [("a",)],
    "B": [("b",)],
}


def cyk(grammar: Grammar, start: str, word: str) -> bool:
    """word が start 記号から導出できれば True を返す。"""
    n = len(word)
    if n == 0:
        return False  # この実装では空列を生成する規則を扱わない
    # table[i][j]: 部分文字列 word[i:i + j + 1] を導出できる変数の集合
    table: list[list[set[str]]] = [[set() for _ in range(n)] for _ in range(n)]
    for i, ch in enumerate(word):
        for head, bodies in grammar.items():
            if (ch,) in bodies:
                table[i][0].add(head)
    for length in range(2, n + 1):  # 部分文字列の長さ
        for i in range(n - length + 1):  # 開始位置
            for split in range(1, length):  # 左側の長さ
                left = table[i][split - 1]
                right = table[i + split][length - split - 1]
                for head, bodies in grammar.items():
                    for body in bodies:
                        if (len(body) == 2 and body[0] in left
                                and body[1] in right):
                            table[i][length - 1].add(head)
    return start in table[0][n - 1]


def main() -> None:
    for word in ["ab", "aabb", "aaabbb", "aab", "abab", "ba"]:
        result = "受理" if cyk(AN_BN, "S", word) else "拒否"
        print(f"{word:>6}: {result}")


if __name__ == "__main__":
    main()
