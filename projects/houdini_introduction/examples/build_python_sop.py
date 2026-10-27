r"""python_sop_wave.py のコードを設定した Python SOP を作る。

Python Shell での実行例:

    import sys
    sys.path.append(r"C:\houdini_intro\examples")
    import build_python_sop
    build_python_sop.build()
"""

from __future__ import annotations

import hou

from common import EXAMPLES_DIR, check_errors, finish, recreate_geo, save_hip_from_argv


def build() -> hou.Node:
    """/obj/python_wave に Python SOP を作り、出力の Null ノードを返す。"""
    geo = recreate_geo("python_wave")
    python_sop = geo.createNode("python", "wave")
    code = (EXAMPLES_DIR / "python_sop_wave.py").read_text(encoding="utf-8")
    python_sop.parm("python").set(code)

    out = geo.createNode("null", "OUT")
    out.setFirstInput(python_sop)
    finish(geo, out)
    return out


def main() -> None:
    out = build()
    check_errors(out.parent())
    geometry = out.geometry()
    print(f"ポイント: {len(geometry.points())}, プリミティブ: {len(geometry.prims())}")
    print(f"バウンディングボックス: {geometry.boundingBox()}")
    save_hip_from_argv()


if __name__ == "__main__":
    main()
