.. _ch-rest-basics:

=======================
reStructuredText の基本
=======================

この章では、Sphinx のソースファイルを書くための :term:`reStructuredText`\ （reST）の基本的な記法を説明します。ここで紹介する記法をまとめたサンプルを :download:`rest_sample.rst <../examples/rest_sample.rst>` として用意しています。

reST は、Python の Docutils というライブラリが解釈するマークアップ言語です。Sphinx は Docutils の機能をもとに、複数のファイルにまたがる目次や相互参照などの機能を追加しています。

.. _sec-paragraph:

段落と改行
==========

段落は空行で区切ります。空行を挟まずに改行した場合、改行は段落の区切りにならず、半角空白に置き換えられます。

英語の文章では単語の間に空白が入るため問題になりませんが、日本語の文章では不自然な空白が表示されます。次の例では、「ドキュメントを」と「生成する」の間に空白が入ります。

.. code-block:: rst
   :linenos:

   Sphinx はソースファイルからドキュメントを
   生成するツールです。

日本語の段落は途中で改行せず、1 つの段落を 1 行で書くと、この問題を避けられます。

.. _sec-inline-markup:

インライン記法
==============

文章の一部を装飾するには、:numref:`table-inline-markup` の記法を使います。

.. _table-inline-markup:

.. list-table:: 主なインライン記法
   :header-rows: 1
   :widths: 40 30 30

   * - 記法
     - 表示
     - 用途
   * - ``*強調*``
     - *強調*
     - 強調（斜体）
   * - ``**強い強調**``
     - **強い強調**
     - 強い強調（太字）
   * - ````リテラル````
     - ``リテラル``
     - コードやファイル名
   * - ```Sphinx <https://www.sphinx-doc.org/>`_``
     - `Sphinx <https://www.sphinx-doc.org/>`_
     - 外部へのリンク

インライン記法は、前後に空白または句読点がないと認識されません。そのため、日本語の文章中で次のように書くと、記号がそのまま表示されます。

.. code-block:: rst
   :linenos:

   設定は``conf.py``に書きます。

インライン記法の前後に半角空白を入れるか、空白を表示したくない場合は、バックスラッシュと半角空白の組み合わせ（``\`` の後に空白）を入れます。バックスラッシュと半角空白の組み合わせは、出力には何も表示されません。

.. code-block:: rst
   :linenos:

   設定は ``conf.py`` に書きます。
   設定は\ ``conf.py``\ に書きます。

1 行目は「設定は conf.py に書きます。」のように前後に空白が入った状態で表示され、2 行目は空白なしで表示されます。「、」「。」「（」「）」などの全角の句読点や括弧に接している場合は、空白を入れなくても認識されます。

外部へのリンクの書き方は、:ref:`sec-external-link`\ で詳しく説明します。

.. _sec-heading:

見出し
======

見出しは、見出しの文字列の下に記号を並べた行を置いて表します。上下の両方に記号の行を置くこともできます。

.. code-block:: rst
   :linenos:

   ==========
   章の見出し
   ==========

   節の見出し
   ==========

   項の見出し
   ----------

見出しの階層は、記号の種類と登場する順番で決まります。ファイルの中で最初に使った記号が第 1 階層、次に使った記号が第 2 階層になります。特定の記号が特定の階層を表すわけではないため、プロジェクト全体で記号の使い方を統一しておくと混乱を防げます。本書では、章に上下の ``=``、節に下だけの ``=``、項に ``-``、その下の階層に ``^`` を使っています。

記号の行は、見出しの文字列と同じ長さ以上にする必要があります。短いと警告が出ます。全角文字は半角文字 2 文字分の長さとして数えられるため、日本語の見出しでは記号を多めに並べておくと安全です。

.. _sec-list:

リスト
======

箇条書きは ``-``、``*``、``+`` のいずれかで始めます。番号付きリストは ``1.`` のような数字で始めるか、``#.`` と書いて番号を自動で振ります。

.. code-block:: rst
   :linenos:

   - 箇条書きの項目
   - 箇条書きの項目

     - 入れ子の項目

   #. 番号付きリストの項目
   #. 番号付きリストの項目

入れ子にする場合は、4 行目のように親の項目の本文の開始位置にそろえて字下げし、前後に空行を入れます。

