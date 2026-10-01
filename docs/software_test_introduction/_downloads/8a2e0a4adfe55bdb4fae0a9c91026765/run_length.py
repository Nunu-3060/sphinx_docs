"""ランレングス符号化（同じ文字の連続を「文字と個数」の組で表す）."""


def encode(text: str) -> list[tuple[str, int]]:
    """文字列を (文字, 連続する個数) の並びに変換する.

    例: "aaab" は [("a", 3), ("b", 1)] になる。
    """
    runs: list[tuple[str, int]] = []
    for char in text:
        if runs and runs[-1][0] == char:
            runs[-1] = (char, runs[-1][1] + 1)
        else:
            runs.append((char, 1))
    return runs


def decode(runs: list[tuple[str, int]]) -> str:
    """encode の結果から元の文字列を復元する."""
    return "".join(char * count for char, count in runs)
