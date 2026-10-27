"""モンテカルロ積分の収束と重点サンプリングの効果を確かめる。

1. 正方形内に一様に点を打ち、四分円に入った割合から円周率を推定する。
2. 半球上の積分 ∫ cos^3θ dω（厳密値は π / 2）を、一様サンプリングと
   コサイン重み付きサンプリングの 2 通りで推定し、誤差を比べる。

実行例::

    python monte_carlo.py --output-dir .
"""

import argparse
import math
from collections.abc import Callable
from pathlib import Path

import matplotlib
import numpy as np
import numpy.typing as npt

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FloatArray = npt.NDArray[np.float64]
Estimator = Callable[[int, np.random.Generator], float]


def estimate_pi(n: int, rng: np.random.Generator) -> float:
    """n 個の乱数点を使って円周率を推定する。"""
    x = rng.random(n)
    y = rng.random(n)
    inside = x * x + y * y <= 1.0
    return 4.0 * float(np.mean(inside))


def integrand(cos_theta: FloatArray) -> FloatArray:
    """被積分関数 cos^3θ。半球上で積分すると π / 2 になる。"""
    result: FloatArray = cos_theta ** 3
    return result


EXACT_VALUE = math.pi / 2.0


def estimate_uniform(n: int, rng: np.random.Generator) -> float:
    """半球上の一様サンプリング（pdf = 1 / 2π）による推定値。

    半球上の一様な方向では cosθ が [0, 1] の一様分布に従う。
    被積分関数が θ だけに依存するので、cosθ だけをサンプリングすればよい。
    """
    cos_theta = rng.random(n)
    pdf = 1.0 / (2.0 * math.pi)
    return float(np.mean(integrand(cos_theta) / pdf))


def estimate_cosine(n: int, rng: np.random.Generator) -> float:
    """コサイン重み付きサンプリング（pdf = cosθ / π）による推定値。"""
    cos_theta = np.sqrt(1.0 - rng.random(n))
    pdf = cos_theta / math.pi
    return float(np.mean(integrand(cos_theta) / pdf))


def rms_error(estimator: Estimator, exact: float, n: int, trials: int, rng: np.random.Generator) -> float:
    """推定を trials 回繰り返したときの二乗平均平方根誤差を返す。"""
    errors = np.array([estimator(n, rng) - exact for _ in range(trials)])
    return float(np.sqrt(np.mean(errors ** 2)))


def sample_counts() -> list[int]:
    """グラフの横軸に使うサンプル数（10 から 100000 まで対数的に等間隔）。"""
    return sorted({int(round(n)) for n in np.logspace(1, 5, 17)})


def plot_convergence(output: Path, seed: int = 0) -> None:
    """円周率推定のサンプル数と誤差の関係を両対数グラフで描く。"""
    rng = np.random.default_rng(seed)
    counts = sample_counts()
    errors = [rms_error(estimate_pi, math.pi, n, 100, rng) for n in counts]
    reference = errors[0] * math.sqrt(counts[0]) / np.sqrt(counts)

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.loglog(counts, errors, "o-", label="RMS error of the estimate")
    ax.loglog(counts, reference, "--", color="gray", label=r"$\propto 1/\sqrt{N}$")
    ax.set_xlabel("Number of samples N")
    ax.set_ylabel("RMS error")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def plot_importance(output: Path, seed: int = 0) -> None:
    """一様サンプリングとコサイン重み付きサンプリングの誤差を比べる。"""
    rng = np.random.default_rng(seed)
    counts = sample_counts()
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for name, estimator in [("Uniform hemisphere sampling", estimate_uniform),
                            ("Cosine-weighted sampling", estimate_cosine)]:
        errors = [rms_error(estimator, EXACT_VALUE, n, 100, rng) for n in counts]
        ax.loglog(counts, errors, "o-", label=name)
    ax.set_xlabel("Number of samples N")
    ax.set_ylabel("RMS error")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="モンテカルロ積分の実験")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="出力先フォルダ")
    args = parser.parse_args()

    rng = np.random.default_rng(0)
    for n in [100, 10_000, 1_000_000]:
        print(f"N = {n:>9}: 円周率の推定値 = {estimate_pi(n, rng):.5f}")
    for n in [16, 256]:
        print(f"N = {n:>4}: 一様 = {estimate_uniform(n, rng):.4f}, "
              f"コサイン重み付き = {estimate_cosine(n, rng):.4f}, 厳密値 = {EXACT_VALUE:.4f}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    plot_convergence(args.output_dir / "mc_convergence.png")
    plot_importance(args.output_dir / "mc_importance.png")
    print(f"{args.output_dir} に mc_convergence.png, mc_importance.png を保存した")


if __name__ == "__main__":
    main()
