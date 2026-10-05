"""文字色と背景色のコントラスト比を計算し、WCAG の基準を満たすか判定するサンプルです。

文字と背景のコントラストが低いと、ロービジョンの人や高齢者、
屋外でスマートフォンを使う人にとって、文字が読みにくくなります。
WCAG 2.2 では、通常の文字には 4.5:1 以上、大きな文字には 3:1 以上の
コントラスト比を求めています（達成基準 1.4.3、レベル AA）。

実行方法::

    python contrast_check.py
"""

NORMAL_TEXT_MINIMUM = 4.5
LARGE_TEXT_MINIMUM = 3.0


def parse_hex_color(color: str) -> tuple[int, int, int]:
    """「#1a2b3c」形式の色を、0〜255 の RGB の値に変換します。"""
    value = color.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"6 桁の 16 進数で指定してください: {color}")
    red, green, blue = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return red, green, blue


def linearize(channel: int) -> float:
    """sRGB の値（0〜255）を、光の強さに比例する値（0〜1）に変換します。"""
    c = channel / 255
    if c <= 0.04045:
        return c / 12.92
    return float(((c + 0.055) / 1.055) ** 2.4)


def relative_luminance(color: str) -> float:
    """色の相対輝度（黒が 0、白が 1）を計算します。"""
    red, green, blue = (linearize(c) for c in parse_hex_color(color))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    """2 色のコントラスト比（1〜21）を計算します。"""
    lighter, darker = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def judge(ratio: float) -> str:
    """コントラスト比が、どの文字の大きさで基準を満たすかを返します。"""
    if ratio >= NORMAL_TEXT_MINIMUM:
        return "通常の文字でも基準を満たします"
    if ratio >= LARGE_TEXT_MINIMUM:
        return "大きな文字だけ基準を満たします"
    return "基準を満たしません"


def main() -> None:
    """よく使われる配色のコントラスト比を判定します。"""
    pairs = [
        ("#000000", "#ffffff"),  # 黒の文字、白の背景
        ("#767676", "#ffffff"),  # 濃い灰色の文字、白の背景
        ("#949494", "#ffffff"),  # 中間の灰色の文字、白の背景
        ("#aaaaaa", "#ffffff"),  # 薄い灰色の文字、白の背景
        ("#ffffff", "#ff9900"),  # 白の文字、オレンジの背景
    ]
    for foreground, background in pairs:
        ratio = contrast_ratio(foreground, background)
        print(f"文字 {foreground} / 背景 {background}: "
              f"{ratio:.2f}:1  {judge(ratio)}")


if __name__ == "__main__":
    main()
