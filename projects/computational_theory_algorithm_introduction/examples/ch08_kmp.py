"""第 8 章: KMP 法 (クヌース-モリス-プラット法) による文字列照合。

パターン P の各位置について「一致に失敗したらパターンのどこから照合を
再開すればよいか」を前計算しておく (失敗関数)。これはパターンを受理する
有限オートマトンを作ることに相当し、テキストを 1 回走査するだけで
全ての出現位置が O(n + m) で求まる。

実行例::

    python ch08_kmp.py
"""

from __future__ import annotations


def failure_function(pattern: str) -> list[int]:
    """fail[i] は pattern[:i + 1] の、真の接頭辞かつ接尾辞である最長の長さ。"""
    fail = [0] * len(pattern)
    k = 0  # 現在一致している接頭辞の長さ
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    return fail


def kmp_search(text: str, pattern: str) -> list[int]:
    """text の中で pattern が現れる開始位置をすべて返す。"""
    if not pattern:
        return list(range(len(text) + 1))
    fail = failure_function(pattern)
    positions: list[int] = []
    k = 0
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            k = fail[k - 1]  # テキスト側は戻らず、パターン側だけ戻る
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            positions.append(i - k + 1)
            k = fail[k - 1]
    return positions


def main() -> None:
    pattern = "ABABC"
    print("失敗関数:", failure_function(pattern))
    text = "ABABDABABCABABABC"
    print("出現位置:", kmp_search(text, pattern))
    print("重なりのある出現:", kmp_search("AAAAA", "AAA"))


if __name__ == "__main__":
    main()
