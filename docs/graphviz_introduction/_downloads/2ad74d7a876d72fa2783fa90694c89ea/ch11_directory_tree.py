"""11 章：フォルダーの構成をツリー図にするサンプル.

指定したフォルダーの中のフォルダーとファイルを再帰的にたどり、親から子への
エッジを持つ有向グラフにする。フォルダーはコマンドライン引数で指定する。
指定しない場合は、このファイルがあるフォルダーを対象にする。

使い方::

    python ch11_directory_tree.py [フォルダー]

出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

import sys
from pathlib import Path

import graphviz

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"

# ツリーに含めないフォルダーの名前
IGNORED = {"__pycache__", "output", ".git", ".mypy_cache"}


def add_entries(graph: graphviz.Digraph, folder: Path, root: Path) -> None:
    """フォルダーの中身をノードとして追加し、親から子へのエッジを引く.

    ノードの ID には root からの相対パスを使う。ファイル名だけを ID にすると、
    別のフォルダーにある同じ名前のファイルが 1 つのノードにまとめられてしまう。
    """
    parent_id = folder.relative_to(root).as_posix()
    entries = sorted(folder.iterdir(),
                     key=lambda path: (path.is_file(), path.name))
    for entry in entries:
        if entry.name in IGNORED:
            continue
        entry_id = entry.relative_to(root).as_posix()
        if entry.is_dir():
            graph.node(entry_id, entry.name + "/", shape="folder",
                       style="filled", fillcolor="lightyellow")
            add_entries(graph, entry, root)
        else:
            graph.node(entry_id, entry.name, shape="note")
        graph.edge(parent_id, entry_id)


def build_graph(root: Path = HERE) -> graphviz.Digraph:
    """フォルダーの構成を表す有向グラフを返す."""
    graph = graphviz.Digraph("directory_tree")
    graph.attr(rankdir="LR", nodesep="0.1")
    graph.attr("node", fontsize="10", height="0.3")
    graph.attr("edge", arrowhead="none")

    # root 自身の相対パスは "." になる
    graph.node(".", root.name + "/", shape="folder", style="filled",
               fillcolor="lightblue")
    add_entries(graph, root, root)
    return graph


def main() -> int:
    """ツリー図を SVG ファイルに出力し、終了コードを返す."""
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
    if not root.is_dir():
        print(f"{root} はフォルダーではありません。", file=sys.stderr)
        return 1

    graph = build_graph(root.resolve())
    path = graph.render(outfile=OUTPUT_DIR / "ch11_directory_tree.svg")
    print(f"{path} を出力しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
