.. _ch-directives-roles:

======================
ディレクティブとロール
======================

reST と Sphinx の機能の多くは、:term:`ディレクティブ`\ と\ :term:`ロール`\ という 2 つの仕組みで提供されています。この章では、2 つの仕組みの書き方と、表、数式、脚注、目次などのよく使うディレクティブとロールを説明します。

ディレクティブとロールの書き方
==============================

ディレクティブは、段落や図などのブロック単位の要素を作る仕組みです。``..`` と半角空白に続けてディレクティブ名を書き、``::`` で終えます。

.. code-block:: rst
   :linenos:

   .. figure:: images/build_flow.svg
      :alt: Sphinx がドキュメントを生成する流れの図
      :width: 100%

      Sphinx がドキュメントを生成する流れ

ディレクティブは次の要素で構成されます。

- 引数：1 行目の ``::`` の後に書く値です。この例では画像のパスです。
- オプション：2 行目以降に ``:名前: 値`` の形で書く設定です。
- 内容：オプションの後に空行を挟んで書くブロックです。この例ではキャプションです。

オプションと内容は、ディレクティブ名の先頭にそろえて字下げします。字下げの幅は 3 文字が一般的です。

ロールは、文章の一部に意味を持たせる仕組みです。``:ロール名:`` の直後に、バッククォートで囲んだ文字列を続けます。

.. code-block:: rst
   :linenos:

   円の面積は :math:`\pi r^2` です。詳しくは :ref:`ch-autodoc` を参照してください。

この例では、``math`` ロールで数式を、``ref`` ロールで章への参照を書いています。

.. _sec-table:

表
==

表を書く方法はいくつかありますが、本書では ``list-table`` ディレクティブをお勧めします。``list-table`` では、表を入れ子のリストとして書きます。外側のリストの項目が行、内側のリストの項目がセルになります。

.. code-block:: rst
   :linenos:

   .. list-table:: 拡張子と言語
      :header-rows: 1
      :widths: 30 70

      * - 拡張子
        - 言語
      * - ``.rst``
        - reStructuredText
      * - ``.md``
        - Markdown

このソースファイルは、次のように表示されます。

.. list-table:: 拡張子と言語
   :header-rows: 1
   :widths: 30 70

   * - 拡張子
     - 言語
   * - ``.rst``
     - reStructuredText
   * - ``.md``
     - Markdown

``list-table`` の主なオプションを\ :numref:`table-list-table-options` に示します。

.. _table-list-table-options:

.. list-table:: list-table の主なオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``:header-rows:``
     - 見出しにする行の数を指定します。
   * - ``:stub-columns:``
     - 見出しにする列の数を指定します。
   * - ``:widths:``
     - 各列の幅の比率を、空白で区切った数値で指定します。
   * - ``:align:``
     - 表の配置を ``left``、``center``、``right`` のいずれかで指定します。

reST には、罫線を文字で描く ``grid`` 形式や ``simple`` 形式の表もあります。これらの形式では、セルの幅を文字数でそろえる必要があります。全角文字と半角文字が混ざるとそろえにくく、表が崩れる原因になるため、日本語のドキュメントでは ``list-table`` を使うほうが安全です。CSV のデータを表にする場合は、``csv-table`` ディレクティブも使えます。

.. _sec-math:

数式
====

数式は、LaTeX の記法で書きます。独立した行に数式を表示するには ``math`` ディレクティブを、文章中に数式を書くには ``math`` ロールを使います。

.. code-block:: rst
   :linenos:

   2 次方程式 :math:`ax^2 + bx + c = 0` の解は、次の式で求められます。

   .. math::
      :label: eq-quadratic

      x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

   式 :eq:`eq-quadratic` は解の公式と呼ばれます。

このソースファイルは、次のように表示されます。

2 次方程式 :math:`ax^2 + bx + c = 0` の解は、次の式で求められます。

.. math::
   :label: eq-quadratic

   x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}

式 :eq:`eq-quadratic` は解の公式と呼ばれます。

``:label:`` オプションを付けると数式に番号が振られ、``eq`` ロールで参照できます。``math`` ディレクティブの中で空行を挟むと、それぞれが別の数式として表示されます。複数行の数式の位置をそろえるには、``aligned`` 環境などを使います。

