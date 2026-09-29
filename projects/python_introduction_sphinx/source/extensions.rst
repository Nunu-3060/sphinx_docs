.. _ch-extensions:

==============
拡張機能の活用
==============

Sphinx の機能は、:term:`拡張機能`\ を追加することで広げられます。この章では、Sphinx に付属する拡張機能、サードパーティの拡張機能、そして自作の拡張機能について説明します。

拡張機能の仕組み
================

拡張機能は、``setup`` という関数を持つ Python のモジュールです。``conf.py`` の ``extensions`` にモジュール名を指定すると、Sphinx は起動時にそのモジュールを ``import`` し、``setup`` 関数を呼び出します。拡張機能は ``setup`` 関数の中で、新しいディレクティブやロール、ビルダー、設定値などを Sphinx に登録します。

付属の拡張機能
==============

Sphinx には、:numref:`table-builtin-extensions` の拡張機能が付属しています。追加のインストールは必要ありません。

.. _table-builtin-extensions:

.. list-table:: Sphinx に付属する主な拡張機能
   :header-rows: 1
   :widths: 35 65

   * - 拡張機能
     - 説明
   * - ``sphinx.ext.autodoc``
     - docstring からドキュメントを生成します（:ref:`ch-autodoc`）。
   * - ``sphinx.ext.autosummary``
     - モジュールのメンバーの一覧表を生成します。
   * - ``sphinx.ext.napoleon``
     - Google 形式と NumPy 形式の docstring に対応します。
   * - ``sphinx.ext.doctest``
     - ドキュメントの中のコード例をテストします。
   * - ``sphinx.ext.viewcode``
     - Python のソースコードのページを生成し、API ドキュメントからリンクします。
   * - ``sphinx.ext.intersphinx``
     - 外部のドキュメントへの相互参照を可能にします（:ref:`sec-intersphinx`）。
   * - ``sphinx.ext.extlinks``
     - よく使う URL を短いロールで書けるようにします。
   * - ``sphinx.ext.todo``
     - 執筆中の作業メモを書く ``todo`` ディレクティブを追加します。
   * - ``sphinx.ext.graphviz``
     - Graphviz で描いた図を埋め込みます。Graphviz のインストールが別に必要です。
   * - ``sphinx.ext.mathjax``
     - HTML で数式を MathJax で描画します。HTML の出力では既定で有効です。
   * - ``sphinx.ext.imgmath``
     - 数式を画像に変換して埋め込みます。LaTeX のインストールが別に必要です。
   * - ``sphinx.ext.githubpages``
     - GitHub Pages で公開するための ``.nojekyll`` ファイルを出力します（:ref:`sec-github-pages`）。

例えば ``sphinx.ext.extlinks`` を使うと、Python の Issue へのリンクを次のように短く書けます。

.. code-block:: python
   :linenos:

   extensions = ["sphinx.ext.extlinks"]

   extlinks = {
       "issue": ("https://github.com/python/cpython/issues/%s", "gh-%s"),
   }

この設定で ``:issue:`12345``` と書くと、``https://github.com/python/cpython/issues/12345`` への「gh-12345」というリンクになります。

サードパーティの拡張機能
========================

PyPI では、多くのサードパーティの拡張機能が公開されています。ここでは、本書で使っている sphinx-copybutton と、Markdown を使えるようにする MyST-Parser を紹介します。

sphinx-copybutton
-----------------

コードの右上に、コードをクリップボードにコピーするボタンを追加します。本書のコードの例にも、このボタンが表示されています。

.. code-block:: text
   :linenos:

   python -m pip install sphinx-copybutton

.. code-block:: python
   :linenos:

   extensions = ["sphinx_copybutton"]

既定の設定では、``:linenos:`` で表示した行番号はコピーされません。コマンドの例に ``$`` などのプロンプトを付けている場合は、``copybutton_prompt_text`` にプロンプトの文字列を指定すると、プロンプトを除いてコピーできます。

.. _sec-myst:

MyST-Parser
-----------

`MyST-Parser <https://myst-parser.readthedocs.io/>`_ は、Sphinx で :term:`MyST` という Markdown の拡張記法を使えるようにする拡張機能です。reST と Markdown のソースファイルを 1 つのプロジェクトに混在させることもできます。本書の動作確認環境にはインストールしていないため、ここでは概要だけを紹介します。

.. code-block:: text
   :linenos:

   python -m pip install myst-parser

.. code-block:: python
   :linenos:

   extensions = ["myst_parser"]

拡張機能を有効にすると、拡張子が ``.md`` のファイルもソースファイルとして読み込まれます。MyST では、ディレクティブをコードブロックの記法で書きます。

.. code-block:: markdown
   :linenos:

   # 見出し

   本文は Markdown で書きます。**太字** や `コード` も使えます。

   ```{note}
   ディレクティブは、言語名の代わりに {ディレクティブ名} と書いたコードブロックで表します。
   ```

   ロールは {ref}`sec-install` のように書きます。

MyST の記法の詳細は、MyST-Parser のドキュメントを参照してください。

.. _sec-custom-extension:

拡張機能の自作
==============

拡張機能は Python のモジュールなので、自分で書くこともできます。ここでは例として、``:github:`owner/repo``` と書くと GitHub のリポジトリへのリンクになるロールを作ります。

.. literalinclude:: ../examples/my_extension.py
   :language: python
   :linenos:
   :caption: my_extension.py

このファイルは :download:`my_extension.py <../examples/my_extension.py>` からダウンロードできます。コードの要点は次のとおりです。

- 21〜44 行目：ロールの処理を、Sphinx が提供する ``SphinxRole`` クラスを継承したクラスとして書いています。``run`` メソッドでは、ロールに渡された文字列を ``self.text`` から取り出し、リンクを表すノードを作って返します。
- 31〜39 行目：文字列が ``owner/repo`` の形式でない場合は、エラーを報告します。エラーはビルド時のメッセージに表示され、出力されたページでは該当する箇所が目立つように表示されます。
- 47〜61 行目：Sphinx が拡張機能を読み込むときに呼び出す ``setup`` 関数です。``app.add_role`` でロールを登録し、拡張機能のメタデータを返します。``parallel_read_safe`` と ``parallel_write_safe`` は、並列ビルドに対応しているかどうかを表します。

作成したモジュールを ``import`` できる場所に置き、``conf.py`` の ``extensions`` に追加すると、ロールを使えるようになります。本書でも、``examples`` ディレクトリを ``sys.path`` に追加し（:ref:`sec-sys-path`）、この拡張機能を有効にしています。

.. code-block:: rst
   :linenos:

   Sphinx のソースコードは :github:`sphinx-doc/sphinx` で公開されています。

このソースファイルは、次のように表示されます。

Sphinx のソースコードは :github:`sphinx-doc/sphinx` で公開されています。

なお、この程度の単純なリンクであれば、前に紹介した ``sphinx.ext.extlinks`` でも実現できます。入力の検証や、複雑なノードの生成が必要な場合に拡張機能を自作すると効果的です。
