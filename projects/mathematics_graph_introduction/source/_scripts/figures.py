"""本文で使用する図を matplotlib で生成するスクリプト。

conf.py から generate_all() を呼び出し、ビルドのたびに図を出力する。
グラフの構造を示す図は本文中の Graphviz で描き、ここでは数値計算を伴う図だけを扱う。
"""

import heapq
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

FONT_CANDIDATES = ["Yu Gothic", "Meiryo", "BIZ UDGothic", "Noto Sans JP", "Noto Sans CJK JP", "IPAexGothic",
                   "Hiragino Sans", "MS Gothic"]

BLUE = "#2a6fb0"
ORANGE = "#e07b28"
GRAY = "#8a8a8a"


def setup_font() -> None:
    """利用可能な日本語フォントを探して matplotlib に設定する。"""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 120


def save(fig: Figure, out_dir: Path, name: str) -> None:
    """図を PNG で保存して閉じる。"""
    fig.tight_layout()
    fig.savefig(out_dir / name)
    plt.close(fig)


# -- 第 12 章 ------------------------------------------------------------------

def _grid_search(grid: list[str], start: tuple[int, int], goal: tuple[int, int],
                 use_heuristic: bool) -> tuple[set[tuple[int, int]], list[tuple[int, int]]]:
    """格子上で A* 探索（use_heuristic=False ならダイクストラ法）を行い、展開したセルと経路を返す。"""
    def h(c: tuple[int, int]) -> int:
        return abs(c[0] - goal[0]) + abs(c[1] - goal[1]) if use_heuristic else 0

    g_cost = {start: 0}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    heap = [(h(start), 0, start)]
    closed: set[tuple[int, int]] = set()
    counter = 0
    while heap:
        _, _, c = heapq.heappop(heap)
        if c in closed:
            continue
        closed.add(c)
        if c == goal:
            break
        r, col = c
        for nr, nc in ((r + 1, col), (r - 1, col), (r, col + 1), (r, col - 1)):
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
                ng = g_cost[c] + 1
                if ng < g_cost.get((nr, nc), 10 ** 9):
                    g_cost[(nr, nc)] = ng
                    parent[(nr, nc)] = c
                    counter += 1
                    heapq.heappush(heap, (ng + h((nr, nc)), counter, (nr, nc)))
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return closed, path


def astar_vs_dijkstra(out_dir: Path) -> None:
    """格子上の最短経路探索で、ダイクストラ法と A* 探索が展開するセルを比較する。"""
    rows, cols = 21, 31
    grid = [["." for _ in range(cols)] for _ in range(rows)]
    for r in range(3, 18):
        grid[r][20] = "#"
    for c in range(10, 21):
        grid[3][c] = "#"
    lines = ["".join(row) for row in grid]
    start, goal = (10, 4), (10, 27)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, use_h, title in ((axes[0], False, "ダイクストラ法"), (axes[1], True, "A* 探索（マンハッタン距離）")):
        closed, path = _grid_search(lines, start, goal, use_h)
        img = np.zeros((rows, cols))
        for r, c in closed:
            img[r, c] = 1
        for r in range(rows):
            for c in range(cols):
                if lines[r][c] == "#":
                    img[r, c] = 2
        for r, c in path:
            img[r, c] = 3
        cmap = ListedColormap(["#ffffff", "#bcd6ee", "#333333", ORANGE])
        ax.imshow(img, cmap=cmap, vmin=0, vmax=3)
        ax.plot(start[1], start[0], "o", color="green", markersize=8)
        ax.plot(goal[1], goal[0], "*", color="red", markersize=12)
        ax.set_title(f"{title}: 展開したセル {len(closed)} 個")
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, out_dir, "ch12_astar.png")


# -- 第 14 章 ------------------------------------------------------------------

def fiedler_karate(out_dir: Path) -> None:
    """空手クラブのネットワークをフィードラーベクトルの符号で 2 分割した図。"""
    g = nx.karate_club_graph()
    n = g.number_of_nodes()
    a = nx.to_numpy_array(g, nodelist=list(range(n)), weight=None)
    lap = np.diag(a.sum(axis=1)) - a
    _, vecs = np.linalg.eigh(lap)
    fiedler = vecs[:, 1]
    if fiedler[0] > 0:  # 頂点 0 側が負になるよう符号をそろえる
        fiedler = -fiedler

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.1, 1]})
    pos = nx.spring_layout(g, seed=3)
    colors = [BLUE if fiedler[v] < 0 else ORANGE for v in range(n)]
    actual = ["s" if g.nodes[v]["club"] == "Mr. Hi" else "o" for v in range(n)]
    nx.draw_networkx_edges(g, pos, ax=axes[0], edge_color="#bbbbbb")
    for shape in ("s", "o"):
        nodes = [v for v in range(n) if actual[v] == shape]
        nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_color=[colors[v] for v in nodes], node_shape=shape,
                               node_size=180, ax=axes[0])
    nx.draw_networkx_labels(g, pos, font_size=7, font_color="white", ax=axes[0])
    axes[0].set_title("色: フィードラーベクトルの符号　形: 実際の分裂（■ 0 側, ● 33 側）", fontsize=10)
    axes[0].axis("off")

    order = np.argsort(fiedler)
    axes[1].bar(range(n), fiedler[order], color=[colors[v] for v in order])
    axes[1].set_xticks(range(n))
    axes[1].set_xticklabels([str(v) for v in order], fontsize=6, rotation=90)
    axes[1].axhline(0, color=GRAY, linewidth=0.8)
    axes[1].set_xlabel("頂点（成分の小さい順）")
    axes[1].set_ylabel("フィードラーベクトルの成分")
    axes[1].grid(axis="y", alpha=0.3)
    save(fig, out_dir, "ch14_fiedler.png")


