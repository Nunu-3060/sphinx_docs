"""ローパスフィルタの仕様（許容範囲）と、仕様を満たす FIR フィルタの振幅特性を描く."""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import signal

import fig_common

FS = 1000.0
PASS_EDGE = 80.0  # 通過域端 [Hz]
STOP_EDGE = 150.0  # 阻止域端 [Hz]
RIPPLE = 1.0  # 通過域の許容偏差 [dB]
ATTENUATION = 50.0  # 阻止域の減衰量 [dB]


def create_figure() -> Figure:
    h = signal.firwin(51, 115.0, window="hamming", fs=FS)
    freqs, response = signal.freqz(h, worN=4096, fs=FS)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.fill_between([0, PASS_EDGE], -RIPPLE, -200, color="C3", alpha=0.15, linewidth=0)
    ax.fill_between([0, PASS_EDGE], RIPPLE, 50, color="C3", alpha=0.15, linewidth=0)
    ax.fill_between([STOP_EDGE, FS / 2], -ATTENUATION, 50, color="C3", alpha=0.15, linewidth=0)
    ax.plot(freqs, fig_common.to_db(response), color="C0", label="設計した FIR フィルタ")
    ax.text(PASS_EDGE / 2, -40, "通過域", ha="center", fontsize=11)
    ax.text((PASS_EDGE + STOP_EDGE) / 2, -90, "遷移域", ha="center", fontsize=11)
    ax.text((STOP_EDGE + FS / 2) / 2, -90, "阻止域", ha="center", fontsize=11)
    ax.annotate(f"通過域の許容偏差 ±{RIPPLE:.0f} dB", xy=(PASS_EDGE * 0.6, RIPPLE), xytext=(PASS_EDGE * 0.9, 12),
                arrowprops={"arrowstyle": "->"}, fontsize=10)
    ax.annotate(f"阻止域の減衰量 {ATTENUATION:.0f} dB 以上", xy=(STOP_EDGE + 60, -ATTENUATION),
                xytext=(STOP_EDGE + 90, -25), arrowprops={"arrowstyle": "->"}, fontsize=10)
    ax.axvline(PASS_EDGE, color="0.4", linestyle=":", linewidth=1.0)
    ax.axvline(STOP_EDGE, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_xticks([0, PASS_EDGE, STOP_EDGE, 200, 300, 400, 500])
    ax.set_xlim(0, FS / 2)
    ax.set_ylim(-110, 20)
    ax.set_xlabel("周波数 [Hz]")
    ax.set_ylabel("利得 [dB]")
    ax.legend(loc="upper right")
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
