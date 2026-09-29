.. _ch-configuration:

==================
conf.py による設定
==================

Sphinx のプロジェクトの設定は、ソースディレクトリにある ``conf.py`` に書きます。この章では、``conf.py`` の仕組みと、よく使う設定値を説明します。よく使う設定をまとめたサンプルを :download:`conf_sample.py <../examples/conf_sample.py>` として用意しています。本書自体の設定ファイルも :download:`conf.py <conf.py>` からダウンロードできます。

conf.py の仕組み
================

``conf.py`` は、Sphinx の起動時に Python のコードとして実行されます。モジュールの変数として定義した値が、そのまま設定値になります。Python のコードなので、``import`` 文でモジュールを読み込んだり、環境変数に応じて設定を切り替えたりすることもできます。

``conf.py`` に書いていない設定値には、既定値が使われます。設定値の一覧と既定値は、Sphinx の公式ドキュメントの\ `設定 <https://www.sphinx-doc.org/ja/master/usage/configuration.html>`_\ のページで確認できます。

ビルドのときに一時的に設定値を変えたい場合は、``sphinx-build`` の ``-D`` オプションを使います。次の例では、``conf.py`` の内容にかかわらず、``language`` を ``en`` にしてビルドします。

.. code-block:: text
   :linenos:

   sphinx-build -b html -D language=en source build/html

プロジェクト情報
================

ドキュメントの名前や著者などの情報を設定します。これらの値は、ページのタイトルやフッターなどに表示されます。

.. list-table:: プロジェクト情報の設定値
   :header-rows: 1
   :widths: 30 70

   * - 設定値
     - 説明
   * - ``project``
     - ドキュメントの名前です。
   * - ``author``
     - 著者名です。
   * - ``copyright``
     - フッターに表示される著作権表示です。``"2026, author"`` のように書きます。
   * - ``release``
     - ``1.0.0`` のような、バージョンの完全な表記です。
   * - ``version``
     - ``1.0`` のような、バージョンの短い表記です。

言語
====

``language`` には、ドキュメントの言語を指定します。``"ja"`` を指定すると、次の効果があります。

- 「図 1.1」のような図表の番号の表記や、索引、検索結果のページなど、Sphinx が生成する文言が日本語になります。テーマが独自に表示する文言は、テーマの翻訳の状況によって異なります。本書で使っている sphinx_rtd_theme では、「Previous」「Next」などの一部の文言が英語のまま表示されます。
- 検索機能が日本語の単語の区切りに対応し、日本語の文章を検索できるようになります。

拡張機能
========

``extensions`` には、有効にする\ :term:`拡張機能`\ のモジュール名をリストで指定します。Sphinx に付属する拡張機能は ``sphinx.ext.`` で始まる名前です。

.. code-block:: python
   :linenos:

   extensions = [
       "sphinx.ext.autodoc",
       "sphinx.ext.napoleon",
       "sphinx_copybutton",
   ]

3 行目の ``sphinx.ext.napoleon`` は付属の拡張機能、4 行目の ``sphinx_copybutton`` は pip で別にインストールするサードパーティの拡張機能です。指定したモジュールは ``import`` できる必要があります。拡張機能については\ :ref:`ch-extensions`\ で詳しく説明します。

HTML 出力の設定
===============

HTML の出力に関する設定値は ``html_`` で始まります。主な設定値を\ :numref:`table-html-options` に示します。

.. _table-html-options:

.. list-table:: HTML 出力の主な設定値
   :header-rows: 1
   :widths: 30 70

   * - 設定値
     - 説明
   * - ``html_theme``
     - 使用する\ :term:`テーマ`\ の名前です。
   * - ``html_theme_options``
     - テーマ固有の設定を辞書で指定します。指定できる項目はテーマによって異なります。
   * - ``html_title``
     - ページのタイトルです。省略すると ``project`` と ``release`` から作られます。
   * - ``html_static_path``
     - CSS や画像などの静的ファイルを置くディレクトリのリストです。中身は出力先の ``_static`` にコピーされます。
   * - ``html_css_files``
     - 追加で読み込む CSS ファイルのリストです。``html_static_path`` からの相対パスで指定します。
   * - ``html_logo``
     - サイドバーなどに表示するロゴ画像です。
   * - ``html_show_sourcelink``
     - ``True`` の場合、各ページにソースファイルを表示するリンクを付けます。既定値は ``True`` です。
   * - ``html_copy_source``
     - ``True`` の場合、ソースファイルを出力先の ``_sources`` にコピーします。既定値は ``True`` です。

HTML の利用者にソースファイルを見せたくない場合は、``html_show_sourcelink`` と ``html_copy_source`` の両方を ``False`` にします。``html_show_sourcelink`` だけを ``False`` にすると、リンクは表示されなくなりますが、ソースファイルは ``_sources`` にコピーされるため、URL を直接指定すれば閲覧できてしまいます。本書もこの 2 つを ``False`` にしています。

.. _sec-theme:

テーマ
======

HTML の見た目は\ :term:`テーマ`\ で決まります。Sphinx には ``alabaster``\ （既定のテーマ）、``classic``、``nature`` などのテーマが付属しています。サードパーティのテーマもあり、本書では Read the Docs で広く使われている ``sphinx_rtd_theme`` を使っています。

サードパーティのテーマを使うには、pip でインストールしてから ``html_theme`` にテーマの名前を指定します。

.. code-block:: text
   :linenos:

   python -m pip install sphinx-rtd-theme

.. code-block:: python
   :linenos:

   html_theme = "sphinx_rtd_theme"

ほかにも、``furo`` や ``pydata-sphinx-theme`` などのテーマがよく使われています。テーマごとの見た目は、`Sphinx Themes Gallery <https://sphinx-themes.org/>`_ で比較できます。

ビルドの対象と警告の扱い
========================

ソースディレクトリの中に、ビルドの対象にしたくないファイルがある場合は、``exclude_patterns`` にパターンを指定します。

.. code-block:: python
   :linenos:

   exclude_patterns = ["drafts/*", "**/_*.rst"]

ビルド時の警告の扱いは、``sphinx-build`` のオプションで変えられます。

.. list-table:: 警告に関する sphinx-build のオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``-W``
     - 警告をエラーとして扱います。ビルドは最後まで続き、すべての警告を表示した後に失敗として終了します。CI で使うと、警告のあるドキュメントの公開を防げます。
   * - ``-w ファイル名``
     - 警告を指定したファイルにも書き出します。
   * - ``-n``
     - 参照先が見つからない相互参照をすべて警告します。``conf.py`` に ``nitpicky = True`` と書くのと同じです。
   * - ``-q``
     - 警告とエラー以外のメッセージを表示しません。

警告の読み方は\ :ref:`sec-warnings`\ で説明します。

conf.py のサンプル
==================

ここまでに説明した設定をまとめると、次のようになります。

.. literalinclude:: ../examples/conf_sample.py
   :language: python
   :linenos:
   :caption: conf_sample.py

11 行目の ``sys.path`` への追加は、:term:`autodoc` がモジュールを ``import`` できるようにするためのものです。詳しくは\ :ref:`sec-sys-path`\ で説明します。
