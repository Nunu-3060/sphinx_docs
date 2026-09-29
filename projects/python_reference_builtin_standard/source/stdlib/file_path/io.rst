io
==

ストリーム（入出力）を扱うための基盤となるモジュール。組み込み関数 ``open()`` が返すファイルオブジェクトも、実はこのモジュールで定義されたクラス（``TextIOWrapper`` や ``BufferedReader`` など）のインスタンスである。メモリ上にファイルのように振る舞うオブジェクトを作れるため、ディスクに実際のファイルを作らずに入出力処理をテストしたい場合によく利用される。

io.StringIO
------------

メモリ上に文字列を保持するテキストストリーム。``open()`` で開いたテキストファイルと同じように ``read`` / ``write`` / ``readline`` などが使える。

.. code-block:: python

   >>> import io
   >>> buf = io.StringIO()
   >>> buf.write("Hello, ")
   7
   >>> buf.write("World!\n")
   7
   >>> buf.getvalue()
   'Hello, World!\n'
   >>> buf.seek(0)
   0
   >>> buf.readline()
   'Hello, World!\n'

io.BytesIO
-----------

メモリ上にバイト列を保持するバイナリストリーム。画像データやネットワークから受信したバイナリデータなどを、ファイルに書き出さずに処理したい場合に使う。

.. code-block:: python

   >>> import io
   >>> buf = io.BytesIO()
   >>> buf.write(b"\x89PNG\r\n")
   6
   >>> buf.getvalue()
   b'\x89PNG\r\n'
   >>> buf.seek(0)
   0
   >>> buf.read(4)
   b'\x89PNG'

ファイル入出力のユニットテストでの活用
----------------------------------------

ファイルを受け取って処理する関数をテストする際、実際にディスクへファイルを作成する代わりに ``StringIO`` / ``BytesIO`` を渡すことで、高速かつ副作用のないテストが書ける。

.. code-block:: python

   >>> def count_lines(fileobj):
   ...     return sum(1 for _ in fileobj)
   ...
   >>> import io
   >>> fake_file = io.StringIO("line1\nline2\nline3\n")
   >>> count_lines(fake_file)
   3

open() が返すオブジェクトとの関係
-----------------------------------

組み込み関数 ``open()`` は、モードに応じて ``io`` モジュールのクラスのインスタンスを返す。テキストモード（``"r"`` など）では ``io.TextIOWrapper``、バイナリモード（``"rb"`` など）では ``io.BufferedReader`` や ``io.BufferedWriter`` が返される。

.. code-block:: python

   >>> import io
   >>> f = open("source/index.rst", "r", encoding="utf-8")
   >>> isinstance(f, io.TextIOWrapper)
   True
   >>> f.close()
   >>> fb = open("source/index.rst", "rb")
   >>> isinstance(fb, io.BufferedReader)
   True
   >>> fb.close()

.. note::

   ``StringIO`` と ``BytesIO`` はどちらも ``with`` 文をサポートしているため、通常のファイルと同様に ``with io.StringIO(...) as f:`` の形で使うこともできる。
