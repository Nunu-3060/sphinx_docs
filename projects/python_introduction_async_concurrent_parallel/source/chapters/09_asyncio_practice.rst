第 9 章 asyncio による非同期処理（実践）
========================================

この章では、``asyncio`` を実際のプログラムで使うときに必要になる技術を説明する。同時実行数の制限、キューによる仕事の分配、ブロッキングする処理との組み合わせ、キャンセルと後始末、ネットワーク通信を扱う。

同時実行数の制限
----------------

``asyncio`` では、タスクを作るだけで数千の処理を同時に開始できる。しかし、接続先のサーバーに数千の要求を一度に送ると、相手に過大な負荷をかけたり、接続を拒否されたりする。開けるファイルやソケットの数にも OS の上限がある。そのため、実際のプログラムでは同時に実行する数を制限する必要がある。

同時実行数の制限には ``asyncio.Semaphore`` を使う。``Semaphore(4)`` は、``async with`` ブロックに同時に入れるタスクを 4 つまでに制限する。5 つ目のタスクは、どれかのタスクがブロックを抜けるまで待たされる。

次のサンプルでは、``asyncio`` のストリームを使ってローカルに TCP のエコーサーバーを起動し、12 個のクライアントから接続する。同時に接続するクライアントは ``Semaphore`` で 4 つまでに制限する。

:download:`echo_semaphore.py <../../examples/ch09_asyncio_practice/echo_semaphore.py>`

.. literalinclude:: ../../examples/ch09_asyncio_practice/echo_semaphore.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

実行すると、次のような結果になる。

.. code-block:: text

   こんにちは 0
   こんにちは 1
   （中略）
   こんにちは 11
   同時接続数の最大: 4, 経過時間: 1.6 秒

サーバーは 1 件の要求に 0.5 秒かけて応答する。12 件を 4 件ずつ処理するため、全体は約 1.5 秒になる。同時接続数の最大が 4 になっていることから、``Semaphore`` による制限が効いていることが分かる。

このサンプルで使っているストリームの API は次のとおりである。

.. list-table:: asyncio のストリームの主な API
   :header-rows: 1
   :widths: 40 60

   * - API
     - 説明
   * - ``asyncio.start_server(handler, host, port)``
     - TCP サーバーを起動する。接続があるたびに、``handler(reader, writer)`` が新しいタスクとして実行される。
   * - ``asyncio.open_connection(host, port)``
     - TCP サーバーに接続し、``StreamReader`` と ``StreamWriter`` の組を返す。
   * - ``await reader.readline()``、``await reader.read()``
     - データを受信する。データが届くまでの間、他のタスクが実行される。
   * - ``writer.write(data)`` と ``await writer.drain()``
     - データを送信する。``write()`` は送信用のバッファにデータを入れるだけなので、``drain()`` でバッファに空きができるまで待つ。
   * - ``writer.close()`` と ``await writer.wait_closed()``
     - 接続を閉じ、閉じ終わるまで待つ。

実務で HTTP の通信を行う場合は、``aiohttp`` や ``httpx`` などの非同期に対応した HTTP クライアントのライブラリを使うのが一般的である。標準ライブラリの ``urllib.request`` は同期的な API なので、``asyncio`` から使う場合は後で説明する ``asyncio.to_thread()`` を使う。

キューによる仕事の分配
----------------------

``asyncio.Queue`` は、``asyncio`` のタスク間でデータを受け渡すためのキューである。``queue.Queue`` と同じように使えるが、``get()`` や ``put()`` は ``await`` で待つコルーチンになっている。決まった数のワーカータスクに仕事を分配する場合に使う。

:download:`worker_queue.py <../../examples/ch09_asyncio_practice/worker_queue.py>`

.. literalinclude:: ../../examples/ch09_asyncio_practice/worker_queue.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 6-

このサンプルのポイントは次のとおりである。

* ワーカーは ``while True`` のループで仕事を取り出し続ける。仕事を 1 つ処理し終えるたびに ``task_done()`` を呼ぶ。
* ``jobs.join()`` は、キューに入れたすべての仕事で ``task_done()`` が呼ばれるまで待つ。
* すべての仕事が終わった後、ワーカーは次の仕事を ``get()`` で待ち続けているため、``cancel()`` で終了させる。キャンセルされたタスクは ``CancelledError`` で終わるため、``gather(..., return_exceptions=True)`` で終了を待つ。

``asyncio.Semaphore`` を使う方法と比べると、ワーカーの数だけタスクを作れば済むため、仕事の数が非常に多い場合でもタスクの数を抑えられる。

ブロッキングする処理との組み合わせ
----------------------------------

:doc:`08_asyncio_basics` で説明したとおり、コルーチンの中でブロッキングする処理を呼ぶと、その間はイベントループ全体が止まる。次のサンプルでは、0.2 秒ごとに経過時間を表示するタスク（``heartbeat()``）と、1 秒かかるブロッキングする処理（``blocking_io()``）を並行に実行する。

:download:`blocking_call.py <../../examples/ch09_asyncio_practice/blocking_call.py>`

.. literalinclude:: ../../examples/ch09_asyncio_practice/blocking_call.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

実行すると、次の結果になる。

.. code-block:: text

   --- 直接呼ぶ場合 ---
    0.0 秒: heartbeat
    0.0 秒: blocking_io() を直接呼ぶ
    1.0 秒: 同期処理の結果
    1.0 秒: heartbeat
    1.2 秒: heartbeat
    1.4 秒: heartbeat
    1.6 秒: heartbeat
    1.8 秒: heartbeat
   --- asyncio.to_thread() を使う場合 ---
    0.0 秒: heartbeat
    0.0 秒: blocking_io() を asyncio.to_thread() で呼ぶ
    0.2 秒: heartbeat
    0.4 秒: heartbeat
    0.6 秒: heartbeat
    0.8 秒: heartbeat
    1.0 秒: 同期処理の結果
    1.0 秒: heartbeat

