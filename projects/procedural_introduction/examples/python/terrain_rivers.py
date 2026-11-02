"""第 7 章「地形」: 窪地の埋め立て、D8 法による流向、集水量から川と湖を求める。

* depression.png: 窪地の埋め立て（Priority-Flood）を断面で見た図
* d8.png: 小さな格子での流向と集水量
* rivers.png: 侵食した地形の集水量と、川・湖を描いた地図

flow_network() は、バイオームのスクリプトからも使う。
"""

from __future__ import annotations

import heapq

import numpy as np

from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib
from heightmap import SEA_LEVEL, shaded_relief
from terrain_erosion import eroded_terrain

# 8 近傍の位置のずれ (dy, dx)
OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def priority_flood(heights: FloatArray, sea_level: float, epsilon: float = 0.0) -> FloatArray:
    """窪地を埋めた高さを返す（Priority-Flood 法、Barnes ら 2014 年）。

    海と地図の端を出発点として、低い所から順に内陸へ広げていく。まだ訪れていない隣の
    高さが、今いる所の高さより低ければ、そこは窪地なので今の高さ（+ epsilon）まで埋める。
    epsilon > 0 にすると、埋めた面にわずかな傾きが付き、どの点からも必ず下りの隣がある。
    """
    rows, columns = heights.shape
    filled = heights.copy()
    done = np.zeros((rows, columns), dtype=bool)
    queue: list[tuple[float, int, int]] = []
    border = np.zeros_like(done)
    border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
    for y, x in zip(*np.nonzero(border | (heights < sea_level))):
        heapq.heappush(queue, (float(heights[y, x]), int(y), int(x)))
        done[y, x] = True
    while queue:
        z, y, x = heapq.heappop(queue)
        for dy, dx in OFFSETS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < columns and not done[ny, nx]:
                done[ny, nx] = True
                filled[ny, nx] = max(heights[ny, nx], z + epsilon)
                heapq.heappush(queue, (float(filled[ny, nx]), ny, nx))
    return filled


def d8_receivers(heights: FloatArray) -> IntArray:
    """D8 法の流向。各点から、8 近傍のうち下りの傾きが最も大きい点の番号（無ければ -1）を返す。"""
    rows, columns = heights.shape
    padded = np.pad(heights, 1, constant_values=np.inf)
    best_slope = np.zeros((rows, columns))
    receiver = np.full((rows, columns), -1, dtype=np.int64)
    y, x = np.mgrid[0:rows, 0:columns]
    for dy, dx in OFFSETS:
        neighbor = padded[1 + dy:1 + dy + rows, 1 + dx:1 + dx + columns]
        slope = (heights - neighbor) / np.hypot(dy, dx)  # 斜めの隣は距離が √2 倍
        better = slope > best_slope
        best_slope = np.where(better, slope, best_slope)
        receiver = np.where(better, (y + dy) * columns + (x + dx), receiver)
    return receiver.reshape(-1)


def flow_accumulation(heights: FloatArray, receivers: IntArray, rain: FloatArray | None = None) -> FloatArray:
    """集水量。各点に降った雨（既定は 1）を、高い点から順に流向の先へ足し込む。"""
    accumulation = (np.ones(heights.size) if rain is None else rain.reshape(-1)).astype(np.float64)
    order = np.argsort(-heights.reshape(-1), kind="stable")
    target = receivers.tolist()
    values = accumulation.tolist()
    for index in order.tolist():
        receiver = target[index]
        if receiver >= 0:
            values[receiver] += values[index]
    return np.array(values).reshape(heights.shape)


def flow_network(heights: FloatArray) -> tuple[FloatArray, IntArray, FloatArray]:
    """湖の深さ、流向、集水量をまとめて求める。"""
    lake_depth = priority_flood(heights, SEA_LEVEL) - heights
    routed = priority_flood(heights, SEA_LEVEL, epsilon=1e-6)
    receivers = d8_receivers(routed)
    receivers[(heights < SEA_LEVEL).reshape(-1)] = -1  # 海に入ったら流れは終わる
    return lake_depth, receivers, flow_accumulation(routed, receivers)


