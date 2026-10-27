"""本文で使う図（matplotlib / Pillow）を生成するスクリプト。

conf.py の builder-inited イベントから generate_all() が呼ばれる。
単体で実行した場合は source/_generated/ に図を出力する。
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

DPI = 100

# 英文における各アルファベットの出現頻度 [%]（a〜z）
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406,
    6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]


def letter_frequency(out: Path) -> None:
    """英文の文字頻度と、シーザー暗号（鍵 3）で暗号化した後の文字頻度を並べた図。"""
    letters = [chr(ord("a") + i) for i in range(26)]
    shifted = ENGLISH_FREQ[-3:] + ENGLISH_FREQ[:-3]
    fig, axes = plt.subplots(2, 1, figsize=(8, 5.2), sharey=True)
    axes[0].bar(letters, ENGLISH_FREQ, color="#4c72b0")
    axes[0].set_title("英文の平文における文字の出現頻度")
    axes[1].bar([c.upper() for c in letters], shifted, color="#dd8452")
    axes[1].set_title("シーザー暗号（鍵 3）で暗号化した後の出現頻度")
    for ax in axes:
        ax.set_ylabel("頻度 [%]")
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)


def _make_plain_image(width: int, height: int) -> Image.Image:
    """単色の領域で構成された、暗号化前の画像を作る。"""
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    # 南京錠を模した図形
    draw.rounded_rectangle((64, 88, 192, 176), radius=12, fill=(40, 40, 40))
    draw.arc((84, 24, 172, 124), start=180, end=360, fill=(40, 40, 40), width=16)
    draw.rectangle((84, 72, 100, 92), fill=(40, 40, 40))
    draw.rectangle((156, 72, 172, 92), fill=(40, 40, 40))
    draw.ellipse((116, 112, 140, 136), fill=(230, 180, 30))
    draw.rectangle((124, 128, 132, 160), fill=(230, 180, 30))
    return img


def ecb_vs_cbc(out: Path) -> None:
    """同じ画像を AES-ECB と AES-CBC で暗号化し、画素値として表示した図。"""
    width, height = 256, 192  # 1 行 = 768 バイト = 48 ブロック
    plain = _make_plain_image(width, height)
    data = plain.tobytes()
    key = bytes(range(16))
    iv = bytes(16)

    ecb = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    ecb_data = ecb.update(data) + ecb.finalize()
    cbc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    cbc_data = cbc.update(data) + cbc.finalize()

    images = [
        (plain, "元の画像"),
        (Image.frombytes("RGB", (width, height), ecb_data), "ECB モードで暗号化"),
        (Image.frombytes("RGB", (width, height), cbc_data), "CBC モードで暗号化"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.9))
    for ax, (img, title) in zip(axes, images):
        ax.imshow(np.asarray(img))
        ax.set_title(title)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)


def birthday(out: Path) -> None:
    """誕生日問題における衝突確率のグラフ。"""
    days = 365
    ns = np.arange(1, 81)
    exact = []
    p_distinct = 1.0
    for n in ns:
        p_distinct *= (days - (n - 1)) / days
        exact.append(1.0 - p_distinct)
    approx = 1.0 - np.exp(-ns * (ns - 1) / (2 * days))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ns, exact, label="厳密値", color="#4c72b0")
    ax.plot(ns, approx, "--", label=r"近似 $1-e^{-n(n-1)/2N}$", color="#dd8452")
    ax.axhline(0.5, color="gray", lw=0.8)
    ax.axvline(23, color="gray", lw=0.8)
    ax.annotate(f"n = 23 で {exact[22] * 100:.1f} %", xy=(23, exact[22]), xytext=(32, 0.3),
                arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("人数 n")
    ax.set_ylabel("誕生日が一致する組が存在する確率")
    ax.set_xlim(1, 80)
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)


def elliptic_curve_real(out: Path) -> None:
    """実数体上の楕円曲線 y^2 = x^3 - x + 1 と点の加算の図。"""
    root = min(r.real for r in np.roots([1, 0, -1, 1]) if abs(r.imag) < 1e-9)
    x = np.concatenate([[root], np.linspace(root, 2.0, 2000)[1:]])
    rhs = x ** 3 - x + 1
    y = np.sqrt(np.clip(rhs, 0, None))

    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.plot(x, y, color="#4c72b0")
    ax.plot(x, -y, color="#4c72b0")
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.plot([-1.6, 2.0], [1, 1], color="#dd8452", lw=1)
    ax.plot([1, 1], [1, -1], "--", color="gray", lw=1)
    points = {"P": (-1, 1), "Q": (0, 1), "−(P+Q)": (1, 1), "P+Q": (1, -1)}
    offsets = {"P": (-0.25, 0.15), "Q": (-0.1, 0.15), "−(P+Q)": (0.05, 0.15), "P+Q": (0.08, -0.25)}
    for name, (px, py) in points.items():
        ax.plot(px, py, "o", color="#c44e52")
        dx, dy = offsets[name]
        ax.text(px + dx, py + dy, name, fontsize=12)
    ax.set_xlim(-1.6, 2.0)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title(r"$y^2 = x^3 - x + 1$")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)


def elliptic_curve_finite(out: Path) -> None:
    """有限体 F_97 上の楕円曲線 y^2 = x^3 + x + 4 の点の散布図。"""
    p, a, b = 97, 1, 4
    xs = []
    ys = []
    for px in range(p):
        for py in range(p):
            if (py * py - (px ** 3 + a * px + b)) % p == 0:
                xs.append(px)
                ys.append(py)
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    ax.scatter(xs, ys, s=12, color="#4c72b0")
    ax.axhline(p / 2, color="gray", lw=0.8, ls="--")
    ax.set_xlim(-2, p + 1)
    ax.set_ylim(-2, p + 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(rf"$y^2 \equiv x^3 + x + {b} \ (\mathrm{{mod}}\ {p})$（{len(xs) + 1} 点）")
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=DPI)
    plt.close(fig)


def generate_all(out_dir: Path) -> None:
    """全ての図を out_dir に出力する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    letter_frequency(out_dir / "letter_frequency.png")
    ecb_vs_cbc(out_dir / "ecb_vs_cbc.png")
    birthday(out_dir / "birthday.png")
    elliptic_curve_real(out_dir / "elliptic_curve_real.png")
    elliptic_curve_finite(out_dir / "elliptic_curve_finite.png")
    assert math.isclose(sum(ENGLISH_FREQ), 100.0, abs_tol=0.1)


if __name__ == "__main__":
    generate_all(Path(__file__).resolve().parent.parent / "_generated")
