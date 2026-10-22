"""本書のすべての図をまとめて生成する。

実行方法（examples ディレクトリで実行する）::

    python make_all_figures.py

各章の図生成スクリプト fig_chNN.py の main() を順に呼び出し、図を source/images に保存する。
"""

import fig_ch01
import fig_ch02
import fig_ch03
import fig_ch04
import fig_ch05
import fig_ch06
import fig_ch07
import fig_ch08
import fig_ch09
import fig_ch10


def main() -> None:
    """すべての章の図を生成する。"""
    for module in (fig_ch01, fig_ch02, fig_ch03, fig_ch04, fig_ch05,
                   fig_ch06, fig_ch07, fig_ch08, fig_ch09, fig_ch10):
        print(f"--- {module.__name__} ---")
        module.main()


if __name__ == "__main__":
    main()
