r"""「パラメーターとエクスプレッション」の例を作る。

- 床の大きさを、ボールの半径から ch() で計算する。
- ボールの高さを、フレーム番号 $F を使ったエクスプレッションで弾ませる。
- ボール全体を、キーフレームで 1 回転させる。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_expressions
    build_expressions.build()
"""

from __future__ import annotations

import hou

from common import check_errors, finish, recreate_geo, save_hip_from_argv


def build() -> hou.Node:
    """/obj/expressions に例のネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("expressions")

    ball = geo.createNode("sphere", "ball")
    ball.parm("type").set("polymesh")
    ball.parmTuple("rad").set((0.5, 0.5, 0.5))

    # 高さ: |sin($F * 6)| は 30 フレームごとに 0 に戻る（Hscript の sin は度で計算する）。
    bounce = geo.createNode("xform", "bounce")
    bounce.setFirstInput(ball)
    bounce.parm("ty").setExpression('ch("../ball/radx") + abs(sin($F * 6)) * 2')

    # 床: 一辺をボールの半径の 8 倍にする。
    floor = geo.createNode("grid", "floor")
    floor.parm("sizex").setExpression('ch("../ball/radx") * 8')
    floor.parm("sizey").setExpression('ch("sizex")')

    merge = geo.createNode("merge", "merge")
    merge.setInput(0, bounce)
    merge.setInput(1, floor)

    # 回転: 1 フレーム目に 0 度、120 フレーム目に 360 度のキーフレームを打つ。
    spin = geo.createNode("xform", "spin")
    spin.setFirstInput(merge)
    spin.parm("tx").set(1.0)
    for frame, angle in ((1, 0.0), (120, 360.0)):
        key = hou.Keyframe()
        key.setFrame(frame)
        key.setValue(angle)
        key.setExpression("linear()")
        spin.parm("ry").setKeyframe(key)

    out = geo.createNode("null", "OUT")
    out.setFirstInput(spin)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    bounce = hou.node("/obj/expressions/bounce")
    spin = hou.node("/obj/expressions/spin")
    for frame in (1, 15, 30, 60, 120):
        hou.setFrame(frame)
        print(f"フレーム {frame:3d}: 高さ {bounce.parm('ty').eval():.3f}, 回転 {spin.parm('ry').eval():.1f} 度")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
