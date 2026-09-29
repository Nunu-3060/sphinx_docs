レイアウトの制御
================

Graphviz はノードの配置を自動的に決めますが、属性を使って配置の方針を指示できます。この章では、既定のレイアウトエンジンである dot で使える、配置を調整する方法を説明します。ここで説明する属性の多くは dot 専用で、ほかのレイアウトエンジン（9 章）では無視されます。

4 章で説明したとおり、dot はノードを段（ランク）に分けて並べます。このとき、エッジの始点のノードを上の段に、終点のノードを下の段に置き、エッジの交差ができるだけ少なくなるように、同じ段の中でノードを並べ替えます。配置を調整するときは、この「段に分けて並べる」という仕組みを意識すると、属性の効果を理解しやすくなります。

グラフの向き
------------

``rankdir`` 属性で、段を並べる方向を指定します。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 意味
   * - ``TB``
     - 上から下（Top to Bottom）。既定値です。
   * - ``LR``
     - 左から右（Left to Right）。
   * - ``BT``
     - 下から上（Bottom to Top）。
   * - ``RL``
     - 右から左（Right to Left）。

.. literalinclude:: ../examples/dot/ch07_rankdir.dot
   :language: dot
   :caption: examples/dot/ch07_rankdir.dot

.. graphviz:: ../examples/dot/ch07_rankdir.dot
   :align: center

処理の流れを表す図は、横長の画面や資料に収めやすい ``LR`` がよく使われます。

同じ段に並べる
--------------

``{rank=same; ノード; ノード; ...}`` と書くと、指定したノードを同じ段に並べられます。

.. literalinclude:: ../examples/dot/ch07_rank_same.dot
   :language: dot
   :caption: examples/dot/ch07_rank_same.dot

.. graphviz:: ../examples/dot/ch07_rank_same.dot
   :align: center

``rank=same`` を指定しない場合、``c`` は ``start`` のすぐ下の段に置かれます。指定したことで、``b`` と ``d`` と同じ段に揃えられています。

``rank`` 属性には、``same`` のほかに次の値も指定できます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 意味
   * - ``min``、``max``
     - 指定したノードを、最も上の段（``min``）または最も下の段（``max``）に並べます。ほかのノードも同じ段に置かれることがあります。
   * - ``source``、``sink``
     - 指定したノードだけを、最も上の段（``source``）または最も下の段（``sink``）に並べます。

ノードの間隔
------------

ノードの間隔は、グラフの属性で指定します。単位はインチです。

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 属性
     - 既定値
     - 意味
   * - ``nodesep``
     - 0.25
     - 同じ段の中のノードどうしの間隔。
   * - ``ranksep``
     - 0.5
     - 段と段の間隔。

図が窮屈に見える場合は、これらの値を大きくします。

エッジの重み
------------

``weight`` 属性は、エッジを短くまっすぐに描くことの重要度を表します。既定値は 1 で、大きい値を指定したエッジほど、短くまっすぐに描かれやすくなります。

.. literalinclude:: ../examples/dot/ch07_weight.dot
   :language: dot
   :caption: examples/dot/ch07_weight.dot

.. graphviz:: ../examples/dot/ch07_weight.dot
   :align: center

``weight`` を指定しない場合は、``b`` と ``c`` が ``a`` の左右に対称に置かれます。``a -> b`` に大きい ``weight`` を指定すると、``b`` が ``a`` の真下に置かれ、``a -> b`` がまっすぐに描かれます。処理の主な流れを 1 本の直線で見せたい場合に便利です。

段の決定から除く
----------------

dot は、エッジの始点のノードを終点のノードより上の段に置こうとします。``constraint=false`` を指定したエッジは、この段の決定に使われなくなります。

.. literalinclude:: ../examples/dot/ch07_constraint.dot
   :language: dot
   :caption: examples/dot/ch07_constraint.dot

.. graphviz:: ../examples/dot/ch07_constraint.dot
   :align: center

このグラフから ``constraint=false`` を取り除くと、次のように ``write_docs`` と ``publish`` が ``test`` の下の段に押し下げられ、2 つのチームの作業が 1 列につながってしまいます。

.. graphviz::
   :align: center

   digraph constraint_off {
       node [shape=box];
       design -> implement -> test;
       write_docs -> publish;
       test -> write_docs [style=dashed, label="feedback"];
   }

``constraint=false`` は、補足的な関係を表すエッジや、流れを逆にたどる「戻り」のエッジに指定すると、主な流れの配置を崩さずに済みます。

ポート
------

エッジは、既定ではノードの中心に向かって引かれ、ノードの外形との交点でつながります。``ノード:方角`` の形でポートを指定すると、ノードのどの位置にエッジをつなぐかを指定できます。

.. literalinclude:: ../examples/dot/ch07_ports.dot
   :language: dot
   :caption: examples/dot/ch07_ports.dot

.. graphviz:: ../examples/dot/ch07_ports.dot
   :align: center

方角には ``n``\ （上）、``ne``\ （右上）、``e``\ （右）、``se``\ （右下）、``s``\ （下）、``sw``\ （左下）、``w``\ （左）、``nw``\ （左上）、``c``\ （中央）を指定できます。``rankdir`` を変えても、方角は図の上下左右のままです。

record シェイプや HTML 風ラベルでは、フィールドやセルに付けたポート名を使って ``user:group`` のように書きます（6 章）。``user:group:e`` のように、ポート名の後ろに方角を続けることもできます。

エッジの描き方
--------------

``splines`` 属性で、エッジの線の描き方を指定します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 値
     - 意味
   * - ``spline``
     - 滑らかな曲線で描きます。既定値です。
   * - ``polyline``
     - 折れ線で描きます。
   * - ``line``
     - 直線で描きます。ノードと重なることがあります。
   * - ``ortho``
     - 水平線と垂直線だけで描きます。
   * - ``curved``
     - 弧を描く曲線で描きます。
   * - ``none``
     - エッジを描きません。

.. literalinclude:: ../examples/dot/ch07_splines.dot
   :language: dot
   :caption: examples/dot/ch07_splines.dot

.. graphviz:: ../examples/dot/ch07_splines.dot
   :align: center

``ortho`` は構成図などで見栄えがよくなりますが、エッジの ``label`` とポートには対応していません。``ortho`` でエッジにラベルを付けたい場合は、``label`` の代わりに ``xlabel`` を使います。

見えないノードとエッジ
----------------------

``style=invis`` を指定したノードやエッジは、描画されませんが、配置の計算には使われます。これを利用すると、図に表れない制約を加えて配置を整えられます。

.. literalinclude:: ../examples/dot/ch07_invisible.dot
   :language: dot
   :caption: examples/dot/ch07_invisible.dot

.. graphviz:: ../examples/dot/ch07_invisible.dot
   :align: center

見えないエッジ ``step1 -> step2 -> step3`` がない場合、3 組のノードはすべて同じ段に置かれ、横 1 列に並びます。見えないエッジを加えたことで、``step1``、``step2``、``step3`` が上から順に並んでいます。

ただし、見えないノードやエッジを多用すると、DOT ファイルが読みにくくなり、ノードを追加したときに配置が崩れやすくなります。まずは ``rankdir`` や ``rank=same`` などの属性で調整し、それでも足りない場合に使うようにしましょう。

同じ段の中の並び順
------------------

同じ段の中のノードの並び順は、エッジの交差が少なくなるように dot が決めるため、書いた順になるとは限りません。``ordering=out`` をグラフに指定すると、同じノードから出るエッジの終点が、エッジを書いた順に左から並ぶようになります。ツリー図で子ノードの順番を揃えたい場合に使います。
