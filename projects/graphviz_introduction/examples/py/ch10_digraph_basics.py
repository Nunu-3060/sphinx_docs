"""10 章：graphviz パッケージの基本的な使い方のサンプル.

注文処理の流れを表す有向グラフを組み立て、DOT の文字列を表示してから
SVG に出力する。出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# 日本語を含むフォント。macOS では "Hiragino Sans" などに変更する。
FONT = "Meiryo"


def build_graph() -> graphviz.Digraph:
    """注文処理の流れを表す有向グラフを返す."""
    # グラフ全体、ノード、エッジの既定の属性は、辞書で指定する
    graph = graphviz.Digraph(
        "order_flow",
        graph_attr={"rankdir": "LR", "fontname": FONT},
        node_attr={"shape": "box", "style": "rounded", "fontname": FONT},
        edge_attr={"fontname": FONT, "fontsize": "10"},
    )

    # node(ID, ラベル) でノードを追加する。属性はキーワード引数で指定する
    graph.node("order", "注文を受け付ける")
    graph.node("stock", "在庫を確認する")
    graph.node("ship", "発送する")
    graph.node("wait", "入荷を待つ", style="rounded,dashed")

    # edge(始点の ID, 終点の ID) でエッジを追加する
    graph.edge("order", "stock")
    graph.edge("stock", "ship", label="在庫あり")
    graph.edge("stock", "wait", label="在庫なし")

    # edges() は、属性を付けない複数のエッジをまとめて追加する
    graph.edges([("wait", "stock")])
    return graph


def main() -> None:
    """DOT の文字列を表示し、グラフを SVG ファイルに出力する."""
    graph = build_graph()
    print(graph.source)
    path = graph.render(outfile=OUTPUT_DIR / "ch10_digraph_basics.svg")
    print(f"{path} を出力しました。")


if __name__ == "__main__":
    main()
