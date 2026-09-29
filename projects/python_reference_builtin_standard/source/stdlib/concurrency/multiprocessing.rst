multiprocessing
===============

複数のプロセスを用いて処理を並列実行するためのモジュール。それぞれの
プロセスが独立した Python インタプリタと GIL を持つため、CPU バウンドな
処理を複数の CPU コアで真に並列に実行できる。

multiprocessing.Process
-------------------------

``Process`` オブジェクトに実行したい関数を渡してプロセスを生成する。API は ``threading.Thread`` とよく似ており、``start()`` で開始し ``join()`` で終了を待つ。

.. code-block:: python

   >>> import multiprocessing as mp
   >>>
   >>> def worker(name):
   ...     print(f"{name}: 開始")
   ...
   >>> if __name__ == "__main__":
   ...     p = mp.Process(target=worker, args=("process-1",))
   ...     p.start()
   ...     p.join()
   ...

.. note::

   spawn 方式を使う環境（Windows や macOS など。macOS はデフォルトの子プロセス生成方式が ``spawn`` になっている）では、プロセス生成のコードは ``if __name__ == "__main__":`` の中に書く必要がある。書かないと、子プロセスがモジュールを再import した際に無限にプロセスを生成してしまう。

.. note::

   ``Process`` や ``Pool.map()`` に渡す関数は、``spawn`` 方式では pickle 可能である必要があり、そのためにはモジュールのトップレベルで定義された（import 可能な）関数でなければならない。ラムダ式や関数内で定義したクロージャ、対話モード（REPL）でその場に定義した関数は pickle できず、``PicklingError`` などのエラーになる。これは ``multiprocessing`` を使う際にもっともよく遭遇するエラーの一つである。

なぜ GIL を回避できるのか
--------------------------

前述のとおり各プロセスが独立した GIL を持つのは、``multiprocessing`` が OS のプロセスを個別に起動するためである。GIL（Global Interpreter Lock）は 1 つのプロセス内で 1 つのインタプリタがバイトコードを実行することを保証する仕組みであり、そもそもプロセスをまたいで共有されるものではないため、プロセスを分ければ複数コアを並列に使うことができる。

multiprocessing.Pool
----------------------

``Pool`` はワーカープロセスの集団を管理し、``map()`` でイテラブルの
各要素に関数を適用する処理を各プロセスに分配してくれる。CPU バウンドな
処理を並列化する際によく使われる。

.. code-block:: python

   >>> def square(x):
   ...     return x * x
   ...
   >>> if __name__ == "__main__":
   ...     with mp.Pool(processes=4) as pool:
   ...         results = pool.map(square, range(10))
   ...     print(results)
   ...
   [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

``map()`` の他にも、目的に応じて使い分けられるメソッドがある。

- ``starmap()``: ``map()`` は単一引数の関数しか渡せないが、``starmap()`` は ``(引数1, 引数2, ...)`` のタプルのイテラブルを渡すことで、複数引数を取る関数を並列化できる。
- ``apply_async()``: 1回だけ非同期に関数を呼び出し、``Future`` に似た
  結果オブジェクトを返す。``callback`` 引数に関数を渡すと、結果が
  得られた時点でそれを自動的に呼び出せる。
- ``imap()`` / ``imap_unordered()``: ``map()`` はすべての結果が揃うまで
  ブロックしてリストを返すが、これらは結果を1件ずつ遅延的に返す
  イテレータを返す。大量データを扱う場合や、結果が出るたびに進捗を
  表示したい場合に向く（``imap_unordered`` は結果が出た順に返すため、
  入力順を保持する ``imap`` より速く結果を得られることがある）。

.. code-block:: python

   >>> def power(base, exp):
   ...     return base ** exp
   ...
   >>> if __name__ == "__main__":
   ...     with mp.Pool(processes=4) as pool:
   ...         results = pool.starmap(power, [(2, 3), (3, 2), (5, 2)])
   ...     print(results)
   ...
   [8, 9, 25]

``apply_async()`` に ``callback`` を渡す例は以下の通り。結果を待たずに
処理を続け、結果が得られた時点で ``callback`` に指定した関数が呼ばれる。

.. code-block:: python

   >>> results = []
   >>>
   >>> def store_result(value):
   ...     results.append(value)
   ...
   >>> if __name__ == "__main__":
   ...     with mp.Pool(processes=4) as pool:
   ...         pool.apply_async(square, args=(10,), callback=store_result)
   ...         pool.close()
   ...         pool.join()  # コールバックの完了を含めて待つ
   ...     print(results)
   ...
   [100]

multiprocessing.Queue
------------------------

プロセスはメモリ空間を共有しないため、変数を直接共有することはできない。
プロセス間通信（IPC）には ``Queue`` を使うのが基本的な方法で、
内部でデータをシリアライズしてやり取りする。

.. code-block:: python

   >>> def producer(q):
   ...     for i in range(5):
   ...         q.put(i)
   ...     q.put(None)  # 終了の合図
   ...
   >>> def consumer(q):
   ...     while True:
   ...         item = q.get()
   ...         if item is None:
   ...             break
   ...         print(f"受信: {item}")
   ...
   >>> if __name__ == "__main__":
   ...     q = mp.Queue()
   ...     p1 = mp.Process(target=producer, args=(q,))
   ...     p2 = mp.Process(target=consumer, args=(q,))
   ...     p1.start()
   ...     p2.start()
   ...     p1.join()
   ...     p2.join()
   ...

Value / Array / Manager による状態共有
------------------------------------------

``Queue`` によるメッセージのやり取りとは別に、単純な値や配列を複数のプロセス間で直接共有したい場合は ``multiprocessing.Value``・``multiprocessing.Array`` が使える。内部で共有メモリを使い、``threading.Lock`` と同様にロックを介して安全に更新できる。

.. code-block:: python

   >>> def increment(counter, lock):
   ...     for _ in range(1000):
   ...         with lock:
   ...             counter.value += 1
   ...
   >>> if __name__ == "__main__":
   ...     counter = mp.Value("i", 0)  # "i" は int を表す型コード
   ...     lock = mp.Lock()
   ...     procs = [mp.Process(target=increment, args=(counter, lock))
   ...              for _ in range(4)]
   ...     for p in procs:
   ...         p.start()
   ...     for p in procs:
   ...         p.join()
   ...     print(counter.value)
   ...
   4000

リストや辞書のような、より複雑なデータ構造を共有したい場合は、``multiprocessing.Manager()`` が返す ``dict``/``list`` 風のプロキシオブジェクトを使うと簡単に扱える。

.. code-block:: python

   >>> if __name__ == "__main__":
   ...     with mp.Manager() as manager:
   ...         shared_dict = manager.dict()
   ...         shared_dict["count"] = 0
   ...         # shared_dict を各プロセスに渡して更新できる
   ...

.. note::

   より高レベルな ``Pool``/``Executor`` 風の API を使いたい場合は :doc:`concurrent_futures` の ``ProcessPoolExecutor`` も検討するとよい。一方、並列化したい処理が CPU バウンドではなく I/O 待ちが中心の場合は、プロセスを起動するオーバーヘッドをかけずに :doc:`threading` を使う方が適していることが多い。
