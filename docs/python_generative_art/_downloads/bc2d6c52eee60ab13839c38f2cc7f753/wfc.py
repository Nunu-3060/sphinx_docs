"""Wave Function Collapse(WFC)による、隣接制約を満たすタイル配置。

格子の各セルに「まだ置ける可能性のあるタイルの集合」を持たせ、
次の2つの操作を、全てのセルのタイルが1つに決まるまで繰り返す。

観測(observe)
    候補がもっとも少ないセルを1つ選び、候補の中から1枚を
    ランダムに選んで確定させる。
伝播(propagate)
    確定によって、隣のセルで辺がつながらなくなった候補を取り除く。
    取り除いた結果、さらにその隣の候補も減ることがあるため、
    変化がなくなるまで連鎖的に繰り返す。

ここでは Maxim Gumin の WFC のうち、タイルの辺の種類だけから
隣接関係を決める「simple tiled model」を、配管のようなタイルで
実装する。
"""

import numpy as np
from PIL import Image, ImageDraw

# 方向の番号: 0=上, 1=右, 2=下, 3=左。反対側の方向は (d + 2) % 4。
_OFFSETS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def pipe_tiles() -> np.ndarray:
    """配管タイルの一覧を、形状 (タイル数, 4) の配列で返す。

    各行は上・右・下・左の辺に管がつながっているか(1)いないか(0)を
    表す。4辺の 0/1 の組み合わせ16通りのうち、管が1辺にしか
    つながらない「行き止まり」の4通りを除いた12枚を使う。
    """
    tiles: list[list[int]] = []
    for code in range(16):
        edges: list[int] = [(code >> d) & 1 for d in range(4)]
        if sum(edges) != 1:
            tiles.append(edges)
    return np.array(tiles)


def compatibility(tiles: np.ndarray) -> np.ndarray:
    """方向ごとのタイルの隣接可否を、形状 (4, T, T) の真偽値配列で返す。

    ``result[d, a, b]`` は、タイル ``a`` の方向 ``d`` の隣にタイル ``b``
    を置けるかどうか(``a`` の辺 ``d`` と ``b`` の反対側の辺が一致するか)。
    """
    return np.stack(
        [
            tiles[:, d, np.newaxis] == tiles[np.newaxis, :, (d + 2) % 4]
            for d in range(4)
        ]
    )


def _propagate(
    wave: np.ndarray, compat: np.ndarray, stack: list[tuple[int, int]]
) -> bool:
    """``stack`` のセルから候補の削減を伝播させる。矛盾が起きたら False。"""
    rows: int
    cols: int
    rows, cols = wave.shape[:2]
    while stack:
        r, c = stack.pop()
        for d, (dr, dc) in enumerate(_OFFSETS):
            nr: int = r + dr
            nc: int = c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # (r, c) に残っている候補のどれか1つとでもつながるタイルだけ残す。
            allowed: np.ndarray = compat[d][wave[r, c]].any(axis=0)
            reduced: np.ndarray = wave[nr, nc] & allowed
            if not reduced.any():
                return False
            if not np.array_equal(reduced, wave[nr, nc]):
                wave[nr, nc] = reduced
                stack.append((nr, nc))
    return True


