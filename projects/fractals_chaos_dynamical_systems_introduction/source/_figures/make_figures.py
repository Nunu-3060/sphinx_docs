"""本文で使う図と実行結果を、examples のサンプルから生成する.

conf.py から、サンプルごとに別のプロセスとして並列に呼び出す。単独でも実行できる。

使い方: python make_figures.py SAMPLE.py OUTPUT_DIR

* create_figures() の図   → OUTPUT_DIR/figures/<サンプル名>_<図の名前>.png
* report() の出力          → OUTPUT_DIR/outputs/<サンプル名>.txt
* create_animation() の GIF → OUTPUT_DIR/figures/<サンプル名>.gif
"""

import contextlib
import importlib.util
import io
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面を持たないバックエンドで描画する

import matplotlib.pyplot as plt  # noqa: E402


def build(sample: Path, out_dir: Path) -> None:
    """サンプル sample を読み込み、図、実行結果、アニメーションを out_dir に書き出す."""
    figures_dir = out_dir / "figures"
    outputs_dir = out_dir / "outputs"
    figures_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True  # examples に __pycache__ を作らない
    sys.path.insert(0, str(sample.parent))  # サンプル間の import を解決する
    spec = importlib.util.spec_from_file_location(sample.stem, sample)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    plot_util = importlib.import_module("plot_util")
    plot_util.setup_font()
    if hasattr(module, "report"):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            module.report()
        (outputs_dir / f"{sample.stem}.txt").write_text(buffer.getvalue(), encoding="utf-8")
    if hasattr(module, "create_figures"):
        for name, fig in module.create_figures().items():
            fig.savefig(figures_dir / f"{sample.stem}_{name}.png", dpi=110, bbox_inches="tight")
            plt.close(fig)
    if hasattr(module, "create_animation"):
        module.create_animation(figures_dir / f"{sample.stem}.gif")


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    build(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())


if __name__ == "__main__":
    main()
