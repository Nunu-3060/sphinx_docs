"""第 11 章「レベルとダンジョン」: 道路の成長規則で街路網を作る（Parish と Müller の方法を簡略化したもの）。

* streets_growth.png: 道路が伸びていく途中の様子と完成図（背景は人口密度）
* streets_blocks.png: 道路で囲まれた領域（街区）を色分けしたもの
* streets.mp4: 道路が伸びていく動画
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2
from video import VideoWriter, find_ffmpeg

SIZE = 1000.0  # 街の範囲（m）
HIGHWAY_LENGTH = 60.0
STREET_LENGTH = 32.0
SNAP_DISTANCE = 14.0  # この距離より近い交差点には、道路の端を吸着させる
EXTEND_DISTANCE = 18.0  # この距離だけ先に既存の道路があれば、そこまで延ばしてつなぐ
STREET_DELAY = 6.0  # 街路は幹線道路より遅れて伸び始める
MAX_SEGMENTS = 1600


@dataclass
class Proposal:
    """これから置くかどうかを判定する道路の区間。"""

    start: tuple[float, float]
    angle: float  # 伸ばす向き（ラジアン）
    highway: bool

    def end(self) -> tuple[float, float]:
        length = HIGHWAY_LENGTH if self.highway else STREET_LENGTH
        return (self.start[0] + length * math.cos(self.angle), self.start[1] + length * math.sin(self.angle))


def population(x: FloatArray, y: FloatArray) -> FloatArray:
    """人口密度（0〜1）。中心ほど高く、ノイズでむらを付ける。座標は m。"""
    r = np.hypot(x - SIZE / 2, y - SIZE / 2) / (SIZE / 2)
    noise = fbm(perlin2, x / 260.0, y / 260.0, octaves=3, seed=4)
    return np.clip(1.1 - r + 0.6 * noise, 0.0, 1.0)


def density_at(point: tuple[float, float]) -> float:
    return float(population(np.array(point[0]), np.array(point[1])))


class Network:
    """置いた道路の区間の集まり。交差の判定のため、端点を NumPy の配列で持つ。"""

    def __init__(self) -> None:
        self.starts = np.zeros((MAX_SEGMENTS, 2))
        self.ends = np.zeros((MAX_SEGMENTS, 2))
        self.highway = np.zeros(MAX_SEGMENTS, dtype=bool)
        self.count = 0

    def add(self, start: tuple[float, float], end: tuple[float, float], highway: bool) -> None:
        self.starts[self.count] = start
        self.ends[self.count] = end
        self.highway[self.count] = highway
        self.count += 1

    def first_crossing(self, a: FloatArray, b: FloatArray) -> FloatArray | None:
        """線分 a→b が既存の区間と交わる点のうち、a に最も近いものを返す（a でつながる区間は除く）。"""
        p, q = self.starts[:self.count], self.ends[:self.count]
        r, s = b - a, q - p
        denominator = r[0] * s[:, 1] - r[1] * s[:, 0]
        ap = p - a
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (ap[:, 0] * s[:, 1] - ap[:, 1] * s[:, 0]) / denominator
            u = (ap[:, 0] * r[1] - ap[:, 1] * r[0]) / denominator
        touches_a = (np.hypot(*(p - a).T) < 1e-6) | (np.hypot(*(q - a).T) < 1e-6)
        hit = (np.abs(denominator) > 1e-9) & (t > 1e-6) & (t <= 1.0) & (u >= 0.0) & (u <= 1.0) & ~touches_a
        if not hit.any():
            return None
        nearest = float(t[hit].min())
        result: FloatArray = a + r * nearest
        return result

    def nearest_endpoint(self, point: FloatArray) -> FloatArray | None:
        """point から SNAP_DISTANCE 以内にある、最も近い既存の端点（交差点）。"""
        if self.count == 0:
            return None
        points = np.concatenate([self.starts[:self.count], self.ends[:self.count]])
        distance = np.hypot(*(points - point).T)
        k = int(np.argmin(distance))
        return points[k] if distance[k] < SNAP_DISTANCE else None


def local_constraints(network: Network, proposal: Proposal) -> tuple[tuple[float, float], bool] | None:
    """局所的な制約で区間を修正する。(修正した終点, そこで伸びるのを止めるか) を返す。置けなければ None。

    1. 区間を EXTEND_DISTANCE だけ延ばした線が既存の道路と交われば、その交点で止める
       （交差点を作る。少し手前で途切れた道路は、延ばしてつなぐ）。
    2. 終点の近くに既存の交差点があれば、そこへ吸着させて止める。
    3. 街の範囲の外に出る区間や、修正の結果短くなりすぎた区間は置かない。
    """
    a = np.array(proposal.start)
    b = np.array(proposal.end())
    direction = (b - a) / np.linalg.norm(b - a)
    end, stop = b, False
    crossing = network.first_crossing(a, b + direction * EXTEND_DISTANCE)
    if crossing is not None:
        end, stop = crossing, True
    else:
        snapped = network.nearest_endpoint(b)
        if snapped is not None and np.linalg.norm(snapped - a) > 1e-6:
            end, stop = snapped, True
    if not (0.0 <= end[0] <= SIZE and 0.0 <= end[1] <= SIZE):
        return None
    if np.linalg.norm(end - a) < 0.3 * STREET_LENGTH:
        return None
    return (float(end[0]), float(end[1])), stop


def global_goals(proposal: Proposal, end: tuple[float, float],
                 rng: np.random.Generator) -> list[tuple[float, Proposal]]:
    """置いた区間の終点から伸ばす次の区間（と、それを処理するまでの遅れ）を決める。

    * 幹線道路は、少しずつ向きを変えた 3 本の候補のうち、先の人口密度が最も高い向きへ伸びる。
      まれに直角に分岐して新しい幹線道路を作り、人口のある所では両側に街路を出す。
    * 街路は、人口密度がある程度高い所でだけ、まっすぐ伸び、確率で直角に分岐する。
    """
    results: list[tuple[float, Proposal]] = []
    if proposal.highway:
        candidates = [Proposal(end, proposal.angle + delta, True) for delta in (-0.25, 0.0, 0.25)]
        best = max(candidates, key=lambda p: density_at(p.end()))
        if density_at(best.end()) > 0.05:
            results.append((1.0, best))
        if rng.random() < 0.06:
            side = 1.0 if rng.random() < 0.5 else -1.0
            results.append((1.0, Proposal(end, proposal.angle + side * math.pi / 2, True)))
        if density_at(end) > 0.25:
            for side in (-1.0, 1.0):
                if rng.random() < 0.7:
                    results.append((STREET_DELAY, Proposal(end, proposal.angle + side * math.pi / 2, False)))
    elif density_at(end) > 0.3:
        results.append((1.0, Proposal(end, proposal.angle + rng.normal(0.0, 0.03), False)))
        for side in (-1.0, 1.0):
            if rng.random() < 0.3:
                results.append((1.0, Proposal(end, proposal.angle + side * math.pi / 2, False)))
    return results


def grow_streets(seed: int) -> Network:
    """優先度付きキューで、時刻の早い提案から順に処理して街路網を作る。"""
    rng = np.random.default_rng(seed)
    network = Network()
    center = (SIZE / 2, SIZE / 2)
    angle = float(rng.uniform(0.0, math.pi))
    queue: list[tuple[float, int, Proposal]] = []
    counter = 0  # 時刻が同じ提案を、追加した順に取り出すための番号
    for direction in (angle, angle + math.pi):  # 中心から反対向きに 2 本の幹線道路を伸ばす
        heapq.heappush(queue, (0.0, counter, Proposal(center, direction, True)))
        counter += 1
    while queue and network.count < MAX_SEGMENTS:
        time, _, proposal = heapq.heappop(queue)
        accepted = local_constraints(network, proposal)
        if accepted is None:
            continue
        end, stop = accepted
        network.add(proposal.start, end, proposal.highway)
        if stop:
            continue
        for delay, successor in global_goals(proposal, end, rng):
            heapq.heappush(queue, (time + delay, counter, successor))
            counter += 1
    return network


def population_image(resolution: int = 200) -> FloatArray:
    xs = (np.arange(resolution) + 0.5) / resolution * SIZE
    x, y = np.meshgrid(xs, xs)
    return population(x, y)


def draw_network(ax: object, network: Network, count: int) -> None:
    for k in range(count):
        (x0, y0), (x1, y1) = network.starts[k], network.ends[k]
        highway = bool(network.highway[k])
        ax.plot([x0, x1], [y0, y1], color="#c44e52" if highway else "#333333",  # type: ignore[attr-defined]
                linewidth=1.8 if highway else 0.7, solid_capstyle="round")


def draw_growth(file_name: str, network: Network) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(13, 4.6))
    background = population_image()
    for ax, count in zip(axes, [60, 400, network.count]):
        ax.imshow(background, extent=(0, SIZE, SIZE, 0), cmap="Greens", vmin=0.0, vmax=1.6)
        draw_network(ax, network, count)
        ax.set_xlim(0, SIZE)
        ax.set_ylim(SIZE, 0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{count} 区間", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def rasterize(network: Network, pixels: int, count: int | None = None, width: int = 3) -> Image.Image:
    """道路を白黒の画像に描く（道路が 255）。"""
    image = Image.new("L", (pixels, pixels), 0)
    draw = ImageDraw.Draw(image)
    scale = pixels / SIZE
    for k in range(network.count if count is None else count):
        (x0, y0), (x1, y1) = network.starts[k] * scale, network.ends[k] * scale
        draw.line([(x0, y0), (x1, y1)], fill=255, width=width + (2 if network.highway[k] else 0))
    return image


def blocks(network: Network, pixels: int = 800) -> FloatArray:
    """道路で囲まれた領域（街区）を、連結成分のラベル付けで求めて色分けした画像を返す。

    画像の縁に接する領域は、道路で囲まれていないので街区としない。
    """
    road = np.asarray(rasterize(network, pixels)) > 0
    labels, count = ndimage.label(~road)
    edge_labels = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    rng = np.random.default_rng(0)
    palette = 0.55 + 0.4 * rng.random((count + 1, 3))
    palette[edge_labels] = 1.0
    image = palette[labels]
    image[road] = (0.25, 0.25, 0.28)
    result: FloatArray = image
    return result


def draw_blocks(file_name: str, network: Network) -> None:
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(blocks(network), extent=(0, SIZE, SIZE, 0))
    ax.set_axis_off()
    figure.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    save_figure(figure, output_dir(__file__) / file_name)


def write_video(file_name: str, network: Network) -> None:
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    pixels = 360
    background = np.asarray(Image.fromarray((population_image(pixels) * 255).astype(np.uint8)), dtype=np.float64)
    base = 1.0 - 0.25 * (background / 255.0)[..., None] * np.array([0.6, 0.2, 0.6])  # 人口の多い所を緑っぽく
    counts = list(range(4, network.count, 8)) + [network.count] * 45
    with VideoWriter(output_dir(__file__) / file_name, pixels, pixels, fps=30) as writer:
        for count in counts:
            road = np.asarray(rasterize(network, pixels, count, width=1), dtype=np.float64)[..., None] / 255.0
            writer.write(base * (1.0 - road) + 0.2 * road)


def main() -> None:
    setup_matplotlib()
    network = grow_streets(seed=5)
    draw_growth("streets_growth.png", network)
    draw_blocks("streets_blocks.png", network)
    write_video("streets.mp4", network)


if __name__ == "__main__":
    main()
