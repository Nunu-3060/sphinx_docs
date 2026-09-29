ラベル
======

ノードやエッジに表示する文字をラベルと呼びます。この章では、ラベルの指定方法と、表のような複雑なラベルを作る方法を説明します。

ラベルの種類
------------

ノードのラベルは既定ではノードの ID と同じで、エッジには既定ではラベルがありません。表示する文字は次の属性で指定します。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 属性
     - 対象
     - 表示される位置
   * - ``label``
     - ノード、エッジ、グラフ
     - ノードの中、エッジの中央付近、グラフの下（``labelloc=t`` で上）。
   * - ``xlabel``
     - ノード、エッジ
     - ノードやエッジの外側。できるだけほかの要素と重ならない位置に置かれます。
   * - ``taillabel``
     - エッジ
     - エッジの始点の近く。
   * - ``headlabel``
     - エッジ
     - エッジの終点の近く。

.. literalinclude:: ../examples/dot/ch06_edge_labels.dot
   :language: dot
   :caption: examples/dot/ch06_edge_labels.dot

.. graphviz:: ../examples/dot/ch06_edge_labels.dot
   :align: center

``taillabel`` と ``headlabel`` は、関係の多重度（「1」や「0..*」など）を表すのに便利です。ノードからの距離は ``labeldistance`` 属性で調整できます。

改行と行揃え
------------

ラベルの中では、次のエスケープシーケンスで改行できます。改行の種類によって、その行の揃え方が決まります。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 記法
     - 意味
   * - ``\n``
     - 改行し、直前の行を中央に揃えます。
   * - ``\l``
     - 改行し、直前の行を左に揃えます。
   * - ``\r``
     - 改行し、直前の行を右に揃えます。

揃え方は改行の直前の行に適用されるため、最後の行にも改行を付けておく必要があります。たとえば ``"first\lsecond"`` と書くと、``second`` の行は左揃えになりません。左揃えにしたい行は、すべて ``\l`` で終えるようにします。

.. literalinclude:: ../examples/dot/ch06_align.dot
   :language: dot
   :caption: examples/dot/ch06_align.dot

.. graphviz:: ../examples/dot/ch06_align.dot
   :align: center

ラベルでは、ほかにも次のエスケープシーケンスが使えます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 記法
     - 置き換えられる文字
   * - ``\N``
     - ノードの ID。ノードのラベルの既定値は ``\N`` です。
   * - ``\G``
     - グラフの名前。
   * - ``\T``、``\H``
     - エッジの始点、終点のノードの ID。
   * - ``\\``
     - バックスラッシュそのもの。

ラベルにバックスラッシュを表示したい場合は ``\\`` と書く必要があります。たとえば ``"C:\release"`` と書くと、``\r`` が右揃えの改行と解釈されてしまいます。

record シェイプ
---------------

``shape=record`` を指定すると、ラベルを ``|`` で区切って、ノードを複数のフィールドに分割できます。

.. literalinclude:: ../examples/dot/ch06_record.dot
   :language: dot
   :caption: examples/dot/ch06_record.dot

.. graphviz:: ../examples/dot/ch06_record.dot
   :align: center

record シェイプのラベルには、次の記法があります。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 記法
     - 意味
   * - ``|``
     - フィールドを区切ります。
   * - ``{`` と ``}``
     - 囲んだ部分の区切りの方向を、縦と横で入れ替えます。``rankdir`` が既定の ``TB`` のとき、一番外側のフィールドは横に並ぶため、縦に並べたい場合は全体を ``{`` と ``}`` で囲みます。
   * - ``<名前>``
     - フィールドにポート名を付けます。``user:group -> group:id`` のように、エッジをフィールドにつなぐときに使います。

``{``、``}``、``|``、``<``、``>`` は record シェイプの記法に使われる文字なので、文字として表示したい場合は ``\{`` のようにバックスラッシュを付けます。

HTML 風ラベル
-------------

record シェイプは手軽ですが、セルごとに色や揃え方を変えることはできません。より細かく指定したい場合は、HTML 風ラベルを使います。公式ドキュメントでも、record シェイプより HTML 風ラベルの使用が推奨されています。

HTML 風ラベルは、``label=<...>`` のように、二重引用符の代わりに ``<`` と ``>`` で囲んで書きます。中には HTML に似たタグで表を記述します。

.. literalinclude:: ../examples/dot/ch06_html_label.dot
   :language: dot
   :caption: examples/dot/ch06_html_label.dot

.. graphviz:: ../examples/dot/ch06_html_label.dot
   :align: center

HTML 風ラベルを使うノードには、``shape=plain`` を指定するのが一般的です。``plain`` は枠も余白もない形で、表の枠がそのままノードの外形になります。

主なタグと属性は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - タグ
     - 意味
   * - ``<table>``
     - 表。``border``\ （外枠の太さ）、``cellborder``\ （セルの枠の太さ）、``cellspacing``\ （セルの間隔）、``cellpadding``\ （セル内の余白）などを指定できます。
   * - ``<tr>``、``<td>``
     - 行とセル。``<td>`` には ``port``\ （ポート名）、``bgcolor``\ （背景色）、``align``\ （揃え方）、``colspan``、``rowspan`` などを指定できます。
   * - ``<b>``、``<i>``、``<u>``
     - 太字、斜体、下線。
   * - ``<font>``
     - 文字の色（``color``）、大きさ（``point-size``）、フォント（``face``）を指定します。
   * - ``<br/>``
     - 改行。``<br align="left"/>`` のように揃え方も指定できます。

HTML 風ラベルは HTML と同様に解釈されるため、``<``、``>``、``&`` を文字として表示したい場合は、``&lt;``、``&gt;``、``&amp;`` と書きます。また、閉じタグを忘れるなど、タグの対応が取れていないと構文エラーになります。

HTML 風ラベルを使った ER 図の例を 11 章で紹介します。
