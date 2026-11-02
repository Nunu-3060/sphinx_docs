"""第 8 章「文法と成長による形状」: 分割文法（split grammar）による建物の外壁。

* facade_derivation.png: 外壁を 階 → 柱間 → 窓 の順に分割していく様子
* facades.png: シードだけを変えて作った外壁
* buildings3d.png: 外壁の分割を箱形の建物の 4 面に貼った立体の街並み
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

from color import hex_to_rgb
from common import FloatArray, output_dir, save_figure, setup_matplotlib


@dataclass
class Rect:
    """外壁の上の長方形の領域（左下の角 x, y と幅 w、高さ h。単位は m）。"""

    x: float
    y: float
    w: float
    h: float


@dataclass
class Terminal:
    """これ以上分割しない形（終端記号）。kind は壁・窓・扉などの種類。"""

    kind: str
    rect: Rect
    depth: int


@dataclass
class Style:
    """建物ごとに乱数で決めるパラメーター。"""

    floors: int
    floor_height: float
    ground_height: float
    tile_width: float
    window_ratio: float
    window: str  # 窓の種類: plain, arch, shutter, balcony
    wall: str
    trim: str


WALLS = ["#d8c3a5", "#c97b63", "#e8e1d0", "#9fb4c7", "#b9a07a", "#d9a5a0"]
TRIMS = ["#f4f1ea", "#5b4a3f", "#3e4a5a", "#efe6d2"]
WINDOWS = ["plain", "arch", "shutter", "balcony"]


def random_style(seed: int) -> Style:
    """シードから建物のパラメーターを決める（範囲を決めて、その中で乱数を使う）。"""
    rng = np.random.default_rng(seed)
    return Style(
        floors=int(rng.integers(3, 7)),
        floor_height=float(rng.uniform(2.9, 3.5)),
        ground_height=float(rng.uniform(3.8, 4.6)),
        tile_width=float(rng.uniform(2.2, 3.4)),
        window_ratio=float(rng.uniform(0.38, 0.6)),
        window=WINDOWS[int(rng.integers(len(WINDOWS)))],
        wall=WALLS[int(rng.integers(len(WALLS)))],
        trim=TRIMS[int(rng.integers(len(TRIMS)))],
    )


# 分割の大きさの指定。数値は m 単位の固定の大きさ、"~" は残りを等分する可変の大きさ。
Size = float | str


def split(rect: Rect, axis: str, sizes: list[Size]) -> list[Rect]:
    """rect を axis（"x" は左から右、"y" は下から上）の向きに、sizes の大きさで分ける。"""
    length = rect.w if axis == "x" else rect.h
    fixed = sum(size for size in sizes if not isinstance(size, str))
    flexible = sum(1 for size in sizes if isinstance(size, str))
    rest = max(length - fixed, 0.0) / flexible if flexible else 0.0
    scale = 1.0 if flexible or fixed == 0 else length / fixed  # 可変が無ければ全体を伸縮する
    parts = []
    position = rect.x if axis == "x" else rect.y
    for size in sizes:
        amount = rest if isinstance(size, str) else size * scale
        if axis == "x":
            parts.append(Rect(position, rect.y, amount, rect.h))
        else:
            parts.append(Rect(rect.x, position, rect.w, amount))
        position += amount
    return parts


def repeat(rect: Rect, axis: str, size: float) -> list[Rect]:
    """rect を、大きさ size に近い等しい大きさで、できるだけ多く並べて分ける。"""
    length = rect.w if axis == "x" else rect.h
    count = max(1, int(round(length / size)))
    return split(rect, axis, ["~"] * count)


class FacadeGrammar:
    """外壁の分割文法。規則は「記号の名前 → 領域を分けて子の記号を返す関数」で表す。"""

    def __init__(self, style: Style) -> None:
        self.style = style
        self.rules: dict[str, Callable[[Rect], list[tuple[str, Rect]]]] = {
            "Facade": self.facade,
            "Floors": self.floors,
            "Floor": self.floor,
            "Tile": self.tile,
            "WindowColumn": self.window_column,
            "Ground": self.ground,
            "DoorTile": self.door_tile,
            "ShopTile": self.shop_tile,
        }

    def facade(self, r: Rect) -> list[tuple[str, Rect]]:
        ground, floors, cornice = split(r, "y", [self.style.ground_height, "~", 0.7])
        return [("Ground", ground), ("Floors", floors), ("cornice", cornice)]

    def floors(self, r: Rect) -> list[tuple[str, Rect]]:
        return [("Floor", part) for part in repeat(r, "y", self.style.floor_height)]

    def floor(self, r: Rect) -> list[tuple[str, Rect]]:
        left, tiles, right = split(r, "x", [0.6, "~", 0.6])
        return [("wall", left)] + [("Tile", t) for t in repeat(tiles, "x", self.style.tile_width)] + [("wall", right)]

    def tile(self, r: Rect) -> list[tuple[str, Rect]]:
        width = r.w * self.style.window_ratio
        left, column, right = split(r, "x", ["~", width, "~"])
        return [("wall", left), ("WindowColumn", column), ("wall", right)]

    def window_column(self, r: Rect) -> list[tuple[str, Rect]]:
        below, window, above = split(r, "y", [0.9, "~", 0.6])
        return [("wall", below), ("window", window), ("wall", above)]

    def ground(self, r: Rect) -> list[tuple[str, Rect]]:
        left, tiles, right = split(r, "x", [0.6, "~", 0.6])
        parts = repeat(tiles, "x", self.style.tile_width)
        middle = len(parts) // 2  # 中央の柱間を入口にする
        children = [("DoorTile" if k == middle else "ShopTile", part) for k, part in enumerate(parts)]
        return [("wall", left)] + children + [("wall", right)]

    def door_tile(self, r: Rect) -> list[tuple[str, Rect]]:
        left, door, right = split(r, "x", ["~", min(1.6, 0.8 * r.w), "~"])
        door_part, above = split(door, "y", [min(2.8, r.h - 0.6), "~"])
        return [("wall", left), ("door", door_part), ("wall", above), ("wall", right)]

    def shop_tile(self, r: Rect) -> list[tuple[str, Rect]]:
        left, shop, right = split(r, "x", [0.25, "~", 0.25])
        below, glass, above = split(shop, "y", [0.5, "~", 0.7])
        return [("wall", left), ("wall", below), ("shop", glass), ("wall", above), ("wall", right)]

    def derive(self, symbol: str, rect: Rect, max_depth: int = 99, depth: int = 0) -> list[Terminal]:
        """記号 symbol を、規則が無くなるまで（または max_depth 段まで）再帰的に分割する。"""
        rule = self.rules.get(symbol)
        if rule is None or depth >= max_depth:
            return [Terminal(symbol, rect, depth)]
        result = []
        for child, child_rect in rule(rect):
            result += self.derive(child, child_rect, max_depth, depth + 1)
        return result


def facade_height(style: Style) -> float:
    return style.ground_height + style.floors * style.floor_height + 0.7


def draw_terminal(ax: object, terminal: Terminal, style: Style) -> None:
    """終端記号を 1 つ描く。窓の種類による飾り（アーチ、鎧戸、バルコニー）もここで描く。"""
    from matplotlib.patches import Rectangle, Wedge

    r = terminal.rect
    wall = hex_to_rgb(style.wall)
    trim = hex_to_rgb(style.trim)
    glass = (0.30, 0.42, 0.55)

    def box(x: float, y: float, w: float, h: float, color: tuple[float, float, float]) -> None:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, linewidth=0))  # type: ignore[attr-defined]

    if terminal.kind == "wall":
        box(r.x, r.y, r.w, r.h, wall)
    elif terminal.kind == "cornice":
        box(r.x, r.y, r.w, r.h, tuple(0.8 * c for c in wall))  # type: ignore[arg-type]
        box(r.x, r.y + r.h - 0.15, r.w, 0.15, trim)
    elif terminal.kind == "door":
        box(r.x, r.y, r.w, r.h, wall)
        box(r.x + 0.1, r.y, r.w - 0.2, r.h - 0.1, (0.40, 0.26, 0.18))
    elif terminal.kind == "shop":
        box(r.x, r.y, r.w, r.h, trim)
        box(r.x + 0.08, r.y + 0.08, r.w - 0.16, r.h - 0.16, (0.55, 0.68, 0.78))
    elif terminal.kind == "window":
        box(r.x, r.y, r.w, r.h, wall)
        top = r.h
        if style.window == "arch":
            top = r.h - r.w / 2
            ax.add_patch(Wedge((r.x + r.w / 2, r.y + top), r.w / 2, 0, 180,  # type: ignore[attr-defined]
                               facecolor=trim, linewidth=0))
            ax.add_patch(Wedge((r.x + r.w / 2, r.y + top), r.w / 2 - 0.1, 0, 180,  # type: ignore[attr-defined]
                               facecolor=glass, linewidth=0))
        box(r.x, r.y, r.w, top, trim)
        box(r.x + 0.1, r.y + 0.1, r.w - 0.2, top - (0.1 if style.window == "arch" else 0.2), glass)
        box(r.x - 0.1, r.y - 0.12, r.w + 0.2, 0.12, trim)  # 窓台
        if style.window == "shutter":
            for x in (r.x - r.w * 0.45, r.x + r.w):
                box(x, r.y, r.w * 0.45, r.h, (0.30, 0.45, 0.32))
        if style.window == "balcony":
            box(r.x - 0.35, r.y - 0.1, r.w + 0.7, 0.12, (0.25, 0.25, 0.25))
            for k in range(7):
                box(r.x - 0.35 + k * (r.w + 0.6) / 6, r.y, 0.05, 0.9, (0.25, 0.25, 0.25))
            box(r.x - 0.35, r.y + 0.9, r.w + 0.7, 0.06, (0.25, 0.25, 0.25))


LEVEL_COLORS = ["#4c72b0", "#dd8452", "#55a868", "#c44e52", "#8172b3"]


def draw_derivation(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    style = random_style(3)
    grammar = FacadeGrammar(style)
    facade = Rect(0.0, 0.0, 14.0, facade_height(style))
    figure, axes = plt.subplots(1, 5, figsize=(13, 4.2))
    titles = ["0 段: 外壁全体", "1 段: 地上階・上の階・軒", "2 段: 各階と地上階の柱間", "3 段: 上の階の柱間", "完成"]
    for depth, (ax, title) in enumerate(zip(axes, titles)):
        if depth < 4:
            for terminal in grammar.derive("Facade", facade, max_depth=depth):
                r = terminal.rect
                kind = terminal.kind
                color = "#ffffff" if kind[0].islower() else LEVEL_COLORS[depth % len(LEVEL_COLORS)]
                ax.add_patch(Rectangle((r.x, r.y), r.w, r.h, facecolor=color, alpha=0.35 if kind[0].isupper() else 1,
                                       edgecolor="#333333", linewidth=0.6))
                if kind[0].isupper() and r.w > 1.5:
                    ax.text(r.x + r.w / 2, r.y + r.h / 2, kind, ha="center", va="center", fontsize=6)
        else:
            for terminal in grammar.derive("Facade", facade):
                draw_terminal(ax, terminal, style)
        ax.set_xlim(-0.5, facade.w + 0.5)
        ax.set_ylim(-0.3, facade.h + 0.3)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(title, fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_facades(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(figsize=(13, 4.4))
    x = 0.0
    rng = np.random.default_rng(100)
    for seed in range(6):
        style = random_style(seed)
        width = float(rng.uniform(9.0, 15.0))
        facade = Rect(x, 0.0, width, facade_height(style))
        for terminal in FacadeGrammar(style).derive("Facade", facade):
            draw_terminal(ax, terminal, style)
        label = f"シード {seed}\n{style.floors + 1} 階、{style.window}"
        ax.text(x + width / 2, -2.6, label, ha="center", fontsize=9)
        x += width + 1.2
    ax.plot([-0.5, x - 0.7], [0, 0], color="#555555", linewidth=1)
    ax.set_xlim(-0.5, x - 0.7)
    ax.set_ylim(-2.8, 26)
    ax.set_aspect("equal")
    ax.set_axis_off()
    save_figure(figure, output_dir(__file__) / file_name)


KIND_COLORS = {"door": (0.40, 0.26, 0.18), "shop": (0.55, 0.68, 0.78), "window": (0.30, 0.42, 0.55)}


def building_quads(style: Style, origin: tuple[float, float], width: float, depth: float) -> list[
        tuple[FloatArray, tuple[float, float, float]]]:
    """箱形の建物の 4 面に外壁の分割を貼り、四角形（4 頂点）と色の組の列を返す。屋根も加える。"""
    height = facade_height(style)
    x0, y0 = origin
    # 各面の左下の角と、外から見て右へ向かう向き u。u × (0, 0, 1) が外向きの法線になる。
    sides = [((x0, y0), (1.0, 0.0), width), ((x0 + width, y0), (0.0, 1.0), depth),
             ((x0 + width, y0 + depth), (-1.0, 0.0), width), ((x0, y0 + depth), (0.0, -1.0), depth)]
    grammar = FacadeGrammar(style)
    wall = hex_to_rgb(style.wall)
    quads = []
    for (cx, cy), (ux, uy), length in sides:
        corner = np.array([cx, cy, 0.0])
        u = np.array([ux, uy, 0.0])
        for terminal in grammar.derive("Facade", Rect(0.0, 0.0, length, height)):
            r = terminal.rect
            color = KIND_COLORS.get(terminal.kind, wall)
            points = np.array([corner + u * r.x + [0, 0, r.y], corner + u * (r.x + r.w) + [0, 0, r.y],
                               corner + u * (r.x + r.w) + [0, 0, r.y + r.h], corner + u * r.x + [0, 0, r.y + r.h]])
            quads.append((points, color))
    roof = np.array([[x0, y0, height], [x0 + width, y0, height], [x0 + width, y0 + depth, height],
                     [x0, y0 + depth, height]])
    quads.append((roof, (0.55, 0.53, 0.50)))
    return quads


def draw_buildings(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    elev, azim = 22.0, -62.0
    eye = np.array([np.cos(np.radians(elev)) * np.cos(np.radians(azim)),
                    np.cos(np.radians(elev)) * np.sin(np.radians(azim)), np.sin(np.radians(elev))])
    light = np.array([0.4, -0.7, 0.6]) / np.linalg.norm([0.4, -0.7, 0.6])
    polygons = []
    colors = []
    x = 0.0
    rng = np.random.default_rng(7)
    for seed in range(5):
        width = float(rng.uniform(9.0, 14.0))
        for points, color in building_quads(random_style(seed + 10), (x, 0.0), width, 10.0):
            normal = np.cross(points[1] - points[0], points[3] - points[0])
            normal /= np.linalg.norm(normal)
            if normal @ eye <= 0:  # カメラに背を向けた面は描かない（背面カリング）
                continue
            polygons.append(points)
            colors.append(np.clip(np.array(color) * (0.55 + 0.45 * max(float(normal @ light), 0.0)), 0, 1))
        x += width + 2.0
    figure = plt.figure(figsize=(12, 5.0))
    ax = figure.add_subplot(1, 1, 1, projection="3d")
    ax.add_collection3d(Poly3DCollection(polygons, facecolors=colors, edgecolors=colors, linewidths=0.2))
    # 3 軸の縮尺をそろえる（箱の縦横比を、軸の範囲の比にする）。
    ax.set_xlim(-4, x + 2)
    ax.set_ylim(-2, 12)
    ax.set_zlim(0, 26)
    ax.set_box_aspect((x + 6, 14.0, 26.0), zoom=1.25)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    figure.subplots_adjust(left=0, right=1, top=1, bottom=0)
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_derivation("facade_derivation.png")
    draw_facades("facades.png")
    draw_buildings("buildings3d.png")


if __name__ == "__main__":
    main()
