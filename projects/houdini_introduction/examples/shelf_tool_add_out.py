"""シェルフツールの例: 選択した SOP ノードの後ろに、出力用の Null ノードを追加する。

シェルフツールの Script タブに、このファイルの中身をそのまま貼り付けて使う。
貼り付けた場合は、最後の行で add_out_nulls() が実行される。
"""

from __future__ import annotations

import hou


def add_out_nulls() -> list[hou.Node]:
    """選択中の SOP ノードそれぞれの後ろに OUT という Null ノードを作り、表示する。"""
    created = []
    for node in hou.selectedNodes():
        if node.type().category() != hou.sopNodeTypeCategory():
            continue    # SOP 以外のノードは対象外
        null = node.parent().createNode("null", "OUT")   # 名前が重なると OUT1 などになる
        null.setFirstInput(node)
        null.moveToGoodPosition()
        null.setDisplayFlag(True)
        null.setRenderFlag(True)
        created.append(null)
    if not created:
        hou.ui.displayMessage("SOP ノードを選択してから実行する。")
    return created


add_out_nulls()
