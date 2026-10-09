付録 D サンプルコード一覧
=========================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダーの中に次の構成でファイルが配置される。

.. code-block:: text
   :linenos:

   examples/
   ├── setup.cfg   flake8 と mypy の設定
   ├── py/         Python のサンプルと補助モジュール
   └── dot/        Graphviz の DOT ファイル

実行と検査の方法
----------------

Python のサンプルは、``examples/py`` フォルダーで実行する。サンプルの多くは補助モジュール（``jpfont.py`` など）を import するので、個別にダウンロードした場合は、一覧の「補助モジュール」の列に示したファイルも同じフォルダーに置く。

.. code-block:: console
   :linenos:

   $ cd examples/py
   $ python ch03_bar.py

DOT ファイルは、Graphviz の dot コマンドで画像に変換する。``-K`` オプションでレイアウトエンジンを指定できる。

.. code-block:: console
   :linenos:

   $ cd examples/dot
   $ dot -Tsvg ch10_undirected.dot -o ch10_undirected.svg
   $ dot -Kneato -Tsvg ch10_layout.dot -o ch10_layout_neato.svg

Python のサンプルは、flake8（PEP 8 などのコーディング規約の検査）と mypy（型ヒントの検査）で違反がないことを確認している。``examples`` フォルダーで次のコマンドを実行すると、``setup.cfg`` の設定で検査できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m flake8 .
   $ python -m mypy py

ファイルの一覧
--------------

第 1 章 可視化とグラフ
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch01_anscombe.py <../examples/py/ch01_anscombe.py>`
     - アンスコムの例：要約統計量が同じでも、グラフにすると違いが分かる
     - ``jpfont.py``

第 2 章 可視化の基礎
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch02_anatomy.py <../examples/py/ch02_anatomy.py>`
     - グラフの構成要素：タイトル、軸ラベル、目盛り、凡例、注釈
     - ``jpfont.py``
   * - :download:`ch02_colormaps.py <../examples/py/ch02_colormaps.py>`
     - カラーマップの 3 つの種類：質的、連続、発散
     - ``jpfont.py``
   * - :download:`ch02_figure_axes.py <../examples/py/ch02_figure_axes.py>`
     - matplotlib の基本構造：Figure と Axes
     - ``jpfont.py``
   * - :download:`ch02_visual_channels.py <../examples/py/ch02_visual_channels.py>`
     - 同じ 5 つの値を、異なる視覚変数で表す
     - ``jpfont.py``

第 3 章 量を比較する
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch03_bar.py <../examples/py/ch03_bar.py>`
     - 棒グラフ：カテゴリごとの量を比較する
     - ``jpfont.py``
   * - :download:`ch03_dot_plot.py <../examples/py/ch03_dot_plot.py>`
     - ドットプロット：2 時点の値を点と線で比較する
     - ``jpfont.py``
   * - :download:`ch03_grouped_stacked.py <../examples/py/ch03_grouped_stacked.py>`
     - グループ化棒グラフと積み上げ棒グラフ
     - ``jpfont.py``
   * - :download:`ch03_radar.py <../examples/py/ch03_radar.py>`
     - レーダーチャート：複数の評価項目をまとめて比較する
     - ``jpfont.py``

第 4 章 分布を見る
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch04_box_violin.py <../examples/py/ch04_box_violin.py>`
     - 箱ひげ図とバイオリンプロット
     - ``jpfont.py``
   * - :download:`ch04_ecdf.py <../examples/py/ch04_ecdf.py>`
     - 経験累積分布関数（ECDF）：分布を階級なしで比較する
     - ``jpfont.py``
   * - :download:`ch04_histogram.py <../examples/py/ch04_histogram.py>`
     - ヒストグラム：階級の幅によって分布の見え方が変わる
     - ``jpfont.py``
   * - :download:`ch04_strip.py <../examples/py/ch04_strip.py>`
     - ストリッププロット：個々のデータ点をすべて描く
     - ``jpfont.py``

