"""本文で使用する matplotlib の図を生成するスクリプト。

build_html.bat から Sphinx のビルド前に実行される。
生成した画像は source/images/ に保存する。
"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'images'
FONT_CANDIDATES = ['Noto Sans JP', 'Yu Gothic', 'Meiryo']
MARK_COLOR = '#2a6fdb'
INK_PRIMARY = '#1f2328'
INK_MUTED = '#59636e'
GRID_COLOR = '#d8dee4'

# ラベルの位置ごとのオフセット（ポイント単位）と水平方向の揃え
LABEL_POSITIONS: dict[str, tuple[tuple[int, int], str]] = {
    'upper_left': ((-8, 10), 'right'),
    'below': ((0, -24), 'center'),
    'right': ((10, -4), 'left'),
}


@dataclass(frozen=True)
class DataPoint:
    """図に描く 1 製品分のデータ。"""

    year: int
    label: str
    value: float
    position: str = 'upper_left'  # ラベルの位置（LABEL_POSITIONS のキー）。重なりを避けるために変更する


# トランジスタ数（単位: 10 億個）。各社のアーキテクチャ資料による公称値。
TRANSISTORS: list[DataPoint] = [
    DataPoint(1999, 'GeForce 256', 0.023, position='right'),
    DataPoint(2006, 'G80', 0.681),
    DataPoint(2010, 'GF100', 3.0),
    DataPoint(2012, 'GK110', 7.08),
    DataPoint(2016, 'GP100', 15.3, position='below'),
    DataPoint(2017, 'GV100', 21.1),
    DataPoint(2020, 'GA100', 54.2),
    DataPoint(2022, 'GH100', 80.0),
    DataPoint(2024, 'B200', 208.0),
]

# メモリ帯域幅（単位: GB/s）。各製品の公称値。
BANDWIDTH: list[DataPoint] = [
    DataPoint(1999, 'GeForce 256 DDR', 4.8, position='right'),
    DataPoint(2006, 'GeForce 8800 GTX', 86.4),
    DataPoint(2010, 'Tesla C2050', 144.0),
    DataPoint(2012, 'Tesla K20X', 250.0),
    DataPoint(2016, 'Tesla P100', 732.0, position='below'),
    DataPoint(2017, 'Tesla V100', 900.0),
    DataPoint(2020, 'A100', 1555.0),
    DataPoint(2022, 'H100', 3350.0),
    DataPoint(2024, 'B200', 8000.0),
]


def select_fonts() -> list[str]:
    """標準の太さ（400）で使える日本語フォントを優先順に並べて返す。

    Noto Sans JP が可変フォント版のみの場合、matplotlib では極細の字形しか使えないため候補から外す。
    """
    usable = {f.name for f in font_manager.fontManager.ttflist if f.weight == 400 or f.weight == 'normal'}
    available = [name for name in FONT_CANDIDATES if name in usable]
    return available if available else ['sans-serif']


def format_number(value: float, _position: int) -> str:
    """対数軸の目盛りを読みやすい数値表記にする。"""
    if value >= 1:
        return f'{value:,.0f}'
    return f'{value:g}'


def plot_log_trend(points: list[DataPoint], title: str, ylabel: str, filename: str) -> None:
    """年ごとの推移を対数軸の折れ線グラフとして保存する。"""
    years = [p.year for p in points]
    values = [p.value for p in points]

    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=110)
    ax.plot(years, values, color=MARK_COLOR, linewidth=2, marker='o', markersize=7,
            markeredgecolor='white', markeredgewidth=2, zorder=3)

    for p in points:
        offset, align = LABEL_POSITIONS[p.position]
        ax.annotate(p.label, (p.year, p.value), textcoords='offset points', xytext=offset,
                    ha=align, fontsize=9, color=INK_PRIMARY)

    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(FuncFormatter(format_number))
    ax.set_title(title, fontsize=13, color=INK_PRIMARY, loc='left')
    ax.set_xlabel('発表年', color=INK_MUTED)
    ax.set_ylabel(ylabel, color=INK_MUTED)
    ax.set_xlim(1997, 2026)
    ax.grid(True, which='major', color=GRID_COLOR, linewidth=0.8)
    ax.tick_params(colors=INK_MUTED)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(GRID_COLOR)

    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename)
    plt.close(fig)


def main() -> None:
    """すべての図を生成する。"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams['font.family'] = select_fonts()
    plot_log_trend(TRANSISTORS, 'NVIDIA の大型 GPU のトランジスタ数', 'トランジスタ数（10 億個、対数軸）',
                   'transistors.png')
    plot_log_trend(BANDWIDTH, 'NVIDIA の GPU のメモリ帯域幅', 'メモリ帯域幅（GB/s、対数軸）',
                   'bandwidth.png')


if __name__ == '__main__':
    main()
