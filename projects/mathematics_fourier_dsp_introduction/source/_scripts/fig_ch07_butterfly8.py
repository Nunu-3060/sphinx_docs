"""N = 8 の基数 2・時間間引き FFT の信号流れ図を描く.

入力はビット反転した順に並べ、3 段のバタフライ演算で出力 X[0] から X[7] を得る。
各バタフライの下側の入力には回転因子 W_N^k を掛け、下側の出力では符号を反転して足す。
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

N_POINTS = 8
STAGES = 3


def bit_reverse(i: int, bits: int) -> int:
    """i を bits ビットの 2 進数とみなし、ビットの並びを逆にした数を返す."""
    return int(f"{i:0{bits}b}"[::-1], 2)


def create_figure() -> Figure:
    fig, ax = plt.subplots(figsize=(10, 5.6))
    xs = [0.0, 2.5, 5.0, 7.5]  # 各段の列の位置

    def y(row: int) -> float:
        return float(N_POINTS - 1 - row)

    for stage in range(STAGES):
        span = 2**stage  # バタフライの上下の間隔
        size = 2 * span  # このステージの DFT の長さ
        x0, x1 = xs[stage] + 0.35, xs[stage + 1] - 0.35
        for group in range(0, N_POINTS, size):
            for j in range(span):
                top, bottom = group + j, group + j + span
                color = f"C{j % 4}"
                ax.plot([x0, x1], [y(top), y(top)], color=color, linewidth=1.0)
                ax.plot([x0, x1], [y(bottom), y(bottom)], color=color, linewidth=1.0)
                ax.plot([x0, x1], [y(top), y(bottom)], color=color, linewidth=1.0)
                ax.plot([x0, x1], [y(bottom), y(top)], color=color, linewidth=1.0)
                exponent = j * N_POINTS // size
                ax.text(x0 + 0.05, y(bottom) - 0.32, f"$W_8^{exponent}$", fontsize=9, color=color)
                ax.text(x1 - 0.3, y(bottom) - 0.32, "−1", fontsize=9, color=color)
        ax.text((x0 + x1) / 2, N_POINTS - 0.1, f"第 {stage + 1} 段（長さ {size} の DFT）", ha="center", fontsize=10)
    for row in range(N_POINTS):
        for x in xs:
            ax.plot(x, y(row), "o", color="k", markersize=4)
        ax.text(xs[0] - 0.3, y(row), f"x[{bit_reverse(row, STAGES)}]", ha="right", va="center", fontsize=11)
        ax.text(xs[-1] + 0.3, y(row), f"X[{row}]", ha="left", va="center", fontsize=11)
    ax.set_xlim(-1.5, 9.0)
    ax.set_ylim(-0.8, N_POINTS + 0.3)
    ax.axis("off")
    fig.tight_layout()
    return fig
