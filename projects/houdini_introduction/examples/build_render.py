r"""「マテリアルとレンダリング」の例: 机を Solaris に読み込み、Karma でレンダリングする。

/stage に次の LOP ネットワークを作る。

    SOP Import（机） ─┐
    SOP Create（床） ─┴ Merge → Material Library → Camera → Dome Light
        → Distant Light → Karma Render Settings → USD Render ROP

Python Shell での実行例（build_table.py で机を作ってから実行する）:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_table, build_render
    build_table.build()
    rop = build_render.build()
    rop.render()    # $HIP/render/table.jpg に画像を書き出す
"""

from __future__ import annotations

import hou

from common import check_errors, recreate_node, save_hip_from_argv

TABLE_SOP = "/obj/table/OUT"


def add_material(library: hou.Node, name: str, color: tuple[float, float, float],
                 roughness: float, geometry: str) -> None:
    """Material Library の中に MtlX Standard Surface を作り、geometry に割り当てる。"""
    shader = library.createNode("mtlxstandard_surface", name)
    shader.parmTuple("base_color").set(color)
    shader.parm("specular_roughness").set(roughness)

    # Material Library の「Materials」マルチパラメーターに 1 行追加する。
    index = library.parm("materials").eval() + 1
    library.parm("materials").set(index)
    library.parm(f"matnode{index}").set(name)
    library.parm(f"matpath{index}").set(f"/materials/{name}")
    library.parm(f"assign{index}").set(True)
    library.parm(f"geopath{index}").set(geometry)


def build(output_image: str = "$HIP/render/table.jpg") -> hou.Node:
    """/stage にレンダリング用の LOP ネットワークを作り、USD Render ROP を返す。"""
    stage = hou.node("/stage")
    for child in stage.children():
        child.destroy()

    # 机: SOP のジオメトリを USD のプリミティブ /table として読み込む。
    table = recreate_node("/stage", "sopimport", "table")
    table.parm("soppath").set(TABLE_SOP)
    table.parm("primpath").set("/table")

    # 床: SOP Create の中で Grid を作る。
    floor = recreate_node("/stage", "sopcreate", "floor")
    floor.parm("primpath").set("/floor")
    grid = floor.node("sopnet/create").createNode("grid", "grid")
    grid.parmTuple("size").set((6.0, 6.0))
    grid.setDisplayFlag(True)

    merge = stage.createNode("merge", "merge")
    merge.setInput(0, table)
    merge.setInput(1, floor)

    # マテリアル: 机は木の色、床は灰色にする。
    library = stage.createNode("materiallibrary", "materials")
    library.setFirstInput(merge)
    library.parm("materials").set(0)
    add_material(library, "wood", (0.45, 0.28, 0.15), 0.4, "/table")
    add_material(library, "floor_mat", (0.6, 0.6, 0.6), 0.8, "/floor")

    # カメラ: 斜め上から机の中心を見る。
    camera = stage.createNode("camera", "camera")
    camera.setFirstInput(library)
    camera.parm("primpath").set("/cameras/camera")
    camera.parmTuple("t").set((3.2, 2.4, 3.8))
    camera.parm("lookatenable").set(True)
    camera.parmTuple("lookatposition").set((0.0, 0.4, 0.0))

    # ライト: 全体を照らすドームライトと、影を作る平行光源。
    dome = stage.createNode("domelight::3.0", "dome_light")
    dome.setFirstInput(camera)
    dome.parm("xn__inputsintensity_i0a").set(0.6)
    sun = stage.createNode("distantlight::2.0", "sun")
    sun.setFirstInput(dome)
    sun.parmTuple("r").set((-50.0, 30.0, 0.0))
    sun.parm("xn__inputsintensity_i0a").set(2.0)

    # レンダリングの設定: 横 1280 ピクセルにする。縦はカメラの縦横比（16:9）から
    # 自動で決まり 720 になる。Apprentice の上限（1920 x 1080）以内である。
    settings = stage.createNode("karmarendersettings", "render_settings")
    settings.setFirstInput(sun)
    settings.parm("camera").set("/cameras/camera")
    settings.parm("resolutionx").set(1280)
    settings.parm("picture").set(output_image)
    settings.parm("pathtracedsamples").set(32)

    rop = stage.createNode("usdrender_rop", "render")
    rop.setFirstInput(settings)
    settings.setDisplayFlag(True)   # ビューポートにはこのノードまでの結果を表示する
    stage.layoutChildren()
    return rop


def main() -> None:
    import build_table

    build_table.build()
    rop = build()
    check_errors(hou.node("/stage"))
    stage = rop.inputs()[0].stage()
    print("USD のプリミティブ:", [str(p.GetPath()) for p in stage.Traverse()])
    save_hip_from_argv()


if __name__ == "__main__":
    main()
