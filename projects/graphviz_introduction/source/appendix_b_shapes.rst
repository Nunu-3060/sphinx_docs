ノードの形と矢印の形の一覧
==========================

ノードの形（``shape``）と矢印の形（``arrowhead``、``arrowtail``）の主なものを一覧にします。すべての形は、公式ドキュメントの Node Shapes と Arrow Shapes（付録 D）で確認できます。

ノードの形
----------

各ノードのラベルが、``shape`` に指定する値です。ただし、ラベルのない小さな黒丸は ``point`` です。``point`` はラベルを表示しません。

.. graphviz:: ../examples/dot/appendix_b_shapes.dot
   :align: center

``plaintext`` と ``plain`` は、どちらも枠を描かない形です。``plaintext`` はラベルの周りに余白を取り、``plain`` は余白を取りません。``plain`` は、HTML 風ラベル（6 章）と組み合わせて使います。

``box`` と ``rect`` は同じ形です。``rectangle`` と書くこともできます。

矢印の形
--------

各エッジの上のラベルが、``arrowhead`` や ``arrowtail`` に指定する値です。

.. graphviz:: ../examples/dot/appendix_b_arrows.dot
   :align: center

矢印の形の名前には、次の修飾子を付けられます。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 修飾子
     - 例
     - 意味
   * - ``o``
     - ``odot``、``odiamond``
     - 塗りつぶさずに描きます。
   * - ``l``、``r``
     - ``lnormal``、``rnormal``
     - 矢印の左半分、右半分だけを描きます。

また、``arrowhead=dotnormal`` のように、複数の形の名前をつなげて書くと、形を組み合わせた矢印になります。形は、先に書いたものからノードに近い順に並びます。この例では、ノードのすぐ手前に ``dot``\ （黒丸）が、その外側に ``normal``\ （三角）が描かれます。

一覧の DOT ファイルは、付録 E からダウンロードできます。
