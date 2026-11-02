Markdown のその他の活用
=======================

この章では、README や Issue 以外で Markdown を活用する方法を紹介する。Markdown で書いた文書は、他の形式に変換したり、Web サイトにしたりできる。最後に、Python のプログラムで Markdown を HTML に変換する方法を紹介する。

Pandoc で他の形式に変換する
---------------------------

:term:`Pandoc` は、文書の形式を相互に変換するコマンドラインのツールである。Markdown を HTML、Word（``.docx``）、PDF、EPUB などに変換できる。逆に、Word の文書を Markdown に変換することもできる。

.. code-block:: bash
   :linenos:
   :caption: Pandoc で Markdown を変換するコマンドの例

   pandoc report.md -o report.html
   pandoc report.md -o report.docx

``-o`` の後に出力するファイル名を書くと、拡張子から出力の形式が判断される。文書は Markdown で書いて Git で管理し、提出するときだけ Word に変換する、といった使い方ができる。PDF に変換するには、LaTeX などの別のソフトウェアが必要になる。

Web サイトを作る
----------------

Markdown で書いた複数の文書から、Web サイトを生成するツールがある。このようなツールを\ :term:`静的サイトジェネレーター`\ と呼ぶ。

.. list-table:: Markdown を使える主な静的サイトジェネレーター
   :header-rows: 1
   :widths: 25 75

   * - ツール
     - 特徴
   * - MkDocs
     - Python で作られている。プログラムのドキュメントのサイトを作るのに向く
   * - Jekyll
     - Ruby で作られている。GitHub Pages で標準的に使える
   * - Hugo
     - Go で作られている。生成が非常に速い
   * - Sphinx
     - Python で作られている。本来は reStructuredText を使うが、MyST という拡張機能を入れると Markdown でも書ける

本書は Sphinx で作っている。MyST は CommonMark を基礎にしており、Sphinx の相互参照や目次などの機能を Markdown の中で使えるように、独自の記法を加えている。

フロントマター
--------------

静的サイトジェネレーターや技術記事の投稿サービスでは、文書の先頭に、タイトルやタグなどの情報を書くことがある。この部分を\ :term:`フロントマター`\ と呼ぶ。フロントマターは ``---`` だけの行で囲み、中は :term:`YAML` という形式で「名前: 値」の組を書く。

.. md-example::
   :front-matter:

   ---
   title: Markdown の練習
   tags: [markdown, 入門]
   published: true
   ---

   # Markdown の練習

   本文はここから始まる。

フロントマターは本文としては表示されず、サイトのタイトルや記事の一覧を作るのに使われる。上の表示結果でも、フロントマターの部分は表示されていない。GitHub で ``.md`` ファイルを表示した場合は、フロントマターが表として表示される。

どの名前を書けるかは、ツールやサービスによって異なる。たとえば Zenn では記事の絵文字や種類（``emoji``、``type``）を、Jekyll ではページのレイアウト（``layout``）を書く。フロントマターに対応していない場所では、``---`` の行が区切り線や Setext 形式の見出しとして解釈され、表示が崩れるので注意する。

ノートアプリと Jupyter Notebook
-------------------------------

Jupyter Notebook では、コードのセルの他に、Markdown で文章を書くセルを作れる。プログラムの説明や、分析の考察を、見出しや箇条書きを使って書ける。数式（第 10 章）も使えるので、データ分析や機械学習の分野でよく使われる。

Obsidian などのノートアプリでは、メモを Markdown のファイルとして保存する。ファイルはただのテキストなので、アプリを使わなくなっても、他のエディタでそのまま読める。Obsidian では、``[[メモの名前]]`` と書いて他のメモへリンクするなど、独自の記法も使える。

チャットツールの記法
--------------------

Slack や Discord などのチャットツールにも、メッセージを装飾する記法がある。Markdown に似ているが、同じではない。たとえば Slack では、``*`` 1 個で挟んだ文字が太字になり、``_`` で挟んだ文字が斜体になる。Markdown では ``*`` 1 個は強調（斜体）なので、意味が異なる。

チャットツールの記法は、ツールごとに独自に決められている。Markdown と同じだと思い込まず、それぞれのツールのヘルプで確かめるとよい。

プログラムから変換する
----------------------

この節は Python の基本的な文法を知っている読者向けの発展的な内容である。Python を知らない読者は読み飛ばしてよい。

Python には、Markdown を HTML に変換するライブラリがいくつかある。ここでは、CommonMark に準拠した markdown-it-py と、その拡張機能を集めた mdit-py-plugins を使う。次のコマンドでインストールする。

.. code-block:: bash
   :linenos:

   python -m pip install markdown-it-py mdit-py-plugins

次のプログラムは、Markdown のファイルを読み込み、HTML のファイルに変換して保存する。このファイルは :download:`ch13_md_to_html.py <../examples/ch13_md_to_html.py>` からダウンロードできる。

.. literalinclude:: ../examples/ch13_md_to_html.py
   :language: python
   :linenos:
   :caption: Markdown のファイルを HTML のファイルに変換するプログラム

変換の中心は、``convert()`` 関数の 3 行である。31 行目で、CommonMark の規則で変換する ``MarkdownIt`` のオブジェクトを作り、``use(gfm_plugin)`` で GFM の記法（表、取り消し線、タスクリスト、拡張自動リンク）と、脚注、アラートを有効にしている。32 行目の ``render()`` メソッドで Markdown のソースを HTML に変換し、33 行目で HTML の文書の枠組み（``TEMPLATE``）に埋め込んでいる。

次のように、変換する Markdown のファイルと、出力する HTML のファイルを指定して実行する。

.. code-block:: console
   :linenos:

   $ python ch13_md_to_html.py README.md README.html
   README.md を README.html に変換した。

出力された ``README.html`` をブラウザで開くと、Markdown の表示結果が表示される。このプログラムが出力する HTML には見た目の指定（CSS）がないので、表示は簡素になる。

実は、本書の表示結果も、同じ仕組みで作っている。本書を HTML に変換するときに、Markdown の例を markdown-it-py で HTML に変換し、その結果を枠で囲んでページに埋め込んでいる。
