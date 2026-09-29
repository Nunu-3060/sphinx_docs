.. _ch-output-publish:

==============
出力形式と公開
==============

この章では、HTML 以外の形式での出力と、ドキュメントを Web で公開する方法、ドキュメントの多言語化の概要を説明します。

.. _sec-builders:

ビルダーの種類
==============

Sphinx は、:term:`ビルダー`\ を切り替えることで、同じソースファイルからさまざまな形式のドキュメントを出力します。ビルダーは ``sphinx-build`` の ``-b`` オプション（``-M`` の場合は最初の引数）で指定します。主なビルダーを\ :numref:`table-builders` に示します。

.. _table-builders:

.. list-table:: 主なビルダー
   :header-rows: 1
   :widths: 25 75

   * - ビルダー
     - 出力
   * - ``html``
     - ソースファイルごとに HTML ファイルを出力します。
   * - ``dirhtml``
     - ソースファイルごとにディレクトリを作り、その中に ``index.html`` を出力します。URL の末尾に ``.html`` が付かなくなります。
   * - ``singlehtml``
     - ドキュメント全体を 1 つの HTML ファイルに出力します。
   * - ``latex``
     - LaTeX のファイルを出力します。PDF を作るときに使います。
   * - ``epub``
     - 電子書籍の EPUB ファイルを出力します。
   * - ``text``
     - プレーンテキストを出力します。
   * - ``man``
     - Unix の man ページを出力します。
   * - ``gettext``
     - 翻訳用のメッセージカタログ（``.pot`` ファイル）を出力します。
   * - ``linkcheck``
     - ドキュメントの外部へのリンクが有効かどうかを確認します（:ref:`sec-linkcheck`）。
   * - ``doctest``
     - ドキュメントの中のコード例をテストします。

PDF の出力
==========

Sphinx は、LaTeX を経由して PDF を作ります。PDF を作るには、TeX Live などの LaTeX の環境を別にインストールしておく必要があります。LaTeX の環境があれば、次のコマンドで LaTeX のファイルの出力から PDF の作成までをまとめて実行できます。

.. code-block:: text
   :linenos:

   sphinx-build -M latexpdf source build

PDF は ``build/latex`` に出力されます。``language`` が ``"ja"`` の場合、LaTeX のエンジンには日本語に対応した upLaTeX が既定で使われます。使うエンジンは ``conf.py`` の ``latex_engine`` で変更できます。

HTML ではきれいに表示されていても、PDF では表の列の幅や長い行の折り返しの調整が必要になる場合があります。PDF でも配布するドキュメントは、HTML と PDF の両方で表示を確認するようにします。

.. _sec-github-pages:

GitHub Pages での公開
=====================

GitHub Pages は、GitHub のリポジトリの内容を Web サイトとして公開するサービスです。Sphinx で作った HTML は、GitHub Pages でそのまま公開できます。GitHub Pages で公開する方法には、ブランチの内容を公開する方法と、GitHub Actions でビルドして公開する方法の 2 つがあります。

ブランチの内容を公開する方法
----------------------------

ビルドした HTML をリポジトリの特定のブランチやディレクトリに置き、その内容を公開する方法です。この方法では、GitHub Pages が公開の前に Jekyll という静的サイトジェネレーターで内容を処理します。Jekyll は ``_`` で始まるディレクトリを公開の対象から外すため、Sphinx が出力する ``_static`` などのディレクトリが公開されず、ページのデザインが崩れてしまいます。

これを防ぐには、公開するディレクトリの直下に ``.nojekyll`` という空のファイルを置き、Jekyll による処理を無効にします。``sphinx.ext.githubpages`` 拡張機能を有効にすると、HTML をビルドするたびに ``.nojekyll`` が出力先に作られます。本書の ``conf.py`` でも、この拡張機能を有効にしています。

.. code-block:: python
   :linenos:

   extensions = ["sphinx.ext.githubpages"]

``html_baseurl`` に独自のドメインの URL を指定している場合、この拡張機能は GitHub Pages で独自のドメインを使うための ``CNAME`` ファイルも出力します。

