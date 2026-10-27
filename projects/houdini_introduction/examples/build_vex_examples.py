r"""「VEX 入門」の例を作る。

/obj/vex_examples の中に、examples/vex/ の 4 つの VEX のコードを
それぞれ Attribute Wrangle に設定したネットワークを作る。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_vex_examples
    build_vex_examples.build()
"""

from __future__ import annotations

import hou

from common import check_errors, finish, read_vex, recreate_geo, save_hip_from_argv


def add_wrangle(geo: hou.Node, name: str, run_over: str, vex_file: str,
                parms: dict[str, float]) -> hou.Node:
    """VEX のコードとスペアパラメーターを設定した Attribute Wrangle を作る。

    parms には「パラメーター名: 初期値」を渡す。初期値が int なら整数の、
    float なら浮動小数点数のパラメーターを作る。
    """
    wrangle = geo.createNode("attribwrangle", name)
    wrangle.parm("class").set(run_over)
    wrangle.parm("snippet").set(read_vex(vex_file))
    for parm_name, value in parms.items():
        template: hou.ParmTemplate
        if isinstance(value, int):
            template = hou.IntParmTemplate(parm_name, parm_name, 1, default_value=(value,))
        else:
            template = hou.FloatParmTemplate(parm_name, parm_name, 1, default_value=(value,))
        wrangle.addSpareParmTuple(template)
    return wrangle


def build() -> hou.Node:
    """/obj/vex_examples に例のネットワークを作り、波の例の出力ノードを返す。"""
    geo = recreate_geo("vex_examples")

    # 例 1: 波打つグリッド。
    grid = geo.createNode("grid", "grid")
    grid.parm("rows").set(60)
    grid.parm("cols").set(60)
    wave = add_wrangle(geo, "wave", "point", "wave.vex", {"frequency": 2.0, "amplitude": 0.3})
    wave.setFirstInput(grid)
    wave_out = geo.createNode("null", "OUT_wave")
    wave_out.setFirstInput(wave)

    # 例 2: でこぼこの球。法線 N を持つ球を作るため、Normal SOP を通す。
    sphere = geo.createNode("sphere", "sphere")
    sphere.parm("type").set("polymesh")
    sphere.parm("rows").set(60)
    sphere.parm("cols").set(120)
    normal = geo.createNode("normal", "normal")
    normal.setFirstInput(sphere)
    normal.parm("type").set("typepoint")
    bumpy = add_wrangle(geo, "noise_displace", "point", "noise_displace.vex",
                        {"frequency": 3.0, "amplitude": 0.4})
    bumpy.setFirstInput(normal)
    bumpy_out = geo.createNode("null", "OUT_noise")
    bumpy_out.setFirstInput(bumpy)

    # 例 3: らせん。入力は無い。
    spiral = add_wrangle(geo, "spiral", "detail", "spiral.vex", {"count": 200, "turns": 5.0, "height": 3.0})
    spiral_out = geo.createNode("null", "OUT_spiral")
    spiral_out.setFirstInput(spiral)

    # 例 4: らせんに最も近い距離で、グリッドに色を付ける。
    nearest = add_wrangle(geo, "nearest_color", "point", "nearest_color.vex", {"max_distance": 2.0})
    nearest.setInput(0, grid)
    nearest.setInput(1, spiral)
    nearest_out = geo.createNode("null", "OUT_nearest")
    nearest_out.setFirstInput(nearest)

    finish(geo, wave_out)
    return wave_out


def main() -> None:
    out = build()
    check_errors(out.parent())
    for name in ("OUT_wave", "OUT_noise", "OUT_spiral", "OUT_nearest"):
        geometry = out.parent().node(name).geometry()
        print(f"{name}: ポイント {len(geometry.points())}, プリミティブ {len(geometry.prims())}, "
              f"範囲 {geometry.boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
