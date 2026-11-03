第 9 章 ファイルの入出力
========================

ファイルを開く
--------------

Python でファイルを読み書きするには、``open`` 関数を使用する。``open`` 関数は、``with`` 文と組み合わせて使うことで、処理が終わったときに自動的にファイルを閉じられる。ファイルを開いたまま忘れてしまうことがなくなるため、ファイル操作では ``with`` 文を使うのが一般的である。

.. code-block:: python
   :linenos:

   with open("memo.txt", mode="w", encoding="utf-8") as file:
       file.write("こんにちは\n")

``open`` 関数の第 1 引数にはファイル名を、``mode`` 引数にはファイルを開く目的を、``encoding`` 引数にはファイルの文字コードを指定する。``with 式 as 変数名:`` と書くと、開いたファイルを表すオブジェクト（ファイルオブジェクト）が変数に代入され、ブロックの中でファイルを操作できる。

``mode`` 引数には、次のような値を指定する。

.. list-table::
   :header-rows: 1

   * - mode
     - 説明
   * - ``"w"``
     - 書き込み（上書き）
   * - ``"a"``
     - 書き込み（追記）
   * - ``"r"``
     - 読み込み

``encoding`` 引数を省略した場合に使われる文字コードは、Python のバージョンや OS によって異なる。Python 3.14 以前の Windows では、日本語環境の既定の文字コード（cp932）が使われることがあり、UTF-8 で保存されたファイルを読み込むと文字化けやエラーが発生する場合がある。Python 3.15 以降は既定が UTF-8 になったが、どの環境でも同じように動作させるため、本資料では常に ``encoding="utf-8"`` を指定する。

ファイルへの書き込み
--------------------

複数行のテキストをファイルに書き込む場合は、次のようにループを使って 1 行ずつ書き込む。

.. code-block:: python
   :linenos:

   lines = ["1 行目です。", "2 行目です。", "3 行目です。"]
   with open("memo.txt", mode="w", encoding="utf-8") as file:
       for line in lines:
           file.write(line + "\n")

ファイルの読み込み
------------------

ファイルの内容を読み込む場合は、``mode="r"`` を指定して ``open`` 関数を呼び出す。ファイルオブジェクトに対して ``for`` 文を使うと、ファイルの内容を 1 行ずつ取り出せる。

.. code-block:: python
   :linenos:

   with open("memo.txt", mode="r", encoding="utf-8") as file:
       for line in file:
           print(line.rstrip("\n"))

pathlib モジュールの利用
------------------------

ファイルパスを扱う際は、標準ライブラリの ``pathlib`` モジュールを使うと便利である。文字列を ``+`` で連結してパスを組み立てる方法もあるが、``pathlib`` モジュールの ``Path`` クラスを使うと、``/`` 演算子でパスを組み立てられるうえ、Windows と macOS、Linux など OS ごとのパスの区切り文字の違いを意識する必要がなくなる。

.. code-block:: python
   :linenos:

   from pathlib import Path

   file_path = Path("data") / "memo.txt"
   print(file_path)  # data\memo.txt（Windows の場合）

``Path`` オブジェクトは、組み込みの ``open`` 関数の代わりに、``open`` メソッドでファイルを開ける。

.. code-block:: python
   :linenos:

   with file_path.open(mode="r", encoding="utf-8") as file:
       content = file.read()

このほかにも、``Path`` オブジェクトには、ファイルが存在するかを確認する ``exists`` メソッドや、ファイル名だけを取り出す ``name`` 属性など、ファイルパスの操作に役立つ機能が数多く用意されている。

.. code-block:: python
   :linenos:

   print(file_path.exists())  # ファイルが存在すれば True、存在しなければ False
   print(file_path.name)      # memo.txt

一時ファイルの利用（tempfile モジュール）
------------------------------------------

動作確認のためだけにファイルを作成すると、パソコン上に不要なファイルが残ってしまう。標準ライブラリの ``tempfile`` モジュールを使うと、一時的なフォルダを作成し、``with`` 文のブロックを抜けたときに自動的に削除できる。

.. code-block:: python
   :linenos:

   import tempfile
   from pathlib import Path

   with tempfile.TemporaryDirectory() as temp_dir:
       file_path = Path(temp_dir) / "memo.txt"
       with file_path.open(mode="w", encoding="utf-8") as file:
           file.write("一時ファイルの内容です。\n")

``tempfile.TemporaryDirectory()`` は、一時的なフォルダを作成し、``with`` 文と組み合わせると、そのパスを文字列として変数に代入する。``with`` 文のブロックを抜けると、作成したフォルダとその中身は自動的に削除される。後述のサンプルコードでも、このモジュールを利用している。

サンプルコード
--------------

一時フォルダにファイルを作成し、書き込みと読み込みを行うサンプルコードである。実行しても、パソコン上に余分なファイルが残らないように、一時フォルダを利用している。

:download:`file_io.py <../../examples/ch09_file_io/file_io.py>`

.. literalinclude:: ../../examples/ch09_file_io/file_io.py
   :language: python3
   :linenos:
