付録 C サンプルコード一覧
=========================

本書で使用したサンプルコードの一覧である。各ファイル名のリンクからダウンロードできる。

実行環境
--------

サンプルコードは次の環境で動作を確認した。Python 3.12 以降であれば動作するはずである。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ソフトウェア
     - バージョン
   * - Python
     - 3.14.6
   * - NumPy
     - 2.5.1
   * - matplotlib
     - 3.11.2

すべてのファイルは同じディレクトリに置いて実行する。たとえば第 5 章の数値実験は次のように実行する。

.. code-block:: text
   :linenos:

   python ch05_numerical_diff.py

数値実験のスクリプト
--------------------

結果を標準出力に表として表示する。

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - ファイル
     - 章
     - 内容
   * - :download:`ch01_float_error.py <../examples/ch01_float_error.py>`
     - :doc:`第 1 章 <real_numbers>`
     - 浮動小数点数の丸め誤差と機械イプシロン
   * - :download:`ch02_newton_sqrt2.py <../examples/ch02_newton_sqrt2.py>`
     - :doc:`第 2 章 <sequences>`
     - ニュートン法による √2 の近似と収束の速さ
   * - :download:`ch03_series.py <../examples/ch03_series.py>`
     - :doc:`第 3 章 <series>`
     - 調和級数・交代調和級数の部分和と項の並べ替え
   * - :download:`ch04_bisection.py <../examples/ch04_bisection.py>`
     - :doc:`第 4 章 <continuity>`
     - 二分法による方程式の求解と誤差評価
   * - :download:`ch05_numerical_diff.py <../examples/ch05_numerical_diff.py>`
     - :doc:`第 5 章 <differentiation>`
     - 前進差分・中心差分の誤差と刻み幅
   * - :download:`ch06_taylor.py <../examples/ch06_taylor.py>`
     - :doc:`第 6 章 <taylor>`
     - テイラー多項式による近似の精度
   * - :download:`ch07_numerical_integration.py <../examples/ch07_numerical_integration.py>`
     - :doc:`第 7 章 <integration>`
     - 台形公式・シンプソン公式の誤差の次数
   * - :download:`ch08_uniform_convergence.py <../examples/ch08_uniform_convergence.py>`
     - :doc:`第 8 章 <function_sequences>`
     - 関数列の各点収束と一様収束
   * - :download:`ch09_gradient_descent.py <../examples/ch09_gradient_descent.py>`
     - :doc:`第 9 章 <multivariable_differentiation>`
     - 勾配降下法
   * - :download:`ch10_monte_carlo.py <../examples/ch10_monte_carlo.py>`
     - :doc:`第 10 章 <multivariable_integration>`
     - モンテカルロ積分と次元の呪い

図の生成スクリプト
------------------

本文中の matplotlib の図を生成するスクリプトである。図は ``source/images`` に PNG 形式で保存される。``make_all_figures.py`` を実行すると、すべての図をまとめて生成できる。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ファイル
     - 内容
   * - :download:`plot_style.py <../examples/plot_style.py>`
     - 日本語フォントの指定など、図の共通設定
   * - :download:`make_all_figures.py <../examples/make_all_figures.py>`
     - すべての図をまとめて生成する
   * - :download:`fig_ch01.py <../examples/fig_ch01.py>`
     - :doc:`第 1 章 <real_numbers>`\ の図
   * - :download:`fig_ch02.py <../examples/fig_ch02.py>`
     - :doc:`第 2 章 <sequences>`\ の図
   * - :download:`fig_ch03.py <../examples/fig_ch03.py>`
     - :doc:`第 3 章 <series>`\ の図
   * - :download:`fig_ch04.py <../examples/fig_ch04.py>`
     - :doc:`第 4 章 <continuity>`\ の図
   * - :download:`fig_ch05.py <../examples/fig_ch05.py>`
     - :doc:`第 5 章 <differentiation>`\ の図
   * - :download:`fig_ch06.py <../examples/fig_ch06.py>`
     - :doc:`第 6 章 <taylor>`\ の図
   * - :download:`fig_ch07.py <../examples/fig_ch07.py>`
     - :doc:`第 7 章 <integration>`\ の図
   * - :download:`fig_ch08.py <../examples/fig_ch08.py>`
     - :doc:`第 8 章 <function_sequences>`\ の図
   * - :download:`fig_ch09.py <../examples/fig_ch09.py>`
     - :doc:`第 9 章 <multivariable_differentiation>`\ の図
   * - :download:`fig_ch10.py <../examples/fig_ch10.py>`
     - :doc:`第 10 章 <multivariable_integration>`\ の図

検査の設定
----------

すべてのスクリプトは flake8 と mypy（strict モード）で検査している。設定ファイルは次のとおりである。

:download:`setup.cfg <../examples/setup.cfg>`

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:

examples ディレクトリで次のコマンドを実行すると検査できる。

.. code-block:: text
   :linenos:

   python -m flake8 .
   python -m mypy .
