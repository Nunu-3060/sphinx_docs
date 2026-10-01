第 9 章 ファイルの入出力
========================

ファイルを開く
--------------

Python でファイルを読み書きするには、``open`` 関数を使用します。``open`` 関数は、``with`` 文と組み合わせて使うことで、処理が終わったときに自動的にファイルを閉じられます。ファイルを開いたまま忘れてしまうことがなくなるため、ファイル操作では ``with`` 文を使うことをお勧めします。

.. code-block:: python
   :linenos:

   with open("memo.txt", mode="w", encoding="utf-8") as file:
       file.write("こんにちは\n")

``mode`` 引数には、次のような値を指定します。

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

ファイルへの書き込み
--------------------

複数行のテキストをファイルに書き込む場合は、次のようにループを使って 1 行ずつ書き込みます。

.. code-block:: python
   :linenos:

   lines = ["1 行目です。", "2 行目です。", "3 行目です。"]
   with open("memo.txt", mode="w", encoding="utf-8") as file:
       for line in lines:
           file.write(line + "\n")

ファイルの読み込み
------------------

ファイルの内容を読み込む場合は、``mode="r"`` を指定して ``open`` 関数を呼び出します。ファイルオブジェクトに対して ``for`` 文を使うと、ファイルの内容を 1 行ずつ取り出せます。

.. code-block:: python
   :linenos:

   with open("memo.txt", mode="r", encoding="utf-8") as file:
       for line in file:
           print(line.rstrip("\n"))

pathlib モジュールの利用
------------------------

ファイルパスを扱う際は、標準ライブラリの ``pathlib`` モジュールを使うと便利です。文字列を ``+`` で連結してパスを組み立てる方法もありますが、``pathlib`` モジュールの ``Path`` クラスを使うと、``/`` 演算子でパスを組み立てられるうえ、Windows と macOS、Linux など OS ごとのパスの区切り文字の違いを意識する必要がなくなります。

.. code-block:: python
   :linenos:

   from pathlib import Path

   file_path = Path("data") / "memo.txt"
   print(file_path)  # data\memo.txt（Windows の場合）

``Path`` オブジェクトは、組み込みの ``open`` 関数の代わりに、``open`` メソッドでファイルを開けます。

.. code-block:: python
   :linenos:

   with file_path.open(mode="r", encoding="utf-8") as file:
       content = file.read()

このほかにも、``Path`` オブジェクトには、ファイルが存在するかを確認する ``exists`` メソッドや、ファイル名だけを取り出す ``name`` 属性など、ファイルパスの操作に役立つ機能が数多く用意されています。

.. code-block:: python
   :linenos:

   print(file_path.exists())  # ファイルが存在すれば True、存在しなければ False
   print(file_path.name)      # memo.txt

一時ファイルの利用（tempfile モジュール）
------------------------------------------

動作確認のためだけにファイルを作成すると、パソコン上に不要なファイルが残ってしまいます。標準ライブラリの ``tempfile`` モジュールを使うと、一時的なディレクトリを作成し、``with`` 文のブロックを抜けたときに自動的に削除できます。

.. code-block:: python
   :linenos:

   import tempfile
   from pathlib import Path

   with tempfile.TemporaryDirectory() as temp_dir:
       file_path = Path(temp_dir) / "memo.txt"
       with file_path.open(mode="w", encoding="utf-8") as file:
           file.write("一時ファイルの内容です。\n")

``tempfile.TemporaryDirectory()`` は、一時的なディレクトリを作成し、そのパスを文字列として返します。``with`` 文のブロックを抜けると、作成したディレクトリとその中身は自動的に削除されます。後述のサンプルコードでも、このモジュールを利用しています。

サンプルコード
--------------

一時ディレクトリにファイルを作成し、書き込みと読み込みを行うサンプルコードです。実行しても、パソコン上に余分なファイルが残らないように、一時ディレクトリを利用しています。

:download:`file_io.py <../../examples/ch09_file_io/file_io.py>`

.. literalinclude:: ../../examples/ch09_file_io/file_io.py
   :language: python3
   :linenos:
