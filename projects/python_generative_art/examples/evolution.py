"""半透明の三角形による、進化的アルゴリズムを使った画像近似。

**進化的アルゴリズム** は、乱数による変異(mutation)と、目標に対する
「良さ」(適応度、fitness)による選択(selection)を繰り返すことで、
設計者が手続きを直接書かなくても解が徐々に洗練されていく手法である。
:doc:`../fractals` のIFSが「決まった変換を繰り返し適用する」手法
だったのに対し、進化的アルゴリズムは「変異のたびに良くなったかどうかを
判定し、良くなった場合だけ採用する」という、フィードバックを伴う
反復である点が異なる。

ここでは、多数の半透明三角形を重ね合わせて1枚の目標画像に近づける、
という単純な題材を扱う。個体(genome)を「三角形のリスト」として
表現し、次の1手だけで探索する **(1+1)進化戦略** という、実装が
もっとも単純な形の進化的アルゴリズムを使う。

1. 現在の個体を複製し、ランダムに1箇所だけ変異させる(三角形を
   1枚追加・削除する、頂点を少しずらす、色を少し変える、のいずれか)。
2. 変異後の個体を描画し、目標画像との差(平均二乗誤差)を測る。
3. 差が変異前より小さくなっていれば採用し、そうでなければ棄てて
   元の個体に戻る。
4. 1-3を指定世代数だけ繰り返す。

集団(population)を持たず「現在の1個体」だけを保持するため、
本来の遺伝的アルゴリズムにある交叉(crossover)は行わない。それでも、
改善する変異だけを採用する **登山法** (hill climbing) を積み重ねる
だけで、三角形の集合が目標画像に徐々に近づいていく様子が観察できる。
"""

import math
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw

Triangle = tuple[np.ndarray, tuple[int, int, int, int]]
Genome = list[Triangle]


def make_target(width: int, height: int) -> Image.Image:
    """近似の目標にする、単純な図形だけから成る画像を合成する。

    外部の画像ファイルに頼らず、空のグラデーション・太陽・山という
    3種類の平坦な図形だけで構成することで、少数の三角形でも近似の
    様子が分かりやすい題材にしている。
    """
    top: np.ndarray = np.array([120.0, 170.0, 230.0])
    bottom: np.ndarray = np.array([245.0, 245.0, 250.0])
    ys: np.ndarray = np.linspace(0.0, 1.0, height)[:, None]
    gradient: np.ndarray = top[None, :] * (1 - ys) + bottom[None, :] * ys
    pixels: np.ndarray = np.tile(gradient[:, None, :], (1, width, 1))
    img: Image.Image = Image.fromarray(pixels.astype(np.uint8), "RGB")

    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    draw.ellipse(
        [width * 0.62, height * 0.08, width * 0.90, height * 0.36],
        fill=(250, 200, 80),
    )
    draw.polygon(
        [(0, height), (width * 0.38, height * 0.32), (width * 0.7, height)],
        fill=(95, 135, 95),
    )
    draw.polygon(
        [
            (width * 0.28, height),
            (width * 0.64, height * 0.5),
            (width, height),
        ],
        fill=(60, 95, 70),
    )
    return img


def random_triangle(
    width: int, height: int, rng: np.random.Generator
) -> Triangle:
    """画面内のランダムな位置を中心とした、小ぶりな三角形を1つ作る。

    アルファ値を低め(20-130 程度)に抑えることで、複数枚重なった
    ときに色が徐々に混ざり合い、単色のベタ塗りより滑らかに目標画像へ
    近づけるようにしている。
    """
    max_radius: float = min(width, height) * 0.35
    center: np.ndarray = rng.uniform([0.0, 0.0], [width, height])
    angles: np.ndarray = rng.uniform(0.0, 2.0 * math.pi, size=3)
    radii: np.ndarray = rng.uniform(0.2, 1.0, size=3) * max_radius
    vertices: np.ndarray = center + np.stack(
        [radii * np.cos(angles), radii * np.sin(angles)], axis=-1
    )
    color: tuple[int, int, int, int] = (
        int(rng.integers(0, 256)),
        int(rng.integers(0, 256)),
        int(rng.integers(0, 256)),
        int(rng.integers(20, 130)),
    )
    return vertices, color


