r"""「プロシージャルモデリングの実践」の階段を作る。

段数、1 段の高さ、奥行き、幅をパラメーターとして持つ Attribute Wrangle で
ポイントを作り、そのポイントに箱をコピーして階段にする。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_stairs
    build_stairs.build()
"""

from __future__ import annotations

import hou

from common import check_errors, finish, read_vex, recreate_geo, save_hip_from_argv


def add_float_parm(node: hou.Node, name: str, label: str, default: float) -> None:
    """node に浮動小数点数のスペアパラメーターを 1 個追加する。"""
    node.addSpareParmTuple(hou.FloatParmTemplate(name, label, 1, default_value=(default,)))


def add_int_parm(node: hou.Node, name: str, label: str, default: int) -> None:
    """node に整数のスペアパラメーターを 1 個追加する。"""
    node.addSpareParmTuple(hou.IntParmTemplate(name, label, 1, default_value=(default,), min=1, max=50))


def build() -> hou.Node:
    """/obj/stairs に階段のネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("stairs")

    # 段ごとのポイントを作る。入力は無く、Detail で 1 回だけ実行する。
    points = geo.createNode("attribwrangle", "step_points")
    points.parm("class").set("detail")
    points.parm("snippet").set(read_vex("stairs_points.vex"))
    add_int_parm(points, "step_count", "Step Count", 10)
    add_float_parm(points, "step_height", "Step Height", 0.18)
    add_float_parm(points, "step_depth", "Step Depth", 0.28)
    add_float_parm(points, "width", "Width", 1.0)

    # 1 辺 1 の箱を、各ポイントの scale に合わせて拡大しながらコピーする。
    box = geo.createNode("box", "unit_box")
    copy = geo.createNode("copytopoints::2.0", "copy_steps")
    copy.setInput(0, box)
    copy.setInput(1, points)

    out = geo.createNode("null", "OUT")
    out.setFirstInput(copy)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    print(f"バウンディングボックス: {out.geometry().boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
