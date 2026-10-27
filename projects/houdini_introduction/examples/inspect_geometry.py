r"""ノードの出力ジオメトリの中身を表示する。

「Python による操作」で使う。Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import inspect_geometry
    inspect_geometry.describe("/obj/table/OUT")
"""

from __future__ import annotations

import hou


def describe(node_path: str, max_points: int = 5) -> None:
    """node_path のノードが出力するジオメトリの要素数、アトリビュート、先頭のポイントを表示する。"""
    node = hou.node(node_path)
    if node is None:
        raise ValueError(f"ノードが見つからない: {node_path}")
    geo = node.geometry()

    print(f"== {node.path()} ({node.type().name()}) ==")
    print(f"ポイント: {len(geo.points())}, プリミティブ: {len(geo.prims())}, "
          f"バーテックス: {geo.intrinsicValue('vertexcount')}")

    # アトリビュートを、所属する階層（クラス）ごとに表示する。
    for label, attribs in (("ポイント", geo.pointAttribs()),
                           ("バーテックス", geo.vertexAttribs()),
                           ("プリミティブ", geo.primAttribs()),
                           ("ディテール", geo.globalAttribs())):
        names = ", ".join(f"{a.name()}({a.dataType().name()}x{a.size()})" for a in attribs)
        print(f"{label}アトリビュート: {names or 'なし'}")

    # 先頭のポイントの位置を表示する。
    for point in geo.points()[:max_points]:
        x, y, z = point.position()
        print(f"  ポイント {point.number()}: P = ({x:.3f}, {y:.3f}, {z:.3f})")


def main() -> None:
    import build_table
    build_table.build()
    describe("/obj/table/OUT")


if __name__ == "__main__":
    main()
