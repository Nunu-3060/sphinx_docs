r"""第 16 章: 島の地形に木を散布するネットワーク（/obj/scatter）を組む。

第 10 章の「マスクに従った散布」と「インスタンスの大きさ・向きのばらつき」を、
Houdini のノードで組んだ例である。

    島の地形 → Attribute Wrangle（density を計算）→ Scatter（density に比例して散布、緩和）
    → Attribute Wrangle（pscale と orient を決める）→ Copy to Points（木を複製）

Geometry オブジェクト /obj/scatter には、全体を操作する「つまみ」として
seed・tree_count・max_slope の 3 つのパラメーターを付ける。

hython での実行例（examples/houdini で）:

    hython build_scatter.py
"""

from __future__ import annotations

import hou

from build_lsystem import add_tree
from build_terrain import add_island_terrain
from hou_common import add_controls, add_wrangle, check_errors, describe, finish, recreate_geo, save_hip


def add_cone_tree(geo: hou.Node) -> hou.Node:
    """円錐の葉と円柱の幹からなる、簡易な木（高さ 1）を作って返す。"""
    leaves = geo.createNode("tube", "leaves")
    leaves.parm("type").set("poly")
    leaves.parm("cap").set(True)
    leaves.parm("rad1").set(0.0)  # 上端の半径を 0 にして円錐にする
    leaves.parm("rad2").set(0.3)
    leaves.parm("height").set(0.8)
    leaves.parm("ty").set(0.6)
    trunk = geo.createNode("tube", "trunk")
    trunk.parm("type").set("poly")
    trunk.parm("cap").set(True)
    trunk.parm("rad1").set(0.05)
    trunk.parm("rad2").set(0.05)
    trunk.parm("height").set(0.2)
    trunk.parm("ty").set(0.1)
    merge = geo.createNode("merge", "cone_tree")
    for index, (part, rgb) in enumerate(((leaves, (0.20, 0.45, 0.20)), (trunk, (0.45, 0.32, 0.20)))):
        color = geo.createNode("color", f"{part.name()}_color")
        color.parmTuple("color").set(rgb)
        color.setFirstInput(part)
        merge.setInput(index, color)
    return merge


def build() -> hou.Node:
    """/obj/scatter を作り、地形と木をまとめた出力ノードを返す。"""
    geo = recreate_geo("scatter")
    add_controls(geo, {"seed": 0, "tree_count": 400, "max_slope": 35.0})

    terrain = add_island_terrain(geo)

    # 斜面の傾きと高さから、木の生えやすさ density を計算する。
    density = add_wrangle(geo, "slope_density", "slope_density.vex",
                          {"max_slope": 'ch("../max_slope")', "min_height": 0.1, "max_height": 2.8,
                           "sea_level": 0.0})
    density.setFirstInput(terrain)

    # density に比例する密度で tree_count 個の点を散布し、緩和で間隔をそろえる（第 10 章）。
    scatter = geo.createNode("scatter::2.0", "scatter")
    scatter.setFirstInput(density)
    scatter.parm("usedensityattrib").set(True)
    scatter.parm("densityattrib").set("density")
    scatter.parm("forcetotal").set(True)
    scatter.parm("npts").setExpression('ch("../tree_count")')
    scatter.parm("seed").setExpression('ch("../seed")')
    scatter.parm("relaxpoints").set(True)
    scatter.parm("relaxiterations").set(10)

    # 1 本ずつの大きさと向きを決める。
    instance = add_wrangle(geo, "instance_attribs", "instance_attribs.vex",
                           {"seed": 'ch("../seed")', "min_scale": 0.35, "max_scale": 0.7, "max_tilt": 8.0})
    instance.setFirstInput(scatter)

    # 複製する木: 0 = 円錐の簡易な木、1 = L-system の木。Switch を切り替えるだけで差し替えられる。
    switch = geo.createNode("switch", "tree_shape")
    switch.setInput(0, add_cone_tree(geo))
    lsystem_tree = add_tree(geo, "lsystem_tree")
    lsystem_tree.parm("stepinit").set(0.12)  # 円錐の木と同じくらいの高さにする
    switch.setInput(1, lsystem_tree)
    switch.parm("input").set(0)

    copy = geo.createNode("copytopoints::2.0", "copy_to_points")
    copy.setInput(0, switch)  # 入力 0: 複製するもの
    copy.setInput(1, instance)  # 入力 1: 複製先のポイント（pscale・orient を持つ）
    trees_out = geo.createNode("null", "OUT_trees")
    trees_out.setFirstInput(copy)

    terrain_out = geo.createNode("null", "OUT_terrain")
    terrain_out.setFirstInput(density)
    points_out = geo.createNode("null", "OUT_points")
    points_out.setFirstInput(instance)

    merge = geo.createNode("merge", "merge")
    merge.setInput(0, terrain_out)
    merge.setInput(1, trees_out)
    out = geo.createNode("null", "OUT_scene")
    out.setFirstInput(merge)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    geo = out.parent()
    check_errors(geo)
    for name in ("OUT_terrain", "OUT_points", "OUT_trees", "OUT_scene"):
        print(describe(geo.node(name)))
    points = geo.node("OUT_points").geometry()
    scales = points.pointFloatAttribValues("pscale")
    print(f"pscale の範囲: {min(scales):.3f}〜{max(scales):.3f}")
    print(f"保存した: {save_hip('scatter')}")


if __name__ == "__main__":
    main()
