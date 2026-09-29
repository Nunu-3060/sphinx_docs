asyncio
=======

単一スレッド・単一プロセスの中で、コルーチンを用いて I/O バウンドな
処理を並行実行するためのモジュール。イベントループが、待ち時間の発生した
コルーチンから別のコルーチンへと実行を切り替えることで、効率よく
多数の処理を同時に進めることができる。

async def / await
--------------------

``async def`` で定義した関数はコルーチン関数となり、呼び出しても即座には
実行されず、コルーチンオブジェクトを返す。``await`` を使うと、その
コルーチンの完了を待ちながら、他の処理に制御を譲ることができる。

.. code-block:: python

   >>> import asyncio
   >>>
   >>> async def say_hello(name, delay):
   ...     await asyncio.sleep(delay)  # I/O 待ちを模したノンブロッキングな待機
   ...     print(f"こんにちは、{name}さん")
   ...

asyncio.run
------------

``asyncio.run()`` はイベントループを新規作成し、渡したコルーチンを
実行してループを閉じる。トップレベルの非同期プログラムを起動する際の
基本的な入り口となる関数。

.. code-block:: python

   >>> asyncio.run(say_hello("Alice", 1))
   こんにちは、Aliceさん

asyncio.create_task / asyncio.gather
---------------------------------------

``create_task()`` はコルーチンをイベントループ上のタスクとしてスケジュールし、即座にバックグラウンドで実行を開始させる。複数のコルーチンをまとめて並行実行し、すべての結果を待ちたい場合は ``asyncio.gather()`` を使う。

.. code-block:: python

   >>> async def main():
   ...     # 3 つのタスクを同時にスケジュール
   ...     await asyncio.gather(
   ...         say_hello("Alice", 1),
   ...         say_hello("Bob", 2),
   ...         say_hello("Carol", 1),
   ...     )
   ...
   >>> asyncio.run(main())
   こんにちは、Aliceさん
   こんにちは、Carolさん
   こんにちは、Bobさん

``say_hello`` を順番に ``await`` で呼び出した場合は合計 4 秒かかるが、``gather()`` でまとめて並行実行すると、最も遅い待機時間である 2 秒程度ですべて完了する。

asyncio.TaskGroup による構造化された並行実行
------------------------------------------------

Python 3.11 以降では、``gather()`` の代わりに ``asyncio.TaskGroup`` を
使うことが推奨されている。``async with`` ブロックを抜ける際に、ブロック
内で ``create_task()`` した全タスクの完了を待つ。いずれかのタスクが
例外を発生させた場合、他の実行中のタスクは自動的にキャンセルされ、
例外はブロックを抜ける際にまとめて送出される。``gather()`` よりも
キャンセルと例外伝播の扱いが安全で分かりやすい。

.. code-block:: python

   >>> async def main():
   ...     async with asyncio.TaskGroup() as tg:
   ...         tg.create_task(say_hello("Alice", 1))
   ...         tg.create_task(say_hello("Bob", 2))
   ...         tg.create_task(say_hello("Carol", 1))
   ...
   >>> asyncio.run(main())
   こんにちは、Aliceさん
   こんにちは、Carolさん
   こんにちは、Bobさん

asyncio.Queue によるタスク間の連携
-------------------------------------

コルーチン同士でデータをやり取りしたい場合は ``asyncio.Queue`` が使える。
プロデューサー・コンシューマー間の連携によく利用される。

.. code-block:: python

   >>> async def producer(queue):
   ...     for i in range(3):
   ...         await queue.put(i)
   ...     await queue.put(None)
   ...
   >>> async def consumer(queue):
   ...     while True:
   ...         item = await queue.get()
   ...         if item is None:
   ...             break
   ...         print(f"受信: {item}")
   ...
   >>> async def main():
   ...     queue = asyncio.Queue()
   ...     await asyncio.gather(producer(queue), consumer(queue))
   ...
   >>> asyncio.run(main())
   受信: 0
   受信: 1
   受信: 2

.. note::

   ``asyncio`` はシングルスレッドで動作するため、GIL による制限が問題にならず、スレッド切り替えのオーバーヘッドやロックによる競合状態の心配も基本的に不要になる。大量の同時ネットワーク接続を扱うサーバーなど、I/O 待ちの処理を極めて多数同時に扱いたい場合、``threading`` よりも ``asyncio`` の方が少ないリソースで効率よくスケールすることが多い。ただし、対象のライブラリが async 対応している必要があり、CPU バウンドな処理には :doc:`multiprocessing` が適している。
