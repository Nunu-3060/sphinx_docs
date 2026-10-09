第 11 章 階層構造を見る
=======================

ディレクトリ構成、組織図、クラスの継承関係のように、親と子の関係を持つ構造を\ :term:`階層構造`\ という。グラフ理論では、閉路を持たず、すべてのノードがつながった無向グラフを\ :term:`木`\ という。階層構造は、根（最上位のノード）を持つ木として表せる。

この章では、階層構造を描く木構造図、入れ子のツリーマップ、サンバースト図と、階層的にまとめた結果を描くデンドログラムを扱う。

木構造図
--------

木構造図は、親を上（または左）に、子を下（または右）に置き、親子をエッジで結んだノードリンク図である。Graphviz の dot エンジンは、ノードを層に分けて配置するため、木構造図に向いている。

:numref:`fig-ch11-directory` は、あるプロジェクトのディレクトリ構成である。

.. _fig-ch11-directory:

.. graphviz:: ../examples/dot/ch11_directory_tree.dot
   :caption: プロジェクトのディレクトリ構成の木構造図
   :align: center

.. literalinclude:: ../examples/dot/ch11_directory_tree.dot
   :language: dot
   :linenos:
   :caption: ch11_directory_tree.dot

フォルダーとファイルを色で区別している。木構造図では、同じ深さ（層）のノードが同じ高さに並ぶので、階層の深さが一目で分かる。この例では、``models.py`` と ``views.py`` が最も深い 3 段目にある。

親子関係のエッジは向きが明らかなので、矢印を省略することが多い（``arrowhead=none``）。一方、クラスの継承関係のように向きに意味がある場合は、矢印で示す。:numref:`fig-ch11-exception` は、Python の組み込み例外のクラス階層の一部である。

.. _fig-ch11-exception:

.. graphviz:: ../examples/dot/ch11_exception_tree.dot
   :caption: Python の組み込み例外のクラス階層（一部）
   :align: center

.. literalinclude:: ../examples/dot/ch11_exception_tree.dot
   :language: dot
   :linenos:
   :caption: ch11_exception_tree.dot

UML のクラス図にならい、子クラスから親クラスへ、先端が白抜きの三角形の矢印を引いている。``rankdir=BT``（下から上へ）を指定して、親クラスが上に来るようにしている。この図から、例えば ``except LookupError:`` と書くと ``IndexError`` と ``KeyError`` の両方を捕捉できることが分かる。

木構造図は、ノードが数十程度までなら見やすい。ノードが多い場合は、横に広がりすぎるので、``rankdir=LR`` で左から右へ配置するか、深い階層を折りたたんで描く。

入れ子のツリーマップ
--------------------

第 6 章のツリーマップは、1 段の構成比を表した。長方形の中をさらに子の長方形で分割すれば、階層構造と各ノードの量を同時に表せる [Shneiderman1992]_。:numref:`fig-ch11-treemap-nested` は、架空のファイルサーバーの使用容量を、部署とフォルダーの 2 段で描いたものである。

.. _fig-ch11-treemap-nested:

.. figure:: ../build/figures/ch11_treemap_nested.svg
   :alt: 部署とフォルダーの 2 段の入れ子のツリーマップ

   使用容量の入れ子のツリーマップ。濃い色の枠が部署、薄い色の長方形がフォルダーである

開発部が全体の約 4 割を使っていること、その中ではビルド成果物が最も大きいことが分かる。木構造図と違い、ツリーマップは各ノードの量（面積）を表せる。一方、階層が 3 段以上になると、どの長方形がどの親に属するかが分かりにくくなる。各段の境界を、枠線の太さや余白で区別するとよい。

.. literalinclude:: ../examples/py/ch11_treemap_nested.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch11_treemap_nested.py の create_figure()

まず部署の合計で外側の長方形を分割し、次に各部署の長方形から、部署名の帯と余白を除いた領域を、フォルダーの値で分割している。分割には、第 6 章の ``treemap.squarify()`` を使う。

サンプルの全体：:download:`ch11_treemap_nested.py <../examples/py/ch11_treemap_nested.py>`、:download:`treemap.py <../examples/py/treemap.py>`

サンバースト図
--------------

:term:`サンバースト図`\ は、階層構造を同心円で表すグラフである。根を中心に置き、1 段目を内側の輪、2 段目をその外側の輪に配置する。各ノードの量は、扇形の角度で表す（:numref:`fig-ch11-sunburst`）。

