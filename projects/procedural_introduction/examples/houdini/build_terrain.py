r"""第 16 章: 地形を作るネットワーク（/obj/terrain）を組む。

2 つの作り方を並べる。

* ポリゴンの地形: Grid → Mountain（fBm で変位）→ Attribute Wrangle（島の形）→ Normal
* ハイトフィールドの地形: HeightField → HeightField Noise → HeightField Erode → Convert HeightField

hython での実行例（examples/houdini で）:

    hython build_terrain.py

Houdini の Python Shell での実行例:

    import sys
    sys.path.append(r"C:\procedural_introduction\examples\houdini")
    import build_terrain
    build_terrain.build()
"""

from __future__ import annotations

import time

import hou

from hou_common import add_controls, add_wrangle, check_errors, describe, finish, out_path, recreate_geo, save_hip


def add_island_terrain(geo: hou.Node) -> hou.Node:
    """geo の中にポリゴンの島の地形を作り、法線を付けた最後のノードを返す。

    geo にはスペアパラメーター seed が必要である（add_controls で作る）。
    """
    grid = geo.createNode("grid", "grid")
    grid.parmTuple("size").set((20.0, 20.0))  # 20 × 20 の正方形（Y が上向き）
    grid.parm("rows").set(161)
    grid.parm("cols").set(161)

    # Mountain: 法線（グリッドでは +Y）の向きに fBm のノイズで変位させる。
    # シードの代わりに、ノイズを読み取る位置（offset）をシードからずらす。
    mountain = geo.createNode("mountain::2.0", "mountain")
    mountain.setFirstInput(grid)
    mountain.parm("height").set(8.0)
    mountain.parm("elementsize").set(7.0)
    mountain.parm("oct").set(6)
    mountain.parm("rough").set(0.5)
    mountain.parm("offsetx").setExpression('ch("../seed") * 17.31')
    mountain.parm("offsetz").setExpression('ch("../seed") * 5.77')

    island = add_wrangle(geo, "island", "island.vex",
                         {"radius": 10.0, "lift": 1.0, "depth": 1.0, "sea_level": 0.0})
    island.setFirstInput(mountain)

    # 変位した後の形から、ポイントの法線 N を計算し直す（斜面の傾きの計算に使う）。
    normal = geo.createNode("normal", "normal")
    normal.setFirstInput(island)
    normal.parm("type").set("typepoint")
    return normal


def add_heightfield_terrain(geo: hou.Node) -> hou.Node:
    """geo の中にハイトフィールドの地形を作り、ポリゴンに変換した最後のノードを返す。"""
    # 200 m × 200 m を 2 m 間隔で標本化する（100 × 100 の格子）。
    field = geo.createNode("heightfield", "heightfield")
    field.parm("sizex").set(200.0)
    field.parm("sizey").set(200.0)
    field.parm("gridspacing").set(2.0)

    noise = geo.createNode("heightfield_noise", "heightfield_noise")
    noise.setFirstInput(field)
    noise.parm("amp").set(150.0)
    noise.parm("elementsize").set(90.0)
    noise.parm("offsetx").setExpression('ch("../seed") * 17.31')

    # 水による侵食（第 7 章）。数フレーム分のシミュレーションを行う。
    erode = geo.createNode("heightfield_erode::3.0", "heightfield_erode")
    erode.setFirstInput(noise)
    erode.parm("freezeframe").set(20)  # 20 フレーム分の侵食を進めた状態で止める

    convert = geo.createNode("convertheightfield", "convert_to_polygons")
    convert.setFirstInput(erode)
    return convert


def build() -> hou.Node:
    """/obj/terrain を作り、ポリゴンの島の地形の出力ノードを返す。"""
    geo = recreate_geo("terrain")
    add_controls(geo, {"seed": 0})

    island_out = geo.createNode("null", "OUT_island")
    island_out.setFirstInput(add_island_terrain(geo))
    field_out = geo.createNode("null", "OUT_heightfield")
    field_out.setFirstInput(add_heightfield_terrain(geo))

    finish(geo, island_out)
    return island_out


def main() -> None:
    start = time.perf_counter()
    out = build()
    geo = out.parent()
    check_errors(geo)
    for name in ("OUT_island", "OUT_heightfield"):
        print(describe(geo.node(name)))
        # ほかのツールで確かめられるように OBJ 形式でも書き出す
        geo.node(name).geometry().saveToFile(out_path(f"terrain_{name[4:].lower()}.obj").as_posix())
    print(f"保存した: {save_hip('terrain')}（{time.perf_counter() - start:.1f} 秒）")


if __name__ == "__main__":
    main()
