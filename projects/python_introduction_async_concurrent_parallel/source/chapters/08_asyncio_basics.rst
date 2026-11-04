第 8 章 asyncio による非同期処理（基礎）
========================================

この章では、``asyncio`` モジュールによる非同期処理の基礎を説明する。``asyncio`` は、1 つのスレッドの中で多数のタスクを切り替えながら並行に進める仕組みであり、多数のネットワーク接続を扱う I/O バウンドな処理に向いている。

コルーチンと async / await
--------------------------

``async def`` で定義した関数を **コルーチン関数** という。コルーチン関数を呼び出しても、関数の中身はすぐには実行されず、**コルーチン** と呼ばれるオブジェクトが返される。コルーチンは、``await`` されたときやタスクとして登録されたときに実行される。

.. code-block:: python
   :linenos:

   import asyncio


   async def greet(name: str) -> str:
       await asyncio.sleep(1.0)  # 1 秒待つ間、他のタスクに実行を譲る
       return f"こんにちは、{name}"


   async def main() -> None:
       message = await greet("Python")  # greet() の完了を待って結果を受け取る
       print(message)


   asyncio.run(main())

``await`` は、コルーチン関数の中でだけ使える。``await 式`` と書くと、その式の処理が完了するまでコルーチンの実行が中断され、完了すると結果を受け取って続きが実行される。中断している間、スレッドは止まらず、他のタスクが実行される。この点が、スレッド全体を止める ``time.sleep()`` との違いである。

``await`` の対象にできるオブジェクトを **awaitable** という。awaitable には、コルーチン、タスク（``asyncio.Task``）、フューチャー（``asyncio.Future``）がある。

``asyncio.run()`` は、イベントループを作成し、渡されたコルーチンを最後まで実行してからイベントループを閉じる。プログラムの入り口で 1 回だけ呼び出すのが基本である。

イベントループの仕組み
----------------------

``asyncio`` の中心にあるのが **イベントループ** である。イベントループは、実行できる状態になったタスクを 1 つずつ取り出して実行する処理を繰り返す。:numref:`fig-event-loop` に、その流れを示す。

.. _fig-event-loop:

.. graphviz::
   :caption: イベントループがタスクを切り替える流れ
   :align: center

   digraph event_loop {
       graph [rankdir=LR, nodesep=0.4, ranksep=0.5, bgcolor="transparent"];
       node [shape=box, style="rounded,filled", fillcolor="#ffffff", color="#8a8984", fontsize=11];
       edge [color="#8a8984", fontsize=10];

       ready [label="実行待ちのタスク", fillcolor="#e8f1fb", color="#2a78d6"];
       run [label="タスクを 1 つ取り出し\n次の await まで実行"];
       waiting [label="I/O や時間の経過を\n待っているタスク", fillcolor="#fdeee7", color="#eb6834"];
       os [label="OS\n（ソケットの監視など）", shape=box, style="rounded,dashed"];

       ready -> run;
       run -> waiting [label="await で中断"];
       run -> ready [label="完了・再開可能"];
       waiting -> os [label="監視を依頼", style=dashed];
       os -> ready [label="準備ができた\nことを通知"];
   }

1. イベントループは、実行待ちのタスクを 1 つ取り出し、そのタスクが次に ``await`` で中断するまで実行する。
2. タスクがネットワークの応答などを ``await`` で待つと、そのタスクは中断され、イベントループに制御が戻る。イベントループは、そのタスクが待っている I/O の監視を OS に依頼する。
3. イベントループは、次の実行待ちのタスクを取り出して実行する。
4. OS から I/O の準備ができたと通知されると、待っていたタスクが実行待ちに戻り、中断した箇所から再開される。

この仕組みから、``asyncio`` の重要な性質が 2 つ導かれる。

* **タスクが切り替わるのは await の箇所だけである。**\ OS が任意のタイミングで切り替えるスレッドと異なり、``await`` と ``await`` の間のコードは他のタスクに割り込まれない。そのため、スレッドに比べて競合状態が起きにくい。このように、タスクが自分から制御を譲ることで切り替わる方式を **協調的マルチタスク** という。
* **await せずに時間のかかる処理をすると、イベントループ全体が止まる。**\ 1 つのタスクが CPU バウンドな計算や ``time.sleep()`` のようなブロッキングする処理を行うと、その間は他のすべてのタスクが止まる。この問題と対策は :doc:`09_asyncio_practice` で説明する。

タスクによる並行実行
--------------------

コルーチンを ``await`` で 1 つずつ待つと、前のコルーチンが完了するまで次のコルーチンは始まらない。複数のコルーチンを並行に実行するには、コルーチンを **タスク** としてイベントループに登録する。

次のサンプルでは、1 秒かかる 3 つの処理を、順に ``await`` する方法、``asyncio.gather()`` を使う方法、``asyncio.TaskGroup`` を使う方法で実行する。

:download:`sequential_vs_concurrent.py <../../examples/ch08_asyncio_basics/sequential_vs_concurrent.py>`

.. literalinclude:: ../../examples/ch08_asyncio_basics/sequential_vs_concurrent.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 3-

実行すると、次のような結果になる（``with_task_group`` の出力は ``with_gather`` と同じなので省略する）。

