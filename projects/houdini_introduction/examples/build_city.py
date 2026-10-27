r"""「プロシージャルモデリングの実践」の建物群を作る。

グリッドの各マスを区画とし、区画ごとに乱数で決めた高さまで押し出して
建物にする。区画ごとの押し出しには For-Each ループを使う。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_city
    build_city.build()
"""

from __future__ import annotations

import hou

from common import check_errors, finish, read_vex, recreate_geo, save_hip_from_argv

# ループの中で、処理中の区画（プリミティブ 0 番）の height アトリビュートを読む式。
HEIGHT_EXPR = 'prim(opinputpath(".", 0), 0, "height", 0)'
FLOOR_HEIGHT = 3.0   # 1 フロアの高さ（メートル）
MAX_HEIGHT = 60.0    # 建物の高さの上限（メートル）


def add_float_parm(node: hou.Node, name: str, label: str, default: float) -> None:
    """node に浮動小数点数のスペアパラメーターを 1 個追加する。"""
    node.addSpareParmTuple(hou.FloatParmTemplate(name, label, 1, default_value=(default,)))


def build() -> hou.Node:
    """/obj/city に建物群のネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("city")

    # 地面: 100 m 四方を 10 x 10 のマスに分けたグリッド。
    ground = geo.createNode("grid", "ground")
    ground.parmTuple("size").set((100.0, 100.0))
    ground.parm("rows").set(11)
    ground.parm("cols").set(11)

    # 区画: 各マスを内側に縮め、マスごとに独立した面にする。
    lots = geo.createNode("polyextrude::2.0", "make_lots")
    lots.setFirstInput(ground)
    lots.parm("splittype").set("elements")
    lots.parm("inset").set(1.5)
    lots.parm("outputside").set(False)

    # 区画ごとに高さを決め、一部を空き地にする。
    attrs = geo.createNode("attribwrangle", "lot_attributes")
    attrs.setFirstInput(lots)
    attrs.parm("class").set("primitive")
    attrs.parm("snippet").set(read_vex("lot_attributes.vex"))
    add_float_parm(attrs, "seed", "Seed", 0.0)
    add_float_parm(attrs, "empty_ratio", "Empty Ratio", 0.2)
    add_float_parm(attrs, "min_height", "Min Height", 6.0)
    add_float_parm(attrs, "max_height", "Max Height", MAX_HEIGHT)

    # For-Each ループ: 区画（プリミティブ）を 1 個ずつ取り出して押し出す。
    begin = geo.createNode("block_begin", "foreach_begin")
    end = geo.createNode("block_end", "foreach_end")
    begin.setFirstInput(attrs)
    begin.parm("method").set("piece")
    begin.parm("blockpath").set("../foreach_end")
    end.parm("itermethod").set("pieces")
    end.parm("method").set("merge")
    end.parm("class").set("primitive")
    end.parm("useattrib").set(False)
    end.parm("blockpath").set("../foreach_begin")
    end.parm("templatepath").set("../foreach_begin")

    extrude = geo.createNode("polyextrude::2.0", "extrude_building")
    extrude.setFirstInput(begin)
    extrude.parm("dist").setExpression(HEIGHT_EXPR)
    extrude.parm("divs").setExpression(f"max(1, floor({HEIGHT_EXPR} / {FLOOR_HEIGHT}))")
    end.setFirstInput(extrude)

    # 高さに応じて色を付ける。
    color = geo.createNode("attribwrangle", "building_color")
    color.setFirstInput(end)
    color.parm("class").set("point")
    color.parm("snippet").set(read_vex("building_color.vex"))
    add_float_parm(color, "max_height", "Max Height", MAX_HEIGHT)

    # 地面と建物をまとめる。
    merge = geo.createNode("merge", "merge")
    merge.setInput(0, ground)
    merge.setInput(1, color)

    out = geo.createNode("null", "OUT")
    out.setFirstInput(merge)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    geometry = out.geometry()
    print(f"プリミティブ数: {len(geometry.prims())}")
    print(f"バウンディングボックス: {geometry.boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
