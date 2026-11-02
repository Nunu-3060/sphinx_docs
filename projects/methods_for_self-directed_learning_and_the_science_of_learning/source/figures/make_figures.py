"""本文で使う matplotlib の図を生成する。

conf.py から make_all() を呼び出し、source/_generated/ に PNG を出力する。
図はいずれも記憶を単純化したモデルによる模式図であり、実測値ではない。

モデル:
    保持率 R(t) = 1 / (1 + t / (9 * S))
        t: 最後の学習からの経過日数
        S: 安定性（保持率が 0.9 まで下がるのにかかる日数）
    復習すると安定性 S は BASE_GAIN + GAIN * (1 - R) 倍になる。
    R は復習した時点の保持率である。思い出しにくくなってから復習するほど
    安定性が大きく伸びる、という「望ましい困難」の考え方を単純な式で
    表したものである。
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from numpy.typing import NDArray  # noqa: E402

plt.rcParams['font.family'] = ['Meiryo', 'Yu Gothic', 'MS Gothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

INITIAL_STABILITY = 1.0  # 初回学習後の安定性（日）
BASE_GAIN = 1.3          # 復習による安定性の伸び（最小値）
GAIN = 8.0               # 思い出しにくさに応じた安定性の伸び
DPI = 110

COLOR_MAIN = '#1565c0'
COLOR_SUB = '#c62828'
COLOR_GRID = '#dddddd'


def retention(elapsed: float, stability: float) -> float:
    """最後の学習から elapsed 日後の保持率を返す。"""
    return 1.0 / (1.0 + elapsed / (9.0 * stability))


def simulate(review_days: list[float], t_end: float, n: int = 2000) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """初回学習を 0 日目とし、review_days に復習したときの保持率の推移を返す。"""
    t = np.linspace(0.0, t_end, n)
    r = np.empty_like(t)
    stability = INITIAL_STABILITY
    last = 0.0
    events = sorted(review_days)
    k = 0
    for i, ti in enumerate(t):
        while k < len(events) and events[k] <= ti:
            recall = retention(events[k] - last, stability)
            stability *= BASE_GAIN + GAIN * (1.0 - recall)
            last = events[k]
            k += 1
        r[i] = retention(float(ti) - last, stability)
    return t, r


def _style(ax: plt.Axes, xlabel: str) -> None:
    ax.set_xlabel(xlabel)
    ax.set_ylabel('思い出せる確率（モデル）')
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, color=COLOR_GRID, linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def make_forgetting_curve(path: pathlib.Path) -> None:
    """復習しない場合と、間隔を広げながら復習した場合の比較図。"""
    t_end = 30.0
    t0, r0 = simulate([], t_end)
    t1, r1 = simulate([1.0, 3.0, 7.0, 14.0], t_end)

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(t0, r0, color=COLOR_SUB, linestyle='--', label='復習しない')
    ax.plot(t1, r1, color=COLOR_MAIN, label='1, 3, 7, 14 日目に復習する')
    for day in [1.0, 3.0, 7.0, 14.0]:
        ax.axvline(day, color=COLOR_MAIN, linewidth=0.6, alpha=0.4)
    _style(ax, '初回学習からの経過日数')
    ax.legend(loc='lower left', frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


def make_spacing_comparison(path: pathlib.Path) -> None:
    """同じ 4 回の学習を 1 日に集中させた場合と、日を空けた場合の比較図。"""
    t_end = 30.0
    massed = [0.04, 0.08, 0.12]  # 0 日目のうちに 1 時間おきに 3 回繰り返す
    spaced = [1.0, 3.0, 7.0]
    tm, rm = simulate(massed, t_end)
    ts, rs = simulate(spaced, t_end)

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(tm, rm, color=COLOR_SUB, linestyle='--', label='集中学習（0 日目に 4 回）')
    ax.plot(ts, rs, color=COLOR_MAIN, label='分散学習（0, 1, 3, 7 日目に 1 回ずつ）')
    test_day = 21.0
    ax.axvline(test_day, color='#555555', linewidth=0.8, linestyle=':')
    ax.annotate('21 日目に確認テスト', xy=(test_day, 0.05), xytext=(test_day + 0.5, 0.05), fontsize=9, color='#555555')
    _style(ax, '初回学習からの経過日数')
    ax.legend(loc='lower left', frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


def make_all(output_dir: pathlib.Path) -> None:
    """すべての図を output_dir に出力する。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    make_forgetting_curve(output_dir / 'forgetting_curve.png')
    make_spacing_comparison(output_dir / 'spacing_comparison.png')


if __name__ == '__main__':
    make_all(pathlib.Path(__file__).resolve().parent.parent / '_generated')
