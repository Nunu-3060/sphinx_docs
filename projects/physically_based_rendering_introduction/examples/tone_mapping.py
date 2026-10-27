"""表示のための変換（sRGB の符号化とトーンマッピング）を比べる。

次の 3 種類の図を描く。

* sRGB の符号化曲線
* トーンマッピング関数（切り詰め、Reinhard、ACES 近似）の比較
* 明るさが大きく変化する HDR 画像に各トーンマッピングを適用した結果

実行例::

    python tone_mapping.py --output-dir .
"""

import argparse
from collections.abc import Callable
from pathlib import Path

import matplotlib
import numpy as np
import numpy.typing as npt

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FloatArray = npt.NDArray[np.float64]
ToneMapper = Callable[[FloatArray], FloatArray]


def srgb_encode(linear: FloatArray) -> FloatArray:
    """線形な値（0〜1）を sRGB の符号化値（0〜1）に変換する。"""
    c = np.clip(linear, 0.0, 1.0)
    result: FloatArray = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1.0 / 2.4) - 0.055)
    return result


def srgb_decode(encoded: FloatArray) -> FloatArray:
    """sRGB の符号化値（0〜1）を線形な値（0〜1）に戻す。"""
    c = np.clip(encoded, 0.0, 1.0)
    result: FloatArray = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return result


def clamp(x: FloatArray) -> FloatArray:
    """1 を超える値を 1 に切り詰めるだけの変換。"""
    result: FloatArray = np.clip(x, 0.0, 1.0)
    return result


def reinhard(x: FloatArray) -> FloatArray:
    """Reinhard の単純な演算子 x / (1 + x)。"""
    result: FloatArray = x / (1.0 + x)
    return result


def aces_approx(x: FloatArray) -> FloatArray:
    """Narkowicz による ACES フィルム調カーブの近似式。"""
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    result: FloatArray = np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0)
    return result


TONE_MAPPERS: list[tuple[str, ToneMapper]] = [
    ("Clamp", clamp),
    ("Reinhard", reinhard),
    ("ACES (Narkowicz)", aces_approx),
]


def plot_srgb_curve(output: Path) -> None:
    """sRGB の符号化曲線を、べき乗 1/2.2 の曲線と比べて描く。"""
    x = np.linspace(0.0, 1.0, 501)
    fig, ax = plt.subplots(figsize=(4.8, 4.0))
    ax.plot(x, srgb_encode(x), label="sRGB encoding")
    ax.plot(x, x ** (1.0 / 2.2), "--", label=r"$x^{1/2.2}$")
    ax.plot(x, x, ":", color="gray", label="linear")
    ax.set_xlabel("Linear value")
    ax.set_ylabel("Encoded value")
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def plot_tone_curves(output: Path) -> None:
    """トーンマッピング関数を、横軸を対数にして比べる。"""
    x = np.logspace(-2, 2, 801)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for name, mapper in TONE_MAPPERS:
        ax.semilogx(x, mapper(x), label=name)
    ax.set_xlabel("Scene-referred linear value (HDR)")
    ax.set_ylabel("Display linear value")
    ax.set_ylim(0.0, 1.05)
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def make_hdr_ramp(width: int = 512, height: int = 40) -> FloatArray:
    """左端 2^-4 から右端 2^6 まで、明るさが指数的に増える HDR 画像を作る。

    上半分は無彩色、下半分はオレンジ色とする。
    """
    exposure = 2.0 ** np.linspace(-4.0, 6.0, width)
    gray = np.ones(3)
    orange = np.array([1.0, 0.45, 0.1])
    top = exposure[None, :, None] * gray
    bottom = exposure[None, :, None] * orange
    result: FloatArray = np.concatenate([np.repeat(top, height // 2, axis=0),
                                         np.repeat(bottom, height // 2, axis=0)], axis=0)
    return result


def plot_tone_mapping_comparison(output: Path) -> None:
    """HDR 画像に各トーンマッピングを適用し、sRGB で符号化した結果を並べる。"""
    hdr = make_hdr_ramp()
    fig, axes = plt.subplots(len(TONE_MAPPERS), 1, figsize=(6.4, 3.2))
    for ax, (name, mapper) in zip(axes, TONE_MAPPERS):
        ax.imshow(srgb_encode(mapper(hdr)), aspect="auto", extent=(-4.0, 6.0, 0.0, 1.0))
        ax.set_yticks([])
        ax.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=9)
        ax.set_xticks(range(-4, 7))
        ax.tick_params(labelbottom=False)
    axes[-1].tick_params(labelbottom=True)
    axes[-1].set_xlabel(r"Scene-referred value ($\log_2$)")
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="sRGB の符号化とトーンマッピングの比較")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="出力先フォルダ")
    args = parser.parse_args()

    for value in [0.18, 0.5]:
        encoded = float(srgb_encode(np.array([value]))[0])
        print(f"線形値 {value} を sRGB で符号化すると {encoded:.3f}（8 ビットで {round(encoded * 255)}）")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    plot_srgb_curve(args.output_dir / "srgb_curve.png")
    plot_tone_curves(args.output_dir / "tone_curves.png")
    plot_tone_mapping_comparison(args.output_dir / "tone_mapping_comparison.png")
    print(f"{args.output_dir} に srgb_curve.png, tone_curves.png, tone_mapping_comparison.png を保存した")


if __name__ == "__main__":
    main()
