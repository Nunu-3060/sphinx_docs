"""本文で使用する図を matplotlib で生成するスクリプト。

conf.py から generate_all() を呼び出し、ビルドのたびに図を出力する。
"""

import math
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import numpy.typing as npt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from scipy import stats  # noqa: E402

FONT_CANDIDATES = ["Yu Gothic", "Meiryo", "BIZ UDGothic", "Noto Sans JP", "Noto Sans CJK JP", "IPAexGothic",
                   "Hiragino Sans", "MS Gothic"]


def setup_font() -> None:
    """利用可能な日本語フォントを探して matplotlib に設定する。"""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 120
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3


def save(fig: Figure, out_dir: Path, name: str) -> None:
    """図を PNG で保存して閉じる。"""
    fig.tight_layout()
    fig.savefig(out_dir / name)
    plt.close(fig)


def venn(out_dir: Path) -> None:
    """集合演算のベン図。"""
    x, y = np.meshgrid(np.linspace(-2.2, 2.2, 600), np.linspace(-1.6, 1.6, 440))
    in_a = (x + 0.6) ** 2 + y ** 2 <= 1.0
    in_b = (x - 0.6) ** 2 + y ** 2 <= 1.0
    panels: list[tuple[str, npt.NDArray[np.bool_]]] = [
        (r"$A \cup B$", in_a | in_b),
        (r"$A \cap B$", in_a & in_b),
        (r"$A \setminus B$", in_a & ~in_b),
        (r"$\overline{A}$", ~in_a),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for ax, (title, mask) in zip(axes, panels):
        ax.imshow(mask, extent=(-2.2, 2.2, -1.6, 1.6), origin="lower", cmap="Blues", vmin=0, vmax=1.6)
        theta = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(theta) - 0.6, np.sin(theta), color="black", lw=1)
        ax.plot(np.cos(theta) + 0.6, np.sin(theta), color="black", lw=1)
        ax.text(-1.0, 0.0, "A", fontsize=14, ha="center", va="center")
        ax.text(1.0, 0.0, "B", fontsize=14, ha="center", va="center")
        ax.text(-2.0, 1.35, "U", fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
    save(fig, out_dir, "ch02_venn.png")


def birthday(out_dir: Path) -> None:
    """誕生日問題の確率。"""
    ns = np.arange(1, 81)
    probs = []
    p_distinct = 1.0
    for n in ns:
        p_distinct *= (365 - (n - 1)) / 365
        probs.append(1 - p_distinct)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ns, probs, marker=".", label="一致する組がある確率")
    ax.axhline(0.5, color="gray", ls="--", lw=1)
    ax.axvline(23, color="gray", ls="--", lw=1)
    ax.annotate("n = 23 で 0.5 を超える", xy=(23, 0.507), xytext=(35, 0.35), arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("人数 n")
    ax.set_ylabel("確率")
    ax.legend(loc="lower right")
    save(fig, out_dir, "ch06_birthday.png")


def bar_panels(out_dir: Path, name: str, title_pmfs: list[tuple[str, npt.NDArray[np.int64], npt.NDArray[np.float64]]],
               xlabel: str) -> None:
    """複数の確率質量関数を横に並べた棒グラフを描く。"""
    fig, axes = plt.subplots(1, len(title_pmfs), figsize=(4 * len(title_pmfs), 3.2), sharey=True)
    for ax, (title, ks, pmf) in zip(np.atleast_1d(axes), title_pmfs):
        ax.bar(ks, pmf, width=0.8)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
    np.atleast_1d(axes)[0].set_ylabel("確率")
    save(fig, out_dir, name)


def distributions(out_dir: Path) -> None:
    """第 8 章の各分布の確率質量関数。"""
    ks = np.arange(0, 21)
    bar_panels(out_dir, "ch08_binomial.png", [
        (f"Bin(20, {p})", ks, stats.binom.pmf(ks, 20, p)) for p in [0.2, 0.5, 0.8]
    ], "k")
    ks1 = np.arange(1, 21)
    bar_panels(out_dir, "ch08_geometric.png", [
        (f"Geo({p})", ks1, stats.geom.pmf(ks1, p)) for p in [0.2, 0.5]
    ], "k")
    ks2 = np.arange(0, 21)
    bar_panels(out_dir, "ch08_poisson.png", [
        (f"Po({lam})", ks2, stats.poisson.pmf(ks2, lam)) for lam in [1, 4, 10]
    ], "k")

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    ks3 = np.arange(0, 13)
    for ax, n in zip(axes, [10, 100]):
        p = 3 / n
        ax.bar(ks3 - 0.2, stats.binom.pmf(ks3, n, p), width=0.4, label=f"Bin({n}, {p:g})")
        ax.bar(ks3 + 0.2, stats.poisson.pmf(ks3, 3), width=0.4, label="Po(3)")
        ax.set_xlabel("k")
        ax.legend()
    axes[0].set_ylabel("確率")
    save(fig, out_dir, "ch08_poisson_approx.png")


def dice_sum(out_dir: Path) -> None:
    """サイコロ n 個の和の分布。"""
    die = np.array([0.0] + [1 / 6] * 6)
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2))
    dist = np.array([1.0])
    for n, ax in enumerate(axes, start=1):
        dist = np.convolve(dist, die)
        ks = np.arange(len(dist))
        ax.bar(ks[n:], dist[n:], width=0.8)
        ax.set_title(f"サイコロ {n} 個の和")
        ax.set_xlabel("和")
    axes[0].set_ylabel("確率")
    save(fig, out_dir, "ch09_dice_sum.png")


