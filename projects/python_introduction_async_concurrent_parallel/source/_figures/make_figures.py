"""本文で使う図を生成するスクリプト。conf.py からビルド開始時に呼び出される。"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402

plt.rcParams["font.family"] = ["BIZ UDPGothic", "Yu Gothic", "Meiryo", "sans-serif"]
plt.rcParams["font.size"] = 11
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.edgecolor"] = "#8a8984"
plt.rcParams["xtick.color"] = "#52514e"
plt.rcParams["ytick.color"] = "#52514e"
plt.rcParams["axes.labelcolor"] = "#52514e"

# 分類用の色（固定の順序で使う）
TASK_COLORS = {"A": "#2a78d6", "B": "#eb6834", "C": "#1baf7a"}
TEXT = "#0b0b0b"
MUTED = "#8a8984"
SURFACE = "#fcfcfb"
DPI = 110

# 第 4 章のベンチマーク（examples/ch04_choosing/benchmark.py）を執筆環境で実行した結果（秒）。
# 執筆環境: Windows 11、CPU 16 コア、Python 3.14.6。ビルド時には計測しない。
BENCHMARK = {
    "逐次": (2.18, 4.00),
    "スレッド": (3.96, 0.51),
    "プロセス": (0.91, 0.92),
    "asyncio": (2.27, 0.50),
}


def _bar(ax: Axes, lane: float, start: float, length: float, color: str, label: str = "",
         waiting: bool = False) -> None:
    """lane 行目に start から length の長さの棒を描く。waiting が真なら待ち時間として淡く描く。"""
    if waiting:
        ax.barh(lane, length, left=start, height=0.5, color=color, alpha=0.18, edgecolor=color,
                linewidth=1.0, hatch="///")
    else:
        ax.barh(lane, length, left=start, height=0.5, color=color, edgecolor=SURFACE, linewidth=2.0)
    if label:
        ax.text(start + length / 2, lane, label, ha="center", va="center", fontsize=10,
                color=TEXT if waiting else "white")


def _setup_lanes(ax: Axes, labels: list[str], title: str, xmax: float) -> None:
    ax.set_yticks(range(len(labels)), labels)
    ax.set_ylim(len(labels) - 0.5, -0.5)
    ax.set_xlim(0, xmax)
    ax.set_title(title, loc="left", fontsize=12, color=TEXT)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)


def _save(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=DPI, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def make_execution_models(path: Path) -> None:
    """逐次・並行・並列の違いを時系列で示す。"""
    fig, axes = plt.subplots(3, 1, figsize=(8.0, 5.6), sharex=True,
                             gridspec_kw={"height_ratios": [1, 1, 3]}, facecolor=SURFACE)
    sequential, concurrent, parallel = axes

    for i, name in enumerate("ABC"):
        _bar(sequential, 0, i * 3, 3, TASK_COLORS[name], name)
    _setup_lanes(sequential, ["コア 1"], "逐次処理: 1 つずつ順に実行する", 9.2)

    for step in range(9):
        name = "ABC"[step % 3]
        _bar(concurrent, 0, step, 1, TASK_COLORS[name], name)
    _setup_lanes(concurrent, ["コア 1"], "並行処理: 1 つのコアで切り替えながら進める", 9.2)

    for i, name in enumerate("ABC"):
        _bar(parallel, i, 0, 3, TASK_COLORS[name], name)
    _setup_lanes(parallel, ["コア 1", "コア 2", "コア 3"], "並列処理: 複数のコアで同時に実行する", 9.2)

    parallel.set_xlabel("時間 →")
    parallel.set_xticks([])
    fig.tight_layout()
    _save(fig, path)


def make_async_wait(path: Path) -> None:
    """I/O 待ちを重ねることで全体の時間が短くなる様子を示す。"""
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 4.6), sharex=True, facecolor=SURFACE)
    send, wait, receive = 0.3, 2.0, 0.4
    total = send + wait + receive

    ax = axes[0]
    for i, name in enumerate("ABC"):
        start = i * total
        color = TASK_COLORS[name]
        _bar(ax, i, start, send, color)
        _bar(ax, i, start + send, wait, color, "応答待ち", waiting=True)
        _bar(ax, i, start + send + wait, receive, color)
    _setup_lanes(ax, ["要求 A", "要求 B", "要求 C"], "同期的に実行: 応答を待つ間も次の要求を送らない", 3 * total + 0.2)

    ax = axes[1]
    previous_end = 0.0
    for i, name in enumerate("ABC"):
        start = i * send
        color = TASK_COLORS[name]
        _bar(ax, i, start, send, color)
        # CPU は 1 つなので、応答の処理は前の処理が終わってから始まる
        receive_start = max(start + send + wait, previous_end)
        _bar(ax, i, start + send, receive_start - start - send, color, "応答待ち", waiting=True)
        _bar(ax, i, receive_start, receive, color)
        previous_end = receive_start + receive
    _setup_lanes(ax, ["要求 A", "要求 B", "要求 C"], "非同期に実行: 応答を待つ間に次の要求を送る", 3 * total + 0.2)

    axes[1].set_xlabel("時間 →（濃い部分は CPU で処理している時間）")
    axes[1].set_xticks([])
    fig.tight_layout()
    _save(fig, path)


def make_gil(path: Path) -> None:
    """GIL の下でのスレッドの動きを、CPU バウンドと I/O バウンドで比べる。"""
    fig, axes = plt.subplots(2, 1, figsize=(8.0, 4.0), sharex=True, facecolor=SURFACE)
    colors = [TASK_COLORS["A"], TASK_COLORS["B"]]

    ax = axes[0]
    for step in range(10):
        thread = step % 2
        _bar(ax, thread, step, 1, colors[thread])
        _bar(ax, 1 - thread, step, 1, MUTED, waiting=True)
    _setup_lanes(ax, ["スレッド 1", "スレッド 2"], "CPU バウンド: GIL を持つスレッドだけが実行され、交互に進む", 10.2)

    ax = axes[1]
    for thread, offset in ((0, 0.0), (1, 0.6)):
        for cycle in range(3):
            start = offset + cycle * 3.4
            _bar(ax, thread, start, 0.6, colors[thread])
            _bar(ax, thread, start + 0.6, 2.8, colors[thread], "I/O 待ち（GIL を解放）", waiting=True)
    _setup_lanes(ax, ["スレッド 1", "スレッド 2"], "I/O バウンド: 待っている間は GIL を手放すため、待ち時間が重なる", 10.2)

    axes[1].set_xlabel("時間 →（濃い部分は GIL を持って Python のコードを実行している時間）")
    axes[1].set_xticks([])
    fig.tight_layout()
    _save(fig, path)


def make_benchmark(path: Path) -> None:
    """第 4 章のベンチマーク結果を棒グラフで示す。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.2), facecolor=SURFACE)
    names = list(BENCHMARK)
    titles = ["CPU バウンド（8 タスク）", "I/O バウンド（8 タスク）"]
    for column, (ax, title) in enumerate(zip(axes, titles)):
        values = [BENCHMARK[name][column] for name in names]
        ax.barh(range(len(names)), values, height=0.55, color=TASK_COLORS["A"], edgecolor=SURFACE, linewidth=2.0)
        for i, value in enumerate(values):
            ax.text(value + 0.05, i, f"{value:.2f} 秒", va="center", fontsize=10, color=TEXT)
        ax.set_yticks(range(len(names)), names)
        ax.set_ylim(len(names) - 0.5, -0.5)
        ax.set_xlim(0, max(values) * 1.3)
        ax.set_title(title, loc="left", fontsize=12, color=TEXT)
        ax.set_xlabel("経過時間（秒、短いほど速い）")
        ax.tick_params(axis="y", length=0)
        ax.spines["left"].set_visible(False)
        ax.grid(axis="x", color="#e4e3df", linewidth=0.8)
        ax.set_axisbelow(True)
    fig.tight_layout()
    _save(fig, path)


def generate(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    make_execution_models(output_dir / "execution_models.png")
    make_async_wait(output_dir / "async_wait.png")
    make_gil(output_dir / "gil.png")
    make_benchmark(output_dir / "benchmark.png")


if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent / "_generated")