def draw_depression(file_name: str) -> None:
    import matplotlib.pyplot as plt

    x = np.linspace(0.0, 10.0, 400)
    ground = 0.3 + 0.05 * x + 0.35 * np.exp(-((x - 7.0) / 0.8) ** 2) - 0.45 * np.exp(-((x - 4.5) / 1.3) ** 2)
    ground[x > 7.0] = np.maximum(ground[x > 7.0], 1.0 - 0.08 * (x[x > 7.0] - 7.0))
    # 1 次元の Priority-Flood: 左端（海）から順に、それまでの高さの最大値で埋める。
    filled = np.maximum.accumulate(ground[::-1])[::-1]
    filled = np.minimum(filled, np.maximum.accumulate(ground))
    figure, ax = plt.subplots(figsize=(8, 3.0))
    ax.fill_between(x, 0, ground, color="#c8b48a")
    ax.fill_between(x, ground, filled, where=filled > ground + 1e-9, color="#6fa8dc", label="埋めた部分（湖）")
    ax.plot(x, ground, color="#6b5530", linewidth=1.5, label="元の地面")
    ax.plot(x, filled, color="#1f4f8f", linewidth=1.0, linestyle="--", label="埋めた後の高さ")
    left = x < 4.5
    outlet = int(np.argmax(np.where(left, ground, -np.inf)))
    ax.annotate("窪地の出口（鞍部）", (x[outlet], ground[outlet]), (x[outlet] + 0.4, 0.8),
                arrowprops={"arrowstyle": "->"}, fontsize=9)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper center", ncol=3, fontsize=9)
    ax.set_title("窪地の埋め立て（断面）", fontsize=10)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_d8(file_name: str) -> None:
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(4)
    size = 6
    yy, xx = np.mgrid[0:size, 0:size]
    heights = np.round(10 + 6 * np.hypot(xx - 4.5, yy - 0.2) / 6 + rng.uniform(0, 2.5, (size, size)), 0)
    heights[0, 5] = 5  # 出口（ここから地図の外へ流れ出る）
    receivers = d8_receivers(heights)
    receivers[0 * size + 5] = -1
    accumulation = flow_accumulation(heights, receivers)

    figure, axes = plt.subplots(1, 2, figsize=(9, 4.4))
    for ax, title in zip(axes, ["高さと流向（D8）", "集水量（上流の点の数 + 1）"]):
        ax.set_xlim(-0.5, size - 0.5)
        ax.set_ylim(size - 0.5, -0.5)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=10)
    axes[0].imshow(heights, cmap="terrain", vmin=0, vmax=24, alpha=0.6)
    axes[1].imshow(np.log(accumulation), cmap="Blues", vmin=0, vmax=np.log(size * size) + 0.5)
    for index, receiver in enumerate(receivers):
        y, x = divmod(index, size)
        axes[0].text(x, y, f"{heights[y, x]:g}", ha="center", va="center", fontsize=10)
        axes[1].text(x, y, f"{accumulation[y, x]:g}", ha="center", va="center", fontsize=10)
        if receiver >= 0:
            ty, tx = divmod(int(receiver), size)
            for ax, color in zip(axes, ["#1f4f8f", "#888888"]):
                ax.annotate("", (x + 0.75 * (tx - x), y + 0.75 * (ty - y)), (x + 0.25 * (tx - x), y + 0.25 * (ty - y)),
                            arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 1.0})
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def river_segments(receivers: IntArray, accumulation: FloatArray, threshold: float) -> tuple[FloatArray, FloatArray]:
    """集水量が threshold 以上の点から流向の先へ引く線分と、その集水量。"""
    rows, columns = accumulation.shape
    flat = accumulation.reshape(-1)
    source = np.nonzero((flat >= threshold) & (receivers >= 0))[0]
    target = receivers[source]
    start = np.stack([source % columns, source // columns], axis=-1)
    end = np.stack([target % columns, target // columns], axis=-1)
    return np.stack([start, end], axis=1).astype(np.float64), flat[source]


def draw_rivers(file_name: str, heights: FloatArray) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    lake_depth, receivers, accumulation = flow_network(heights)
    land = heights >= SEA_LEVEL
    figure, axes = plt.subplots(1, 2, figsize=(10, 5.2))
    cmap = plt.get_cmap("Blues").with_extremes(bad="#cccccc")
    axes[0].imshow(np.where(land, np.log10(accumulation), np.nan), cmap=cmap, vmin=0, vmax=3.5)
    axes[0].set_title("集水量（対数、灰色は海）", fontsize=10)

    relief = shaded_relief(heights)
    lake = (lake_depth > 1e-3) & land  # 深さが 0.001（高さの 0.1 %）を超える窪地だけを湖とする
    relief[lake] = 0.2 * relief[lake] + 0.8 * np.array([0.33, 0.58, 0.80])
    axes[1].imshow(relief)
    receivers = np.where(lake.reshape(-1), -1, receivers)  # 湖の中には川を描かない
    segments, values = river_segments(receivers, accumulation, threshold=60)
    widths = 0.4 + 0.9 * np.log10(values / 60)
    axes[1].add_collection(LineCollection(list(segments), linewidths=widths, colors="#1f5fbf", capstyle="round"))
    axes[1].set_title("集水量 60 以上を川、深い窪地を湖として描いた地図", fontsize=10)
    for ax in axes:
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_depression("depression.png")
    draw_d8("d8.png")
    draw_rivers("rivers.png", eroded_terrain())


if __name__ == "__main__":
    main()