.. _fig-ch11-sunburst:

.. figure:: ../build/figures/ch11_sunburst.svg
   :alt: 部署とフォルダーの 2 段のサンバースト図
   :width: 65%

   使用容量のサンバースト図。内側の輪が部署、外側の輪がフォルダーである

子の扇形は、必ず親の扇形の外側の範囲に収まるので、どの子がどの親に属するかは、入れ子のツリーマップより分かりやすい。一方、量は角度で表すため、円グラフと同じく正確な比較には向かない。また、外側の輪ほど扇形が細くなり、ラベルを置く場所が足りなくなる。

.. literalinclude:: ../examples/py/ch11_sunburst.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch11_sunburst.py の create_figure()

matplotlib には専用の関数がないため、``pie()`` の ``wedgeprops`` で幅（``width``）を指定した輪を、半径を変えて 2 つ重ねている。外側の輪の値を部署の順に並べることで、子の扇形が親の扇形の外側にそろう。

サンプルの全体：:download:`ch11_sunburst.py <../examples/py/ch11_sunburst.py>`

デンドログラム
--------------

:term:`デンドログラム`\ （樹形図）は、似たものから順にまとめていく\ :term:`階層クラスタリング`\ の結果を描く図である。生物の系統樹や、顧客の分類、文書の分類などに使う。

階層クラスタリングは、次の手順で行う。

#. 最初は、各データ点を 1 つのクラスター（まとまり）とする。
#. 最も距離の近い 2 つのクラスターを結合して、1 つのクラスターにする。
#. クラスターが 1 つになるまで、2 を繰り返す。

クラスター間の距離の定義にはいくつかの方法がある。サンプルでは、2 つのクラスターに属する点のすべての組の距離の平均を使う\ :term:`群平均法`\ を使っている。

.. _fig-ch11-dendrogram:

.. figure:: ../build/figures/ch11_dendrogram.svg
   :alt: 平面上の 10 個の点と、その階層クラスタリングのデンドログラム

   平面上の 10 個の点（左）と、群平均法によるデンドログラム（右）

:numref:`fig-ch11-dendrogram` の右の図では、横に元のデータ点を並べ、結合したクラスターを「コ」の字を下に向けた線でつないでいる。線の高さは、結合したときのクラスター間の距離である。

* 低い位置で結合した点どうしは、互いに近い。P0、P1、P2、P3 は距離 1 未満で 1 つにまとまる。
* 破線の高さ（2.5）で横に切ると、線が 3 本切れる。つまり、データは 3 つのクラスター（P0 から P3、P4 から P6、P7 から P9）に分かれる。切る高さを変えれば、クラスターの数を調整できる。
* 最後の結合（高さ約 4.2）は、左下のまとまりとそれ以外を結合している。右上と右下のまとまりの方が、左下のまとまりよりも互いに近いことが分かる。

.. literalinclude:: ../examples/py/ch11_dendrogram.py
   :pyobject: average_linkage
   :lineno-match:
   :caption: ch11_dendrogram.py の average_linkage()

``average_linkage()`` は、結合のたびにすべてのクラスターの組の距離を計算し、最小の組を結合する。結合の記録（結合した 2 つのクラスターと距離）を順に返す。

.. literalinclude:: ../examples/py/ch11_dendrogram.py
   :pyobject: draw_dendrogram
   :lineno-match:
   :caption: ch11_dendrogram.py の draw_dendrogram()

``draw_dendrogram()`` は、まず木を左からたどってデータ点の並び順を決める。この順に並べると、線が交差しない。次に、結合の記録の順に、2 つの子を線でつなぎ、子の中点を親の位置とする。実務では、SciPy の ``scipy.cluster.hierarchy`` モジュールの ``linkage()`` と ``dendrogram()`` を使うことが多い。

サンプルの全体：:download:`ch11_dendrogram.py <../examples/py/ch11_dendrogram.py>`

まとめ
------

* 階層構造の親子関係は、dot エンジンによる木構造図で描く。向きに意味がある場合は矢印を付ける。
* 各ノードの量も示したい場合は、入れ子のツリーマップやサンバースト図を使う。
* 階層クラスタリングの結果は、デンドログラムで描く。切る高さによってクラスターの数が決まる。
