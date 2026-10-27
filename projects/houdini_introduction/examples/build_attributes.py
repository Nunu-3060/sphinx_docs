r"""「ジオメトリとアトリビュート」の例を作る。

グリッドをノイズで起伏させて地形にし、法線（N）、高さ（height）、高さに応じた
色（Cd）、ランダムな大きさ（pscale）、高い所のポイントのグループ（peak）を付ける。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_attributes
    build_attributes.build()
"""

from __future__ import annotations

import hou

from common import check_errors, finish, recreate_geo, save_hip_from_argv


def build() -> hou.Node:
    """/obj/terrain にアトリビュートの例のネットワークを作り、出力の Null ノードを返す。"""
    geo = recreate_geo("terrain")

    grid = geo.createNode("grid", "grid")
    grid.parm("rows").set(50)
    grid.parm("cols").set(50)

    # ポイントごとの法線（N）を付ける。平らなグリッドなので全て真上を向く。
    normal = geo.createNode("normal", "normal")
    normal.setFirstInput(grid)
    normal.parm("type").set("typepoint")

    # 位置（P）にノイズを加える。Noise Along Vector をオンにすると、
    # ノイズは法線（N）の方向、つまり真上にだけ加わる。
    noise = geo.createNode("attribnoise::2.0", "bumps")
    noise.setFirstInput(normal)
    noise.parm("attribtype").set("vec")
    noise.parm("attribs").set("P")
    noise.parm("displace").set(True)
    noise.parm("displaceattrib").set("N")
    noise.parm("amplitude").set(1.5)
    noise.parm("elementsize").set(3.0)

    # 起伏を付けた後の法線を計算し直す。
    renormal = geo.createNode("normal", "recompute_normal")
    renormal.setFirstInput(noise)
    renormal.parm("type").set("typepoint")

    # 各ポイントの高さ（P の y 成分）を height アトリビュートにコピーする。
    # $TY は「処理中のポイントの y 座標」を表すローカル変数である。
    height = geo.createNode("attribcreate::2.0", "height")
    height.setFirstInput(renormal)
    height.parm("name1").set("height")
    height.parm("value1v1").setExpression("$TY")

    # height の値に応じて色（Cd）を付ける。低い所は緑、高い所は白にする。
    color = geo.createNode("color", "color_by_height")
    color.setFirstInput(height)
    color.parm("colortype").set("3")       # Ramp from Attribute
    color.parm("rampattribute").set("height")
    color.parm("ramprange1").set(0.0)
    color.parm("ramprange2").set(1.5)
    color.parm("ramp").set(hou.Ramp(
        (hou.rampBasis.Linear, hou.rampBasis.Linear),
        (0.0, 1.0),
        ((0.15, 0.35, 0.1), (0.95, 0.95, 0.95)),
    ))

    # ポイントごとにランダムな大きさ（pscale）を付ける。
    randomize = geo.createNode("attribrandomize", "random_pscale")
    randomize.setFirstInput(color)
    randomize.parm("name").set("pscale")
    randomize.parm("dimensions").set(1)
    randomize.parm("minx").set(0.05)
    randomize.parm("maxx").set(0.15)

    # height が 1 以上のポイントを peak グループに入れる。
    group = geo.createNode("groupexpression", "peak_group")
    group.setFirstInput(randomize)
    group.parm("grouptype").set("point")
    group.parm("groupname1").set("peak")
    group.parm("snippet1").set("@height >= 1.0")

    out = geo.createNode("null", "OUT")
    out.setFirstInput(group)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    geometry = out.geometry()
    print("ポイントアトリビュート:", [a.name() for a in geometry.pointAttribs()])
    print("ポイントグループ:", [g.name() for g in geometry.pointGroups()])
    print(f"peak グループのポイント数: {len(geometry.findPointGroup('peak').points())}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