GitHub Actions で公開する方法
-----------------------------

GitHub Actions でドキュメントをビルドし、その結果を公開する方法です。ビルドした HTML をリポジトリに含める必要がなく、ソースファイルを更新するたびに自動で公開されます。この方法では Jekyll による処理は行われません。

次のファイルを、リポジトリの ``.github/workflows/docs.yml`` として置きます。このファイルは :download:`workflow_sample.yml <../examples/workflow_sample.yml>` からダウンロードできます。

.. literalinclude:: ../examples/workflow_sample.yml
   :language: yaml
   :linenos:
   :caption: workflow_sample.yml

このワークフローは、``main`` ブランチに変更がプッシュされるたびに次の処理を行います。

1. ``build`` ジョブ（17〜30 行目）：リポジトリの内容を取得して Python の環境を用意し、HTML をビルドします。ビルドした HTML は、公開用の成果物としてアップロードします。
2. ``deploy`` ジョブ（32〜40 行目）：アップロードした成果物を GitHub Pages に公開します。

27 行目では ``-W`` オプションを指定して、警告が出た場合はビルドを失敗させ、問題のあるドキュメントが公開されないようにしています。25 行目でインストールする ``requirements.txt`` には、ビルドに必要なパッケージを書いておきます。

.. code-block:: text
   :linenos:
   :caption: requirements.txt

   sphinx
   sphinx-rtd-theme
   sphinx-copybutton

ワークフローで使うアクションのバージョンは、それぞれのアクションのリポジトリで最新のものを確認してください。

Read the Docs での公開
======================

`Read the Docs <https://about.readthedocs.com/>`_ は、ドキュメントのビルドと公開を行うサービスです。GitHub などのリポジトリと連携すると、変更をプッシュするたびにドキュメントが自動でビルドされます。ソフトウェアのバージョンごとにドキュメントを公開したり、プルリクエストごとにプレビューを作ったりする機能もあります。

Read the Docs でビルドするには、リポジトリのルートに ``.readthedocs.yaml`` という設定ファイルを置きます。このファイルは :download:`readthedocs_sample.yaml <../examples/readthedocs_sample.yaml>` からダウンロードできます。

.. literalinclude:: ../examples/readthedocs_sample.yaml
   :language: yaml
   :linenos:
   :caption: readthedocs_sample.yaml

11〜13 行目で ``conf.py`` の場所を指定し、警告が出た場合はビルドを失敗させる設定にしています。15〜17 行目では、ビルドの前にインストールするパッケージを指定しています。

多言語化
========

Sphinx には、ドキュメントを翻訳する仕組みがあります。原文のソースファイルはそのままに、翻訳した文を別のファイルで管理します。翻訳のファイルの管理には、sphinx-intl というツールを使うと便利です。

まず、``conf.py`` に翻訳のファイルを置くディレクトリを指定します。

.. code-block:: python
   :linenos:

   locale_dirs = ["locale/"]
   gettext_compact = False

次に、翻訳の作業を次の手順で行います。この例では英語に翻訳します。

.. code-block:: text
   :linenos:

   python -m pip install sphinx-intl
   sphinx-build -b gettext source build/gettext
   sphinx-intl update -p build/gettext -l en -d source/locale
   sphinx-build -b html -D language=en source build/html/en

1. 1 行目：sphinx-intl をインストールします。
2. 2 行目：``gettext`` ビルダーで、翻訳の対象の文を集めた ``.pot`` ファイルを作ります。
3. 3 行目：sphinx-intl で、``.pot`` ファイルから英語用の ``.po`` ファイルを ``source/locale/en/LC_MESSAGES`` に作ります。この ``.po`` ファイルに翻訳した文を書き込みます。
4. 4 行目：``language`` を ``en`` にしてビルドすると、翻訳した文を使った HTML が出力されます。

原文を更新したときは、2 行目と 3 行目を実行し直すと、``.po`` ファイルに新しい文が追加されます。
