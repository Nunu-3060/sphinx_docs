"""BRDF の形を可視化する。

次の 3 種類の図を描く。

* 入射面内での反射分布（ランバート、Phong、GGX マイクロファセット）
* ラフネスごとの GGX 法線分布関数
* ラフネスとメタリックを変えた球のシェーディング結果

実行例::

    python brdf_plot.py --output-dir .
"""

import argparse
import math
from pathlib import Path
from typing import cast

import matplotlib
import numpy as np
import numpy.typing as npt

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.projections.polar import PolarAxes  # noqa: E402

FloatArray = npt.NDArray[np.float64]


def ggx_distribution(cos_h: FloatArray, alpha: float) -> FloatArray:
    """GGX（Trowbridge-Reitz）法線分布関数 D。"""
    a2 = alpha * alpha
    denom = cos_h * cos_h * (a2 - 1.0) + 1.0
    result: FloatArray = a2 / (math.pi * denom * denom)
    return result


def smith_g1(cos_v: FloatArray, alpha: float) -> FloatArray:
    """GGX に対する Smith のマスキング関数 G1。"""
    a2 = alpha * alpha
    result: FloatArray = 2.0 * cos_v / (cos_v + np.sqrt(a2 + (1.0 - a2) * cos_v * cos_v))
    return result


def fresnel_schlick(cos_theta: FloatArray, f0: FloatArray) -> FloatArray:
    """フレネル反射率の Schlick 近似。"""
    result: FloatArray = f0 + (1.0 - f0) * (1.0 - cos_theta) ** 5
    return result


def cook_torrance_specular(cos_i: FloatArray, cos_o: FloatArray, cos_h: FloatArray,
                           alpha: float) -> FloatArray:
    """フレネル項を 1 とした Cook-Torrance 鏡面反射項 D G / (4 cosθ_i cosθ_o)。"""
    d = ggx_distribution(cos_h, alpha)
    g = smith_g1(cos_i, alpha) * smith_g1(cos_o, alpha)
    result: FloatArray = d * g / (4.0 * cos_i * cos_o)
    return result


