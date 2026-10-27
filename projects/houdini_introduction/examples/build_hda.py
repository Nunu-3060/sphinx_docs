r"""「デジタルアセット」の例: 階段のネットワークを HDA にする。

1. サブネットワークの中に階段のネットワークを作る。
2. サブネットワークを HDA に変換し、.hdanc ファイルに保存する。
3. HDA のパラメーターインターフェースに Step Count などを追加し、
   中のノードのパラメーターから ch() で参照する。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_hda
    build_hda.build()

hython からは ``hython build_hda.py stairs.hipnc`` のように実行する。
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import hou

from common import check_errors, read_vex, recreate_geo, save_hip_from_argv

# HDA のノードタイプ名。「名前空間::名前::バージョン」の形にする。
ASSET_NAME = "intro::stairs::1.0"
ASSET_LABEL = "Intro Stairs"
# HDA を保存するファイル。$HOUDINI_USER_PREF_DIR/otls の HDA は起動時に読み込まれる。
DEFAULT_HDA_PATH = "$HOUDINI_USER_PREF_DIR/otls/intro_stairs.hdanc"

# HDA のパラメーター: (名前, ラベル, 初期値)。
PARMS: list[tuple[str, str, float]] = [
    ("step_count", "Step Count", 10),
    ("step_height", "Step Height", 0.18),
    ("step_depth", "Step Depth", 0.28),
    ("width", "Width", 1.0),
]


def build_contents(subnet: hou.Node) -> None:
    """サブネットワークの中に階段のネットワークを作る（build_stairs.py と同じ構成）。"""
    points = subnet.createNode("attribwrangle", "step_points")
    points.parm("class").set("detail")
    points.parm("snippet").set(read_vex("stairs_points.vex"))

    box = subnet.createNode("box", "unit_box")
    copy = subnet.createNode("copytopoints::2.0", "copy_steps")
    copy.setInput(0, box)
    copy.setInput(1, points)

    output = subnet.createNode("output", "output0")
    output.setFirstInput(copy)
    subnet.layoutChildren()


def setup_interface(asset: hou.Node) -> None:
    """HDA にパラメーターを追加し、中の Wrangle から参照させる。"""
    definition = asset.type().definition()
    group = definition.parmTemplateGroup()
    for name, label, default in PARMS:
        template: hou.ParmTemplate
        if isinstance(default, int):
            template = hou.IntParmTemplate(name, label, 1, default_value=(default,), min=1, max=50)
        else:
            template = hou.FloatParmTemplate(name, label, 1, default_value=(default,))
        group.append(template)
    definition.setParmTemplateGroup(group)

    # VEX の chi("step_count") などは Wrangle 自身のパラメーターを読む。そこで
    # Wrangle にも同じ名前のパラメーターを作り、Hscript の ch() で HDA の値を参照させる。
    wrangle = asset.node("step_points")
    for name, label, default in PARMS:
        template = group.find(name)
        wrangle.addSpareParmTuple(template)
        wrangle.parm(name).setExpression(f'ch("../{name}")')
    definition.updateFromNode(asset)


def build(hda_path: str = DEFAULT_HDA_PATH) -> hou.Node:
    """/obj/hda_demo に階段の HDA を作り、そのノードを返す。"""
    geo = recreate_geo("hda_demo")
    subnet = geo.createNode("subnet", "stairs")
    build_contents(subnet)

    file_path = hou.text.expandString(hda_path)
    asset = subnet.createDigitalAsset(
        name=ASSET_NAME,
        hda_file_name=file_path,
        description=ASSET_LABEL,
        min_num_inputs=0,
        max_num_inputs=0,
    )
    setup_interface(asset)
    asset.setDisplayFlag(True)
    asset.setRenderFlag(True)
    print(f"HDA を保存した: {file_path}")
    return asset


def main() -> None:
    # hython で試すときは、HDA を一時ディレクトリに保存する。
    hda_path = str(Path(tempfile.gettempdir()) / "intro_stairs.hdanc")
    asset = build(hda_path)
    check_errors(asset.parent())
    asset.parm("step_count").set(5)
    print(f"5 段にしたときの範囲: {asset.geometry().boundingBox()}")

    # 2 個目のインスタンスを作り、別の値を設定できることを確かめる。
    second = asset.parent().createNode(ASSET_NAME, "stairs_wide")
    second.parm("width").set(3.0)
    print(f"2 個目（幅 3 m）の範囲: {second.geometry().boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