直接呼ぶ場合は、``blocking_io()`` が実行されている 1 秒間、``heartbeat()`` の表示が止まっている。``asyncio.to_thread()`` を使う場合は、``blocking_io()`` が別のスレッドで実行されるため、その間も ``heartbeat()`` が動き続けている。

ブロッキングする処理を ``asyncio`` から呼ぶ方法を次にまとめる。

.. list-table:: ブロッキングする処理を asyncio から呼ぶ方法
   :header-rows: 1
   :widths: 40 60

   * - 方法
     - 用途
   * - ``await asyncio.to_thread(func, *args)``
     - 同期的な I/O を行う関数を、別のスレッドで実行する。同期的な API しか持たないライブラリを使う場合に使う。
   * - ``await loop.run_in_executor(executor, func, *args)``
     - 指定した ``Executor`` で関数を実行する。``ProcessPoolExecutor`` を指定すれば、CPU バウンドな処理を別のプロセスで実行できる（:doc:`12_case_studies` で使う）。

``loop`` は ``asyncio.get_running_loop()`` で取得する。``asyncio.to_thread()`` も内部では既定の ``ThreadPoolExecutor`` を使っている。

コルーチンの中で次のような処理を呼んでいないか、注意が必要である。

* ``time.sleep()``\ （代わりに ``await asyncio.sleep()`` を使う）
* ``requests`` や ``urllib.request`` などの同期的な HTTP クライアント
* 同期的なデータベースのドライバー
* 時間のかかる CPU バウンドな計算
* 大きなファイルの読み書き

キャンセルと後始末
------------------

``Task.cancel()`` を呼ぶと、そのタスクが ``await`` で中断している箇所に ``asyncio.CancelledError`` が送出される。``asyncio.timeout()`` や ``TaskGroup`` も、内部でこの仕組みを使ってタスクをキャンセルしている。

タスクがキャンセルされても資源を確実に解放できるよう、後始末は ``try`` ... ``finally`` や ``async with`` で書く。

:download:`cancellation.py <../../examples/ch09_asyncio_practice/cancellation.py>`

.. literalinclude:: ../../examples/ch09_asyncio_practice/cancellation.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

実行すると、次の結果になる。

.. code-block:: text

   タスク: 接続を開いた
   タスク: ステップ 1
   タスク: ステップ 2
   タスク: ステップ 3
   タスク: 接続を閉じた
   キャンセルされた: cancelled() = True

1 秒後に ``cancel()`` が呼ばれると、``asyncio.sleep()`` で待っていたタスクに ``CancelledError`` が送出され、``finally`` で接続が閉じられる。キャンセルについて、次の点に注意する。

* ``CancelledError`` は ``Exception`` ではなく ``BaseException`` を継承している。そのため、``except Exception:`` では捕まらない。
* ``CancelledError`` を捕まえた場合は、後始末をした後に必ず送出し直す。握りつぶすと、キャンセルが正しく伝わらない。
* ``await`` していない間（CPU バウンドな計算の最中など）は、キャンセルは届かない。次に ``await`` したときに初めて ``CancelledError`` が送出される。

よくある誤り
------------

``asyncio`` を使い始めたときに起こしやすい誤りを次にまとめる。

.. list-table:: asyncio でよくある誤り
   :header-rows: 1
   :widths: 35 65

   * - 誤り
     - 説明と対策
   * - ``await`` を付け忘れる
     - コルーチン関数を ``await`` せずに呼ぶと、コルーチンが作られるだけで実行されない。``RuntimeWarning: coroutine '...' was never awaited`` という警告が出る。mypy などの型チェッカーでも検出できる。
   * - コルーチンの中でブロッキングする処理を呼ぶ
     - イベントループ全体が止まる。``asyncio.to_thread()`` などで別のスレッドやプロセスに任せる。
   * - 作ったタスクの参照を保持しない
     - ``asyncio.create_task()`` の戻り値を保持しないと、タスクが途中で消えることがある。``TaskGroup`` を使うか、戻り値を保持する。
   * - タスクの例外を確認しない
     - ``create_task()`` で作ったタスクを待たずに放置すると、タスクの中で発生した例外に気付けない。``TaskGroup`` を使えば、例外は必ず呼び出し元に伝わる。
   * - タイムアウトを設定しない
     - 相手が応答しないと、タスクが永久に待ち続ける。ネットワーク通信には ``asyncio.timeout()`` を設定する。
   * - スレッドから asyncio のオブジェクトを直接操作する
     - ``asyncio`` のオブジェクトの多くはスレッドセーフではない。別のスレッドからイベントループに処理を依頼する場合は、``asyncio.run_coroutine_threadsafe()`` や ``loop.call_soon_threadsafe()`` を使う。

asyncio が向く場面・向かない場面
--------------------------------

.. list-table:: asyncio が向く場面・向かない場面
   :header-rows: 1
   :widths: 50 50

   * - 向く場面
     - 向かない場面
   * - 数百から数千以上のネットワーク接続を同時に扱う（Web サーバー、クローラー、チャットサーバーなど）
     - CPU バウンドな処理（プロセスを使う）
   * - 非同期に対応したライブラリ（``aiohttp``、``httpx``、非同期のデータベースドライバーなど）を使える
     - 使いたいライブラリが同期的な API しか持たず、``to_thread()`` で包む箇所が多くなる
   * - タイムアウトやキャンセルを細かく制御したい
     - 既存の大きな同期的なプログラムの一部だけを並行化したい（スレッドのほうが変更が少ない）
