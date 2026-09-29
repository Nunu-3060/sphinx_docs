サブグラフとクラスター
======================

サブグラフを使うと、グラフの中のノードやエッジをグループにまとめられます。この章では、サブグラフの使い方と、グループを枠で囲んで表示するクラスターを説明します。

サブグラフ
----------

サブグラフは ``subgraph 名前 { ... }`` の形で書きます。サブグラフには、主に次の 3 つの役割があります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 役割
     - 例
   * - 属性の適用範囲を限定する
     - サブグラフの中の属性文は、そのサブグラフの中のノードやエッジにだけ適用されます。
   * - 配置の制約を指定する
     - 7 章の ``{rank=same; b; c; d;}`` は、名前のないサブグラフに ``rank`` 属性を指定したものです。
   * - クラスターを作る
     - 次の節で説明します。

次の例では、入力と出力のノードをそれぞれサブグラフにまとめ、サブグラフごとにノードの塗りつぶしの色を指定しています。

.. literalinclude:: ../examples/dot/ch08_subgraph.dot
   :language: dot
   :caption: examples/dot/ch08_subgraph.dot

.. graphviz:: ../examples/dot/ch08_subgraph.dot
   :align: center

``loader`` はサブグラフの外で作られているため、サブグラフの中の属性文の影響を受けません。

サブグラフの名前は省略できます。4 章で説明した ``x -> {y z}`` の ``{y z}`` も、名前のないサブグラフです。

クラスター
----------

名前が ``cluster`` で始まるサブグラフは、クラスターとして扱われます。クラスターに属するノードはまとめて配置され、周りを枠で囲んで描かれます。システムの構成要素を層やサーバーごとにまとめて見せたい場合に便利です。

.. literalinclude:: ../examples/dot/ch08_cluster.dot
   :language: dot
   :caption: examples/dot/ch08_cluster.dot

.. graphviz:: ../examples/dot/ch08_cluster.dot
   :align: center

クラスターの主な属性は次のとおりです。クラスターの中に ``属性=値;`` の形で書きます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 属性
     - 意味
   * - ``label``
     - クラスターの見出し。既定では枠の上側に表示されます。
   * - ``style``
     - ``filled`` で塗りつぶし、``rounded`` で角を丸め、``dashed`` で枠を破線にします。
   * - ``fillcolor``、``bgcolor``
     - 塗りつぶしの色。``fillcolor`` は ``style=filled`` のときに、``bgcolor`` は常に使われます。
   * - ``color``、``pencolor``
     - 枠線の色。
   * - ``labeljust``
     - 見出しの揃え方。``l`` で左揃え、``r`` で右揃えになります。

クラスターの属性は、内側のクラスターにも引き継がれます。上の例では、``cluster_storage`` に ``style`` を指定していませんが、外側の ``cluster_backend`` の ``style=filled`` が引き継がれるため、``fillcolor=white`` で塗りつぶされています。

クラスターを使うときは、次の点に注意してください。

* クラスターは入れ子にできますが、1 つのノードを、入れ子の関係にない複数のクラスターに入れることはできません。
* クラスターに対応しているのは、dot、fdp、osage、patchwork などの一部のレイアウトエンジンだけです。sfdp、circo、twopi ではクラスターの枠が描かれません。neato は、版によって対応の状況が異なります（9 章）。

クラスターにエッジをつなぐ
--------------------------

エッジはノードどうしを結ぶものなので、クラスターそのものに直接エッジを引くことはできません。ただし、グラフに ``compound=true`` を指定し、エッジに ``lhead`` または ``ltail`` 属性を指定すると、エッジをクラスターの枠で切って、クラスターにつながっているように見せられます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 属性
     - 意味
   * - ``lhead``
     - エッジの終点側を、指定したクラスターの枠で切ります。
   * - ``ltail``
     - エッジの始点側を、指定したクラスターの枠で切ります。

.. literalinclude:: ../examples/dot/ch08_compound.dot
   :language: dot
   :caption: examples/dot/ch08_compound.dot

.. graphviz:: ../examples/dot/ch08_compound.dot
   :align: center

``a1 -> b1`` は、``cluster_a`` の枠から ``cluster_b`` の枠へのエッジとして描かれています。一方、``lhead`` と ``ltail`` を指定していない ``a2 -> b2`` は、ノードどうしを結んでいます。エッジの端のノード（この例では ``a1`` と ``b1``）は、そのクラスターに属している必要があります。
