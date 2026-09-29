"""3 章：最初のグラフを Python から出力するサンプル.

ch03_hello.dot と同じグラフを graphviz パッケージで組み立て、SVG に出力する。
出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def build_graph() -> graphviz.Digraph:
    """Hello から World へのエッジを持つ有向グラフを返す."""
    graph = graphviz.Digraph("hello")
    graph.edge("Hello", "World")
    return graph


def main() -> None:
    """グラフを SVG ファイルに出力する."""
    graph = build_graph()
    path = graph.render(outfile=OUTPUT_DIR / "ch03_first_graph.svg")
    print(f"{path} を出力しました。")


if __name__ == "__main__":
    main()
