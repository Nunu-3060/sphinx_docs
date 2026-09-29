Python から使う
===============

この章では、Python の graphviz パッケージを使ってグラフを生成する方法を説明します。graphviz パッケージは、Python のメソッド呼び出しから DOT 言語のテキストを組み立て、Graphviz 本体のコマンドを呼び出して画像に出力するライブラリです。4 章～8 章で説明した DOT 言語の知識が、そのまま使えます。

グラフを組み立てる
------------------

主なクラスとメソッドは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Python
     - 対応する DOT
     - 意味
   * - ``graphviz.Graph(name)``
     - ``graph name { }``
     - 無向グラフを作ります。
   * - ``graphviz.Digraph(name)``
     - ``digraph name { }``
     - 有向グラフを作ります。
   * - ``g.node(id, label, **attrs)``
     - ``id [label=...]``
     - ノードを追加します。
   * - ``g.edge(tail, head, label, **attrs)``
     - ``tail -> head [label=...]``
     - エッジを追加します。
   * - ``g.edges([(tail, head), ...])``
     - ``tail -> head`` を並べたもの
     - 属性を持たないエッジをまとめて追加します。
   * - ``g.attr(**attrs)``
     - ``名前=値``
     - グラフの属性を指定します。
   * - ``g.attr("node", **attrs)``
     - ``node [...]``
     - ノードの既定の属性を指定します。``"edge"`` を指定するとエッジの既定の属性になります。

次のサンプルは、注文処理の流れを表す有向グラフを組み立てます。

.. literalinclude:: ../examples/py/ch10_digraph_basics.py
   :language: python
   :caption: examples/py/ch10_digraph_basics.py

実行すると、次の DOT が表示されます。

.. literalinclude:: ../build/generated/ch10_digraph_basics.gv
   :language: dot

.. graphviz:: ../build/generated/ch10_digraph_basics.gv
   :align: center

コードと出力された DOT を見比べると、次のことがわかります。

* ``Digraph`` の引数 ``graph_attr``、``node_attr``、``edge_attr`` は、それぞれ DOT の ``graph [...]``、``node [...]``、``edge [...]`` になります。
* ``node()`` と ``edge()`` のキーワード引数は、そのまま DOT の属性になります。
* ID やラベルに空白や日本語などが含まれる場合は、自動的に二重引用符で囲まれます。文字列の中の二重引用符も自動的にエスケープされます。

属性の値には文字列を渡します。``fontsize="10"`` のように、数値の属性も文字列で指定してください。数値を渡すと ``TypeError`` 例外が発生します。

属性の名前が Python の予約語と同じ場合は、キーワード引数として書けません。その場合は、``_attributes`` 引数に辞書で渡します。たとえば、SVG の要素に CSS のクラスを付ける ``class`` 属性は ``g.node("a", _attributes={"class": "important"})`` のように指定します。

サブグラフとクラスター
----------------------

サブグラフは、``subgraph()`` メソッドを ``with`` 文と組み合わせて作ります。``with`` のブロックの中で追加したノードやエッジが、そのサブグラフに入ります。名前を ``cluster`` で始めるとクラスターになるのは、DOT と同じです。

プログラムからグラフを生成する利点は、データの構造をそのまま図にできることです。次のサンプルは、システムの層とコンポーネント、呼び出し関係をデータとして持ち、そこからクラスターを持つグラフを組み立てます。

.. literalinclude:: ../examples/py/ch10_subgraph.py
   :language: python
   :caption: examples/py/ch10_subgraph.py

.. graphviz:: ../build/generated/ch10_subgraph.gv
   :align: center

層やコンポーネントが増えても、データを変更するだけで図を更新できます。

画像に出力する
--------------

組み立てたグラフは、次のメソッドで出力します。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド、プロパティ
     - 意味
   * - ``g.source``
     - DOT のテキストを文字列で返します。
   * - ``g.render(outfile="out.svg")``
     - DOT ファイルと画像ファイルを出力します。出力形式は ``outfile`` の拡張子で決まります。DOT ファイルは、拡張子を ``.gv`` に変えた名前で出力されます。戻り値は画像ファイルのパスです。
   * - ``g.pipe(format="svg")``
     - ファイルに保存せず、画像のデータを ``bytes`` で返します。Web アプリケーションで画像を返す場合などに使います。
   * - ``g.view()``
     - 画像を出力し、OS の既定のアプリケーションで開きます。

レイアウトエンジンは、``Digraph("name", engine="neato")`` のように作成時に指定するか、``g.engine = "neato"`` のように後から指定します。

``render()`` などで画像を出力する際に、Graphviz 本体の ``dot`` コマンドが見つからないと、``graphviz.ExecutableNotFound`` 例外が発生します。この例外が発生した場合は、2 章を参照して Graphviz 本体のインストールと PATH の設定を確認してください。``g.source`` で DOT のテキストを取り出すだけであれば、Graphviz 本体は必要ありません。

既存の DOT ファイルを読み込む
-----------------------------

手で書いた DOT ファイルを Python から画像に変換したい場合は、``graphviz.Source`` クラスを使います。

.. code-block:: python

   import graphviz

   source = graphviz.Source.from_file("ch03_hello.dot")
   source.render(outfile="ch03_hello.svg")

``graphviz.Source("digraph { a -> b }")`` のように、DOT の文字列から作ることもできます。

Jupyter で表示する
------------------

Jupyter Notebook や JupyterLab では、グラフのオブジェクトをセルの最後の式に書くと、図がそのまま表示されます。図を見ながらグラフを組み立てられるので、試行錯誤するときに便利です。

.. code-block:: python

   import graphviz

   g = graphviz.Digraph()
   g.edge("Hello", "World")
   g  # セルの最後に書くと図が表示される

パッケージを使わずに DOT を生成する
-----------------------------------

DOT はテキストなので、graphviz パッケージを使わずに文字列として組み立てることもできます。追加のパッケージをインストールできない環境や、ほかのプログラミング言語に移植する場合に役立ちます。

この場合に注意が必要なのは、ID やラベルのエスケープです。次のサンプルは、二重引用符やバックスラッシュを含むタスク名を、正しくエスケープして DOT を組み立てます。

.. literalinclude:: ../examples/py/ch10_dot_from_string.py
   :language: python
   :caption: examples/py/ch10_dot_from_string.py

生成される DOT と図は次のとおりです。

.. literalinclude:: ../build/generated/ch10_dot_from_string.gv
   :language: dot

.. graphviz:: ../build/generated/ch10_dot_from_string.gv
   :align: center

``quote()`` では、先にバックスラッシュを ``\\`` に置き換えてから、二重引用符を ``\"`` に置き換えています。順序を逆にすると、二重引用符のエスケープに使ったバックスラッシュまで ``\\`` に置き換えられ、``\\"`` という誤った文字列になってしまいます。

バックスラッシュをエスケープしないと、``C:\release`` の ``\r`` が右揃えの改行と解釈され、ラベルが正しく表示されません（6 章）。graphviz パッケージは二重引用符を自動的にエスケープしますが、バックスラッシュは ``\l`` などの改行に使えるように、そのまま出力します。graphviz パッケージでバックスラッシュを文字として表示したい場合は、``graphviz.escape()`` 関数でエスケープしてから渡してください。
