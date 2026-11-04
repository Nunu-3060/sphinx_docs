第 7 章 concurrent.futures による統一的な書き方
===============================================

``concurrent.futures`` モジュールは、スレッドとプロセスを同じ書き方で扱うためのモジュールである。:doc:`06_processes` で使った ``ProcessPoolExecutor`` もこのモジュールに含まれている。この章では、このモジュールの使い方を詳しく説明する。

Executor と Future
------------------

``concurrent.futures`` の中心となるのは、次の 2 つの概念である。

.. list-table:: Executor と Future
   :header-rows: 1
   :widths: 20 80

   * - 名前
     - 説明
   * - ``Executor``
     - タスクを受け取って実行する仕組み。スレッドで実行する ``ThreadPoolExecutor``、プロセスで実行する ``ProcessPoolExecutor``、サブインタプリタで実行する ``InterpreterPoolExecutor``\ （Python 3.14 以降）がある。
   * - ``Future``
     - 実行を依頼したタスクの「将来の結果」を表すオブジェクト。タスクが完了したかどうかの確認、結果の取得、例外の取得、キャンセルができる。

3 つの ``Executor`` は同じメソッドを持っているため、``Executor`` のクラスを差し替えるだけで、スレッドとプロセスを切り替えられる。

``Executor`` は ``with`` 文で使う。``with`` ブロックを抜けるとき、``shutdown(wait=True)`` が呼ばれ、実行中のタスクがすべて終わるのを待ってからスレッドやプロセスを終了する。

submit と map
-------------

``Executor`` にタスクを渡すメソッドには、``submit()`` と ``map()`` がある。

.. list-table:: submit と map
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 説明
   * - ``submit(fn, *args, **kwargs)``
     - 1 つのタスクを渡し、``Future`` を返す。タスクごとに異なる関数や引数を渡す場合や、完了した順に結果を処理したい場合に使う。
   * - ``map(fn, *iterables)``
     - 組み込みの ``map()`` と同じように、複数の引数で ``fn`` を呼び出す。結果は、タスクを渡した順に返す。

.. code-block:: python
   :linenos:

   from concurrent.futures import ThreadPoolExecutor


   def square(n: int) -> int:
       return n * n


   with ThreadPoolExecutor(max_workers=4) as executor:
       future = executor.submit(square, 3)
       print(future.result())  # 9（完了するまで待ってから結果を返す）

       print(list(executor.map(square, range(5))))  # [0, 1, 4, 9, 16]

``Future.result()`` はタスクが完了するまで待ち、結果を返す。タスクの中で例外が発生した場合は、``result()`` を呼んだ時点でその例外が送出される。``map()`` の場合は、結果を取り出すときに例外が送出される。

as_completed で完了した順に処理する
-----------------------------------

``as_completed()`` 関数は、``Future`` の集まりを受け取り、完了した順に ``Future`` を返す。処理時間がタスクによって異なる場合、早く終わったタスクの結果からすぐに処理を始められる。進捗の表示にも使える。

次のサンプルでは、ファイルのダウンロードを模擬した 4 つのタスクを実行し、完了した順に結果を表示する。1 つのタスクは例外を送出する。

:download:`futures_demo.py <../../examples/ch07_futures/futures_demo.py>`

.. literalinclude:: ../../examples/ch07_futures/futures_demo.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 11-

引数を付けずに実行すると、次のような結果になる。

.. code-block:: text

    0.5 秒: 完了 b.txt (0.5 秒)
    1.0 秒: 失敗 broken: broken のダウンロードに失敗した
    1.3 秒: 完了 c.txt (0.8 秒)
    1.5 秒: 完了 a.txt (1.5 秒)
   thread で実行した。合計 1.5 秒

このサンプルのポイントは次のとおりである。

* ``submit()`` が返す ``Future`` をキーに、タスクの名前を値にした辞書を作っている。``as_completed()`` から返された ``Future`` がどのタスクのものかを、この辞書で調べられる。
* 結果は投入した順（a、b、broken、c）ではなく、完了した順に表示されている。
* ``broken`` のタスクで発生した ``ValueError`` は、``future.result()`` を呼んだときに送出される。1 つのタスクが失敗しても、他のタスクは影響を受けない。
* ``python futures_demo.py process`` のように引数に ``process`` を指定すると、``ProcessPoolExecutor`` で実行する。``create_executor()`` 以外のコードは変わらない。プロセスの起動に時間がかかるため、全体の時間は少し長くなる。

wait で待ち方を指定する
-----------------------

``wait()`` 関数を使うと、``Future`` の集まりについて、待ち方を指定できる。``return_when`` 引数に次の値を指定する。

.. list-table:: wait の return_when 引数
   :header-rows: 1
   :widths: 35 65

   * - 値
     - いつ戻るか
   * - ``ALL_COMPLETED``\ （既定値）
     - すべての ``Future`` が完了したとき
   * - ``FIRST_COMPLETED``
     - いずれか 1 つの ``Future`` が完了したとき
   * - ``FIRST_EXCEPTION``
     - いずれか 1 つの ``Future`` が例外で終了したとき（例外が無ければ、すべて完了したとき）

``wait()`` は、完了した ``Future`` の集合と、完了していない ``Future`` の集合を返す。たとえば、1 つでも失敗したら残りを中止したい場合は、次のように書ける。

.. code-block:: python
   :linenos:

   from concurrent.futures import FIRST_EXCEPTION, wait

   done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
   for future in not_done:
       future.cancel()  # まだ実行が始まっていないタスクを取り消す

キャンセルとタイムアウト
------------------------

``Future.cancel()`` はタスクを取り消す。ただし、取り消せるのはまだ実行が始まっていないタスクだけである。実行中のスレッドやプロセスを外から強制的に止める方法は用意されていない。長時間かかるタスクを途中で止めたい場合は、タスク自身が定期的に停止の合図（``threading.Event`` など）を確認するように作る必要がある。

``Executor.shutdown(cancel_futures=True)`` を呼ぶと、まだ実行が始まっていないタスクをまとめて取り消せる。

``Future.result()``、``as_completed()``、``wait()`` は ``timeout`` 引数で待つ時間の上限を指定できる。時間内に完了しなかった場合は ``TimeoutError`` が送出される。ただし、待つのをやめるだけで、タスク自体は実行され続ける。

ワーカー数の決め方
------------------

``max_workers`` 引数で、同時に実行するスレッドやプロセスの数を指定する。省略した場合の既定値は次のとおりである。

.. list-table:: max_workers の既定値
   :header-rows: 1
   :widths: 35 65

   * - Executor
     - 既定値
   * - ``ThreadPoolExecutor``
     - ``min(32, os.process_cpu_count() + 4)``\ （Python 3.12 以前は ``os.cpu_count()`` を使う）
   * - ``ProcessPoolExecutor``
     - ``os.process_cpu_count()``\ （Python 3.12 以前は ``os.cpu_count()``）。Windows では 61 が上限になる。

CPU バウンドな処理をプロセスで実行する場合は、CPU のコア数より多くしても速くならない。I/O バウンドな処理をスレッドで実行する場合は、接続先のサーバーの負荷や、接続数の制限を考えて決める。サーバーに大量の要求を同時に送ると、相手に迷惑をかけたり、接続を拒否されたりするためである。