第 5 章 関係を見る
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch05_bubble.py <../examples/py/ch05_bubble.py>`
     - バブルチャート：3 つの量を 1 つの図に描く
     - ``jpfont.py``
   * - :download:`ch05_correlation.py <../examples/py/ch05_correlation.py>`
     - 相関係数と散布図の形
     - ``jpfont.py``
   * - :download:`ch05_overplot.py <../examples/py/ch05_overplot.py>`
     - 点の重なり（オーバープロット）への対策
     - ``jpfont.py``
   * - :download:`ch05_scatter.py <../examples/py/ch05_scatter.py>`
     - 散布図と回帰直線：2 つの量の関係を見る
     - ``jpfont.py``

第 6 章 構成比を見る
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch06_pie_bar.py <../examples/py/ch06_pie_bar.py>`
     - 円グラフと棒グラフ：構成比の読み取りやすさを比べる
     - ``jpfont.py``
   * - :download:`ch06_stacked_percent.py <../examples/py/ch06_stacked_percent.py>`
     - 100% 積み上げ棒グラフ：合計の異なるグループの構成比を比べる
     - ``jpfont.py``
   * - :download:`ch06_treemap.py <../examples/py/ch06_treemap.py>`
     - ツリーマップ：長方形の面積で構成比を表す
     - ``jpfont.py``、``treemap.py``
   * - :download:`ch06_waterfall.py <../examples/py/ch06_waterfall.py>`
     - ウォーターフォールチャート：増減の内訳を示す
     - ``jpfont.py``

第 7 章 時間変化を見る
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch07_area.py <../examples/py/ch07_area.py>`
     - 積み上げ面グラフ：合計と内訳の時間変化を見る
     - ``jpfont.py``
   * - :download:`ch07_calendar_heatmap.py <../examples/py/ch07_calendar_heatmap.py>`
     - カレンダーヒートマップ：曜日と週の周期を見る
     - ``jpfont.py``
   * - :download:`ch07_gantt.py <../examples/py/ch07_gantt.py>`
     - ガントチャート：作業の期間と重なりを描く
     - ``jpfont.py``
   * - :download:`ch07_line.py <../examples/py/ch07_line.py>`
     - 折れ線グラフと移動平均：時間変化の傾向を見る
     - ``jpfont.py``
   * - :download:`ch07_log_scale.py <../examples/py/ch07_log_scale.py>`
     - 対数軸：指数的に増える量を描く
     - ``jpfont.py``
   * - :download:`ch07_step.py <../examples/py/ch07_step.py>`
     - ステップグラフ：値が段階的に変わるデータを描く
     - ``jpfont.py``

第 8 章 多次元データを見る
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch08_heatmap.py <../examples/py/ch08_heatmap.py>`
     - ヒートマップ：相関行列を色で表す
     - ``jpfont.py``、``multivariate_data.py``
   * - :download:`ch08_parallel.py <../examples/py/ch08_parallel.py>`
     - 平行座標プロット：多数の項目を持つデータを折れ線で描く
     - ``jpfont.py``、``multivariate_data.py``
   * - :download:`ch08_pca.py <../examples/py/ch08_pca.py>`
     - 主成分分析（PCA）：多次元のデータを 2 次元に落として描く
     - ``jpfont.py``、``multivariate_data.py``
   * - :download:`ch08_scatter_matrix.py <../examples/py/ch08_scatter_matrix.py>`
     - 散布図行列：すべての項目の組の関係を一覧する
     - ``jpfont.py``、``multivariate_data.py``
   * - :download:`ch08_small_multiples.py <../examples/py/ch08_small_multiples.py>`
     - スモールマルチプル：同じ形式の小さなグラフを並べる
     - ``jpfont.py``

