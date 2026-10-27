r"""「シミュレーション入門」の例: 積んだ箱を球にぶつけて崩す剛体シミュレーション。

RBD Bullet Solver SOP を使う。DOP ネットワークを自分で組まなくても、
SOP の中だけで剛体シミュレーションができる。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_rbd
    build_rbd.build()

作った後、プレイバーで再生するとシミュレーションが進む。
"""

from __future__ import annotations

import hou

from common import check_errors, finish, recreate_geo, save_hip_from_argv

BOX_SIZE = 0.5       # 箱の一辺（メートル）
COLUMNS = 6          # 横に並べる箱の数
LAYERS = 6           # 積む段数


def build() -> hou.Node:
    """/obj/rbd に剛体シミュレーションのネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("rbd")

    # 箱を積む位置: 横 COLUMNS 個 x 縦 LAYERS 段の格子状のポイント（XY 平面）。
    positions = geo.createNode("grid", "wall_points")
    positions.parm("orient").set("xy")
    positions.parm("sizex").set(BOX_SIZE * (COLUMNS - 1))
    positions.parm("sizey").set(BOX_SIZE * (LAYERS - 1))
    positions.parm("rows").set(LAYERS)
    positions.parm("cols").set(COLUMNS)
    positions.parm("ty").set(BOX_SIZE * LAYERS / 2)

    # 箱をコピーして壁にする。箱は少しだけ小さくし、初期状態で重ならないようにする。
    box = geo.createNode("box", "brick")
    box.parmTuple("size").set((BOX_SIZE * 0.98,) * 3)
    wall = geo.createNode("copytopoints::2.0", "wall")
    wall.setInput(0, box)
    wall.setInput(1, positions)
    wall.parm("useimplicitn").set(False)

    # 壁に向かって飛んでいく球。初速度は v アトリビュートで与える。
    ball = geo.createNode("sphere", "ball")
    ball.parm("type").set("polymesh")
    ball.parmTuple("rad").set((0.6, 0.6, 0.6))
    ball.parmTuple("t").set((0.0, 1.2, 4.0))
    velocity = geo.createNode("attribwrangle", "ball_velocity")
    velocity.setFirstInput(ball)
    velocity.parm("class").set("point")
    velocity.parm("snippet").set("v@v = {0, 1, -12};   // 毎秒 12 m で -Z 方向へ")

    # 箱と球を 1 つにまとめる。RBD Bullet Solver は、つながった部分（ここでは
    # 箱 1 個、球 1 個）をそれぞれ 1 個の剛体として扱う。
    merge = geo.createNode("merge", "merge")
    merge.setInput(0, wall)
    merge.setInput(1, velocity)

    solver = geo.createNode("rbdbulletsolver", "rbd_solver")
    solver.setFirstInput(merge)
    solver.parm("useground").set(1)    # Ground Type: Ground Plane（y = 0 に地面を置く）

    out = geo.createNode("null", "OUT")
    out.setFirstInput(solver)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    # フレームを進めて、箱の重心の高さが変わることを確かめる。
    for frame in (1, 24, 48):
        hou.setFrame(frame)
        heights = [point.position()[1] for point in out.geometry().points()]
        print(f"フレーム {frame:2d}: ポイントの高さの平均 {sum(heights) / len(heights):.3f} m")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
