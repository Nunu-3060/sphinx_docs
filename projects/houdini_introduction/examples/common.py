"""サンプルスクリプトで共通に使う関数。

Houdini の Python Shell や hython から使う。単独では実行しない。
"""

from __future__ import annotations

import sys
from pathlib import Path

import hou

# このファイルがあるディレクトリ（examples）。VEX のファイルを探すときに使う。
EXAMPLES_DIR = Path(__file__).resolve().parent


def read_vex(name: str) -> str:
    """examples/vex/ にある VEX のコードを読み込んで返す。"""
    return (EXAMPLES_DIR / "vex" / name).read_text(encoding="utf-8")


def recreate_node(parent_path: str, node_type: str, name: str) -> hou.Node:
    """parent_path の下に node_type のノードを name という名前で作る。

    同じ名前のノードが既にあれば削除してから作る。スクリプトを何度実行しても
    同じ結果になるようにするためである。
    """
    parent = hou.node(parent_path)
    old = parent.node(name)
    if old is not None:
        old.destroy()
    return parent.createNode(node_type, name)


def recreate_geo(name: str) -> hou.Node:
    """/obj の下に Geometry オブジェクトを作り直して返す。"""
    return recreate_node("/obj", "geo", name)


def finish(network: hou.Node, output: hou.Node) -> None:
    """output にディスプレイフラグとレンダーフラグを立て、ノードを整列する。"""
    output.setDisplayFlag(True)
    output.setRenderFlag(True)
    network.layoutChildren()


def check_errors(network: hou.Node) -> None:
    """network の直下の全ノードをクックし、エラーがあれば例外を投げる。"""
    for node in network.children():
        try:
            node.cook(force=True)
        except hou.OperationFailed:
            pass    # エラーの内容は node.errors() で調べる
        errors = node.errors()
        if errors:
            raise RuntimeError(f"{node.path()}: {errors}")


def save_hip_from_argv() -> None:
    """コマンドライン引数でファイル名が渡されていれば、シーンを保存する。

    hython で実行したときに使う。例: hython build_table.py table.hipnc
    """
    if len(sys.argv) > 1:
        hou.hipFile.save(sys.argv[1])
        print(f"保存した: {sys.argv[1]}")
