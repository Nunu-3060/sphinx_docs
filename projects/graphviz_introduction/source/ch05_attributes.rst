属性
====

ノードの形や色、エッジの線の種類などは、属性で指定します。この章では、属性の指定方法と、よく使う属性を説明します。属性の一覧は付録 A にまとめています。

属性の指定方法
--------------

個別に指定する
^^^^^^^^^^^^^^

ノード文やエッジ文の後ろに ``[名前=値, ...]`` と書くと、そのノードやエッジに属性を指定できます。

.. code-block:: dot

   a [shape=box, color=red];
   a -> b [style=dashed];

グラフ全体の属性は、グラフの中に ``名前=値;`` の形で書きます。

.. code-block:: dot

   digraph g {
       rankdir=LR;
       a -> b;
   }

既定値をまとめて指定する
^^^^^^^^^^^^^^^^^^^^^^^^

属性文 ``node [...]``、``edge [...]``、``graph [...]`` を使うと、ノード、エッジ、グラフの既定の属性をまとめて指定できます。

.. literalinclude:: ../examples/dot/ch05_default_attrs.dot
   :language: dot
   :caption: examples/dot/ch05_default_attrs.dot

.. graphviz:: ../examples/dot/ch05_default_attrs.dot
   :align: center

``c`` の塗りつぶしの色は、既定の ``lightyellow`` ではなく、個別に指定した ``lightblue`` になっています。このように、個別に指定した属性は既定の属性より優先されます。

属性文の効果は、その属性文より後に作られたノードやエッジにだけ及びます。属性文より前に作られたノードやエッジには適用されません。属性文はグラフの先頭に書くようにしましょう。

値の単位
^^^^^^^^

属性の値の単位は、属性によって異なります。特に、大きさの単位がインチであることに注意してください。

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 属性の例
     - 単位
     - 既定値の例
   * - ``width``、``height``、``nodesep``、``ranksep``
     - インチ
     - ノードの ``width`` は 0.75、``height`` は 0.5
   * - ``fontsize``
     - ポイント
     - 14
   * - ``penwidth``
     - ポイント
     - 1

ノードの形
----------

ノードの形は ``shape`` 属性で指定します。既定値は ``ellipse``\ （楕円）です。よく使う形を次に示します。

.. literalinclude:: ../examples/dot/ch05_shapes.dot
   :language: dot
   :caption: examples/dot/ch05_shapes.dot

.. graphviz:: ../examples/dot/ch05_shapes.dot
   :align: center

ノードの大きさは、既定ではラベルが収まるように自動的に広がります。``fixedsize=true`` を指定すると、``width`` と ``height`` で指定した大きさに固定されます。この例では、形を比べやすくするために大きさを揃えています。

主な形の用途は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 形
     - 主な用途
   * - ``box``
     - 処理、コンポーネントなど。最もよく使われます。
   * - ``ellipse``、``circle``
     - 一般的なノード、状態など。
   * - ``diamond``
     - フローチャートの分岐。
   * - ``cylinder``
     - データベース、ストレージ。
   * - ``note``、``folder``
     - ファイル、フォルダー。
   * - ``plaintext``
     - 枠を描かずにラベルだけを表示します。

ほかの形は付録 B で紹介します。

スタイル
--------

``style`` 属性で、ノードの塗りつぶしや角の丸め、線の種類を指定します。複数のスタイルを組み合わせる場合は、``style="rounded,filled"`` のようにカンマで区切り、二重引用符で囲みます。

.. literalinclude:: ../examples/dot/ch05_styles.dot
   :language: dot
   :caption: examples/dot/ch05_styles.dot

.. graphviz:: ../examples/dot/ch05_styles.dot
   :align: center

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - スタイル
     - 対象
     - 意味
   * - ``filled``
     - ノード
     - ``fillcolor`` で指定した色で塗りつぶします。
   * - ``rounded``
     - ノード
     - 角を丸めます。``box`` などの角のある形に使います。
   * - ``solid``、``dashed``、``dotted``、``bold``
     - ノード、エッジ
     - 実線、破線、点線、太線で描きます。
   * - ``invis``
     - ノード、エッジ
     - 描画しません。配置の調整に使います（7 章）。

