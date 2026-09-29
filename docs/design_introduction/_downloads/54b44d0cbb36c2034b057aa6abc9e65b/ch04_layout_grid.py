"""第 4 章: グリッドシステムに沿ってレイアウトする。

12 カラムのグリッドを定義し、ダッシュボード風の画面を配置します。

* ch04_no_grid.png: 要素の位置と大きさを目分量で決めた例
* ch04_grid.png: グリッドに沿って配置した例 (グリッド線を重ねて表示)

実行例::

    python ch04_layout_grid.py --outdir output
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

Box = tuple[int, int, int, int]

PAGE_W, PAGE_H = 960, 560
CARD_COLOR = "#e8eef8"
BORDER_COLOR = "#9fb3d9"


@dataclass(frozen=True)
class Grid:
    """カラム数・マージン・ガターから各カラムの位置を計算する。"""

    width: int
    columns: int = 12
    margin: int = 48  # ページ左右の余白
    gutter: int = 24  # カラム間の余白

    @property
    def column_width(self) -> float:
        """1 カラムの幅。"""
        content = self.width - self.margin * 2
        return (content - self.gutter * (self.columns - 1)) / self.columns

    def x(self, column: int) -> int:
        """column 番目 (0 始まり) のカラムの左端の x 座標。"""
        return round(self.margin + column * (self.column_width + self.gutter))

    def span(self, column: int, count: int) -> tuple[int, int]:
        """column 番目から count 個のカラムにまたがる範囲の左端と右端。"""
        left = self.x(column)
        right = round(left + self.column_width * count
                      + self.gutter * (count - 1))
        return left, right


def draw_card(draw: ImageDraw.ImageDraw, box: Box) -> None:
    """カード (角丸の四角形) を描画する。"""
    draw.rounded_rectangle(box, radius=8, fill=CARD_COLOR,
                           outline=BORDER_COLOR)


def draw_no_grid() -> Image.Image:
    """位置と大きさを目分量で決めたレイアウト。"""
    image = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    draw = ImageDraw.Draw(image)
    boxes: list[Box] = [
        (40, 30, 930, 90),  # ヘッダー
        (55, 115, 260, 215), (285, 110, 470, 220),  # 指標カード
        (500, 118, 700, 212), (720, 115, 915, 225),
        (40, 245, 600, 530),  # グラフ
        (625, 250, 925, 525),  # 表
    ]
    for box in boxes:
        draw_card(draw, box)
    return image


def draw_with_grid(show_grid: bool = True) -> Image.Image:
    """12 カラムのグリッドと 8 px 単位の余白に沿ったレイアウト。"""
    grid = Grid(PAGE_W)
    image = Image.new("RGB", (PAGE_W, PAGE_H), "white")

    if show_grid:
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        for column in range(grid.columns):
            left, right = grid.span(column, 1)
            overlay_draw.rectangle((left, 0, right, PAGE_H),
                                   fill=(255, 99, 71, 40))
        image.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(image)
    unit = 8  # 縦方向の余白はすべて 8 の倍数にする
    header_top, header_bottom = unit * 4, unit * 11
    kpi_top, kpi_bottom = unit * 14, unit * 27
    main_top, main_bottom = unit * 30, PAGE_H - unit * 4

    left, right = grid.span(0, 12)
    draw_card(draw, (left, header_top, right, header_bottom))
    for i in range(4):  # 指標カードは 3 カラムずつ
        left, right = grid.span(i * 3, 3)
        draw_card(draw, (left, kpi_top, right, kpi_bottom))
    left, right = grid.span(0, 8)  # グラフは 8 カラム
    draw_card(draw, (left, main_top, right, main_bottom))
    left, right = grid.span(8, 4)  # 表は 4 カラム
    draw_card(draw, (left, main_top, right, main_bottom))
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    grid = Grid(PAGE_W)
    print(f"カラム幅: {grid.column_width:.1f} px")
    draw_no_grid().save(outdir / "ch04_no_grid.png")
    draw_with_grid().save(outdir / "ch04_grid.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
