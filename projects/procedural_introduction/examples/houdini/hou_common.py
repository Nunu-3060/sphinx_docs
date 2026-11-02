"""第 16 章の Houdini のサンプルで共通に使う関数。

hython（または Houdini の Python Shell）から import して使う。単独では実行しない。
"""

from __future__ import annotations

from pathlib import Path

import hou

# このファイルがあるフォルダー（examples/houdini）
HOUDINI_DIR = Path(__file__).resolve().parent
# .hip や書き出したジオメトリの保存先（git の管理外）
OUT_DIR = HOUDINI_DIR / "out"


def read_vex(name: str) -> str:
    """examples/houdini/vex/ にある VEX のコードを読み込んで返す。"""
    return (HOUDINI_DIR / "vex" / name).read_text(encoding="utf-8")


def recreate_geo(name: str) -> hou.Node:
    """/obj の下に Geometry オブジェクトを作り直して返す。

    同じ名前のノードが既にあれば削除してから作る。スクリプトを何度実行しても
    同じネットワークになるようにするためである。
    """
    obj = hou.node("/obj")
    old = obj.node(name)
    if old is not None:
        old.destroy()
    return obj.createNode("geo", name)


def add_controls(node: hou.Node, values: dict[str, int | float]) -> None:
    """node に「つまみ」となるスペアパラメーターを追加する。

    values には「パラメーター名: 初期値」を渡す。初期値が int なら整数の、
    float なら浮動小数点数のパラメーターを作る。ネットワークの中のノードは、
    ch("../名前") という式でこの値を参照する。
    """
    for name, value in values.items():
        template: hou.ParmTemplate
        if isinstance(value, int):
            template = hou.IntParmTemplate(name, name, 1, default_value=(value,))
        else:
            template = hou.FloatParmTemplate(name, name, 1, default_value=(value,))
        node.addSpareParmTuple(template)


def add_wrangle(geo: hou.Node, name: str, vex_file: str, parms: dict[str, int | float | str]) -> hou.Node:
    """vex_file の VEX のコードを設定した、ポイントを処理する Attribute Wrangle を作る。

    コードの中の chf() や chi() が参照するパラメーターは、スクリプトから作るときには
    自動で作られないので、parms から作る（Houdini の画面では、コード欄の右のボタンで作れる）。
    parms の値が int なら整数、float なら実数のパラメーターになる。str なら実数の
    パラメーターを作り、その文字列を式（エクスプレッション）として設定する。
    """
    wrangle = geo.createNode("attribwrangle", name)
    wrangle.parm("class").set("point")
    wrangle.parm("snippet").set(read_vex(vex_file))
    for parm_name, value in parms.items():
        template: hou.ParmTemplate
        if isinstance(value, int):
            template = hou.IntParmTemplate(parm_name, parm_name, 1, default_value=(value,))
        else:
            template = hou.FloatParmTemplate(parm_name, parm_name, 1)
        wrangle.addSpareParmTuple(template)
        if isinstance(value, str):
            wrangle.parm(parm_name).setExpression(value)
        else:
            wrangle.parm(parm_name).set(value)
    return wrangle


def finish(geo: hou.Node, output: hou.Node) -> None:
    """output にディスプレイフラグとレンダーフラグを立て、ノードを整列する。"""
    output.setDisplayFlag(True)
    output.setRenderFlag(True)
    geo.layoutChildren()


def check_errors(geo: hou.Node) -> None:
    """geo の直下の全ノードをクックし、エラーがあれば例外を投げる。"""
    for node in geo.children():
        try:
            node.cook(force=True)
        except hou.OperationFailed:
            pass  # エラーの内容は node.errors() で調べる
        errors = node.errors()
        if errors:
            raise RuntimeError(f"{node.path()}: {errors}")


def describe(node: hou.Node) -> str:
    """ノードの出力ジオメトリのポイント数・プリミティブ数・範囲を 1 行の文字列にする。"""
    geometry = node.geometry()
    box = geometry.boundingBox()
    size = box.sizevec()
    return (f"{node.name()}: ポイント {len(geometry.points())}, プリミティブ {len(geometry.prims())}, "
            f"大きさ {size[0]:.2f} × {size[1]:.2f} × {size[2]:.2f}")


def out_path(name: str) -> Path:
    """examples/houdini/out/<name> のパスを返す。フォルダーが無ければ作る。"""
    path = OUT_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_hip(name: str) -> Path:
    """現在のシーンを examples/houdini/out/<name>.hip に保存して、そのパスを返す。"""
    path = out_path(f"{name}.hip")
    hou.hipFile.save(path.as_posix())
    return path
