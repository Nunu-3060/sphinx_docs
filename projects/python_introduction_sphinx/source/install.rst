.. _ch-install:

================================
インストールと最初のプロジェクト
================================

この章では、Sphinx をインストールし、最小構成のプロジェクトを作って HTML をビルドするまでの手順を説明します。

インストール
============

Sphinx は PyPI で公開されているため、pip でインストールできます。プロジェクトごとに仮想環境を作り、その中にインストールすることをお勧めします。

Windows では、次のコマンドを実行します。

.. code-block:: text
   :linenos:

   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install sphinx

macOS や Linux では、2 行目を次のように読み替えます。

.. code-block:: text
   :linenos:

   source .venv/bin/activate

インストールできたかどうかは、次のコマンドで確認できます。バージョン番号が表示されれば成功です。

.. code-block:: text
   :linenos:

   sphinx-build --version

.. note::

   ``sphinx-build`` コマンドが見つからない場合は、``python -m sphinx`` で代用できます。本書のバッチファイル（:ref:`sec-build-batch`）も、この形で Sphinx を呼び出しています。

.. _sec-quickstart:

プロジェクトの作成
==================

``sphinx-quickstart`` コマンドを使うと、プロジェクトに必要なファイル一式を作成できます。ドキュメントを置きたいディレクトリで、次のコマンドを実行します。

.. code-block:: text
   :linenos:

   sphinx-quickstart

コマンドを実行すると、いくつかの質問が表示されます。主な質問の意味を\ :numref:`table-quickstart` に示します。

.. _table-quickstart:

.. list-table:: sphinx-quickstart の主な質問
   :header-rows: 1
   :widths: 30 70

   * - 質問
     - 説明
   * - ソースとビルドのディレクトリを分けるか
     - ``y`` を選ぶと、ソースファイルを ``source``、出力を ``build`` に分けて置きます。ファイルの管理がしやすくなるため、本書では ``y`` を選びます。
   * - プロジェクト名
     - ドキュメントのタイトルなどに使われます。
   * - 著者名
     - 著作権表示などに使われます。
   * - リリース
     - ドキュメントの対象とするソフトウェアのバージョンです。空欄でも構いません。
   * - ドキュメントの言語
     - 日本語のドキュメントでは ``ja`` を指定します。検索機能や画面の文言が日本語向けになります。

``-q`` オプションを付けると質問を省略し、コマンドの引数で値を指定できます。次の例は、上の質問にすべて答えたものと同じ結果になります。最後の引数 ``docs`` は、プロジェクトを作成するディレクトリです。

.. code-block:: text
   :linenos:

   sphinx-quickstart -q --sep -p demo -a author -r 0.1 -l ja docs

生成されるファイル
==================

ソースとビルドのディレクトリを分けた場合、次のファイルが生成されます。

.. code-block:: text
   :linenos:

   docs/
   ├── Makefile
   ├── make.bat
   ├── build/
   └── source/
       ├── _static/
       ├── _templates/
       ├── conf.py
       └── index.rst

各ファイルとディレクトリの役割を\ :numref:`table-quickstart-files` に示します。

.. _table-quickstart-files:

.. list-table:: sphinx-quickstart が生成するファイル
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 役割
   * - ``source/conf.py``
     - プロジェクトの設定ファイルです。詳しくは :ref:`ch-configuration`\ で説明します。
   * - ``source/index.rst``
     - ドキュメントのトップページになるソースファイルです。ここに書いた :term:`toctree` から、ほかのソースファイルをたどります。
   * - ``source/_static/``
     - CSS や画像など、出力先にそのままコピーするファイルを置くディレクトリです。
   * - ``source/_templates/``
     - HTML のテンプレートを上書きするときに使うディレクトリです。
   * - ``build/``
     - ビルドの結果を出力するディレクトリです。
   * - ``Makefile``、``make.bat``
     - ビルドを簡単に実行するためのファイルです。``make.bat`` は Windows 用です。

生成された ``conf.py`` の中身は次のとおりです。本書のサンプルでは、それぞれの設定値に型ヒントを追加しています。

.. literalinclude:: ../examples/minimal_project/source/conf.py
   :language: python
   :linenos:
   :caption: minimal_project/source/conf.py

``sphinx-quickstart`` で作成したプロジェクトに、ページを 1 つ追加したものを :download:`minimal_project.zip <../examples/minimal_project.zip>` として用意しています。以降の説明を試すときに使ってください。

.. _sec-first-build:

ビルド
======

プロジェクトのディレクトリで次のコマンドを実行すると、HTML が ``build/html`` に出力されます。

.. code-block:: text
   :linenos:

   sphinx-build -M html source build

``sphinx-build`` の基本的な書式は ``sphinx-build -b ビルダー名 ソースディレクトリ 出力ディレクトリ`` です。``-M`` を指定すると、``Makefile`` から実行するときと同じ動作になり、出力先が ``build/html``、中間ファイルの保存先が ``build/doctrees`` になります。次のように ``-b`` を使っても、同じ場所に HTML を出力できます。

.. code-block:: text
   :linenos:

   sphinx-build -b html source build/html

``Makefile`` や ``make.bat`` を使う場合は、次のコマンドで同じ結果になります。Windows の PowerShell では ``.\make html`` と入力します。

.. code-block:: text
   :linenos:

   make html

ビルドが終わったら、``build/html/index.html`` をブラウザで開くと、生成されたドキュメントを確認できます。

.. _sec-build-batch:

ビルド用のバッチファイル
========================

ビルドのたびにコマンドを入力するのは手間がかかるため、手順をバッチファイルにまとめておくと便利です。本書のプロジェクトでは、次の :download:`build_html_example.bat <../build_html_example.bat>` を使っています。

.. literalinclude:: ../build_html_example.bat
   :language: bat
   :linenos:
   :caption: build_html_example.bat

このバッチファイルは、次の処理を順に行います。

1. バッチファイルのあるディレクトリに移動します（5 行目）。
2. 前回のビルド結果が残らないよう、``build`` ディレクトリがあれば削除します（8 行目）。
3. HTML をビルドします。ビルドに失敗した場合は、メッセージを表示して終了します（11〜15 行目）。
4. 生成された ``index.html`` を既定のブラウザで開きます（18 行目）。

``build`` ディレクトリを削除してからビルドすることで、差分ビルドによる表示の食い違い（:ref:`sec-incremental-build`）を防げます。