# -- 第 15 章 ------------------------------------------------------------------

def model_drawings(out_dir: Path) -> None:
    """3 つのネットワークモデルの小さな例を並べて描く。"""
    n = 40
    graphs = [
        ("ER モデル（p = 0.1）", nx.erdos_renyi_graph(n, 0.1, seed=2)),
        ("WS モデル（k = 4, p = 0.1）", nx.watts_strogatz_graph(n, 4, 0.1, seed=5)),
        ("BA モデル（m = 2）", nx.barabasi_albert_graph(n, 2, seed=2)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (title, g) in zip(axes, graphs):
        if title.startswith("WS"):
            pos = nx.circular_layout(g)
        else:
            pos = nx.kamada_kawai_layout(g)
        degrees = dict(g.degree())
        nx.draw_networkx_edges(g, pos, ax=ax, edge_color="#bbbbbb")
        nx.draw_networkx_nodes(g, pos, ax=ax, node_size=[20 + 15 * degrees[v] for v in g.nodes],
                               node_color=BLUE)
        ax.set_title(title)
        ax.axis("off")
    save(fig, out_dir, "ch15_models.png")


def degree_distributions(out_dir: Path) -> None:
    """ER モデルと BA モデルの次数分布を比較する。"""
    n = 10000
    er = nx.erdos_renyi_graph(n, 6 / (n - 1), seed=1)
    ba = nx.barabasi_albert_graph(n, 3, seed=1)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for g, label, color in ((er, "ER モデル", BLUE), (ba, "BA モデル", ORANGE)):
        hist = Counter(d for _, d in g.degree())
        ks = np.array(sorted(hist))
        pk = np.array([hist[k] / n for k in ks])
        axes[0].plot(ks, pk, "o-", color=color, markersize=3, label=label)
        axes[1].loglog(ks, pk, "o", color=color, markersize=3, label=label)
    axes[0].set_xlim(0, 30)
    axes[0].set_title("線形目盛り")
    axes[1].set_title("両対数目盛り")
    for ax in axes:
        ax.set_xlabel("次数 k")
        ax.set_ylabel("割合 P(k)")
        ax.legend()
        ax.grid(alpha=0.3)
    save(fig, out_dir, "ch15_degree.png")


def small_world(out_dir: Path) -> None:
    """WS モデルで、つなぎ替え確率 p に対する平均クラスタ係数と平均距離の変化を示す。"""
    n, k = 500, 6
    ps = np.logspace(-4, 0, 13)
    base = nx.watts_strogatz_graph(n, k, 0.0)
    c0 = nx.average_clustering(base)
    l0 = nx.average_shortest_path_length(base)
    cs, ls = [], []
    for p in ps:
        g = nx.connected_watts_strogatz_graph(n, k, float(p), seed=4)
        cs.append(nx.average_clustering(g) / c0)
        ls.append(nx.average_shortest_path_length(g) / l0)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.semilogx(ps, cs, "o-", color=BLUE, label="平均クラスタ係数 C(p) / C(0)")
    ax.semilogx(ps, ls, "s-", color=ORANGE, label="平均距離 L(p) / L(0)")
    ax.axvspan(3e-3, 1e-1, color="#eeeeee", label="スモールワールド領域（目安）")
    ax.set_xlabel("つなぎ替え確率 p")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower left")
    ax.grid(alpha=0.3)
    save(fig, out_dir, "ch15_small_world.png")


def generate_all(out_dir: Path) -> None:
    """すべての図を生成する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    setup_font()
    astar_vs_dijkstra(out_dir)
    fiedler_karate(out_dir)
    model_drawings(out_dir)
    degree_distributions(out_dir)
    small_world(out_dir)


if __name__ == "__main__":
    generate_all(Path(__file__).resolve().parent.parent / "_generated")
