"""第 6 章: 2 次系の周波数応答 (ボード線図) を描き、共振を確かめる。

2 次系の伝達関数 G(s) = ω_n^2 / (s^2 + 2ζω_n s + ω_n^2) に、
s = jω を代入して、正弦波の入力に対する出力の振幅比 (ゲイン) と
位相のずれを計算します。減衰比 ζ が小さいほど、固有角周波数の
近くで振幅が大きくなる (共振する) ことを確かめます。

図は ch06_frequency_response.png として保存します。

実行例::

    python ch06_frequency_response.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

OMEGA_N = 1.0  # 固有角周波数 [rad/s]
ZETAS = (0.1, 0.3, 0.7, 1.0)


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def frequency_response(omega: NDArray[np.float64],
                       zeta: float) -> NDArray[np.complex128]:
    """2 次系の周波数応答 G(jω) を返す。"""
    s = 1j * omega
    denominator = s ** 2 + 2 * zeta * OMEGA_N * s + OMEGA_N ** 2
    return np.asarray(OMEGA_N ** 2 / denominator, dtype=np.complex128)


def resonance(zeta: float) -> tuple[float, float] | None:
    """共振角周波数と共振ピーク (倍率) を返す。共振しなければ None。"""
    if zeta >= 1 / math.sqrt(2):
        return None
    omega_r = OMEGA_N * math.sqrt(1 - 2 * zeta ** 2)
    peak = 1 / (2 * zeta * math.sqrt(1 - zeta ** 2))
    return omega_r, peak


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("減衰比  共振角周波数[rad/s]  共振ピーク[倍]  [dB]")
    for zeta in ZETAS:
        result = resonance(zeta)
        if result is None:
            print(f"{zeta:6.1f}  共振しない")
            continue
        omega_r, peak = result
        print(f"{zeta:6.1f}  {omega_r:19.3f}  {peak:14.2f}  "
              f"{20 * math.log10(peak):5.1f}")

    setup_font()
    omega = np.logspace(-1, 1, 500)
    fig = Figure(figsize=(7, 6), layout="constrained")
    ax_gain, ax_phase = fig.subplots(2, 1, sharex=True)
    for zeta in ZETAS:
        response = frequency_response(omega, zeta)
        ax_gain.semilogx(omega, 20 * np.log10(np.abs(response)),
                         label=rf"$\zeta$ = {zeta}")
        ax_phase.semilogx(omega, np.degrees(np.angle(response)))
    ax_gain.set_ylabel("ゲイン [dB]")
    ax_gain.set_title(r"2 次系のボード線図 ($\omega_n$ = 1 rad/s)")
    ax_gain.set_ylim(-40, 20)
    ax_gain.grid(alpha=0.3, which="both")
    ax_gain.legend(loc="lower left")
    ax_phase.set_xlabel("角周波数 [rad/s]")
    ax_phase.set_ylabel("位相 [度]")
    ax_phase.set_yticks([0, -45, -90, -135, -180])
    ax_phase.grid(alpha=0.3, which="both")
    fig.savefig(outdir / "ch06_frequency_response.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
