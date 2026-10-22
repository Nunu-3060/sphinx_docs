"""本書の図を作成するスクリプト。

Graphviz の dot ファイルを PNG 画像に変換し、matplotlib で日程の図を描く。
作成した画像は、既定では ../source/figures に保存する。

使い方::

    python make_figures.py                # ../source/figures に保存する
    python make_figures.py --out figures  # 保存先を指定する

必要なもの:

* Graphviz（dot コマンドが実行できること）
* matplotlib
* 日本語のフォント（BIZ UDGothic、Yu Gothic、Meiryo などのいずれか）
"""

import argparse
import shutil
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use('Agg')  # 画面に表示せず、ファイルに保存する

import matplotlib.pyplot as plt  # noqa: E402  (matplotlib.use の後に読み込む)
from matplotlib import font_manager  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402

# このスクリプトがあるフォルダー
HERE = Path(__file__).resolve().parent

# 既定の保存先
DEFAULT_OUT_DIR = HERE.parent / 'source' / 'figures'

# 図の色
BLUE = '#2a78d6'      # 転職活動
ORANGE = '#eb6834'    # 退職に関する活動
GREEN = '#3a9a6b'     # 入社後の活動
TEXT = '#0b0b0b'      # 文字
TEXT_SUB = '#52514e'  # 補助の文字
GRID = '#e4e3df'      # 目盛り線

# 画像の解像度（dots per inch）
DPI = 150

# 日本語を表示できるフォントの候補（先頭から順に探す）
JAPANESE_FONTS = [
    'BIZ UDGothic', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP', 'IPAexGothic',
]

# 帯 1 本分の情報：(見出し, 開始, 終了, 色)
Band = tuple[str, float, float, str]


def choose_font(candidates: list[str]) -> str:
    """候補のうち、インストールされている最初のフォントの名前を返す。"""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    raise RuntimeError('日本語のフォントが見つからない。')


plt.rcParams['font.family'] = choose_font(JAPANESE_FONTS)
plt.rcParams['axes.edgecolor'] = TEXT_SUB
plt.rcParams['axes.labelcolor'] = TEXT
plt.rcParams['xtick.color'] = TEXT_SUB
plt.rcParams['ytick.color'] = TEXT_SUB
plt.rcParams['text.color'] = TEXT


def render_dot(src: Path, dst: Path) -> None:
    """Graphviz の dot ファイルを PNG 画像に変換する。"""
    dot = shutil.which('dot')
    if dot is None:
        raise RuntimeError('Graphviz の dot コマンドが見つからない。')
    subprocess.run(
        [dot, '-Tpng', f'-Gdpi={DPI}', str(src), '-o', str(dst)],
        check=True,
    )


def style_axes(ax: Axes) -> None:
    """グラフの枠と目盛り線を目立たない見た目にする。"""
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.grid(axis='x', color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def draw_bands(ax: Axes, bands: list[Band]) -> None:
    """帯を上から順に描き、縦軸に見出しを付ける。"""
    n = len(bands)
    for row, (_, start, end, color) in enumerate(bands):
        y = n - 1 - row  # 1 つ目の帯を一番上に描く
        ax.barh(y, end - start, left=start, height=0.55, color=color)
    ax.set_yticks(range(n))
    ax.set_yticklabels([b[0] for b in reversed(bands)])
    ax.set_ylim(-0.6, n - 0.4)


def mark(ax: Axes, x: float, top: float, label: str) -> None:
    """縦の点線と、その上に見出しを描く。"""
    ax.axvline(x, color=TEXT_SUB, linewidth=1, linestyle=':')
    ax.text(x, top, label, ha='center', va='bottom', fontsize=9, color=TEXT_SUB)


def plot_overview(dst: Path) -> None:
    """転職の流れと、各段階のおおよその期間の例を描く（第 2 章）。

    横軸は、転職を考え始めてからの月数である。
    """
    bands: list[Band] = [
        ('転職を考える・情報を集める', 0.0, 1.0, BLUE),
        ('経歴の棚卸し・応募書類の作成', 0.5, 1.5, BLUE),
        ('求人を探す・応募する', 1.0, 3.0, BLUE),
        ('選考', 1.5, 3.5, BLUE),
        ('内定・労働条件の確認', 3.0, 4.0, BLUE),
        ('退職の申し出・引き継ぎ', 4.0, 5.5, ORANGE),
        ('有給休暇の消化', 5.5, 6.0, ORANGE),
        ('入社後の手続き・オンボーディング', 6.0, 9.0, GREEN),
    ]
    fig, ax = plt.subplots(figsize=(9, 4.2))
    draw_bands(ax, bands)
    top = len(bands) - 0.45
    mark(ax, 4.0, top, '内定の承諾')
    mark(ax, 6.0, top, '入社')
    ax.set_xticks(range(10))
    ax.set_xticklabels([f'{m} か月' for m in range(10)], fontsize=9)
    ax.set_xlim(0, 9)
    ax.set_xlabel('転職を考え始めてからの期間')
    style_axes(ax)
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_schedule(dst: Path) -> None:
    """内定の承諾から入社日までを逆算した日程の例を描く（第 8 章）。

    横軸は、内定を承諾した週を 0 とした週数である。
    """
    bands: list[Band] = [
        ('上司に退職を申し出る', 0.5, 1.0, ORANGE),
        ('退職日の確定・退職届の提出', 1.0, 1.5, ORANGE),
        ('引き継ぎ', 1.0, 6.0, ORANGE),
        ('有給休暇の消化', 6.0, 9.0, ORANGE),
        ('入社の準備', 7.0, 9.0, GREEN),
    ]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    draw_bands(ax, bands)
    top = len(bands) - 0.45
    mark(ax, 0.0, top, '内定の承諾')
    mark(ax, 6.0, top, '最終出社日')
    mark(ax, 9.0, top, '退職日／入社日')
    ax.set_xticks(range(11))
    ax.set_xticklabels([f'{w} 週' for w in range(11)], fontsize=9)
    ax.set_xlim(-0.2, 10)
    ax.set_xlabel('内定を承諾してからの期間')
    style_axes(ax)
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def make_all(out_dir: Path) -> list[Path]:
    """すべての図を作成し、作成したファイルの一覧を返す。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    for name in ('selection_flow', 'procedures'):
        dst = out_dir / f'{name}.png'
        render_dot(HERE / f'{name}.dot', dst)
        made.append(dst)

    plots = {
        'overview.png': plot_overview,
        'schedule.png': plot_schedule,
    }
    for filename, plot in plots.items():
        dst = out_dir / filename
        plot(dst)
        made.append(dst)
    return made


def main() -> None:
    """コマンドラインから実行したときの処理。"""
    parser = argparse.ArgumentParser(description='本書の図を作成する。')
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT_DIR, help='画像の保存先のフォルダー')
    args = parser.parse_args()
    for path in make_all(args.out):
        print(f'作成した：{path}')


if __name__ == '__main__':
    main()