第 9 章 平面上の量を見る
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch09_contour.py <../examples/py/ch09_contour.py>`
     - 等高線図とカラーマップ：平面上の量を描く
     - ``jpfont.py``
   * - :download:`ch09_surface.py <../examples/py/ch09_surface.py>`
     - 3D サーフェス：2 変数関数を立体的に描く
     - ``jpfont.py``、``ch09_contour.py``
   * - :download:`ch09_vector_field.py <../examples/py/ch09_vector_field.py>`
     - ベクトル場：矢印図と流線図
     - ``jpfont.py``

第 10 章 ネットワーク図の基礎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch10_adjacency_matrix.py <../examples/py/ch10_adjacency_matrix.py>`
     - 隣接行列：グラフを行列として描く
     - ``jpfont.py``、``ch10_graph_from_edges.py``
   * - :download:`ch10_graph_from_edges.py <../examples/py/ch10_graph_from_edges.py>`
     - エッジのリストからグラフを組み立てる
     - なし
   * - :download:`ch10_directed.dot <../examples/dot/ch10_directed.dot>`
     - 有向グラフ：6 つの Web ページのリンク
     - なし
   * - :download:`ch10_layout.dot <../examples/dot/ch10_layout.dot>`
     - レイアウトの比較に使うグラフ
     - なし
   * - :download:`ch10_undirected.dot <../examples/dot/ch10_undirected.dot>`
     - 無向グラフ：6 人の知り合い関係
     - なし
   * - :download:`ch10_weighted.dot <../examples/dot/ch10_weighted.dot>`
     - 重み付きグラフ：5 つの拠点を結ぶ回線と、その遅延時間（ミリ秒）
     - なし

第 11 章 階層構造を見る
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch11_dendrogram.py <../examples/py/ch11_dendrogram.py>`
     - デンドログラム：階層クラスタリングの結果を描く
     - ``jpfont.py``
   * - :download:`ch11_sunburst.py <../examples/py/ch11_sunburst.py>`
     - サンバースト図：階層構造を同心円で描く
     - ``jpfont.py``、``ch11_treemap_nested.py``
   * - :download:`ch11_treemap_nested.py <../examples/py/ch11_treemap_nested.py>`
     - 入れ子のツリーマップ：階層構造と量を同時に描く
     - ``jpfont.py``、``treemap.py``
   * - :download:`ch11_directory_tree.dot <../examples/dot/ch11_directory_tree.dot>`
     - 木構造：プロジェクトのディレクトリ構成
     - なし
   * - :download:`ch11_exception_tree.dot <../examples/dot/ch11_exception_tree.dot>`
     - 木構造：Python の組み込み例外のクラス階層（一部）
     - なし

第 12 章 流れと手順を見る
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch12_sankey.py <../examples/py/ch12_sankey.py>`
     - サンキー図：量の流れを帯の太さで描く
     - ``jpfont.py``
   * - :download:`ch12_sequence.py <../examples/py/ch12_sequence.py>`
     - シーケンス図：時間の流れに沿ったやり取りを描く
     - ``jpfont.py``
   * - :download:`ch12_flowchart.dot <../examples/dot/ch12_flowchart.dot>`
     - フローチャート：ログイン処理の流れ
     - なし
   * - :download:`ch12_pipeline.dot <../examples/dot/ch12_pipeline.dot>`
     - DAG（有向非巡回グラフ）：CI/CD パイプラインのジョブの依存関係
     - なし
   * - :download:`ch12_state_machine.dot <../examples/dot/ch12_state_machine.dot>`
     - 状態遷移図：通販サイトの注文の状態
     - なし

第 13 章 関係とつながりを見る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch13_dependency.py <../examples/py/ch13_dependency.py>`
     - 依存関係グラフ：モジュールの import 関係を描き、循環を見つける
     - なし
   * - :download:`ch13_flow_matrix.py <../examples/py/ch13_flow_matrix.py>`
     - 流量の行列：多数のノードの間のやり取りを行列で描く
     - ``jpfont.py``
   * - :download:`ch13_clusters.dot <../examples/dot/ch13_clusters.dot>`
     - ノードの多いグラフの整理：関連するノードをクラスターにまとめる
     - なし
   * - :download:`ch13_er.dot <../examples/dot/ch13_er.dot>`
     - ER 図：通販サイトのテーブルとリレーション
     - なし
   * - :download:`ch13_network.dot <../examples/dot/ch13_network.dot>`
     - ネットワーク構成図：小さな Web システムの機器とつながり
     - なし

第 14 章 誤解を招くグラフと改善
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch14_3d_bar.py <../examples/py/ch14_3d_bar.py>`
     - 3D の棒グラフ：奥行きと遠近で値が読み取りにくくなる
     - ``jpfont.py``
   * - :download:`ch14_area_scaling.py <../examples/py/ch14_area_scaling.py>`
     - 円の大きさで量を表すときの誤り：半径を値に比例させる
     - ``jpfont.py``
   * - :download:`ch14_chartjunk.py <../examples/py/ch14_chartjunk.py>`
     - 装飾の多いグラフと、装飾を減らしたグラフ
     - ``jpfont.py``
   * - :download:`ch14_dual_axis.py <../examples/py/ch14_dual_axis.py>`
     - 二重軸のグラフ：軸の範囲の選び方で見かけの関係が変わる
     - ``jpfont.py``
   * - :download:`ch14_rainbow.py <../examples/py/ch14_rainbow.py>`
     - 虹色のカラーマップの問題：明るさが値の順に並ばない
     - ``jpfont.py``
   * - :download:`ch14_truncated_axis.py <../examples/py/ch14_truncated_axis.py>`
     - 縦軸を 0 から始めない棒グラフ：差が誇張される
     - ``jpfont.py``

