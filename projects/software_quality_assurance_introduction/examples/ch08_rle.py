"""第 8 章のサンプル: ランレングス符号化（連続する文字を個数で表す圧縮）です。"""


def encode(text: str) -> list[tuple[str, int]]:
    """文字列を (文字, 連続数) の組のリストに変換します。

    例: "aaab" は [("a", 3), ("b", 1)] になります。
    """
    runs: list[tuple[str, int]] = []
    for char in text:
        if runs and runs[-1][0] == char:
            runs[-1] = (char, runs[-1][1] + 1)
        else:
            runs.append((char, 1))
    return runs


def decode(runs: list[tuple[str, int]]) -> str:
    """encode() の結果を元の文字列に戻します。"""
    return "".join(char * count for char, count in runs)