用語とその説明を並べる場合は、定義リストを使います。用語の次の行を字下げして説明を書きます。

.. code-block:: rst
   :linenos:

   toctree
      ドキュメントの構造を定義するディレクティブ。

   autodoc
      docstring からドキュメントを生成する拡張機能。

.. _sec-code:

コード
======

段落の末尾に ``::`` を付けると、続く字下げしたブロックがそのまま表示されます（リテラルブロック）。言語を指定して構文を強調表示したり、行番号を付けたりする場合は、``code-block`` :term:`ディレクティブ`\ を使います。

.. code-block:: rst
   :linenos:

   .. code-block:: python
      :linenos:
      :emphasize-lines: 2
      :caption: greet.py

      def greet(name: str) -> str:
          return f"こんにちは、{name} さん"

このソースファイルは、次のように表示されます。

.. code-block:: python
   :linenos:
   :emphasize-lines: 2
   :caption: greet.py

   def greet(name: str) -> str:
       return f"こんにちは、{name} さん"

:numref:`table-code-block-options` に、``code-block`` の主なオプションを示します。

.. _table-code-block-options:

.. list-table:: code-block の主なオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``:linenos:``
     - 行番号を表示します。
   * - ``:lineno-start:``
     - 行番号の開始値を指定します。
   * - ``:emphasize-lines:``
     - 強調する行を ``2,4-6`` のように指定します。
   * - ``:caption:``
     - コードの上にタイトルを表示します。
   * - ``:name:``
     - 相互参照用のラベルを付けます。

ファイルの内容をそのまま表示する場合は、``literalinclude`` ディレクティブを使います。コードをドキュメントに貼り付ける必要がないため、コードを修正したときにドキュメントの更新を忘れる心配がありません。``:pyobject:`` オプションを使うと、Python のファイルから特定の関数やクラスだけを取り出せます。

.. code-block:: rst
   :linenos:

   .. literalinclude:: ../examples/sample_package/shapes.py
      :pyobject: total_area
      :linenos:

このソースファイルは、次のように表示されます。

.. literalinclude:: ../examples/sample_package/shapes.py
   :pyobject: total_area
   :linenos:

``literalinclude`` のパスは、ソースファイルのあるディレクトリからの相対パスで指定します。``/`` で始めると、ソースディレクトリからのパスになります。``:lines:`` オプションで表示する行を指定したり、``:start-after:`` と ``:end-before:`` オプションで、指定した文字列の間だけを表示したりすることもできます。

.. _sec-image:

画像と図
========

画像を表示するには ``image`` ディレクティブを、キャプション付きの図にするには ``figure`` ディレクティブを使います。

.. code-block:: rst
   :linenos:

   .. figure:: images/build_flow.svg
      :alt: Sphinx がドキュメントを生成する流れの図
      :width: 100%

      Sphinx がドキュメントを生成する流れ

``figure`` ディレクティブでは、オプションの後に空行を挟んで書いた段落がキャプションになります。``:alt:`` オプションには、画像を表示できない環境や読み上げ機能のための説明を書きます。この例は\ :numref:`fig-build-flow` のように表示されます。図に番号を付けて参照する方法は\ :ref:`sec-numref`\ で説明します。

.. _sec-admonition:

注記
====

補足や注意を目立たせるには、注記のディレクティブを使います。

.. code-block:: rst
   :linenos:

   .. note::

      補足情報を書きます。

   .. warning::

      注意すべき点を書きます。

このソースファイルは、次のように表示されます。

.. note::

   補足情報を書きます。

.. warning::

   注意すべき点を書きます。

:numref:`table-admonitions` に、よく使う注記のディレクティブを示します。

.. _table-admonitions:

.. list-table:: よく使う注記のディレクティブ
   :header-rows: 1
   :widths: 30 70

   * - ディレクティブ
     - 用途
   * - ``note``
     - 補足情報
   * - ``tip``
     - 便利な使い方
   * - ``important``
     - 重要な情報
   * - ``warning``
     - 注意すべき点
   * - ``danger``
     - データの消失など、重大な問題につながる点
   * - ``seealso``
     - 関連する情報への参照（Sphinx が追加したディレクティブ）
