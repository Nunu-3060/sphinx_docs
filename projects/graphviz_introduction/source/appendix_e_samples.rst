サンプル一覧
============

本資料で使用したサンプルファイルの一覧です。ファイル名をクリックすると、ファイルをダウンロードできます。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もあります。ZIP ファイルを展開すると、``examples`` フォルダーの中に、次の構成でファイルが配置されます。

.. code-block:: text

   examples/
   ├── setup.cfg        flake8 と mypy の設定
   ├── dot/             DOT 言語のサンプル
   └── py/              Python のサンプル
       └── sample_app/  11 章の依存関係図の解析対象のパッケージ

DOT 言語のサンプル
------------------

コマンドプロンプトで ``dot -Tsvg ファイル名 -o 出力するファイル名`` を実行すると、画像に変換できます（3 章）。

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - ファイル
     - 内容
     - 使用する章
   * - :download:`ch03_hello.dot <../examples/dot/ch03_hello.dot>`
     - 最初のグラフ
     - 3 章
   * - :download:`ch04_graph.dot <../examples/dot/ch04_graph.dot>`
     - 無向グラフ
     - 4 章
   * - :download:`ch04_digraph.dot <../examples/dot/ch04_digraph.dot>`
     - 有向グラフ
     - 4 章
   * - :download:`ch04_strict.dot <../examples/dot/ch04_strict.dot>`
     - ``strict`` による重複したエッジの統合
     - 4 章
   * - :download:`ch04_ids.dot <../examples/dot/ch04_ids.dot>`
     - ID の書き方
     - 4 章
   * - :download:`ch04_edge_chain.dot <../examples/dot/ch04_edge_chain.dot>`
     - エッジの連結と、まとめて接続する書き方
     - 4 章
   * - :download:`ch05_default_attrs.dot <../examples/dot/ch05_default_attrs.dot>`
     - 既定の属性の指定
     - 5 章
   * - :download:`ch05_shapes.dot <../examples/dot/ch05_shapes.dot>`
     - よく使うノードの形
     - 5 章
   * - :download:`ch05_styles.dot <../examples/dot/ch05_styles.dot>`
     - ノードとエッジのスタイル
     - 5 章
   * - :download:`ch05_colors.dot <../examples/dot/ch05_colors.dot>`
     - 色の指定方法
     - 5 章
   * - :download:`ch05_arrows.dot <../examples/dot/ch05_arrows.dot>`
     - 矢印の形と向き
     - 5 章
   * - :download:`ch05_japanese.dot <../examples/dot/ch05_japanese.dot>`
     - 日本語のラベルとフォントの指定
     - 5 章
   * - :download:`ch06_edge_labels.dot <../examples/dot/ch06_edge_labels.dot>`
     - ラベルの種類
     - 6 章
   * - :download:`ch06_align.dot <../examples/dot/ch06_align.dot>`
     - ラベル内の改行と行揃え
     - 6 章
   * - :download:`ch06_record.dot <../examples/dot/ch06_record.dot>`
     - record シェイプ
     - 6 章
   * - :download:`ch06_html_label.dot <../examples/dot/ch06_html_label.dot>`
     - HTML 風ラベル
     - 6 章
   * - :download:`ch07_rankdir.dot <../examples/dot/ch07_rankdir.dot>`
     - ``rankdir`` によるグラフの向きの指定
     - 7 章
   * - :download:`ch07_rank_same.dot <../examples/dot/ch07_rank_same.dot>`
     - ``rank=same`` による段の揃え
     - 7 章
   * - :download:`ch07_weight.dot <../examples/dot/ch07_weight.dot>`
     - ``weight`` によるエッジの重みの指定
     - 7 章
   * - :download:`ch07_constraint.dot <../examples/dot/ch07_constraint.dot>`
     - ``constraint=false`` による段の決定からの除外
     - 7 章
   * - :download:`ch07_ports.dot <../examples/dot/ch07_ports.dot>`
     - ポートによる接続位置の指定
     - 7 章
   * - :download:`ch07_splines.dot <../examples/dot/ch07_splines.dot>`
     - ``splines=ortho`` によるエッジの描き方の指定
     - 7 章
   * - :download:`ch07_invisible.dot <../examples/dot/ch07_invisible.dot>`
     - 見えないエッジによる配置の調整
     - 7 章
   * - :download:`ch08_subgraph.dot <../examples/dot/ch08_subgraph.dot>`
     - サブグラフによる属性の適用範囲の限定
     - 8 章
   * - :download:`ch08_cluster.dot <../examples/dot/ch08_cluster.dot>`
     - クラスター
     - 8 章
   * - :download:`ch08_compound.dot <../examples/dot/ch08_compound.dot>`
     - クラスターの枠につなぐエッジ
     - 8 章
   * - :download:`ch09_engines.dot <../examples/dot/ch09_engines.dot>`
     - レイアウトエンジンの比較に使うグラフ
     - 9 章
   * - :download:`ch11_state_machine.dot <../examples/dot/ch11_state_machine.dot>`
     - 状態遷移図
     - 11 章
   * - :download:`ch11_flowchart.dot <../examples/dot/ch11_flowchart.dot>`
     - フローチャート
     - 11 章
   * - :download:`ch11_er.dot <../examples/dot/ch11_er.dot>`
     - ER 図
     - 11 章
   * - :download:`ch11_class.dot <../examples/dot/ch11_class.dot>`
     - クラス図
     - 11 章
   * - :download:`appendix_b_shapes.dot <../examples/dot/appendix_b_shapes.dot>`
     - 主なノードの形の一覧
     - 付録 B
   * - :download:`appendix_b_arrows.dot <../examples/dot/appendix_b_arrows.dot>`
     - 主な矢印の形の一覧
     - 付録 B

