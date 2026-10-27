"""フレネル反射率と Schlick 近似を比較するグラフを描く。

空気中から各物質に光が入射するときの反射率を、入射角の関数として描く。
実線がフレネル方程式による厳密な値、破線が Schlick 近似である。

実行例::

    python fresnel_plot.py --output fresnel.png
"""

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
import numpy.typing as npt

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FloatArray = npt.NDArray[np.float64]

# 物質名と複素屈折率 n + ik（波長 550 nm 付近の概略値）
MATERIALS: list[tuple[str, complex]] = [
    ("Water (n = 1.33)", complex(1.33, 0.0)),
    ("Glass (n = 1.5)", complex(1.5, 0.0)),
    ("Aluminium (n = 0.96 + 6.69i)", complex(0.96, 6.69)),
]


def fresnel_reflectance(cos_i: FloatArray, eta: complex) -> FloatArray:
    """空気（屈折率 1）から複素屈折率 eta の物質へ入射する光の反射率（偏光なし）を返す。

    s 偏光と p 偏光の反射率の平均をとる。eta の虚部を 0 にすれば誘電体、
    虚部が大きければ金属を表す。
    """
    cos_i_c = cos_i.astype(np.complex128)
    sin2_t = (1.0 - cos_i_c ** 2) / eta ** 2      # スネルの法則
    cos_t = np.sqrt(1.0 - sin2_t)
    r_s = (cos_i_c - eta * cos_t) / (cos_i_c + eta * cos_t)
    r_p = (eta * cos_i_c - cos_t) / (eta * cos_i_c + cos_t)
    result: FloatArray = 0.5 * (np.abs(r_s) ** 2 + np.abs(r_p) ** 2)
    return result


def schlick(cos_i: FloatArray, f0: float) -> FloatArray:
    """Schlick 近似 F0 + (1 - F0)(1 - cosθ)^5 を返す。"""
    result: FloatArray = f0 + (1.0 - f0) * (1.0 - cos_i) ** 5
    return result


def plot_fresnel(output: Path) -> None:
    """入射角と反射率の関係を描いて保存する。"""
    angles = np.linspace(0.0, 90.0, 361)
    cos_i = np.cos(np.radians(angles))

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for (name, eta), color in zip(MATERIALS, ["tab:blue", "tab:green", "tab:gray"]):
        exact = fresnel_reflectance(cos_i, eta)
        f0 = float(exact[0])
        ax.plot(angles, exact, color=color, label=f"{name}, F0 = {f0:.2f}")
        ax.plot(angles, schlick(cos_i, f0), color=color, linestyle="--")
    ax.plot([], [], color="black", linestyle="--", label="Schlick approximation")
    ax.set_xlabel("Angle of incidence [deg]")
    ax.set_ylabel("Reflectance")
    ax.set_xlim(0.0, 90.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_xticks(np.arange(0, 91, 15))
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="フレネル反射率のグラフを描く")
    parser.add_argument("--output", type=Path, default=Path("fresnel.png"), help="出力ファイル名")
    args = parser.parse_args()

    for name, eta in MATERIALS:
        f0 = fresnel_reflectance(np.array([1.0]), eta)[0]
        print(f"{name}: 垂直入射時の反射率 F0 = {f0:.3f}, 理論値 {abs((eta - 1) / (eta + 1)) ** 2:.3f}")
    print(f"ガラスに 80 度で入射したときの反射率: {fresnel_reflectance(np.array([math.cos(math.radians(80))]), 1.5)[0]:.3f}")
    plot_fresnel(args.output)
    print(f"{args.output} を保存した")


if __name__ == "__main__":
    main()