@lru_cache(maxsize=4)
def _pixel_grid(width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    """画素中心の座標グリッドを ``(width, height)`` ごとにキャッシュする。

    本章では同じ画像サイズに対して ``triangle_mask`` を何十万回も
    呼び出すため、画素グリッドをそのたびに作り直すのは無駄が大きい。
    ``functools.lru_cache`` に任せることで、初回だけ計算し、以降は
    同じ配列を使い回す。
    """
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=np.float64) + 0.5,
        np.arange(height, dtype=np.float64) + 0.5,
    )
    return xs, ys


def triangle_mask(
    vertices: np.ndarray, width: int, height: int
) -> np.ndarray:
    """三角形の内部にある画素を真とするブール配列を返す。

    3辺それぞれについて「画素がその辺のどちら側にあるか」を表す
    符号付き面積(edge function)を求め、3辺すべてで符号がそろって
    いる画素だけを内部と判定する。PILで三角形を描いてから配列に
    変換するのではなく、画素グリッド全体に対する1回のNumPy演算で
    判定できるため、世代ごとに全個体を描き直す本節の用途では
    こちらの方が高速である。
    """
    xs, ys = _pixel_grid(width, height)
    (x1, y1), (x2, y2), (x3, y3) = vertices

    d1: np.ndarray = (xs - x2) * (y1 - y2) - (x1 - x2) * (ys - y2)
    d2: np.ndarray = (xs - x3) * (y2 - y3) - (x2 - x3) * (ys - y3)
    d3: np.ndarray = (xs - x1) * (y3 - y1) - (x3 - x1) * (ys - y1)

    has_neg: np.ndarray = (d1 < 0) | (d2 < 0) | (d3 < 0)
    has_pos: np.ndarray = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return ~(has_neg & has_pos)


def render_genome(genome: Genome, width: int, height: int) -> np.ndarray:
    """三角形の集合を白背景に重ね合わせて描画し、RGB配列を返す。

    三角形ごとに ``triangle_mask`` で内部画素を求め、アルファ値で
    重みづけしながら ``canvas = canvas * (1-a) + color * a`` という
    通常のアルファブレンドを行う。
    """
    canvas: np.ndarray = np.full((height, width, 3), 255.0)
    for vertices, color in genome:
        inside: np.ndarray = triangle_mask(vertices, width, height)
        alpha: float = color[3] / 255.0
        canvas[inside] = (
            canvas[inside] * (1 - alpha)
            + np.array(color[:3], dtype=np.float64) * alpha
        )
    return canvas


def fitness(candidate: np.ndarray, target: np.ndarray) -> float:
    """目標画像との平均二乗誤差(小さいほど良い)。"""
    diff: np.ndarray = candidate - target
    return float(np.mean(diff * diff))


_MUTATION_KINDS: tuple[str, str, str, str] = (
    "add", "remove", "vertex", "color"
)
_WEIGHTS_BELOW_LIMIT: tuple[float, float, float, float] = (
    0.25, 0.1, 0.4, 0.25
)
_WEIGHTS_AT_LIMIT: tuple[float, float, float, float] = (0.0, 0.15, 0.55, 0.3)


def _choose_mutation_kind(rng: np.random.Generator, can_add: bool) -> str:
    """変異の種類を重み付き乱数で選ぶ。

    ``rng.choice`` に文字列のリストを渡すと、NumPyの型定義上は
    戻り値の型が一意に決まらない。あらかじめ用意した固定の
    ``tuple[str, ...]`` から累積確率でインデックスを選んで引く
    ことで、戻り値が確実に ``str`` になるようにしている。
    """
    weights: tuple[float, float, float, float] = (
        _WEIGHTS_BELOW_LIMIT if can_add else _WEIGHTS_AT_LIMIT
    )
    cumulative: np.ndarray = np.cumsum(weights)
    index: int = int(np.searchsorted(cumulative, rng.random()))
    return _MUTATION_KINDS[index]