.. code-block:: text

   sequential:
     A: 開始
     A: 終了
     B: 開始
     B: 終了
     C: 開始
     C: 終了
     結果: ['A のデータ', 'B のデータ', 'C のデータ'], 3.0 秒
   with_gather:
     A: 開始
     B: 開始
     C: 開始
     A: 終了
     B: 終了
     C: 終了
     結果: ['A のデータ', 'B のデータ', 'C のデータ'], 1.0 秒

``sequential()`` では処理が 1 つずつ実行され、3 秒かかる。``with_gather()`` と ``with_task_group()`` では 3 つの処理が並行に実行され、1 秒で終わる。

タスクを作る方法と待つ方法を次にまとめる。

.. list-table:: タスクを作る方法と待つ方法
   :header-rows: 1
   :widths: 30 70

   * - 方法
     - 説明
   * - ``asyncio.TaskGroup``
     - ``async with`` ブロックの中で ``create_task()`` を呼んでタスクを作る。ブロックを抜けるときに、すべてのタスクの完了を待つ。いずれかのタスクで例外が発生すると、残りのタスクをキャンセルする（Python 3.11 以降）。
   * - ``asyncio.gather(*aws)``
     - 渡された awaitable をすべて並行に実行し、結果を渡した順のリストで返す。
   * - ``asyncio.create_task(coro)``
     - コルーチンをタスクとして登録し、``Task`` オブジェクトを返す。タスクは登録された時点から、次にイベントループに制御が戻ったときに実行が始まる。

Python 3.11 以降では、基本的に ``asyncio.TaskGroup`` を使うとよい。``TaskGroup`` を使うと、タスクの寿命が ``async with`` ブロックの中に限られるため、タスクの完了を待ち忘れたり、例外を見逃したりすることがない。このように、タスクの寿命をコードのブロック構造に合わせる考え方を **構造化並行性（structured concurrency）** という。

``asyncio.create_task()`` で作ったタスクは、どこからも参照されなくなると、実行中でもガベージコレクションで消えてしまうことがある。``create_task()`` を直接使う場合は、戻り値の ``Task`` を変数やリストに保持しておく必要がある。

例外処理と ExceptionGroup
-------------------------

``TaskGroup`` の中で 1 つのタスクが例外を送出すると、``TaskGroup`` は残りのタスクをキャンセルし、すべてのタスクが終わるのを待ってから、発生した例外を ``ExceptionGroup`` にまとめて送出する。複数のタスクが同時に失敗することもあるため、例外が 1 つでもグループとして送出される。

``ExceptionGroup`` の中の例外は、``except*`` 構文で種類ごとに受け取る。

:download:`taskgroup_errors.py <../../examples/ch08_asyncio_basics/taskgroup_errors.py>`

.. literalinclude:: ../../examples/ch08_asyncio_basics/taskgroup_errors.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 7-

実行すると、次の結果になる。

.. code-block:: text

   TaskGroup の中で例外が発生する場合:
     A: 完了
     C: キャンセルされた
     ValueError を受け取った: B が失敗した
   asyncio.timeout() で時間を制限する場合:
     D: キャンセルされた
     1 秒以内に終わらなかったため打ち切った

A は 0.5 秒で完了する。1 秒後に B が ``ValueError`` を送出すると、まだ実行中の C はキャンセルされる。``except* ValueError`` では、``ExceptionGroup`` の中の ``ValueError`` だけが取り出され、``group_error.exceptions`` で個々の例外を参照できる。

キャンセルされたタスクでは、``await`` している箇所で ``asyncio.CancelledError`` が送出される。``work()`` 関数のように ``CancelledError`` を捕まえて後始末を行うことはできるが、最後に必ず ``raise`` で送出し直す。``CancelledError`` を握りつぶすと、``TaskGroup`` や ``asyncio.timeout()`` が正しく動作しなくなる。

``asyncio.gather()`` では、例外の扱いが異なる。既定では、最初に発生した例外がそのまま送出されるが、他のタスクはキャンセルされずに実行され続ける。``return_exceptions=True`` を指定すると、例外を送出せず、結果のリストの中に例外オブジェクトを入れて返す。

タイムアウト
------------

``asyncio.timeout()`` は、``async with`` ブロックの中の処理に時間の上限を設ける（Python 3.11 以降）。時間内に終わらなかった場合、ブロックの中で実行中の処理はキャンセルされ、ブロックの外に ``TimeoutError`` が送出される。上のサンプルの ``timeout_example()`` では、3 秒かかる処理を 1 秒で打ち切っている。

1 つの awaitable に時間の上限を設ける場合は、``asyncio.wait_for(aw, timeout)`` も使える。ネットワークの通信など、相手の応答が返ってこない可能性がある処理には、必ずタイムアウトを設定する。

同期処理と非同期処理の境界
--------------------------

``asyncio`` を使ったコードには、次の制約がある。

* ``await`` はコルーチン関数の中でしか使えない。そのため、ある関数でコルーチンを ``await`` すると、その関数もコルーチン関数にする必要があり、呼び出し元も同様に書き換える必要がある。このように、非同期処理がコード全体に広がっていく性質がある。
* 通常の関数からコルーチンを実行するには、``asyncio.run()`` を使う。ただし、``asyncio.run()`` はすでにイベントループが動いているスレッドからは呼び出せない。

そのため、``asyncio`` を導入する場合は、プログラムの入り口で ``asyncio.run()`` を 1 回呼び、そこから先をコルーチンで書く構成にするのが基本である。既存の大きな同期的なプログラムの一部だけを速くしたい場合は、スレッドを使うほうが変更が少なく済むことが多い。
