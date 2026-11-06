threading
=========

複数のスレッドを用いて処理を並行実行するためのモジュール。ファイル I/O やネットワーク通信のように「待ち時間」の多い処理を並行させるのに向いている。

threading.Thread
-----------------

``Thread`` オブジェクトに実行したい関数を渡してスレッドを生成する。``start()`` でスレッドの実行を開始し、``join()`` で終了を待ち合わせる。

.. code-block:: python
   :linenos:

   >>> import threading
   >>> import time
   >>>
   >>> def worker(name):
   ...     print(f"{name}: 開始")
   ...     time.sleep(1)
   ...     print(f"{name}: 終了")
   ...
   >>> t = threading.Thread(target=worker, args=("thread-1",))
   >>> t.start()
   >>> t.join()  # スレッドの終了を待つ
   thread-1: 開始
   thread-1: 終了

複数スレッドの並行実行
-----------------------

複数のスレッドを起動し、それぞれを ``join()`` することで、まとめて完了を待つことができる。以下は 3 本のスレッドを並行に走らせる例。

.. code-block:: python
   :linenos:

   >>> threads = [threading.Thread(target=worker, args=(f"thread-{i}",))
   ...            for i in range(3)]
   >>> for t in threads:
   ...     t.start()
   ...
   >>> for t in threads:
   ...     t.join()
   ...

threading.Lock
---------------

複数のスレッドが同じ変数を同時に更新すると、更新内容が失われる「競合状態（race condition）」が発生することがある。``Lock`` を使うと、一度に 1 つのスレッドしかクリティカルセクションに入れないようにできる。

.. code-block:: python
   :linenos:

   >>> counter = 0
   >>> lock = threading.Lock()
   >>>
   >>> def increment():
   ...     global counter
   ...     for _ in range(100000):
   ...         with lock:  # ロックを取得してから更新
   ...             counter += 1
   ...
   >>> threads = [threading.Thread(target=increment) for _ in range(2)]
   >>> for t in threads:
   ...     t.start()
   ...
   >>> for t in threads:
   ...     t.join()
   ...
   >>> counter
   200000

``with lock:`` を外すと、2 つのスレッドが同時に ``counter`` を読み書きしてしまい、最終的な値が 200000 より小さくなることがある。

threading.Event
-----------------

スレッド間で「あるイベントが発生したかどうか」を伝えるためのシンプルなフラグ。``wait()`` で待機し、``set()`` でフラグを立てる。

.. code-block:: python
   :linenos:

   >>> event = threading.Event()
   >>>
   >>> def waiter():
   ...     print("イベント待ち...")
   ...     event.wait()  # set() が呼ばれるまでブロック
   ...     print("イベントを受信")
   ...
   >>> t = threading.Thread(target=waiter)
   >>> t.start()
   >>> time.sleep(1)
   >>> event.set()  # 待っているスレッドを起こす
   >>> t.join()

threading.RLock
-----------------

``RLock``\ （再入可能ロック）は、同じスレッドが既に獲得しているロックを再度獲得してもブロックしない。再帰呼び出しの中で同じロックを取り直す必要がある場合、通常の ``Lock`` の代わりに使う。

.. code-block:: python
   :linenos:

   >>> rlock = threading.RLock()
   >>>
   >>> def outer():
   ...     with rlock:
   ...         inner()
   ...
   >>> def inner():
   ...     with rlock:  # 同じスレッドなのでブロックしない
   ...         print("inner 実行中")
   ...
   >>> outer()
   inner 実行中

threading.Semaphore
----------------------

``Semaphore`` は、リソースへ同時にアクセスできるスレッド数の上限を指定できる、ロックを一般化した仕組み。同時接続数の制限など、アクセス数に上限を設けたい場面で使う。

.. code-block:: python
   :linenos:

   >>> sem = threading.Semaphore(2)  # 同時に 2 スレッドまで
   >>>
   >>> def access_resource(name):
   ...     with sem:
   ...         print(f"{name}: リソース使用中")
   ...

threading.Condition
----------------------

``Condition`` は ``Lock`` に加えて、あるスレッドが特定の条件が満たされるまで待機（``wait()``）し、別のスレッドが条件成立を通知（``notify()``）できる仕組みを提供する。プロデューサー・コンシューマーパターンの実装などに使われる。

.. code-block:: python
   :linenos:

   >>> condition = threading.Condition()
   >>> queue = []
   >>>
   >>> def consumer():
   ...     with condition:
   ...         while not queue:
   ...             condition.wait()  # 通知があるまで待機
   ...         print(f"受信: {queue.pop(0)}")
   ...
   >>> def producer():
   ...     with condition:
   ...         queue.append("item")
   ...         condition.notify()  # 待機中のスレッドを起こす
   ...

threading.local()
-------------------

``threading.local()`` は、スレッドごとに独立した値を持てるオブジェクトを作成する。同じ属性名でアクセスしても、どのスレッドからアクセスしたかによって異なる値が見える。

.. code-block:: python
   :linenos:

   >>> data = threading.local()
   >>>
   >>> def show_value(value):
   ...     data.value = value
   ...     print(data.value)
   ...
   >>> t1 = threading.Thread(target=show_value, args=("A",))
   >>> t2 = threading.Thread(target=show_value, args=("B",))
   >>> t1.start(); t1.join()
   A
   >>> t2.start(); t2.join()
   B

.. note::

   CPython には GIL（Global Interpreter Lock）と呼ばれる仕組みがあり、一度に 1 つのスレッドしか Python バイトコードを実行できない。そのため ``threading`` は CPU に負荷のかかる計算処理を並列化して高速化する目的には向かない。CPU バウンドな処理を並列化したい場合は :doc:`multiprocessing` を、I/O 待ちの多い処理を効率よく扱いたい場合は、そのまま ``threading`` を使うか :doc:`asyncio` を検討するとよい。

フリースレッドビルド
--------------------

Python 3.13 では、GIL を無効化した「フリースレッドビルド」（PEP 703）が実験的に導入され、3.14 で正式にサポートされる位置づけになった（PEP 779）。このビルドでは複数のスレッドが Python コードを真に並列に実行できるため、``threading`` や ``ThreadPoolExecutor`` で CPU バウンドな処理も高速化できる。

ただし、フリースレッドビルドは通常のビルドとは別に提供されるもので（実行ファイル名は ``python3.14t`` など）、デフォルトのビルドでは従来どおり GIL が有効である。また、C 拡張モジュールがフリースレッドに対応していない場合は、import 時に GIL が自動的に再有効化されることがある。GIL が有効かどうかは ``sys._is_gil_enabled()`` で確認できる（:doc:`../system/sys` を参照）。

GIL がなくなっても、複数のスレッドから同じデータを更新する場合に ``Lock`` などによる排他制御が必要であることに変わりはない。
