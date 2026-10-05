"""第 13 章: S-N 曲線とマイナー則で、繰り返し荷重による疲労寿命を見積もる。

鋼の部品に、大きさの異なる繰り返し応力が加わる、という想定です。

* S-N 曲線: 応力振幅 S と、破壊までの繰り返し回数 N の関係
  N = N_ref × (S / S_ref)^(-k)。疲労限度より小さい応力では
  破壊しないものとする (単純化したモデル)
* マイナー則: 応力振幅 S_i の繰り返しを n_i 回受けたときの損傷度を
  D = Σ n_i / N_i とし、D = 1 で破壊すると考える

応力が 10 % 大きくなると寿命がどれだけ縮むかも確かめます。
図は ch13_fatigue.png として保存します。材料定数は説明のための値です。

実行例::

    python ch13_fatigue.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from matplotlib.ticker import NullFormatter

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

S_REF = 300.0  # 基準の応力振幅 [MPa]
N_REF = 1.0e6  # 基準の応力振幅での破壊までの回数
K = 5.0  # S-N 曲線の傾きを決める指数
FATIGUE_LIMIT = 200.0  # 疲労限度 [MPa]

# 1 年間に受ける応力振幅 [MPa] と回数
LOAD_SPECTRUM: list[tuple[float, float]] = [
    (150.0, 5.0e6),
    (220.0, 2.0e5),
    (260.0, 2.0e4),
    (320.0, 1.0e3),
]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def cycles_to_failure(stress: float) -> float:
    """応力振幅 stress [MPa] で破壊するまでの回数を返す。"""
    if stress <= FATIGUE_LIMIT:
        return math.inf
    return float(N_REF * (stress / S_REF) ** (-K))


def damage_per_year(scale: float) -> float:
    """応力を scale 倍したときの、1 年あたりの損傷度を返す。"""
    return sum(cycles / cycles_to_failure(stress * scale)
               for stress, cycles in LOAD_SPECTRUM)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("応力振幅[MPa]  年間の回数  破壊までの回数  年間の損傷度")
    for stress, cycles in LOAD_SPECTRUM:
        n_f = cycles_to_failure(stress)
        damage = cycles / n_f
        n_text = "疲労限度以下" if math.isinf(n_f) else f"{n_f:.3g}"
        print(f"{stress:12.0f}  {cycles:10.3g}  {n_text:>14}  "
              f"{damage:12.4f}")

    for scale in (1.0, 1.1):
        d = damage_per_year(scale)
        print(f"応力 {scale:.1f} 倍: 年間の損傷度 {d:.4f}, "
              f"寿命 {1 / d:.1f} 年")

    setup_font()
    fig = Figure(figsize=(7, 4.2), layout="constrained")
    ax = fig.add_subplot()
    n_values = np.logspace(4, 8, 200)
    s_values = S_REF * (n_values / N_REF) ** (-1 / K)
    s_values = np.maximum(s_values, FATIGUE_LIMIT)
    ax.loglog(n_values, s_values, label="S-N 曲線")
    ax.axhline(FATIGUE_LIMIT, color="gray", linestyle=":",
               label=f"疲労限度 {FATIGUE_LIMIT:.0f} MPa")
    for stress, _ in LOAD_SPECTRUM:
        ax.axhline(stress, color="tab:orange", linewidth=0.8,
                   linestyle="--")
        ax.text(1.2e4, stress * 1.02, f"{stress:.0f} MPa", fontsize=8)
    ax.set_xlabel("破壊までの繰り返し回数 N")
    ax.set_ylabel("応力振幅 S [MPa]")
    ax.set_title("S-N 曲線と、部品に加わる応力振幅 (破線)")
    ax.set_ylim(120, 600)
    ticks = [150, 200, 300, 400, 600]
    ax.set_yticks(ticks, labels=[str(t) for t in ticks])
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper right")
    fig.savefig(outdir / "ch13_fatigue.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
