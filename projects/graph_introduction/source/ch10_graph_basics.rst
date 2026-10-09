第 10 章 ネットワーク図の基礎
=============================

第 II 部では、数値ではなく「構造」、つまり要素と要素の間のつながりを可視化する。この章では、ネットワーク図の基本となるグラフ理論の用語、グラフの表し方、ノードの配置（レイアウト）の方法、Python と Graphviz で図を描く方法を説明する。

ノードとエッジ
--------------

グラフ理論でいう\ :term:`グラフ`\ は、:term:`ノード`\ （頂点）の集まりと、2 つのノードを結ぶ\ :term:`エッジ`\ （辺）の集まりからなる。ノードとエッジに何を対応させるかで、さまざまな構造を表せる。

.. list-table:: ノードとエッジの例
   :header-rows: 1
   :widths: 30 35 35

   * - 対象
     - ノード
     - エッジ
   * - SNS
     - ユーザー
     - フォロー関係
   * - ソフトウェア
     - モジュール
     - import 関係
   * - ネットワーク
     - サーバー、ルーター
     - 回線
   * - Web サイト
     - ページ
     - リンク
   * - プロジェクト
     - 作業
     - 作業の前後関係

無向グラフ
~~~~~~~~~~

エッジに向きのないグラフを\ :term:`無向グラフ`\ という。「A と B は知り合いである」のように、対称な関係を表す（:numref:`fig-ch10-undirected`）。

.. _fig-ch10-undirected:

.. graphviz:: ../examples/dot/ch10_undirected.dot
   :caption: 無向グラフ：6 人の知り合い関係
   :align: center

.. literalinclude:: ../examples/dot/ch10_undirected.dot
   :language: dot
   :linenos:
   :caption: ch10_undirected.dot

ノードにつながるエッジの数を、そのノードの\ :term:`次数`\ という。:numref:`fig-ch10-undirected` では、B、C、E の次数が 3 で最も大きい。次数の大きいノードは、つながりの中心にあることが多い。

有向グラフ
~~~~~~~~~~

エッジに向きのあるグラフを\ :term:`有向グラフ`\ という。「A から B にリンクしている」のように、非対称な関係を表す。エッジは矢印で描く（:numref:`fig-ch10-directed`）。

.. _fig-ch10-directed:

.. graphviz:: ../examples/dot/ch10_directed.dot
   :caption: 有向グラフ：Web ページのリンク
   :align: center

.. literalinclude:: ../examples/dot/ch10_directed.dot
   :language: dot
   :linenos:
   :caption: ch10_directed.dot

エッジをたどってノードを順に訪れる道筋を\ :term:`パス`\ という。始めのノードに戻ってくるパスを\ :term:`閉路`\ （サイクル）という。:numref:`fig-ch10-directed` では、「トップ → 製品一覧 → 製品詳細 → 購入 → トップ」が閉路である。閉路を持たない有向グラフを\ :term:`DAG`\ （有向非巡回グラフ）といい、作業の依存関係などを表すのに使う（第 12 章）。

重み付きグラフ
~~~~~~~~~~~~~~

エッジに数値（重み）を持たせたグラフを\ :term:`重み付きグラフ`\ という。距離、通信の遅延時間、通信量、関係の強さなどを表す。重みは、エッジのラベル、線の太さ、色、長さで表す（:numref:`fig-ch10-weighted`）。

.. _fig-ch10-weighted:

.. graphviz:: ../examples/dot/ch10_weighted.dot
   :caption: 重み付きグラフ：拠点間の回線の遅延時間（ミリ秒）
   :align: center

.. literalinclude:: ../examples/dot/ch10_weighted.dot
   :language: dot
   :linenos:
   :caption: ch10_weighted.dot