色
--

色に関する主な属性は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 属性
     - 意味
   * - ``color``
     - ノードの枠線、エッジの線の色。
   * - ``fillcolor``
     - ノードの塗りつぶしの色。``style=filled`` を指定したときに使われます。
   * - ``fontcolor``
     - 文字の色。
   * - ``bgcolor``
     - グラフ全体の背景色。

色は、次のいずれかの方法で指定します。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 方法
     - 例
     - 備考
   * - 色名
     - ``red``、``steelblue``
     - 使える色名は、公式ドキュメントの Color Names（付録 D）で確認できます。
   * - ``#RRGGBB``
     - ``"#2E8B57"``
     - 赤、緑、青を 16 進数 2 桁ずつで指定します。
   * - ``#RRGGBBAA``
     - ``"#2E8B5780"``
     - 末尾の 2 桁で透明度を指定します。``00`` が透明、``FF`` が不透明です。

``#`` で始まる値は二重引用符で囲む必要があります。

.. literalinclude:: ../examples/dot/ch05_colors.dot
   :language: dot
   :caption: examples/dot/ch05_colors.dot

.. graphviz:: ../examples/dot/ch05_colors.dot
   :align: center

``penwidth`` は線の太さをポイントで指定します。``style=bold`` より細かく太さを調整したいときに使います。

矢印
----

有向グラフのエッジの矢印の形は ``arrowhead`` 属性で、始点側の矢印の形は ``arrowtail`` 属性で指定します。また、``dir`` 属性で矢印を付ける側を指定します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ``dir`` の値
     - 意味
   * - ``forward``
     - 終点側に矢印を付けます。有向グラフの既定値です。
   * - ``back``
     - 始点側に矢印を付けます。
   * - ``both``
     - 両側に矢印を付けます。
   * - ``none``
     - 矢印を付けません。無向グラフの既定値です。

.. literalinclude:: ../examples/dot/ch05_arrows.dot
   :language: dot
   :caption: examples/dot/ch05_arrows.dot

.. graphviz:: ../examples/dot/ch05_arrows.dot
   :align: center

``dir=back`` は、ノードの配置は ``a -> b`` の向きのまま、矢印だけを逆向きにしたい場合に使います。``arrowtail`` は ``dir`` が ``back`` か ``both`` のときにだけ表示されます。ほかの矢印の形は付録 B で紹介します。

フォントと日本語
----------------

文字のフォントは ``fontname`` 属性で、大きさは ``fontsize`` 属性で指定します。既定のフォントは ``Times-Roman`` で、日本語の文字を含みません。日本語のラベルを使う場合は、日本語を含むフォントを ``fontname`` で指定してください。指定しないと、環境によっては日本語が「□」のように表示されます。

.. literalinclude:: ../examples/dot/ch05_japanese.dot
   :language: dot
   :caption: examples/dot/ch05_japanese.dot

.. graphviz:: ../examples/dot/ch05_japanese.dot
   :align: center

``fontname`` は、グラフ、ノード、エッジのそれぞれに指定する必要があります。``graph`` に指定したフォントはグラフのラベルとクラスター（8 章）のラベルに、``node`` に指定したフォントはノードのラベルに、``edge`` に指定したフォントはエッジのラベルに使われます。

日本語を含む主なフォントの名前は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - OS
     - フォント名の例
   * - Windows
     - ``Meiryo``、``Yu Gothic``
   * - macOS
     - ``Hiragino Sans``
   * - Linux
     - ``Noto Sans CJK JP``\ （フォントのインストールが必要な場合があります）

SVG 形式で出力した場合、フォントは画像に埋め込まれず、フォント名だけが記録されます。そのため、閲覧する環境にそのフォントがない場合は、ブラウザーが別のフォントで表示します。本資料のサンプルでは ``Meiryo`` を指定しているため、Windows 以外の環境では、文字の幅と枠の大きさがわずかにずれて表示されることがあります。
