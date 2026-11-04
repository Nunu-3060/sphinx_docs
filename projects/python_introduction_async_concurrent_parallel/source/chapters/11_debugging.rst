第 11 章 デバッグと性能計測
===========================

並行処理や並列処理を使ったプログラムは、実行の順序が毎回変わるため、不具合の原因を見つけにくい。また、「速くなったつもり」で実際には速くなっていないこともある。この章では、性能の計測、デバッグ、テストの方法を説明する。

性能の計測
----------

経過時間の計測
~~~~~~~~~~~~~~

並行処理や並列処理の効果は、経過時間で評価する。経過時間の計測には ``time.perf_counter()`` を使う。``time.time()`` は時計の時刻を返すため、時刻の補正によって値が変わることがあり、計測には向かない。

.. code-block:: python
   :linenos:

   import time

   start = time.perf_counter()
   run()  # 計測したい処理
   elapsed = time.perf_counter() - start
   print(f"{elapsed:.2f} 秒")

:doc:`02_concepts` で説明したとおり、``time.process_time()`` で CPU 時間も測ると、処理が CPU バウンドか I/O バウンドかを判断できる。経過時間に比べて CPU 時間が小さければ I/O バウンド、ほぼ等しければ CPU バウンドである。

計測するときは、次の点に注意する。

* **何度か実行して比べる。**\ 1 回目は、ファイルのキャッシュやモジュールの読み込みの影響で遅くなることがある。他のプログラムの影響も受けるため、複数回実行して傾向を確認する。
* **起動の時間を含めるかどうかを意識する。**\ ``ProcessPoolExecutor`` の起動には時間がかかる。:doc:`06_processes` の ``chunksize.py`` のように、起動を除いた時間を測りたい場合は、先に一度使ってから計測する。実際の利用場面で毎回プロセスを起動するなら、起動の時間も含めて評価する。
* **実際のデータに近い条件で測る。**\ 少量のデータでは並列化の負荷が目立ち、大量のデータでは効果が目立つ。

ボトルネックの特定
~~~~~~~~~~~~~~~~~~

プログラムのどこに時間がかかっているかを調べるには、プロファイラーを使う。標準ライブラリの ``cProfile`` は、関数ごとの呼び出し回数と実行時間を集計する。

.. code-block:: console

   python -m cProfile -s cumtime main.py

``-s cumtime`` は、その関数から呼び出した関数の時間も含めた累積時間で並べ替える指定である。時間の大半が ``socket`` の受信や ``time.sleep()`` などで使われていれば I/O バウンド、自分で書いた計算の関数で使われていれば CPU バウンドと判断できる。

ログによる追跡
--------------

並行処理の不具合を調べるときは、どのスレッドやタスクが、いつ、何をしたかを記録すると原因を絞り込みやすい。``logging`` モジュールは、ログの書式にスレッド名やプロセス ID を含められる。``logging`` モジュールはスレッドセーフなので、複数のスレッドから同時に呼び出しても出力が混ざらない。

.. code-block:: python
   :linenos:

   import logging

   logging.basicConfig(
       level=logging.DEBUG,
       format="%(asctime)s %(processName)s %(threadName)s %(message)s",
   )

``asyncio`` のタスクには、``create_task(coro, name="download-1")`` のように名前を付けられる。実行中のタスクの名前は ``asyncio.current_task().get_name()`` で取得できる。Python 3.12 以降では、ログの書式に ``%(taskName)s`` を指定してタスク名を出力することもできる。

asyncio のデバッグモード
------------------------

``asyncio`` には、よくある誤りを検出するデバッグモードがある。デバッグモードでは、次のような問題が警告として出力される。

* 1 回の実行に一定時間（既定では 0.1 秒）以上かかり、イベントループをブロックした処理
* ``await`` されなかったコルーチンが作られた場所
* 別のスレッドから、スレッドセーフでない ``asyncio`` の API が呼ばれたこと

デバッグモードは、``asyncio.run(main(), debug=True)`` と書くか、環境変数 ``PYTHONASYNCIODEBUG=1`` を設定するか、``python -X dev`` で Python の開発モードを有効にすると使える。

:download:`debug_mode.py <../../examples/ch11_debugging/debug_mode.py>`

.. literalinclude:: ../../examples/ch11_debugging/debug_mode.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 6-

実行すると、``badly_behaved()`` がイベントループを 0.3 秒ブロックしたことが警告される（読みやすさのため、ファイルのパスを省略している）。

.. code-block:: text

   Executing <Task finished name='badly_behaved' coro=<badly_behaved() done, defined at ...\debug_mode.py:14> result=None created at ...\asyncio\taskgroups.py:196> took 0.301 seconds