この図では、遅延時間をラベルで示し、さらに遅延時間に比例するようにエッジの長さを指定している。ただし、エッジの長さを重みに正確に比例させることは、一般にはできない。ノードの配置は、すべてのエッジの長さの条件をなるべく満たすように計算された近似である。長さは目安と考え、正確な値はラベルで示す。

グラフの表し方
--------------

同じグラフを、3 つの方法で表せる。

.. list-table:: グラフの表し方
   :header-rows: 1
   :widths: 18 42 40

   * - 表し方
     - 内容
     - 向いている場面
   * - ノードリンク図
     - ノードを図形、エッジを線で描く。一般に「ネットワーク図」と呼ばれる図である。
     - ノードとエッジが少なく、つながりの経路をたどりたい場合
   * - :term:`隣接行列`
     - ノードを行と列に並べ、エッジがあるマスに印を付けた行列。重み付きグラフでは、マスに重みを書く。
     - ノードが多く、エッジが密な場合。どのノードの組がつながっているかを網羅的に見たい場合
   * - :term:`隣接リスト`
     - ノードごとに、つながっているノードの一覧を持つ。
     - プログラムでグラフを扱う場合（図ではなくデータ構造）

:numref:`fig-ch10-node-link` と\ :numref:`fig-ch10-adjacency` は、6 つのマイクロサービスの呼び出し関係を、ノードリンク図と隣接行列で描いたものである。

.. _fig-ch10-node-link:

.. graphviz:: ../build/figures/ch10_graph_from_edges.gv
   :caption: ノードリンク図：マイクロサービスの呼び出し関係
   :align: center

.. _fig-ch10-adjacency:

.. figure:: ../build/figures/ch10_adjacency_matrix.svg
   :alt: マイクロサービスの呼び出し関係の隣接行列
   :width: 55%

   隣接行列：マイクロサービスの呼び出し関係。行が呼び出し元、列が呼び出し先である

ノードリンク図では、「gateway から order を経て payment に至る」といった経路が直感的に分かる。隣接行列では、行を見ればそのサービスが呼び出す先が、列を見ればそのサービスを呼び出す元が一覧できる。例えば notify の列には印が 2 つあり、order と payment から呼び出されることが分かる。

隣接行列は、ノードの並べ方によって見え方が変わる。関係の深いノードどうしを近くに並べると、印がまとまって見え、グループ構造が分かりやすくなる。

隣接行列は、次のように作る。行と列の番号を対応付ける辞書を作り、エッジごとに 1 を書き込む。

.. literalinclude:: ../examples/py/ch10_adjacency_matrix.py
   :pyobject: adjacency_matrix
   :lineno-match:
   :caption: ch10_adjacency_matrix.py の adjacency_matrix()

サンプルの全体：:download:`ch10_adjacency_matrix.py <../examples/py/ch10_adjacency_matrix.py>`

レイアウト
----------

ノードリンク図を描くには、各ノードを平面上のどこに置くかを決める必要がある。これを\ :term:`レイアウト`\ という。同じグラフでも、レイアウトによって見え方は大きく変わる。良いレイアウトの条件として、エッジの交差が少ないこと、エッジの長さがそろっていること、ノードが重ならないこと、構造（階層、対称性、グループ）が見えることが挙げられる。

Graphviz には、目的の異なる複数のレイアウトエンジンがある [Gansner2000]_。:numref:`fig-ch10-layout-dot` から\ :numref:`fig-ch10-layout-fdp` は、同じグラフを 4 つのエンジンで描いたものである。

.. literalinclude:: ../examples/dot/ch10_layout.dot
   :language: dot
   :linenos:
   :caption: ch10_layout.dot

.. _fig-ch10-layout-dot:

.. graphviz:: ../examples/dot/ch10_layout.dot
   :layout: dot
   :caption: dot：階層レイアウト
   :align: center

.. _fig-ch10-layout-neato:

.. graphviz:: ../examples/dot/ch10_layout.dot
   :layout: neato
   :caption: neato：力学モデルによるレイアウト
   :align: center