def wave_function_collapse(
    tiles: np.ndarray,
    weights: np.ndarray,
    rows: int,
    cols: int,
    rng: np.random.Generator,
    max_attempts: int = 20,
) -> np.ndarray:
    """WFC でタイルを配置し、形状 (rows, cols) のタイル番号配列を返す。

    格子の外周では、外側へ向かう辺に管がつながらないタイルだけを
    候補として始める。候補が1つも残らないセルが出る(矛盾する)と、
    それ以上は進められないため、最初からやり直す。
    """
    compat: np.ndarray = compatibility(tiles)
    closed: np.ndarray = tiles == 0  # closed[t, d]: タイル t の辺 d が空き

    for _ in range(max_attempts):
        wave: np.ndarray = np.ones((rows, cols, len(tiles)), dtype=bool)
        wave[0, :] &= closed[:, 0]
        wave[:, -1] &= closed[:, 1]
        wave[-1, :] &= closed[:, 2]
        wave[:, 0] &= closed[:, 3]
        ok: bool = _propagate(
            wave, compat, [(r, c) for r in range(rows) for c in range(cols)]
        )

        while ok:
            counts: np.ndarray = wave.sum(axis=2)
            if (counts == 1).all():
                return wave.argmax(axis=2)

            # 観測: 候補がもっとも少ないセル(同数なら乱数で選ぶ)を確定させる。
            score: np.ndarray = np.where(
                counts > 1, counts + rng.random((rows, cols)), np.inf
            )
            r, c = np.unravel_index(int(np.argmin(score)), (rows, cols))
            candidates: np.ndarray = np.flatnonzero(wave[r, c])
            p: np.ndarray = weights[candidates] / weights[candidates].sum()
            chosen: int = int(rng.choice(candidates, p=p))
            wave[r, c] = False
            wave[r, c, chosen] = True

            ok = _propagate(wave, compat, [(int(r), int(c))])

    raise RuntimeError("矛盾が解消できず、タイルを配置できなかった。")


def render_pipes(
    grid: np.ndarray,
    tiles: np.ndarray,
    tile_size: int = 20,
    background: tuple[int, int, int] = (22, 30, 45),
    color: tuple[int, int, int] = (90, 210, 200),
) -> Image.Image:
    """タイル番号の配列を、中心から辺の中点へ伸びる管として描く。"""
    rows: int
    cols: int
    rows, cols = grid.shape
    image: Image.Image = Image.new(
        "RGB", (cols * tile_size, rows * tile_size), background
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    width: int = max(2, tile_size // 4)
    half: float = tile_size / 2
    for r in range(rows):
        for c in range(cols):
            edges: np.ndarray = tiles[grid[r, c]]
            if not edges.any():
                continue
            cx: float = c * tile_size + half
            cy: float = r * tile_size + half
            for d, (dr, dc) in enumerate(_OFFSETS):
                if edges[d]:
                    draw.line(
                        [(cx, cy), (cx + dc * half, cy + dr * half)],
                        fill=color,
                        width=width,
                    )
            radius: float = width / 2
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=color,
            )
    return image


def main() -> None:
    tiles: np.ndarray = pipe_tiles()
    connections: np.ndarray = tiles.sum(axis=1)
    straight: np.ndarray = (tiles[:, 0] == tiles[:, 2]) & (
        tiles[:, 1] == tiles[:, 3]
    ) & (connections == 2)

    # 1. 全てのタイルを同じ重みで選ぶ。
    rng: np.random.Generator = np.random.default_rng(seed=2)
    uniform: np.ndarray = np.ones(len(tiles))
    grid: np.ndarray = wave_function_collapse(tiles, uniform, 24, 24, rng)
    render_pipes(grid, tiles).save("wfc_uniform.png")

    # 2. 空白と直線のタイルを選びやすくすると、長い管がまばらに走る。
    weighted: np.ndarray = np.where(
        connections == 0, 6.0, np.where(straight, 4.0, 1.0)
    )
    weighted[connections >= 3] = 0.3
    rng = np.random.default_rng(seed=2)
    grid = wave_function_collapse(tiles, weighted, 24, 24, rng)
    render_pipes(grid, tiles).save("wfc_weighted.png")

    # 参考: 12枚のタイルを、隙間を空けて横に並べた一覧画像。
    tile_size: int = 40
    gap: int = 8
    catalog: Image.Image = Image.new(
        "RGB", (len(tiles) * (tile_size + gap) - gap, tile_size), "white"
    )
    for index in range(len(tiles)):
        single: np.ndarray = np.array([[index]])
        catalog.paste(
            render_pipes(single, tiles, tile_size=tile_size),
            (index * (tile_size + gap), 0),
        )
    catalog.save("wfc_tiles.png")


if __name__ == "__main__":
    main()
