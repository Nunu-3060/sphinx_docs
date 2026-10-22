.. _appendix-e:

付録 E サンプルコード一覧
=========================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダーの中に次の構成でファイルが配置される。

.. code-block:: text
   :linenos:

   examples/
   ├── setup.cfg      flake8 と mypy の設定
   ├── hg.py          双曲平面の計算の共通モジュール
   ├── hg_plot.py     図の描画の補助モジュール
   └── ch02_*.py 〜 ch10_*.py  各章のサンプル

実行と検査の方法
----------------

サンプルは ``examples`` フォルダーで実行する。図を描くサンプルは画面に図を表示し、計算をするサンプルは結果を表示する。多くのサンプルは共通モジュール ``hg.py`` と ``hg_plot.py`` を import するので、個別にダウンロードした場合は、一覧の「必要なもの」の列に示したファイルも同じフォルダーに置く。必要なパッケージ（NumPy、matplotlib）は\ :ref:`はじめに <ch00>`\ を参照。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python ch04_parallels.py

サンプルは、flake8（PEP 8 などのコーディング規約の検査）と mypy（型ヒントの検査）で違反がないことを確認している。``examples`` フォルダーで次のコマンドを実行すると、``setup.cfg`` の設定（行長 120 文字まで、mypy の strict モード）で検査できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m flake8 .
   $ python -m mypy .

matplotlib の 3 次元グラフの機能（``mpl_toolkits``）は型ヒントの情報を持たないため、``setup.cfg`` でこの import の検査を省略している。mypy は実行したフォルダーの ``setup.cfg`` を読むので、ほかのフォルダーから実行する場合は ``python -m mypy --config-file examples/setup.cfg examples`` のように設定ファイルを指定する。

共通モジュール
--------------

.. list-table:: 共通モジュール
   :header-rows: 1
   :widths: 30 56 14

   * - ファイル
     - 内容
     - 必要なもの
   * - :download:`hg.py <../examples/hg.py>`
     - 距離、モデル間の変換、円板モデルでの測地線、鏡映、角度の計算（\ :ref:`第 10 章 <ch10>`\ ）。
     - NumPy
   * - :download:`hg_plot.py <../examples/hg_plot.py>`
     - 日本語フォントの設定、円板と上半平面の座標軸、上半平面の測地線の描画。
     - matplotlib
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定。
     - なし

第 I 部・第 II 部
-----------------

.. list-table:: 第 I 部・第 II 部のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch02_surfaces.py <../examples/ch02_surfaces.py>`
     - 球面、平面、擬球を 3 次元で描く。
     - 図
     - hg_plot.py
   * - :download:`ch03_models.py <../examples/ch03_models.py>`
     - 同じ図形を上半平面モデル、円板モデル、クラインモデルで描く。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch03_hyperboloid.py <../examples/ch03_hyperboloid.py>`
     - 双曲面モデルから円板モデルとクラインモデルへの射影を描く。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch03_conversion.py <../examples/ch03_conversion.py>`
     - 2 点を 4 つのモデルに移し、各モデルの公式で求めた距離が一致することを確かめる。
     - 実行結果
     - hg.py
   * - :download:`ch04_length.py <../examples/ch04_length.py>`
     - 曲線の長さを計量の数値積分で求め、距離の公式と比べる。
     - 実行結果
     - hg.py
   * - :download:`ch04_equal_circles.py <../examples/ch04_equal_circles.py>`
     - 双曲的な半径が等しい円を、2 つのモデルのいろいろな位置に描く。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch04_parallels.py <../examples/ch04_parallels.py>`
     - 測地線と交わる測地線、極限平行線、超平行線を描く。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch05_isometries.py <../examples/ch05_isometries.py>`
     - 楕円型、放物型、双曲型の等長変換による点の動きを描く。
     - 図
     - hg_plot.py
   * - :download:`ch05_classify.py <../examples/ch05_classify.py>`
     - 行列をトレースで分類し、変換が距離を保つことを確かめる。
     - 実行結果
     - hg.py

第 III 部
---------

.. list-table:: 第 III 部のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch06_trig.py <../examples/ch06_trig.py>`
     - 双曲余弦定理、正弦定理、ガウス・ボネの定理を数値で確かめる。
     - 実行結果
     - hg.py
   * - :download:`ch06_triangles.py <../examples/ch06_triangles.py>`
     - 大きさの異なる正三角形と、その内角の和を描く。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch07_growth.py <../examples/ch07_growth.py>`
     - 球面、平面、双曲平面の円周と面積を比べるグラフを描く。
     - 図
     - hg_plot.py
   * - :download:`ch07_curves.py <../examples/ch07_curves.py>`
     - 測地線、円、ホロサイクル、等距離線を描く。
     - 図
     - hg_plot.py
   * - :download:`ch07_tree.py <../examples/ch07_tree.py>`
     - 同じ木をユークリッド平面と双曲平面に描いて比べる。
     - 図
     - hg.py、hg_plot.py
   * - :download:`ch08_tiling.py <../examples/ch08_tiling.py>`
     - 双曲タイリングを鏡映で作図し、層ごとの枚数を数える。
     - 図、実行結果
     - hg.py、hg_plot.py

第 IV 部
--------

.. list-table:: 第 IV 部のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch09_embedding.py <../examples/ch09_embedding.py>`
     - 木構造をリーマン勾配法で円板モデルに埋め込む。
     - 図、実行結果
     - hg_plot.py
   * - :download:`ch09_random_graph.py <../examples/ch09_random_graph.py>`
     - 双曲平面上のランダムグラフを作り、次数の分布を調べる。
     - 図、実行結果
     - hg_plot.py
   * - :download:`ch09_focus_context.py <../examples/ch09_focus_context.py>`
     - 等長変換で木の焦点を移す。
     - 図
     - hg.py、hg_plot.py、ch07_tree.py
   * - :download:`ch09_relativity.py <../examples/ch09_relativity.py>`
     - 特殊相対論の速度の空間が双曲空間であることを確かめる。
     - 実行結果
     - hg.py
   * - :download:`ch09_smith_chart.py <../examples/ch09_smith_chart.py>`
     - スミスチャートを描き、VSWR と双曲距離の関係を確かめる。
     - 図、実行結果
     - hg.py、hg_plot.py
   * - :download:`ch10_precision.py <../examples/ch10_precision.py>`
     - 円板モデルで起こる丸め誤差の例を示す。
     - 実行結果
     - hg.py