デバッグモードは処理が遅くなるため、開発中やテストのときに使い、本番の環境では無効にする。

実行中のタスクを調べる
----------------------

Python 3.14 以降では、実行中の Python のプロセスについて、``asyncio`` のタスクの状態を外から調べられる。プログラムが応答しなくなったときに、どのタスクが何を待っているかを確認するのに役立つ。

.. list-table:: タスクを調べるコマンド
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 説明
   * - ``python -m asyncio ps PID``
     - プロセス ``PID`` のタスクを一覧表示する。
   * - ``python -m asyncio pstree PID``
     - タスクの待ち合わせの関係を木構造で表示する。

次のサンプルは、タスクを入れ子に作成し、60 秒間待ち続ける。

:download:`inspect_tasks.py <../../examples/ch11_debugging/inspect_tasks.py>`

.. literalinclude:: ../../examples/ch11_debugging/inspect_tasks.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 9-

このサンプルを実行したまま、別の端末で ``python -m asyncio pstree PID`` を実行すると、次のように表示される（読みやすさのため、ファイルのパスを省略し、``crawler-B`` 以下を省略している）。

.. code-block:: text

   └── (T) Task-1
       └──  main ...\inspect_tasks.py:25
           └──  TaskGroup.__aexit__ ...\asyncio\taskgroups.py:72
               └──  TaskGroup._aexit ...\asyncio\taskgroups.py:121
                   ├── (T) crawler-A
                   │   └──  crawler ...\inspect_tasks.py:18
                   │       └──  TaskGroup.__aexit__ ...\asyncio\taskgroups.py:72
                   │           └──  TaskGroup._aexit ...\asyncio\taskgroups.py:121
                   │               ├── (T) download-A-0
                   │               │   └──  download ...\inspect_tasks.py:14
                   │               │       └──  sleep ...\asyncio\tasks.py:704
                   │               └── (T) download-A-1
                   │                   └──  download ...\inspect_tasks.py:14
                   │                       └──  sleep ...\asyncio\tasks.py:704
                   └── (T) crawler-B
                       （省略）

``(T)`` はタスクを表す。``main()`` のタスク（``Task-1``）が 2 つの ``crawler`` のタスクを待ち、それぞれの ``crawler`` が 2 つの ``download`` のタスクを待っていること、``download`` のタスクが ``asyncio.sleep()`` で止まっていることが分かる。タスクに名前を付けておくと、このような出力が読みやすくなる。

プログラムが止まったときの調査
------------------------------

デッドロックなどでプログラムが止まった場合は、各スレッドがどこで止まっているかを調べる。標準ライブラリの ``faulthandler`` モジュールを使うと、全スレッドのスタックトレースを出力できる。

.. code-block:: python
   :linenos:

   import faulthandler
   import sys

   # 60 秒経過するたびに、全スレッドのスタックトレースを標準エラー出力に書き出す
   faulthandler.dump_traceback_later(60, repeat=True, file=sys.stderr)

``python -X faulthandler`` で実行すると、プログラムが異常終了したときにもスタックトレースが出力される。

非同期処理のテスト
------------------

コルーチンをテストするには、標準ライブラリの ``unittest.IsolatedAsyncioTestCase`` を使う。このクラスを継承したテストクラスでは、テストメソッドを ``async def`` で定義でき、テストごとに新しいイベントループで実行される。

次のサンプルでは、失敗したときに再試行するコルーチン関数 ``retry()`` をテストする。

:download:`test_retry.py <../../examples/ch11_debugging/test_retry.py>`

.. literalinclude:: ../../examples/ch11_debugging/test_retry.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 8-

テストは次のコマンドで実行する。

.. code-block:: console

   python -m unittest test_retry.py

このサンプルのように、テストでは次の工夫をするとよい。

* **外部のサーバーの代わりにテスト用のオブジェクトを使う。**\ ``FlakyServer`` は、決まった回数だけ失敗するサーバーを模擬している。実際のネットワークを使わないため、テストの結果が安定する。
* **待ち時間を短くする。**\ ``delay=0.01`` のように、テストでは待ち時間を短く指定し、テストの実行時間を抑える。
* **テストにもタイムアウトを設定する。**\ 不具合によってタスクが永久に待ち続けると、テストが終わらなくなる。``asyncio.timeout()`` で上限を設けておく。

スレッドを使うコードのテストでは、競合状態がたまたま起きずにテストが通ってしまうことがある。共有データを扱うクラスは、ロックで保護されていることをコードレビューで確認し、多数のスレッドから繰り返し呼び出すテストも併用するとよい。
