最初のグラフ
============

この章では、DOT ファイルを作成して画像に変換するまでの流れを確認します。DOT 言語の文法は 4 章で詳しく説明するので、ここでは全体の流れをつかむことを目的とします。

DOT ファイルを作る
------------------

次の内容で ``ch03_hello.dot`` というファイルを作成します。文字コードは UTF-8 で保存します。

.. literalinclude:: ../examples/dot/ch03_hello.dot
   :language: dot
   :caption: examples/dot/ch03_hello.dot
   :linenos:

各行の意味は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 行
     - 意味
   * - 1
     - ``//`` から行末まではコメントです。
   * - 2
     - ``digraph`` は有向グラフ（エッジに向きがあるグラフ）を表します。``hello`` はグラフの名前で、省略もできます。グラフの内容は ``{`` と ``}`` の間に書きます。
   * - 3
     - ``Hello`` というノードから ``World`` というノードへのエッジを表します。ノードは、エッジに書くだけで自動的に作られます。

dot コマンドで画像に変換する
----------------------------

DOT ファイルがあるフォルダーで次のコマンドを実行すると、SVG 形式の画像 ``ch03_hello.svg`` が出力されます。

.. code-block:: console

   > dot -Tsvg ch03_hello.dot -o ch03_hello.svg

出力された画像をブラウザーで開くと、次の図が表示されます。

.. graphviz:: ../examples/dot/ch03_hello.dot
   :align: center

``dot`` コマンドの主なオプションは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - オプション
     - 意味
   * - ``-T形式``
     - 出力形式を指定します。``-Tsvg``、``-Tpng``、``-Tpdf`` などがあります。
   * - ``-o ファイル名``
     - 出力先のファイル名を指定します。省略すると標準出力に出力されます。
   * - ``-O``
     - 入力ファイル名に形式の拡張子を付けた名前で出力します。たとえば ``dot -Tpng -O ch03_hello.dot`` は ``ch03_hello.dot.png`` を出力します。
   * - ``-V``
     - バージョンを表示します。

出力形式の選び方
----------------

よく使う出力形式は次の 3 つです。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 形式
     - 特徴
   * - SVG
     - ベクター形式です。拡大しても劣化せず、ブラウザーでそのまま表示できます。Web ページや社内 Wiki に載せる図に向いています。
   * - PNG
     - ビットマップ形式です。どのアプリケーションでも表示できますが、拡大すると粗くなります。解像度は ``-Gdpi=150`` のように指定できます。
   * - PDF
     - ベクター形式です。印刷する資料や、LaTeX の文書に図を埋め込む場合に向いています。

迷った場合は SVG を選ぶとよいでしょう。本資料の図も SVG で出力しています。

Python から出力する
-------------------

同じ図を Python から出力することもできます。次のプログラムは、graphviz パッケージを使って同じグラフを組み立て、SVG に出力します。

.. literalinclude:: ../examples/py/ch03_first_graph.py
   :language: python
   :caption: examples/py/ch03_first_graph.py

実行すると、``output`` フォルダーに DOT ファイル ``ch03_first_graph.gv`` と画像 ``ch03_first_graph.svg`` が出力されます。DOT ファイルの内容は次のとおりです。

.. literalinclude:: ../build/generated/ch03_first_graph.gv
   :language: dot
   :caption: output/ch03_first_graph.gv

``graph.edge("Hello", "World")`` が DOT の ``Hello -> World`` に対応していることがわかります。このように、graphviz パッケージは DOT 言語のテキストを組み立てるためのライブラリです。使い方は 10 章で詳しく説明します。
