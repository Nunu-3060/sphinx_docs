"""第 16 章: シードを変えながら島と木を生成し、ファイルに書き出す。

build_scatter.py のネットワークを作り、Geometry オブジェクトのパラメーター seed を
変えてはクックし、結果を examples/houdini/out/variations/ に書き出す。

* island_<シード>.bgeo.sc: 地形と木をまとめたもの（Houdini の形式。属性をすべて保つ）
* terrain_<シード>.obj、trees_<シード>.obj: 地形と木（ほかのツールで読める OBJ 形式）

hython での実行例（examples/houdini で）。引数は書き出す個数（省略すると 4）:

    hython export_variations.py 8
"""

from __future__ import annotations

import sys
import time

import hou

import build_scatter
from hou_common import OUT_DIR, check_errors, out_path


def export_variation(geo: hou.Node, seed: int) -> str:
    """seed を設定してクックし、ファイルに書き出す。結果を表す 1 行の文字列を返す。"""
    geo.parm("seed").set(seed)
    check_errors(geo)  # 全ノードをクックし直し、エラーがあれば止める

    # 書き出す形式は、ファイル名の拡張子で決まる
    for node_name, file_name in (("OUT_scene", f"island_{seed:03d}.bgeo.sc"),
                                 ("OUT_terrain", f"terrain_{seed:03d}.obj"),
                                 ("OUT_trees", f"trees_{seed:03d}.obj")):
        path = out_path(f"variations/{file_name}")
        geo.node(node_name).geometry().saveToFile(path.as_posix())

    # 確認用の数値: 陸地（海面より高いポイント）の割合と、木の大きさの平均
    terrain = geo.node("OUT_terrain").geometry()
    heights = terrain.pointFloatAttribValues("height")
    land = sum(1 for h in heights if h > 1e-4) / len(heights)
    scales = geo.node("OUT_points").geometry().pointFloatAttribValues("pscale")
    return f"seed {seed:3d}: 陸地 {land:5.1%}、木 {len(scales)} 本、pscale の平均 {sum(scales) / len(scales):.3f}"


def main() -> None:
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    start = time.perf_counter()
    geo = build_scatter.build().parent()
    for seed in range(count):
        print(export_variation(geo, seed))
    print(f"{count} 個を {OUT_DIR / 'variations'} に書き出した（{time.perf_counter() - start:.1f} 秒）")


if __name__ == "__main__":
    main()
