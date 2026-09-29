他のツールとの連携
==================

Graphviz は多くのツールから図の描画に利用されています。この章では、Python のエンジニアがよく使うツールとの連携と、ほかの作図ツールとの違いを紹介します。

Sphinx
------

Python のドキュメント生成ツールである Sphinx には、Graphviz の図を文書に埋め込む拡張機能 ``sphinx.ext.graphviz`` が標準で付属しています。本資料の図も、この拡張機能で描いています。

``conf.py`` の ``extensions`` に拡張機能を追加します。

.. code-block:: python

   extensions = [
       "sphinx.ext.graphviz",
   ]

   # 図を SVG で出力する（既定は PNG）
   graphviz_output_format = "svg"

rst ファイルでは、``graphviz`` ディレクティブに DOT を直接書くか、DOT ファイルのパスを指定します。

.. code-block:: rst

   .. graphviz::

      digraph example {
          a -> b;
      }

   .. graphviz:: ../examples/dot/ch03_hello.dot
      :layout: neato

``:layout:`` オプションでレイアウトエンジンを指定できます。ビルドする環境にも Graphviz 本体が必要です。DOT ファイルのパスを指定する方法では、同じ DOT ファイルを、ソースコードとしての表示（``literalinclude`` ディレクティブ）と図の両方に使えるので、ソースと図が食い違うことがありません。

pyreverse
---------

pyreverse は、静的解析ツール pylint に付属するツールで、Python のソースコードからクラス図とパッケージ図を生成します。pylint をインストールすると使えるようになります。

.. code-block:: console

   > pip install pylint
   > pyreverse -o svg -p sample_app sample_app

このコマンドは、``classes_sample_app.svg``\ （クラス図）と ``packages_sample_app.svg``\ （パッケージ図）を出力します。``-o dot`` を指定すると DOT ファイルを出力するので、出力された DOT を手で修正して見た目を整えることもできます。DOT 以外の形式で出力する場合は、Graphviz 本体が必要です。

pydeps
------

pydeps は、Python のモジュールの import の依存関係図を生成するツールです。11 章で作成したサンプルと同じ種類の図を、標準ライブラリやインストールしたパッケージへの依存も含めて描けます。

.. code-block:: console

   > pip install pydeps
   > pydeps sample_app

大規模なパッケージの依存関係を調べる場合は、11 章のサンプルを拡張するより、pydeps のような専用のツールを使うほうが手軽です。

NetworkX
--------

NetworkX は、グラフの解析（最短経路や中心性の計算など）を行うための Python のライブラリです。NetworkX にも描画の機能はありますが、ノードが多いグラフや有向グラフでは、Graphviz のほうが見やすく配置できることがよくあります。

NetworkX のグラフは、pydot パッケージを使って DOT ファイルに書き出せます。解析は NetworkX で行い、描画は Graphviz に任せる、という使い分けができます。

.. code-block:: python

   import networkx as nx

   g = nx.DiGraph()
   g.add_edges_from([("a", "b"), ("b", "c")])
   nx.nx_pydot.write_dot(g, "graph.dot")  # pydot のインストールが必要

ほかの作図ツールとの比較
------------------------

テキストで図を書くツールは、Graphviz のほかにもあります。代表的な Mermaid と PlantUML との違いは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 16 28 28 28

   * - 観点
     - Graphviz
     - Mermaid
     - PlantUML
   * - 得意な図
     - 汎用のグラフ。依存関係図やネットワーク図など。
     - フローチャート、シーケンス図、ガントチャートなど。
     - UML の各種の図（シーケンス図、クラス図など）。
   * - 記法
     - ノードとエッジを記述する汎用の記法。
     - 図の種類ごとの簡潔な記法。
     - UML に特化した記法。
   * - 見た目の調整
     - 属性で細かく調整できます。
     - 調整できる範囲は限られます。
     - スキンの設定で調整できます。
   * - 表示環境
     - コマンドやライブラリで画像に変換します。
     - GitHub や GitLab などの Markdown の中にそのまま書けます。
     - サーバーやエディターの拡張機能で画像に変換します。

Markdown の文書に手軽に図を入れたい場合は Mermaid が、UML の図を描きたい場合は PlantUML が便利です。プログラムから図を生成したい場合や、ノードの多い図の配置と見た目を細かく調整したい場合は、Graphviz が向いています。