Python のサンプル
-----------------

実行には、Graphviz 本体と graphviz パッケージが必要です（2 章）。``ch10_dot_from_string.py`` だけは、graphviz パッケージがなくても動作します。``examples/py`` フォルダーで ``python ファイル名`` を実行すると、``examples/py/output`` フォルダーに DOT ファイルと SVG ファイルが出力されます。

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - ファイル
     - 内容
     - 使用する章
   * - :download:`ch03_first_graph.py <../examples/py/ch03_first_graph.py>`
     - 最初のグラフを Python から出力するプログラム
     - 3 章
   * - :download:`ch10_digraph_basics.py <../examples/py/ch10_digraph_basics.py>`
     - graphviz パッケージの基本的な使い方
     - 10 章
   * - :download:`ch10_subgraph.py <../examples/py/ch10_subgraph.py>`
     - データからクラスターを持つグラフを生成するプログラム
     - 10 章
   * - :download:`ch10_dot_from_string.py <../examples/py/ch10_dot_from_string.py>`
     - graphviz パッケージを使わずに DOT を生成するプログラム
     - 10 章
   * - :download:`ch11_import_graph.py <../examples/py/ch11_import_graph.py>`
     - Python のパッケージの import の依存関係図を生成するプログラム
     - 11 章
   * - :download:`ch11_directory_tree.py <../examples/py/ch11_directory_tree.py>`
     - フォルダーの構成のツリー図を生成するプログラム
     - 11 章

sample_app パッケージ
^^^^^^^^^^^^^^^^^^^^^

11 章の ``ch11_import_graph.py`` が解析の対象とするパッケージです。``examples/py`` フォルダーで ``python -m sample_app.main`` を実行すると、アプリケーションとしても動作します。

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - ファイル
     - 内容
     - 使用する章
   * - :download:`__init__.py <../examples/py/sample_app/__init__.py>`
     - パッケージの初期化
     - 11 章
   * - :download:`models.py <../examples/py/sample_app/models.py>`
     - タスクを表すデータクラス
     - 11 章
   * - :download:`storage.py <../examples/py/sample_app/storage.py>`
     - タスクを保存するクラス
     - 11 章
   * - :download:`services.py <../examples/py/sample_app/services.py>`
     - タスクの追加や検索などの処理
     - 11 章
   * - :download:`main.py <../examples/py/sample_app/main.py>`
     - アプリケーションの入口
     - 11 章

設定ファイル
------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル
     - 内容
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定です。``examples`` フォルダーで ``python -m flake8 .`` と ``python -m mypy py`` を実行すると、Python のサンプルを検査できます。graphviz パッケージは型ヒントの情報を持たないため、mypy が graphviz パッケージの import をエラーにしないように設定しています。