第 15 章 グラフを選ぶ
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 45 23

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch15_case_comparison.py <../examples/py/ch15_case_comparison.py>`
     - ケーススタディ 3：エンドポイントの応答時間を比較する
     - ``jpfont.py``、``server_log.py``
   * - :download:`ch15_case_distribution.py <../examples/py/ch15_case_distribution.py>`
     - ケーススタディ 2：応答時間の分布を見る
     - ``jpfont.py``、``server_log.py``
   * - :download:`ch15_case_timeseries.py <../examples/py/ch15_case_timeseries.py>`
     - ケーススタディ 1：応答時間の時間変化を見る
     - ``jpfont.py``、``server_log.py``
   * - :download:`ch15_choose.dot <../examples/dot/ch15_choose.dot>`
     - グラフを選ぶための判断フロー
     - なし

補助モジュールと設定
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 32 68

   * - ファイル
     - 内容
   * - :download:`jpfont.py <../examples/py/jpfont.py>`
     - matplotlib で日本語を表示するための設定
   * - :download:`treemap.py <../examples/py/treemap.py>`
     - ツリーマップの配置を計算する（squarified アルゴリズム）
   * - :download:`multivariate_data.py <../examples/py/multivariate_data.py>`
     - 第 8 章のサンプルで共通に使う、多次元の架空データ
   * - :download:`server_log.py <../examples/py/server_log.py>`
     - 第 15 章のケーススタディで使う、架空の Web API のアクセスログ
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定

ソースコード
------------

すべてのサンプルのソースコードを示す。

第 1 章 可視化とグラフ
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch01_anscombe.py
   :language: python
   :linenos:
   :caption: ch01_anscombe.py

第 2 章 可視化の基礎
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch02_anatomy.py
   :language: python
   :linenos:
   :caption: ch02_anatomy.py

.. literalinclude:: ../examples/py/ch02_colormaps.py
   :language: python
   :linenos:
   :caption: ch02_colormaps.py

.. literalinclude:: ../examples/py/ch02_figure_axes.py
   :language: python
   :linenos:
   :caption: ch02_figure_axes.py

.. literalinclude:: ../examples/py/ch02_visual_channels.py
   :language: python
   :linenos:
   :caption: ch02_visual_channels.py

第 3 章 量を比較する
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch03_bar.py
   :language: python
   :linenos:
   :caption: ch03_bar.py

.. literalinclude:: ../examples/py/ch03_dot_plot.py
   :language: python
   :linenos:
   :caption: ch03_dot_plot.py

.. literalinclude:: ../examples/py/ch03_grouped_stacked.py
   :language: python
   :linenos:
   :caption: ch03_grouped_stacked.py

.. literalinclude:: ../examples/py/ch03_radar.py
   :language: python
   :linenos:
   :caption: ch03_radar.py

第 4 章 分布を見る
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch04_box_violin.py
   :language: python
   :linenos:
   :caption: ch04_box_violin.py

.. literalinclude:: ../examples/py/ch04_ecdf.py
   :language: python
   :linenos:
   :caption: ch04_ecdf.py

.. literalinclude:: ../examples/py/ch04_histogram.py
   :language: python
   :linenos:
   :caption: ch04_histogram.py

.. literalinclude:: ../examples/py/ch04_strip.py
   :language: python
   :linenos:
   :caption: ch04_strip.py

第 5 章 関係を見る
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch05_bubble.py
   :language: python
   :linenos:
   :caption: ch05_bubble.py

.. literalinclude:: ../examples/py/ch05_correlation.py
   :language: python
   :linenos:
   :caption: ch05_correlation.py

.. literalinclude:: ../examples/py/ch05_overplot.py
   :language: python
   :linenos:
   :caption: ch05_overplot.py

.. literalinclude:: ../examples/py/ch05_scatter.py
   :language: python
   :linenos:
   :caption: ch05_scatter.py

第 6 章 構成比を見る
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch06_pie_bar.py
   :language: python
   :linenos:
   :caption: ch06_pie_bar.py

.. literalinclude:: ../examples/py/ch06_stacked_percent.py
   :language: python
   :linenos:
   :caption: ch06_stacked_percent.py

.. literalinclude:: ../examples/py/ch06_treemap.py
   :language: python
   :linenos:
   :caption: ch06_treemap.py

.. literalinclude:: ../examples/py/ch06_waterfall.py
   :language: python
   :linenos:
   :caption: ch06_waterfall.py

第 7 章 時間変化を見る
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch07_area.py
   :language: python
   :linenos:
   :caption: ch07_area.py

.. literalinclude:: ../examples/py/ch07_calendar_heatmap.py
   :language: python
   :linenos:
   :caption: ch07_calendar_heatmap.py

.. literalinclude:: ../examples/py/ch07_gantt.py
   :language: python
   :linenos:
   :caption: ch07_gantt.py

.. literalinclude:: ../examples/py/ch07_line.py
   :language: python
   :linenos:
   :caption: ch07_line.py

.. literalinclude:: ../examples/py/ch07_log_scale.py
   :language: python
   :linenos:
   :caption: ch07_log_scale.py

.. literalinclude:: ../examples/py/ch07_step.py
   :language: python
   :linenos:
   :caption: ch07_step.py

第 8 章 多次元データを見る
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch08_heatmap.py
   :language: python
   :linenos:
   :caption: ch08_heatmap.py

.. literalinclude:: ../examples/py/ch08_parallel.py
   :language: python
   :linenos:
   :caption: ch08_parallel.py

.. literalinclude:: ../examples/py/ch08_pca.py
   :language: python
   :linenos:
   :caption: ch08_pca.py

.. literalinclude:: ../examples/py/ch08_scatter_matrix.py
   :language: python
   :linenos:
   :caption: ch08_scatter_matrix.py

.. literalinclude:: ../examples/py/ch08_small_multiples.py
   :language: python
   :linenos:
   :caption: ch08_small_multiples.py

第 9 章 平面上の量を見る
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch09_contour.py
   :language: python
   :linenos:
   :caption: ch09_contour.py

.. literalinclude:: ../examples/py/ch09_surface.py
   :language: python
   :linenos:
   :caption: ch09_surface.py

.. literalinclude:: ../examples/py/ch09_vector_field.py
   :language: python
   :linenos:
   :caption: ch09_vector_field.py

第 10 章 ネットワーク図の基礎
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch10_adjacency_matrix.py
   :language: python
   :linenos:
   :caption: ch10_adjacency_matrix.py

.. literalinclude:: ../examples/py/ch10_graph_from_edges.py
   :language: python
   :linenos:
   :caption: ch10_graph_from_edges.py

.. literalinclude:: ../examples/dot/ch10_directed.dot
   :language: dot
   :linenos:
   :caption: ch10_directed.dot

.. literalinclude:: ../examples/dot/ch10_layout.dot
   :language: dot
   :linenos:
   :caption: ch10_layout.dot

.. literalinclude:: ../examples/dot/ch10_undirected.dot
   :language: dot
   :linenos:
   :caption: ch10_undirected.dot

.. literalinclude:: ../examples/dot/ch10_weighted.dot
   :language: dot
   :linenos:
   :caption: ch10_weighted.dot

第 11 章 階層構造を見る
~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch11_dendrogram.py
   :language: python
   :linenos:
   :caption: ch11_dendrogram.py

.. literalinclude:: ../examples/py/ch11_sunburst.py
   :language: python
   :linenos:
   :caption: ch11_sunburst.py

.. literalinclude:: ../examples/py/ch11_treemap_nested.py
   :language: python
   :linenos:
   :caption: ch11_treemap_nested.py

.. literalinclude:: ../examples/dot/ch11_directory_tree.dot
   :language: dot
   :linenos:
   :caption: ch11_directory_tree.dot

.. literalinclude:: ../examples/dot/ch11_exception_tree.dot
   :language: dot
   :linenos:
   :caption: ch11_exception_tree.dot

第 12 章 流れと手順を見る
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch12_sankey.py
   :language: python
   :linenos:
   :caption: ch12_sankey.py

.. literalinclude:: ../examples/py/ch12_sequence.py
   :language: python
   :linenos:
   :caption: ch12_sequence.py

.. literalinclude:: ../examples/dot/ch12_flowchart.dot
   :language: dot
   :linenos:
   :caption: ch12_flowchart.dot

.. literalinclude:: ../examples/dot/ch12_pipeline.dot
   :language: dot
   :linenos:
   :caption: ch12_pipeline.dot

.. literalinclude:: ../examples/dot/ch12_state_machine.dot
   :language: dot
   :linenos:
   :caption: ch12_state_machine.dot

第 13 章 関係とつながりを見る
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch13_dependency.py
   :language: python
   :linenos:
   :caption: ch13_dependency.py

.. literalinclude:: ../examples/py/ch13_flow_matrix.py
   :language: python
   :linenos:
   :caption: ch13_flow_matrix.py

.. literalinclude:: ../examples/dot/ch13_clusters.dot
   :language: dot
   :linenos:
   :caption: ch13_clusters.dot

.. literalinclude:: ../examples/dot/ch13_er.dot
   :language: dot
   :linenos:
   :caption: ch13_er.dot

.. literalinclude:: ../examples/dot/ch13_network.dot
   :language: dot
   :linenos:
   :caption: ch13_network.dot

第 14 章 誤解を招くグラフと改善
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch14_3d_bar.py
   :language: python
   :linenos:
   :caption: ch14_3d_bar.py

.. literalinclude:: ../examples/py/ch14_area_scaling.py
   :language: python
   :linenos:
   :caption: ch14_area_scaling.py

.. literalinclude:: ../examples/py/ch14_chartjunk.py
   :language: python
   :linenos:
   :caption: ch14_chartjunk.py

.. literalinclude:: ../examples/py/ch14_dual_axis.py
   :language: python
   :linenos:
   :caption: ch14_dual_axis.py

.. literalinclude:: ../examples/py/ch14_rainbow.py
   :language: python
   :linenos:
   :caption: ch14_rainbow.py

.. literalinclude:: ../examples/py/ch14_truncated_axis.py
   :language: python
   :linenos:
   :caption: ch14_truncated_axis.py

第 15 章 グラフを選ぶ
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/ch15_case_comparison.py
   :language: python
   :linenos:
   :caption: ch15_case_comparison.py

.. literalinclude:: ../examples/py/ch15_case_distribution.py
   :language: python
   :linenos:
   :caption: ch15_case_distribution.py

.. literalinclude:: ../examples/py/ch15_case_timeseries.py
   :language: python
   :linenos:
   :caption: ch15_case_timeseries.py

.. literalinclude:: ../examples/dot/ch15_choose.dot
   :language: dot
   :linenos:
   :caption: ch15_choose.dot

補助モジュール
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/py/jpfont.py
   :language: python
   :linenos:
   :caption: jpfont.py

.. literalinclude:: ../examples/py/treemap.py
   :language: python
   :linenos:
   :caption: treemap.py

.. literalinclude:: ../examples/py/multivariate_data.py
   :language: python
   :linenos:
   :caption: multivariate_data.py

.. literalinclude:: ../examples/py/server_log.py
   :language: python
   :linenos:
   :caption: server_log.py