def lln(out_dir: Path) -> None:
    """大数の法則: 標本平均の推移。"""
    rng = np.random.default_rng(1)
    n = 5000
    ns = np.arange(1, n + 1)
    fig, ax = plt.subplots(figsize=(8, 4))
    for _ in range(5):
        rolls = rng.integers(1, 7, size=n)
        ax.plot(ns, np.cumsum(rolls) / ns, lw=1)
    ax.axhline(3.5, color="black", ls="--", lw=1, label="期待値 3.5")
    ax.set_xscale("log")
    ax.set_xlabel("投げた回数 n（対数目盛）")
    ax.set_ylabel("標本平均")
    ax.legend()
    save(fig, out_dir, "ch10_lln.png")


def clt(out_dir: Path) -> None:
    """中心極限定理: 標準化したサイコロの和の分布と標準正規分布の密度関数。"""
    die = np.array([0.0] + [1 / 6] * 6)
    mu, sigma = 3.5, math.sqrt(35 / 12)
    zs = np.linspace(-3.5, 3.5, 300)
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), sharey=True)
    dist = np.array([1.0])
    count = 0
    for n_target, ax in zip([1, 2, 5, 30], axes):
        while count < n_target:
            dist = np.convolve(dist, die)
            count += 1
        ks = np.arange(len(dist))
        scale = sigma * math.sqrt(n_target)
        z = (ks - n_target * mu) / scale
        mask = dist > 0
        # 隣り合う値の間隔は 1 / scale なので、確率を scale 倍すると密度の近似になる
        ax.bar(z[mask], dist[mask] * scale, width=0.9 / scale, alpha=0.7, label="標準化した和")
        ax.plot(zs, stats.norm.pdf(zs), color="black", lw=1.5, label="N(0, 1)")
        ax.set_title(f"n = {n_target}")
        ax.set_xlim(-3.5, 3.5)
        ax.set_xlabel("z")
    axes[0].set_ylabel("密度")
    axes[0].legend(loc="upper left", fontsize=8)
    save(fig, out_dir, "ch10_clt.png")


def markov_convergence(out_dir: Path) -> None:
    """マルコフ連鎖の分布が定常分布に収束する様子。"""
    p = np.array([[0.7, 0.2, 0.1], [0.3, 0.4, 0.3], [0.2, 0.4, 0.4]])
    labels = ["晴れ", "曇り", "雨"]
    steps = np.arange(0, 11)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, start, title in zip(axes, [0, 2], ["晴れから開始", "雨から開始"]):
        dist = np.zeros(3)
        dist[start] = 1.0
        history = [dist]
        for _ in steps[1:]:
            dist = dist @ p
            history.append(dist)
        arr = np.array(history)
        for j in range(3):
            ax.plot(steps, arr[:, j], marker="o", ms=3, label=labels[j])
        ax.set_title(title)
        ax.set_xlabel("日数 n")
    axes[0].set_ylabel("確率")
    axes[1].legend()
    save(fig, out_dir, "ch11_convergence.png")


def bloom(out_dir: Path) -> None:
    """ブルームフィルタの偽陽性率とハッシュ関数の個数 k。"""
    ks = np.arange(1, 21)
    fig, ax = plt.subplots(figsize=(7, 4))
    for ratio in [5, 10, 20]:
        fp = (1 - np.exp(-ks / ratio)) ** ks
        ax.plot(ks, fp, marker="o", ms=3, label=f"m/n = {ratio}")
        k_opt = ratio * math.log(2)
        ax.axvline(k_opt, color="gray", ls=":", lw=1)
    ax.set_yscale("log")
    ax.set_xlabel("ハッシュ関数の個数 k")
    ax.set_ylabel("偽陽性率（対数目盛）")
    ax.legend()
    save(fig, out_dir, "ch12_bloom.png")


def monte_carlo_pi(out_dir: Path) -> None:
    """モンテカルロ法による円周率の推定。"""
    rng = np.random.default_rng(3)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    x, y = rng.random(2000), rng.random(2000)
    inside = x * x + y * y <= 1
    axes[0].scatter(x[inside], y[inside], s=3, label="四分円の内側")
    axes[0].scatter(x[~inside], y[~inside], s=3, label="四分円の外側")
    theta = np.linspace(0, np.pi / 2, 100)
    axes[0].plot(np.cos(theta), np.sin(theta), color="black", lw=1)
    axes[0].set_aspect("equal")
    axes[0].set_title("N = 2000 の乱数点")
    axes[0].legend(loc="lower left", fontsize=8, framealpha=1)

    ns = np.unique(np.logspace(1, 6, 30).astype(int))
    errors = []
    for n in ns:
        estimates = [4 * np.mean(rng.random(n) ** 2 + rng.random(n) ** 2 <= 1) for _ in range(20)]
        errors.append(float(np.mean(np.abs(np.array(estimates) - math.pi))))
    axes[1].loglog(ns, errors, marker="o", ms=3, label="平均絶対誤差（20 回）")
    axes[1].loglog(ns, 1.3 / np.sqrt(ns), ls="--", color="gray", label=r"$\propto 1/\sqrt{N}$")
    axes[1].set_xlabel("点の個数 N")
    axes[1].set_ylabel("誤差")
    axes[1].legend()
    save(fig, out_dir, "ch12_pi.png")


FIGURES: list[Callable[[Path], None]] = [
    venn, birthday, distributions, dice_sum, lln, clt, markov_convergence, bloom, monte_carlo_pi,
]


def generate_all(out_dir: Path) -> None:
    """すべての図を out_dir に生成する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_font()
    for figure in FIGURES:
        figure(out_dir)


if __name__ == "__main__":
    generate_all(Path(__file__).resolve().parent.parent / "_generated")