def mutate(
    genome: Genome,
    rng: np.random.Generator,
    width: int,
    height: int,
    max_triangles: int,
) -> Genome:
    """現在の個体を複製し、1箇所だけランダムに変異させる。"""
    child: Genome = [
        (vertices.copy(), color) for vertices, color in genome
    ]

    if not child:
        child.append(random_triangle(width, height, rng))
        return child

    kind: str = _choose_mutation_kind(rng, can_add=len(child) < max_triangles)

    if kind == "add":
        child.append(random_triangle(width, height, rng))
    elif kind == "remove":
        remove_index: int = int(rng.integers(len(child)))
        del child[remove_index]
    elif kind == "vertex":
        i: int = int(rng.integers(len(child)))
        vertices, color = child[i]
        vertices = vertices.copy()
        j: int = int(rng.integers(3))
        vertices[j] += rng.normal(0.0, min(width, height) * 0.05, size=2)
        child[i] = (vertices, color)
    else:  # color
        i = int(rng.integers(len(child)))
        vertices, color = child[i]
        jitter: np.ndarray = rng.normal(0.0, 20.0, size=4)
        new_color: tuple[int, int, int, int] = (
            int(np.clip(color[0] + jitter[0], 0, 255)),
            int(np.clip(color[1] + jitter[1], 0, 255)),
            int(np.clip(color[2] + jitter[2], 0, 255)),
            int(np.clip(color[3] + jitter[3], 0, 255)),
        )
        child[i] = (vertices, new_color)

    return child


def evolve(
    target: np.ndarray,
    width: int,
    height: int,
    generations: int,
    max_triangles: int,
    rng: np.random.Generator,
    snapshot_at: tuple[int, ...] = (),
) -> tuple[Genome, dict[int, np.ndarray]]:
    """(1+1)進化戦略で、三角形の集合を目標画像へ近づける。"""
    genome: Genome = []
    best_score: float = fitness(render_genome(genome, width, height), target)
    snapshots: dict[int, np.ndarray] = {}

    for generation in range(generations):
        candidate: Genome = mutate(genome, rng, width, height, max_triangles)
        candidate_image: np.ndarray = render_genome(candidate, width, height)
        candidate_score: float = fitness(candidate_image, target)

        if candidate_score < best_score:
            genome = candidate
            best_score = candidate_score

        if generation in snapshot_at:
            snapshots[generation] = render_genome(genome, width, height)

    return genome, snapshots


def _to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def main() -> None:
    width: int = 120
    height: int = 120
    rng: np.random.Generator = np.random.default_rng(seed=0)

    target_img: Image.Image = make_target(width, height)
    target_preview: Image.Image = target_img.resize(
        (240, 240), Image.Resampling.NEAREST
    )
    target_preview.save("evolution_target.png")
    target_arr: np.ndarray = np.asarray(target_img, dtype=np.float64)

    checkpoints: tuple[int, ...] = (30, 300, 1500, 5999)
    best_genome, snapshots = evolve(
        target_arr,
        width,
        height,
        generations=6000,
        max_triangles=100,
        rng=rng,
        snapshot_at=checkpoints,
    )

    tile_size: int = 150
    grid: Image.Image = Image.new(
        "RGB", (tile_size * len(checkpoints), tile_size), "white"
    )
    for i, generation in enumerate(checkpoints):
        tile: Image.Image = _to_image(snapshots[generation]).resize(
            (tile_size, tile_size), Image.Resampling.NEAREST
        )
        grid.paste(tile, (i * tile_size, 0))
    grid.save("evolution_progress.png")

    final_image: Image.Image = _to_image(
        render_genome(best_genome, width, height)
    ).resize((240, 240), Image.Resampling.NEAREST)
    final_image.save("evolution_result.png")


if __name__ == "__main__":
    main()
