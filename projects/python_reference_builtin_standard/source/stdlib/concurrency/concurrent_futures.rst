concurrent.futures
===================

スレッドやプロセスを用いた並行・並列処理を、統一された高レベル API（``Executor``）で扱うためのモジュール。``threading`` や ``multiprocessing`` を直接使うよりも簡潔に、非同期に実行したタスクの結果を取り扱うことができる。

ThreadPoolExecutor
--------------------

スレッドのプールを使って処理を並行実行する。ファイル I/O やネットワーク
アクセスのような I/O バウンドな処理に向いている。

.. code-block:: python

   >>> from concurrent.futures import ThreadPoolExecutor
   >>> import time
   >>>
   >>> def fetch(url):
   ...     time.sleep(1)  # ネットワーク遅延を模したもの
   ...     return f"{url} のデータ"
   ...
   >>> urls = ["http://a.example", "http://b.example", "http://c.example"]
   >>> with ThreadPoolExecutor(max_workers=3) as executor:
   ...     results = list(executor.map(fetch, urls))
   ...
   >>> results
   ['http://a.example のデータ', 'http://b.example のデータ', 'http://c.example のデータ']

ProcessPoolExecutor
----------------------

プロセスのプールを使って処理を並列実行する。GIL の影響を受けないため、CPU バウンドな計算処理を複数コアで高速化したい場合に向いている。インタフェースは ``ThreadPoolExecutor`` とほぼ同じ。

.. code-block:: python

   >>> from concurrent.futures import ProcessPoolExecutor
   >>>
   >>> def is_prime(n):
   ...     if n < 2:
   ...         return False
   ...     return all(n % i for i in range(2, int(n ** 0.5) + 1))
   ...
   >>> if __name__ == "__main__":
   ...     numbers = [1000003, 1000033, 1000037]
   ...     with ProcessPoolExecutor() as executor:
   ...         results = list(executor.map(is_prime, numbers))
   ...     print(results)
   ...
   [True, True, True]

.. note::

   ``ProcessPoolExecutor`` に渡す関数も、``multiprocessing`` と同様に pickle 可能である必要がある。つまりモジュールのトップレベルで定義された（import 可能な）関数でなければならず、ラムダ式や関数内で定義したクロージャ、対話モードでその場に定義した関数は使えない。詳しくは :doc:`multiprocessing` を参照。

submit と Future
-------------------

``map()`` が複数の入力に同じ関数を適用するのに対し、``submit()`` は1 つのタスクを投入し、その結果を表す ``Future`` オブジェクトを即座に返す。``Future.result()`` を呼ぶと、タスクの完了まで待って結果を取得する。

.. code-block:: python

   >>> with ThreadPoolExecutor(max_workers=2) as executor:
   ...     future = executor.submit(fetch, "http://d.example")
   ...     print(future.done())  # まだ完了していないかもしれない
   ...     print(future.result())  # 完了を待って結果を取得
   ...
   False
   http://d.example のデータ

as_completed
--------------

複数のタスクを ``submit()`` した場合、完了した順に結果を処理したい
ことがある。``as_completed()`` は、渡された ``Future`` の集合の中から
完了したものを順次イテレートする。

.. code-block:: python

   >>> from concurrent.futures import as_completed
   >>>
   >>> with ThreadPoolExecutor(max_workers=3) as executor:
   ...     futures = {executor.submit(fetch, url): url for url in urls}
   ...     for future in as_completed(futures):
   ...         url = futures[future]
   ...         print(f"{url} -> {future.result()}")
   ...

例外の伝播
------------

ワーカー内のタスクで例外が発生しても、その場でエラーが表面化するわけ
ではない。例外は ``Future`` に保持され、``Future.result()`` を呼び出した時点で再送出される。``Future.exception()`` を使うと、例外を発生させずにその例外オブジェクトを取得できる（例外が発生していなければ ``None`` を返す）。タスクが失敗していても ``result()`` を呼ぶまで気づかない、というのはよくある落とし穴である。

.. code-block:: python

   >>> def fail():
   ...     raise ValueError("boom")
   ...
   >>> with ThreadPoolExecutor() as executor:
   ...     future = executor.submit(fail)
   ...     print(future.exception())
   ...
   boom

   >>> with ThreadPoolExecutor() as executor:
   ...     future = executor.submit(fail)
   ...     future.result()
   ...
   Traceback (most recent call last):
       ...
   ValueError: boom

.. note::

   ``ThreadPoolExecutor`` と ``ProcessPoolExecutor`` は同じ ``Executor`` インタフェース（``submit`` / ``map`` / ``shutdown``）を共有しているため、I/O バウンドな処理か CPU バウンドな処理かに応じて、コードをほとんど変更せずに切り替えることができる。より細かく低レベルな制御が必要な場合は :doc:`threading` や :doc:`multiprocessing` を、非同期 I/O を中心に設計する場合は :doc:`asyncio` を検討するとよい。
