"""11 章：Python パッケージの import の依存関係図を生成するサンプル.

パッケージ内の各モジュールを ast で解析し、パッケージ内のほかのモジュールを
import している箇所を探して、依存関係を有向グラフにする。
解析するパッケージは、コマンドライン引数で指定する。指定しない場合は、
このファイルと同じフォルダーの sample_app を解析する。

使い方::

    python ch11_import_graph.py [パッケージのフォルダー]

出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

import ast
import sys
from pathlib import Path

import graphviz

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
DEFAULT_PACKAGE = HERE / "sample_app"


def imported_modules(path: Path, package: str) -> set[str]:
    """モジュールが import しているパッケージ内のモジュール名を返す.

    ``from . import models`` のような相対 import と、
    ``from sample_app import models`` や ``import sample_app.models`` のような
    絶対 import の両方に対応する。返すのは ``models`` のような、パッケージ名を
    除いたモジュール名である。
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    prefix = f"{package}."
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(prefix):
                    names.add(alias.name.removeprefix(prefix).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0 or module == package:
                if module and node.level > 0:
                    # from .models import Task
                    names.add(module.split(".")[0])
                else:
                    # from . import models または from sample_app import models
                    names.update(alias.name for alias in node.names)
            elif module.startswith(prefix):
                # from sample_app.models import Task
                names.add(module.removeprefix(prefix).split(".")[0])
    return names


def build_graph(package_dir: Path = DEFAULT_PACKAGE) -> graphviz.Digraph:
    """パッケージ内のモジュールの依存関係を表す有向グラフを返す."""
    package = package_dir.name
    modules = {
        path.stem: path for path in sorted(package_dir.glob("*.py"))
        if path.stem != "__init__"
    }

    graph = graphviz.Digraph(f"{package}_imports")
    graph.attr(rankdir="LR", label=f"package: {package}", labelloc="t")
    graph.attr("node", shape="box", style="rounded,filled",
               fillcolor="lightyellow")

    for name, path in modules.items():
        graph.node(name)
        # 同じパッケージにないモジュール（標準ライブラリなど）は描かない
        for target in sorted(imported_modules(path, package) & modules.keys()):
            graph.edge(name, target)
    return graph


def main() -> int:
    """依存関係図を SVG ファイルに出力し、終了コードを返す."""
    package_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKAGE
    if not package_dir.is_dir():
        print(f"{package_dir} はフォルダーではありません。", file=sys.stderr)
        return 1

    graph = build_graph(package_dir.resolve())
    path = graph.render(outfile=OUTPUT_DIR / "ch11_import_graph.svg")
    print(f"{path} を出力しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