.. code-block:: rst
   :linenos:

   .. math::

      \begin{aligned}
      (a + b)^2 &= a^2 + 2ab + b^2 \\
      (a - b)^2 &= a^2 - 2ab + b^2
      \end{aligned}

このソースファイルは、次のように表示されます。

.. math::

   \begin{aligned}
   (a + b)^2 &= a^2 + 2ab + b^2 \\
   (a - b)^2 &= a^2 - 2ab + b^2
   \end{aligned}

HTML の出力では、特に設定しなくても ``sphinx.ext.mathjax`` 拡張機能が使われ、ブラウザ上で MathJax というライブラリが数式を描画します。MathJax は既定では外部のサーバーから読み込まれるため、インターネットに接続していない環境では数式が表示されません。その場合は、MathJax のファイルを ``_static`` に置いて ``mathjax_path`` で指定するか、数式を画像に変換する ``sphinx.ext.imgmath`` 拡張機能を使います。

脚注
====

脚注は、本文に ``[#]_`` と書き、同じソースファイルの中に ``.. [#]`` で始まる脚注の本文を書きます。番号は自動で振られます。

.. code-block:: rst
   :linenos:

   Sphinx は Python の公式ドキュメントのために開発されました\ [#]_。

   .. [#] Python 2.6 のドキュメントから Sphinx が使われています。

1 行目では、脚注の記号の前に空白を表示しないよう、バックスラッシュと半角空白の組み合わせを入れています（:ref:`sec-inline-markup`）。このソースファイルは、次のように表示されます。

Sphinx は Python の公式ドキュメントのために開発されました\ [#python26]_。

.. [#python26] Python 2.6 のドキュメントから Sphinx が使われています。

脚注の本文は、ページの末尾にまとめて表示されます。

.. _sec-toctree:

目次（toctree）
===============

:term:`toctree` ディレクティブは、ドキュメント全体の構造を定義します。``toctree`` の内容に並べたソースファイルが、そのソースファイルの下位のページになり、目次や前後のページへのリンクが作られます。本書のトップページ（``index.rst``）には、次の ``toctree`` を書いています。

.. code-block:: rst
   :linenos:

   .. toctree::
      :maxdepth: 2
      :numbered:
      :caption: 目次

      introduction
      install
      rest_basics

ソースファイルは、拡張子を省いたパスで指定します。:numref:`table-toctree-options` に、``toctree`` の主なオプションを示します。

.. _table-toctree-options:

.. list-table:: toctree の主なオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``:maxdepth:``
     - 目次に表示する見出しの深さを指定します。
   * - ``:numbered:``
     - 章や節に番号を振ります。
   * - ``:caption:``
     - 目次の上にタイトルを表示します。
   * - ``:hidden:``
     - その場所には目次を表示せず、ドキュメントの構造の定義だけを行います。
   * - ``:glob:``
     - ``chapters/*`` のようなパターンでソースファイルを指定できるようにします。

どの ``toctree`` からもたどれないソースファイルがあると、「document isn't included in any toctree」という警告が出ます。単独のページとしてだけ使うソースファイルでは、ファイルの先頭に ``:orphan:`` と書くと、この警告を抑止できます。

その他のよく使うディレクティブ
==============================

ここまでに紹介したもののほかに、次のディレクティブもよく使います。

.. list-table:: その他のよく使うディレクティブ
   :header-rows: 1
   :widths: 30 70

   * - ディレクティブ
     - 説明
   * - ``include``
     - 別のファイルの内容を、その場所に取り込みます。複数のページで共通の文章を使うときに便利です。
   * - ``only``
     - ``.. only:: html`` のように書くと、指定した形式で出力するときだけ内容を表示します。
   * - ``glossary``
     - 用語集を作ります（:ref:`sec-glossary-term`）。
   * - ``rubric``
     - 目次に表示されない小見出しを作ります。

``include`` で取り込むファイルの拡張子を ``.rst`` にすると、そのファイルも単独のソースファイルとしてビルドされてしまいます。取り込み専用のファイルは ``.inc`` などの別の拡張子にするか、``conf.py`` の ``exclude_patterns`` でビルドの対象から外します。
