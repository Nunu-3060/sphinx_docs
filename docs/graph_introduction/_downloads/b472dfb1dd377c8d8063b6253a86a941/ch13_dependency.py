"""依存関係グラフ: モジュールの import 関係を描き、循環を見つける.

架空のアプリケーションのモジュールの import 関係から有向グラフを作る。
深さ優先探索で循環（A → B → … → A）を見つけ、循環に含まれるエッジを
赤で描く。

使い方: python ch13_dependency.py
"""

import graphviz

# モジュール: そのモジュールが import するモジュール
IMPORTS = {
    "main": ["cli", "config"],
    "cli": ["service", "config"],
    "service": ["repository", "models", "notify"],
    "repository": ["models", "db"],
    "notify": ["service", "config"],  # service と notify が互いに依存
    "models": [],
    "db": ["config"],
    "config": [],
}


def find_cycle_edges() -> set[tuple[str, str]]:
    """循環に含まれるエッジを、深さ優先探索で集める."""
    cycle_edges: set[tuple[str, str]] = set()
    path: list[str] = []  # 探索中のモジュールの並び

    def visit(module: str) -> None:
        if module in path:
            # path の中の module から現在までが 1 つの循環になる
            loop = path[path.index(module):] + [module]
            cycle_edges.update(zip(loop, loop[1:]))
            return
        path.append(module)
        for target in IMPORTS[module]:
            visit(target)
        path.pop()

    for module in IMPORTS:
        visit(module)
    return cycle_edges


def create_graph() -> graphviz.Digraph:
    """import 関係の有向グラフを作る。循環のエッジは赤で描く."""
    cycle_edges = find_cycle_edges()
    graph = graphviz.Digraph("imports")
    graph.attr("node", shape="box", style="rounded,filled",
               fillcolor="#dbe9f6", fontname="Consolas")
    for module, targets in IMPORTS.items():
        for target in targets:
            if (module, target) in cycle_edges:
                graph.edge(module, target, color="red", penwidth="2")
            else:
                graph.edge(module, target)
    return graph


def main() -> None:
    for source, target in sorted(find_cycle_edges()):
        print(f"循環: {source} -> {target}")
    print(create_graph().source)


if __name__ == "__main__":
    main()