def plot_lobes(output: Path, incident_deg: float = 45.0) -> None:
    """入射面内で、出射方向ごとの BRDF の値を極座標で描く（各曲線は最大値で正規化）。"""
    theta_i = math.radians(incident_deg)
    # 出射角。正の向きを正反射側とし、法線から ±89 度の範囲を描く
    theta_o = np.radians(np.linspace(-89.0, 89.0, 721))
    cos_i = np.full_like(theta_o, math.cos(theta_i))
    cos_o = np.cos(theta_o)
    # 入射面内ではハーフベクトルの角度は (θ_o - θ_i) / 2 となる（入射方向は負の側にある）
    cos_h = np.cos((theta_o - theta_i) / 2.0)
    # Phong：正反射方向と出射方向のなす角は θ_o - θ_i
    cos_alpha = np.maximum(np.cos(theta_o - theta_i), 0.0)

    curves: list[tuple[str, FloatArray]] = [
        ("Lambert", np.ones_like(theta_o)),
        ("Phong (exponent 20)", cos_alpha ** 20),
        ("GGX (roughness 0.6)", cook_torrance_specular(cos_i, cos_o, cos_h, 0.6 ** 2)),
        ("GGX (roughness 0.4)", cook_torrance_specular(cos_i, cos_o, cos_h, 0.4 ** 2)),
    ]

    fig = plt.figure(figsize=(6.4, 3.8))
    ax = cast(PolarAxes, fig.add_subplot(projection="polar"))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_thetamin(-90)
    ax.set_thetamax(90)
    for name, values in curves:
        ax.plot(theta_o, values / np.max(values), label=name)
    ax.annotate("", xy=(0.0, 0.0), xytext=(-theta_i, 1.15),
                arrowprops={"arrowstyle": "->", "color": "black", "lw": 1.5})
    ax.text(-theta_i, 1.25, "incident", ha="center", va="center")
    ax.set_rticks([0.25, 0.5, 0.75, 1.0])
    ax.set_rlim(0.0, 1.3)
    ax.set_yticklabels([])
    ax.legend(loc="lower left", bbox_to_anchor=(-0.05, -0.12), fontsize=8)
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def plot_ggx(output: Path) -> None:
    """ラフネスごとの GGX 法線分布関数 D(θ_h) を描く。"""
    theta_h = np.linspace(0.0, 90.0, 361)
    cos_h = np.cos(np.radians(theta_h))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for roughness in [0.2, 0.4, 0.6, 0.8]:
        ax.plot(theta_h, ggx_distribution(cos_h, roughness ** 2), label=f"roughness = {roughness}")
    ax.set_yscale("log")
    ax.set_ylim(1e-2, 1e3)
    ax.set_xlim(0.0, 90.0)
    ax.set_xticks(np.arange(0, 91, 15))
    ax.set_xlabel(r"Angle between microfacet normal and surface normal $\theta_h$ [deg]")
    ax.set_ylabel(r"$D(\theta_h)$ [1/sr]")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def shade_sphere(base_color: tuple[float, float, float], metallic: float, roughness: float,
                 size: int = 128) -> FloatArray:
    """平行光源 1 つで照らした球を、メタリック／ラフネスモデルでシェーディングする。

    戻り値は線形な放射輝度の画像（size × size × 3）。背景は暗い灰色とする。
    """
    rows, cols = np.mgrid[0:size, 0:size]
    x = (cols + 0.5) / size * 2.0 - 1.0
    y = 1.0 - (rows + 0.5) / size * 2.0
    r2 = x * x + y * y
    inside = r2 < 1.0
    z = np.sqrt(np.maximum(0.0, 1.0 - r2))
    normals = np.stack([x, y, z], axis=-1)

    view = np.array([0.0, 0.0, 1.0])
    light = np.array([-0.5, 0.6, 0.62])
    light /= np.linalg.norm(light)
    half = (view + light) / np.linalg.norm(view + light)
    light_irradiance = 3.0                     # 光に垂直な面での放射照度
    alpha = max(roughness ** 2, 1e-3)

    cos_i = np.maximum(normals @ light, 0.0)
    cos_o = np.maximum(normals @ view, 1e-4)
    cos_h = np.maximum(normals @ half, 0.0)
    cos_oh = float(view @ half)

    base = np.array(base_color)
    f0 = 0.04 * (1.0 - metallic) + base * metallic       # 非金属は F0 = 0.04
    fresnel = fresnel_schlick(np.full(3, cos_oh), f0)
    d = ggx_distribution(cos_h, alpha)
    g = smith_g1(np.maximum(cos_i, 1e-4), alpha) * smith_g1(cos_o, alpha)
    specular = fresnel * (d * g / (4.0 * np.maximum(cos_i, 1e-4) * cos_o))[..., None]
    diffuse = (1.0 - fresnel) * (1.0 - metallic) * base / math.pi
    ambient = 0.03 * base                                 # 影側が真っ黒にならないための環境光

    color = (diffuse + specular) * (light_irradiance * cos_i)[..., None] + ambient
    background = np.full(3, 0.02)
    result: FloatArray = np.where(inside[..., None], color, background)
    return result


def to_display(linear: FloatArray) -> FloatArray:
    """線形な値を 0〜1 に切り詰めて sRGB で符号化する。"""
    c = np.clip(linear, 0.0, 1.0)
    result: FloatArray = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1.0 / 2.4) - 0.055)
    return result


def plot_spheres(output: Path) -> None:
    """ラフネス（横方向）とメタリック（縦方向）を変えた球を並べて描く。"""
    roughness_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    rows: list[tuple[str, tuple[float, float, float], float]] = [
        ("metallic = 0\n(red plastic)", (0.8, 0.1, 0.08), 0.0),
        ("metallic = 1\n(gold)", (1.0, 0.782, 0.344), 1.0),
    ]
    fig, axes = plt.subplots(len(rows), len(roughness_values), figsize=(7.5, 3.4))
    for row, (label, base_color, metallic) in enumerate(rows):
        for col, roughness in enumerate(roughness_values):
            ax = axes[row, col]
            ax.imshow(to_display(shade_sphere(base_color, metallic, roughness)))
            ax.set_xticks([])
            ax.set_yticks([])
            if row == 0:
                ax.set_title(f"roughness = {roughness}", fontsize=9)
            if col == 0:
                ax.set_ylabel(label, fontsize=9)
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="BRDF の形を可視化する")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="出力先フォルダ")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    plot_lobes(args.output_dir / "brdf_lobes.png")
    plot_ggx(args.output_dir / "ggx_distribution.png")
    plot_spheres(args.output_dir / "roughness_spheres.png")
    print(f"{args.output_dir} に brdf_lobes.png, ggx_distribution.png, roughness_spheres.png を保存した")


if __name__ == "__main__":
    main()
