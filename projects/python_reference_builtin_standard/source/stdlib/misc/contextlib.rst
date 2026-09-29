contextlib
==========

``with`` 文で使うコンテキストマネージャを作成・利用するためのユーティリティを
提供するモジュール。``__enter__`` / ``__exit__`` を持つクラスを自作しなくても、
ジェネリック関数から簡単にコンテキストマネージャを定義できる。

@contextmanager
---------------

ジェネレータ関数に ``@contextmanager`` を付けることで、``yield`` を境に
「前処理」と「後処理」を書くだけでコンテキストマネージャを定義できる。

.. code-block:: python

   from contextlib import contextmanager

   @contextmanager
   def timer(label):
       import time
       start = time.time()
       print(f"{label}: start")
       yield
       print(f"{label}: {time.time() - start:.3f}s")

   >>> with timer("task"):
   ...     sum(range(1000000))
   task: start
   task: 0.012s

例外が発生した場合でも後処理を確実に実行したいときは、``yield`` を ``try`` / ``finally`` で囲む。

.. code-block:: python

   @contextmanager
   def open_resource(name):
       print(f"open {name}")
       try:
           yield name
       finally:
           print(f"close {name}")

   >>> with open_resource("file.txt") as r:
   ...     raise ValueError("oops")
   open file.txt
   close file.txt
   Traceback (most recent call last):
       ...
   ValueError: oops

suppress()
----------

指定した例外が発生してもプログラムを止めずに無視したい場合に使う。``try`` / ``except`` / ``pass`` を書くよりも簡潔に意図を表現できる。

.. code-block:: python

   from contextlib import suppress
   import os

   with suppress(FileNotFoundError):
       os.remove("not_exist.txt")

   print("続行される")

closing()
---------

``close()`` メソッドは持つが、コンテキストマネージャとしては実装されていない
オブジェクトを ``with`` 文で扱えるようにする。

.. code-block:: python

   from contextlib import closing
   from urllib.request import urlopen

   with closing(urlopen("https://example.com")) as page:
       html = page.read()

.. note::

   ファイルオブジェクトなど、多くの標準ライブラリのオブジェクトは
   すでにコンテキストマネージャとして実装されているため ``closing()`` は
   不要である。``close()`` はあるが ``__enter__`` / ``__exit__`` を
   持たない古いスタイルの API に対して使うことが多い。

ExitStack()
-----------

使用するコンテキストマネージャの数が実行時まで決まらない場合や、複数の後処理を一つの ``with`` ブロックにまとめたい場合には ``ExitStack`` が便利。``enter_context()`` で登録したコンテキストマネージャは、登録した順とは逆順に、``with`` ブロックを抜ける際にまとめて後処理される。

.. code-block:: python

   from contextlib import ExitStack

   def process_all(paths):
       with ExitStack() as stack:
           files = [stack.enter_context(open(p)) for p in paths]
           # files はブロックを抜ける際に、開いた順とは逆順にすべて close される
           return [f.read() for f in files]

その他のユーティリティ
------------------------

``ExitStack`` とは別に、覚えておくと便利な小さなユーティリティをまとめる。

.. note::

   標準出力・標準エラー出力を一時的に別の場所へ差し替えたい場合は ``redirect_stdout``/``redirect_stderr`` が使える。

   .. code-block:: python

      from contextlib import redirect_stdout
      import io

      buf = io.StringIO()
      with redirect_stdout(buf):
          print("captured")

.. note::

   条件によってコンテキストマネージャを使うかどうかを切り替えたい場合、何もしないコンテキストマネージャとして ``nullcontext`` を使うと、``if`` 文で ``with`` の対象を分岐させるコードを書かずに済む。

   .. code-block:: python

      from contextlib import nullcontext

      cm = lock if use_lock else nullcontext()
      with cm:
          ...  # use_lock が False でも同じコードで書ける
