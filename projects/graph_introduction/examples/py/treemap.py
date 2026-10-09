"""ツリーマップの配置を計算する（squarified アルゴリズム）.

ch06_treemap.py と ch11_treemap_nested.py から使う。
長方形を、値に比例した面積を持つ小さな長方形に分割する。小さな長方形が
なるべく正方形に近くなるように、大きい値から順に、行（または列）単位で
並べていく（Bruls, Huizing, van Wijk, 2000）。
"""

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

# 長方形: (左下の x, 左下の y, 幅, 高さ)
Rect = tuple[float, float, float, float]


def _worst_ratio(row: list[float], length: float) -> float:
    """面積の列 row を長さ length の辺に沿って並べたときの、最悪の縦横比."""
    total = sum(row)
    return max(max(length ** 2 * area / total ** 2,
                   total ** 2 / (length ** 2 * area)) for area in row)


def squarify(values: list[float], rect: Rect) -> list[Rect]:
    """rect を values の比で分割した長方形のリストを、values の順で返す."""
    x, y, width, height = rect
    total = sum(values)
    # 大きい値から順に並べる。結果は元の順に戻すため、添字を覚えておく
    order = sorted(range(len(values)), key=lambda i: -values[i])
    areas = [values[i] * width * height / total for i in order]
    placed: list[Rect] = []
    while areas:
        # 短い辺に沿って 1 列分の長方形を選ぶ。加えると縦横比が悪くなる
        # 時点で列を確定する
        length = min(width, height)
        row = [areas[0]]
        while (len(row) < len(areas)
               and _worst_ratio(row + [areas[len(row)]], length)
               <= _worst_ratio(row, length)):
            row.append(areas[len(row)])
        areas = areas[len(row):]
        thickness = sum(row) / length
        offset = 0.0
        for area in row:
            if width >= height:  # 左端に縦 1 列で並べる
                placed.append((x, y + offset, thickness, area / thickness))
            else:                # 下端に横 1 行で並べる
                placed.append((x + offset, y, area / thickness, thickness))
            offset += area / thickness
        if width >= height:
            x, width = x + thickness, width - thickness
        else:
            y, height = y + thickness, height - thickness
    result: list[Rect] = [(0.0, 0.0, 0.0, 0.0)] * len(values)
    for index, placed_rect in zip(order, placed):
        result[index] = placed_rect
    return result


def draw_rect(ax: Axes, rect: Rect, color: str, label: str = "",
              linewidth: float = 1.0) -> None:
    """白い枠線付きの長方形を描き、中央にラベルを書く."""
    x, y, width, height = rect
    ax.add_patch(Rectangle((x, y), width, height, facecolor=color,
                           edgecolor="white", linewidth=linewidth))
    if label:
        ax.text(x + width / 2, y + height / 2, label, ha="center",
                va="center", fontsize=9)
