"""本書の図を作成するスクリプト。

Graphviz の dot ファイルを PNG 画像に変換し、matplotlib でグラフを描きます。
作成した画像は、既定では ../source/figures に保存します。

使い方::

    python make_figures.py               # ../source/figures に保存する
    python make_figures.py --out figures # 保存先を指定する

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
from matplotlib.ticker import FuncFormatter  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

# このスクリプトがあるフォルダー
HERE = Path(__file__).resolve().parent

# 既定の保存先
DEFAULT_OUT_DIR = HERE.parent / 'source' / 'figures'

# 図の色（本文の表やコードの色と調和する、落ち着いた色を使う）
BLUE = '#2a78d6'     # 会社の保険、支給の対象など
ORANGE = '#eb6834'   # 自分で加入する保険、給付制限など
GRAY = '#b5b4ae'     # 待期期間
TEXT = '#0b0b0b'     # 文字
TEXT_SUB = '#52514e'  # 補助の文字
GRID = '#e4e3df'     # 目盛り線

# 画像の解像度（dots per inch）
DPI = 150

# 日本語を表示できるフォントの候補（先頭から順に探す）
JAPANESE_FONTS = [
    'BIZ UDGothic', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP', 'IPAexGothic',
]


def choose_font(candidates: list[str]) -> str:
    """候補のうち、インストールされている最初のフォントの名前を返す。"""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    raise RuntimeError('日本語のフォントが見つかりません。')


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
        raise RuntimeError('Graphviz の dot コマンドが見つかりません。')
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


def plot_month_end(dst: Path) -> None:
    """月末に退職する場合と、その前日に退職する場合の保険の違いを描く。

    3 月 28 日から 4 月 3 日までの 7 日間について、どの保険に加入しているかを
    2 本の帯で示す。日付は、3 月 28 日を 0 とした日数で表す。
    """
    days = ['3/28', '3/29', '3/30', '3/31', '4/1', '4/2', '4/3']
    # (行の見出し, 退職日の位置, 資格喪失日の位置)
    cases = [
        ('3 月 31 日に退職', 3, 4),
        ('3 月 30 日に退職', 2, 3),
    ]

    fig, ax = plt.subplots(figsize=(8, 2.8))
    for row, (title, retire, lose) in enumerate(cases):
        y = len(cases) - 1 - row
        # 会社の健康保険・厚生年金保険（3 月 28 日から退職日まで）
        ax.barh(y, lose, left=0, height=0.5, color=BLUE,
                edgecolor='white', linewidth=2)
        # 国民健康保険・国民年金（資格喪失日から）
        ax.barh(y, len(days) - lose, left=lose, height=0.5, color=ORANGE,
                edgecolor='white', linewidth=2)
        ax.annotate(f'資格喪失日 {days[lose]}', xy=(lose, y + 0.25),
                    xytext=(lose, y + 0.45), ha='center', fontsize=9,
                    color=TEXT_SUB,
                    arrowprops={'arrowstyle': '-', 'color': TEXT_SUB})
        month = '会社の保険' if lose >= 4 else '国民健康保険・国民年金'
        ax.text(len(days) + 0.15, y, f'3 月分の保険料：\n{month}',
                va='center', fontsize=9, color=TEXT)

    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([c[0] for c in reversed(cases)])
    ax.set_xticks([i + 0.5 for i in range(len(days))])
    ax.set_xticklabels(days)
    ax.set_xlim(0, len(days))
    ax.set_ylim(-0.5, len(cases) + 0.05)
    style_axes(ax)
    ax.grid(False)
    ax.axvline(4, color=TEXT_SUB, linewidth=1, linestyle=':')
    ax.text(4, len(cases) - 0.15, '月の変わり目', ha='center', fontsize=9,
            color=TEXT_SUB)
    ax.legend(
        handles=[
            Patch(color=BLUE, label='会社の健康保険・厚生年金保険'),
            Patch(color=ORANGE, label='国民健康保険・国民年金'),
        ],
        loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2,
        frameon=False, fontsize=9,
    )
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_benefit_timeline(dst: Path) -> None:
    """基本手当の支給が始まるまでの期間を、離職理由ごとに描く。

    受給資格の決定日を 0 日目とし、待期期間（7 日）と給付制限（1 か月。
    ここでは 30 日として描く）を帯で示す。
    """
    waiting = 7
    restriction = 30
    end = 60
    # (行の見出し, 給付制限の日数)
    cases = [
        ('会社都合など\n（特定受給資格者など）', 0),
        ('正当な理由のない\n自己都合退職', restriction),
    ]

    fig, ax = plt.subplots(figsize=(8, 2.8))
    for row, (title, limit) in enumerate(cases):
        y = len(cases) - 1 - row
        ax.barh(y, waiting, left=0, height=0.5, color=GRAY,
                edgecolor='white', linewidth=2)
        if limit:
            ax.barh(y, limit, left=waiting, height=0.5, color=ORANGE,
                    edgecolor='white', linewidth=2)
            ax.text(waiting + limit / 2, y, '給付制限（1 か月）',
                    ha='center', va='center', fontsize=9, color='white')
        start = waiting + limit
        ax.barh(y, end - start, left=start, height=0.5, color=BLUE,
                edgecolor='white', linewidth=2)
        ax.text(start + 1.5, y, f'{start + 1} 日目から支給の対象',
                ha='left', va='center', fontsize=9, color='white')
        ax.text(waiting / 2, y, '待期', ha='center', va='center',
                fontsize=9, color=TEXT)

    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([c[0] for c in reversed(cases)])
    ax.set_xlim(0, end)
    ax.set_xticks([0, 7, 14, 21, 28, 37, 44, 51, 58])
    ax.set_xlabel('受給資格の決定日からの日数')
    style_axes(ax)
    ax.legend(
        handles=[
            Patch(color=GRAY, label='待期期間（7 日）'),
            Patch(color=ORANGE, label='給付制限'),
            Patch(color=BLUE, label='基本手当の支給の対象'),
        ],
        loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=3,
        frameon=False, fontsize=9,
    )
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def retirement_deduction(years: int) -> int:
    """勤続年数から退職所得控除額（万円）を求める。"""
    if years <= 20:
        return max(80, 40 * years)
    return 800 + 70 * (years - 20)


def plot_retirement_deduction(dst: Path) -> None:
    """勤続年数と退職所得控除額の関係を描く。"""
    years = list(range(1, 41))
    amounts = [retirement_deduction(y) for y in years]

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(years, amounts, color=BLUE, linewidth=2)
    for y in (20, 30):
        value = retirement_deduction(y)
        ax.plot(y, value, marker='o', markersize=7, color=BLUE,
                markeredgecolor='white', markeredgewidth=2)
        ax.annotate(f'{y} 年：{value:,} 万円', xy=(y, value),
                    xytext=(-12, 10), textcoords='offset points',
                    ha='right', fontsize=9, color=TEXT)
    ax.text(15, 230, '1 年あたり 40 万円', ha='center', fontsize=9,
            color=TEXT_SUB)
    ax.text(31, 900, '1 年あたり 70 万円', ha='center', fontsize=9,
            color=TEXT_SUB)

    ax.set_xlim(0, 41)
    ax.set_ylim(0, 2400)
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30, 35, 40])
    ax.set_xlabel('勤続年数（年）')
    ax.set_ylabel('退職所得控除額（万円）')
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, _pos: f'{value:,.0f}'))
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='y', color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_schedule(dst: Path) -> None:
    """退職日から逆算した、引き継ぎと年次有給休暇の消化の日程の例を描く。

    横軸は退職日を 0 とした週数で、退職日の約 3 か月前（12 週前）に
    退職の意思を伝え、残りの有給休暇（約 15 日）を最後の 3 週間で
    消化する場合を示す。
    """
    notice = -12
    handover_start = -10
    last_day = -3
    retire = 0

    fig, ax = plt.subplots(figsize=(8, 2.9))
    # (行の見出し, 開始, 終了, 色, 帯の中の文字)
    bars = [
        ('業務の引き継ぎ', handover_start, last_day, BLUE,
         '引き継ぎ書の作成、後任者と一緒に業務'),
        ('年次有給休暇', last_day, retire, ORANGE, '消化'),
    ]
    rows = ['退職の意思表示'] + [b[0] for b in bars]
    for title, start, end, color, label in bars:
        y = len(rows) - 1 - rows.index(title)
        ax.barh(y, end - start, left=start, height=0.5, color=color,
                edgecolor='white', linewidth=2)
        ax.text((start + end) / 2, y, label, ha='center', va='center',
                fontsize=9, color='white')
    ax.plot(notice, len(rows) - 1, marker='D', markersize=9, color=BLUE,
            markeredgecolor='white', markeredgewidth=2)
    ax.text(notice + 0.4, len(rows) - 1, '上司に伝え、退職日を決める',
            va='center', fontsize=9, color=TEXT)

    for x, label in ((last_day, '最終出社日'), (retire, '退職日')):
        ax.axvline(x, color=TEXT_SUB, linewidth=1, linestyle=':')
        ax.text(x, len(rows) - 0.35, label, ha='center', fontsize=9,
                color=TEXT_SUB)

    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(list(reversed(rows)))
    ax.set_xlim(-13, 0.8)
    ax.set_ylim(-0.5, len(rows) - 0.1)
    ticks = list(range(-12, 1, 2))
    ax.set_xticks(ticks)
    ax.set_xticklabels([f'{-t} 週前' if t else '0' for t in ticks])
    ax.set_xlabel('退職日までの週数')
    style_axes(ax)
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def plot_resident_tax(dst: Path) -> None:
    """住民税の課税の対象となる所得と、納める期間の関係を描く。

    横軸は、退職した年（N 年）の 1 月から翌年（N + 1 年）の 12 月までの
    24 か月で、0 が N 年 1 月を表す。住民税は、前年の所得にかかり、
    6 月から翌年 5 月までの 12 回に分けて納める。
    """
    # (行の見出し, 開始の月, 終了の月, 色)
    rows = [
        ('N − 2 年の所得', 0, 5, GRAY),
        ('N − 1 年の所得', 5, 17, BLUE),
        ('N 年の所得\n（退職した年）', 17, 24, ORANGE),
    ]
    # 退職した月と、住民税の残りの納め方
    periods = [
        (0, 4, '1〜4 月に退職：\n5 月分まで一括'),
        (4, 5, '5 月'),
        (5, 12, '6〜12 月に退職：次から選ぶ\n一括、普通徴収、\n転職先での特別徴収'),
    ]

    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    n = len(rows) + 1
    for i, (title, start, end, color) in enumerate(rows):
        y = n - 1 - i
        ax.barh(y, end - start, left=start, height=0.5, color=color,
                edgecolor='white', linewidth=2)
    ax.text(11, n - 2, '6 月から翌年 5 月までの 12 回で納める',
            ha='center', va='center', fontsize=9, color='white')
    ax.text(20.5, n - 3, '翌年 6 月から納める', ha='center',
            va='center', fontsize=9, color='white')
    for start, end, label in periods:
        ax.barh(0, end - start, left=start, height=0.8, color='white',
                edgecolor=TEXT_SUB, linewidth=1)
        if end - start > 1:
            ax.text((start + end) / 2, 0, label, ha='center', va='center',
                    fontsize=8.5, color=TEXT)
    ax.annotate('5 月に退職：5 月分を差し引く', xy=(4.5, -0.4),
                xytext=(4.5, -1.1), ha='center', fontsize=8.5, color=TEXT,
                arrowprops={'arrowstyle': '-', 'color': TEXT_SUB})

    ax.axvline(12, color=TEXT_SUB, linewidth=1, linestyle=':')
    ax.text(6, n - 0.3, '退職した年（N 年）', ha='center', fontsize=9,
            color=TEXT_SUB)
    ax.text(18, n - 0.3, '翌年（N + 1 年）', ha='center', fontsize=9,
            color=TEXT_SUB)

    labels = ['退職した月と\n住民税の納め方'] + [r[0] for r in reversed(rows)]
    ax.set_yticks(range(n))
    ax.set_yticklabels(labels)
    ax.set_xticks([m + 0.5 for m in range(24)])
    ax.set_xticklabels([str(m % 12 + 1) for m in range(24)], fontsize=8)
    ax.set_xlim(0, 24)
    ax.set_ylim(-1.4, n + 0.1)
    ax.set_xlabel('月')
    style_axes(ax)
    ax.grid(False)
    fig.savefig(dst, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def make_all(out_dir: Path) -> list[Path]:
    """すべての図を作成し、作成したファイルの一覧を返す。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    dot_names = (
        'retirement_flow', 'deadlines', 'health_insurance_choice',
        'pension_types',
    )
    for name in dot_names:
        dst = out_dir / f'{name}.png'
        render_dot(HERE / f'{name}.dot', dst)
        made.append(dst)

    plots = {
        'month_end.png': plot_month_end,
        'schedule.png': plot_schedule,
        'benefit_timeline.png': plot_benefit_timeline,
        'retirement_deduction.png': plot_retirement_deduction,
        'resident_tax.png': plot_resident_tax,
    }
    for filename, plot in plots.items():
        dst = out_dir / filename
        plot(dst)
        made.append(dst)
    return made


def main() -> None:
    """コマンドラインから実行したときの処理。"""
    parser = argparse.ArgumentParser(description='本書の図を作成します。')
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT_DIR,
                        help='画像の保存先のフォルダー')
    args = parser.parse_args()
    for path in make_all(args.out):
        print(f'作成しました：{path}')


if __name__ == '__main__':
    main()
