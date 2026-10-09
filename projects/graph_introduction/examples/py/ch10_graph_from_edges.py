"""エッジのリストからグラフを組み立てる.

Python のデータ（エッジのリスト）から graphviz パッケージで有向グラフを
作り、DOT のソースを表示する。グラフの画像を作るには Graphviz の dot
コマンドが必要である。

使い方: python ch10_graph_from_edges.py
"""

import graphviz

# 6 つのマイクロサービスの呼び出し関係（呼び出し元, 呼び出し先）
EDGES = [
    ("gateway", "auth"),
    ("gateway", "order"),
    ("gateway", "catalog"),
    ("order", "payment"),
    ("order", "catalog"),
    ("order", "notify"),
    ("payment", "notify"),
]


def nodes() -> list[str]:
    """エッジに現れるノードを、現れた順に重複なく返す."""
    result: list[str] = []
    for source, target in EDGES:
        for name in (source, target):
            if name not in result:
                result.append(name)
    return result


def create_graph() -> graphviz.Digraph:
    """呼び出し関係の有向グラフを作る."""
    graph = graphviz.Digraph("services")
    graph.attr(rankdir="LR")
    graph.attr("node", shape="box", style="rounded,filled",
               fillcolor="#dbe9f6", fontname="Yu Gothic")
    for name in nodes():
        graph.node(name)
    for source, target in EDGES:
        graph.edge(source, target)
    return graph


def main() -> None:
    graph = create_graph()
    print(graph.source)
    # 画像として保存する場合は、次の行のコメントを外す
    # graph.render("services", format="svg", cleanup=True)


if __name__ == "__main__":
    main()
