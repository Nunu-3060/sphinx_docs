入出力
======

標準入出力やファイルの読み書きを行うための関数群。

print
-----

標準出力にオブジェクトを出力する。

.. code-block:: python
   :linenos:

   >>> print("Hello", "World", sep=", ")
   Hello, World

input
-----

標準入力から 1 行読み取り、末尾の改行を除いた文字列を返す。

.. code-block:: python
   :linenos:

   >>> name = input("お名前は？: ")

open
----

ファイルを開き、ファイルオブジェクトを返す。``with`` 文と組み合わせて使うのが一般的である。テキストモードでは ``encoding`` を省略するとプラットフォーム依存のエンコーディング（Windows ではシステムのコードページなど）が使われるため、``encoding="utf-8"`` のように明示するのがよい。

.. code-block:: python
   :linenos:

   >>> with open("sample.txt", encoding="utf-8") as f:
   ...     content = f.read()

書き込みを行う場合は、モードに ``"w"`` を指定する。

.. code-block:: python
   :linenos:

   >>> with open("memo.txt", "w", encoding="utf-8") as f:
   ...     f.write("hello\n")
   6
