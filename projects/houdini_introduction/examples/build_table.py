r"""「はじめてのモデリング」の机を、ノードを組み立てて作る。

Houdini の Python Shell で次のように実行する（パスは各自の環境に合わせる）。

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_table
    build_table.build()

hython からは ``hython build_table.py table.hipnc`` のように実行する。
"""

from __future__ import annotations

import hou

from common import check_errors, finish, recreate_geo, save_hip_from_argv

# 机の寸法（単位はメートル）。
TOP_SIZE = (1.2, 0.04, 0.7)   # 天板の幅、厚さ、奥行き
TABLE_HEIGHT = 0.72           # 床から天板の上面までの高さ
LEG_SIZE = 0.05               # 脚の断面（正方形）の一辺
LEG_INSET = 0.08              # 天板の端から脚の中心までの距離
HOLE_RADIUS = 0.03            # 配線用の穴の半径


def build() -> hou.Node:
    """/obj/table に机のネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("table")
    top_w, top_t, top_d = TOP_SIZE
    leg_h = TABLE_HEIGHT - top_t

    # 天板: 箱を作り、脚の上に載る高さまで持ち上げる。
    top = geo.createNode("box", "top")
    top.parmTuple("size").set(TOP_SIZE)
    lift = geo.createNode("xform", "lift_top")
    lift.setFirstInput(top)
    lift.parm("ty").set(leg_h + top_t / 2)

    # 天板の角を丸める。
    bevel = geo.createNode("polybevel::3.0", "bevel_top")
    bevel.setFirstInput(lift)
    bevel.parm("offset").set(0.005)

    # 配線用の穴: 円柱を天板の奥側に置き、天板から引く。
    hole = geo.createNode("tube", "hole")
    hole.parm("type").set("poly")
    hole.parm("cap").set(True)
    hole.parm("rad1").set(HOLE_RADIUS)
    hole.parm("rad2").set(HOLE_RADIUS)
    hole.parm("height").set(0.2)
    hole.parm("cols").set(24)
    hole.parmTuple("t").set((top_w / 2 - 0.15, leg_h, -(top_d / 2 - 0.1)))
    boolean = geo.createNode("boolean::2.0", "cut_hole")
    boolean.setInput(0, bevel)
    boolean.setInput(1, hole)
    boolean.parm("booleanop").set("subtract")

    # 脚: 底面が y = 0 に来るように中心を高さの半分だけ上げた箱。
    leg = geo.createNode("box", "leg")
    leg.parmTuple("size").set((LEG_SIZE, leg_h, LEG_SIZE))
    leg.parm("ty").set(leg_h / 2)

    # 脚を置く位置: 2 x 2 の点を持つグリッド（XZ 平面）。
    positions = geo.createNode("grid", "leg_positions")
    positions.parm("orient").set("zx")
    positions.parm("sizex").set(top_w - 2 * LEG_INSET)
    positions.parm("sizey").set(top_d - 2 * LEG_INSET)
    positions.parm("rows").set(2)
    positions.parm("cols").set(2)

    # 脚をグリッドの 4 つの点にコピーする。グリッドの面の向き（上向き）に
    # 脚の Z 軸が合わせられて脚が倒れないように、Use Implicit N を切る。
    copy = geo.createNode("copytopoints::2.0", "copy_legs")
    copy.setInput(0, leg)
    copy.setInput(1, positions)
    copy.parm("useimplicitn").set(False)

    # 天板と脚をまとめる。
    merge = geo.createNode("merge", "merge")
    merge.setInput(0, boolean)
    merge.setInput(1, copy)

    out = geo.createNode("null", "OUT")
    out.setFirstInput(merge)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    geometry = out.geometry()
    print(f"ポイント数: {len(geometry.points())}")
    print(f"プリミティブ数: {len(geometry.prims())}")
    print(f"バウンディングボックス: {geometry.boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
