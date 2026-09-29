textwrap
========

長いテキストを指定した幅で折り返したり、インデントを整えたりするための
モジュール。ログ出力や CLI のヘルプメッセージなど、整形されたテキストを
生成する際に使う。

textwrap.wrap
-------------

テキストを指定した幅（既定は 70 文字）で折り返し、行のリストとして返す。

.. code-block:: python

   >>> import textwrap
   >>> text = "The quick brown fox jumps over the lazy dog"
   >>> textwrap.wrap(text, width=20)
   ['The quick brown fox', 'jumps over the lazy', 'dog']

textwrap.fill
-------------

``wrap`` と同様に折り返しを行うが、結果を改行 ``\n`` で連結した1 つの文字列として返す。

.. code-block:: python

   >>> print(textwrap.fill(text, width=20))
   The quick brown fox
   jumps over the lazy
   dog

textwrap.shorten
----------------

テキストを指定した幅に収まるように短縮し、収まりきらない場合は末尾の
単語を省略記号（既定は ``' [...]'``。先頭に半角スペースを含む）に
置き換える。複数の空白は 1 つにまとめられる。

.. code-block:: python

   >>> textwrap.shorten("Hello   world, this is a long sentence", width=20)
   'Hello world, [...]'
   >>> textwrap.shorten("Hello world", width=20)
   'Hello world'

textwrap.dedent
---------------

複数行文字列に共通する先頭の空白（インデント）を取り除く。三重引用符で
インデントして書いた文字列リテラルを整形する際によく使う。

.. code-block:: python

   >>> s = """\
   ...     line1
   ...     line2
   ...         line3
   ...     """
   >>> print(textwrap.dedent(s))
   line1
   line2
       line3

textwrap.indent
----------------

各行の先頭に指定した接頭辞を付加する。``predicate`` を渡すと、
どの行に接頭辞を付けるかを条件で制御できる（既定では空行には付けない）。

.. code-block:: python

   >>> print(textwrap.indent("line1\nline2\n", "> "))
   > line1
   > line2

   >>> print(textwrap.indent("line1\n\nline2\n", "> ", predicate=lambda line: True))
   > line1
   >
   > line2
