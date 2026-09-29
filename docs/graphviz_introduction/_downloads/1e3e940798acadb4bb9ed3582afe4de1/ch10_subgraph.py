"""10 章：データからクラスターを持つグラフを生成するサンプル.

システムの構成（どの層にどのコンポーネントがあるか）と、コンポーネント間の
呼び出し関係をデータとして持ち、そこからグラフを組み立てる。
出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

from pathlib import Path

import graphviz

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

FONT = "Meiryo"

# 層の名前と、その層に属するコンポーネントの一覧
LAYERS: dict[str, list[str]] = {
    "フロントエンド": ["browser", "app"],
    "バックエンド": ["api", "worker"],
    "ストレージ": ["db", "queue"],
}

# コンポーネント間の呼び出し関係（呼び出し元, 呼び出し先）
CALLS: list[tuple[str, str]] = [
    ("browser", "app"),
    ("app", "api"),
    ("api", "db"),
    ("api", "queue"),
    ("queue", "worker"),
    ("worker", "db"),
]

# 層ごとの背景色。層の数より少ない場合は先頭から繰り返して使う
COLORS = ["aliceblue", "honeydew", "lightyellow"]


def build_graph() -> graphviz.Digraph:
    """層をクラスターで囲んだ有向グラフを返す."""
    graph = graphviz.Digraph("layers")
    graph.attr(fontname=FONT)
    graph.attr("node", shape="box", fontname=FONT)

    for index, (layer, components) in enumerate(LAYERS.items()):
        # with 文でサブグラフを作る。名前が cluster で始まるとクラスターになる
        with graph.subgraph(name=f"cluster_{index}") as cluster:
            cluster.attr(label=layer, style="filled",
                         fillcolor=COLORS[index % len(COLORS)])
            for component in components:
                cluster.node(component)

    for caller, callee in CALLS:
        graph.edge(caller, callee)
    return graph


def main() -> None:
    """グラフを SVG ファイルに出力する."""
    graph = build_graph()
    path = graph.render(outfile=OUTPUT_DIR / "ch10_subgraph.svg")
    print(f"{path} を出力しました。")


if __name__ == "__main__":
    main()