.. _fig-ch10-layout-circo:

.. graphviz:: ../examples/dot/ch10_layout.dot
   :layout: circo
   :caption: circo：円形レイアウト
   :align: center

.. _fig-ch10-layout-fdp:

.. graphviz:: ../examples/dot/ch10_layout.dot
   :layout: fdp
   :caption: fdp：力学モデルによるレイアウト（大きなグラフ向け）
   :align: center

.. list-table:: Graphviz の主なレイアウトエンジン
   :header-rows: 1
   :widths: 15 45 40

   * - エンジン
     - 配置の方法
     - 向いているグラフ
   * - dot
     - ノードを層に分け、エッジがなるべく同じ向き（上から下）に流れるように配置する。
     - 有向グラフ、木、DAG、フローチャート
   * - neato
     - エッジをばね、ノードを反発し合う粒子とみなし、エネルギーが最小になる配置を求める（:term:`力学モデル`\ ）。
     - 無向グラフ、ノードが 100 程度までのネットワーク
   * - fdp
     - neato と同じく力学モデルを使うが、計算方法が異なる。クラスター（ノードのまとまり）を扱える。
     - 無向グラフ、クラスターを含むグラフ
   * - circo
     - ノードを円周上に配置する。
     - 環状の構造、ノードの少ないグラフ
   * - sfdp
     - fdp を大きなグラフ向けに高速化したもの。
     - ノードが数千以上のグラフ

dot のレイアウトでは a を頂点とする階層構造が、circo のレイアウトでは a、b、f、g、c を結ぶ環状の構造が強調される。構造が事前に分かっている場合は、それが見えるエンジンを選ぶ。

グラフを Python から描く
------------------------

本書のネットワーク図は、Graphviz で描いている。Graphviz は、グラフを\ :term:`DOT 言語`\ というテキストで記述し、レイアウトと描画を自動で行うソフトウェアである。DOT 言語の基本は次のとおりである。

* 無向グラフは ``graph 名前 { ... }``、有向グラフは ``digraph 名前 { ... }`` で囲む。
* エッジは、無向グラフでは ``a -- b;``、有向グラフでは ``a -> b;`` と書く。エッジに現れたノードは自動で作られる。
* 属性は ``[属性名=値]`` の形で、ノードやエッジの後ろに書く。``node [...]`` や ``edge [...]`` と書くと、それ以降のすべてのノードやエッジの既定値になる。

DOT 言語の詳細は、Graphviz の公式文書 [GraphvizDoc]_ を参照してほしい。

データからグラフを作る場合は、Python の graphviz パッケージを使うと、DOT のテキストを組み立てる処理をプログラムで書ける。次のコードは、エッジのリスト ``EDGES`` から、:numref:`fig-ch10-node-link` の有向グラフを作る。

.. literalinclude:: ../examples/py/ch10_graph_from_edges.py
   :pyobject: create_graph
   :lineno-match:
   :caption: ch10_graph_from_edges.py の create_graph()

``graph.source`` で DOT のテキストを取り出せる。``graph.render("services", format="svg")`` を呼び出すと、Graphviz の dot コマンドで SVG 画像を作る。本書のビルドでは、``create_graph()`` が返すグラフの DOT のテキストを書き出し、Sphinx の graphviz 拡張機能で図にしている。

サンプルの全体：:download:`ch10_graph_from_edges.py <../examples/py/ch10_graph_from_edges.py>`

まとめ
------

* グラフはノードとエッジからなる。関係の性質に応じて、無向グラフ、有向グラフ、重み付きグラフを使い分ける。
* ノードとエッジが少なければノードリンク図、多く密であれば隣接行列が読みやすい。
* レイアウトは見え方を大きく左右する。階層構造には dot、一般のネットワークには neato や fdp を使う。
* Graphviz を使うと、DOT 言語のテキストや Python のプログラムからネットワーク図を描ける。
