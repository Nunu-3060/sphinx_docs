multiprocessing
===============

複数のプロセスを用いて処理を並列実行するためのモジュール。それぞれのプロセスが独立した Python インタプリタと GIL を持つため、CPU バウンドな処理を複数の CPU コアで真に並列に実行できる。

.. note::

   後述のとおり、子プロセスに渡す関数は対話モード（REPL）では定義できない。そのため、このページの例はすべてスクリプトファイルとして保存して実行することを前提としており、出力はコメントで示す。

multiprocessing.Process
-------------------------

``Process`` オブジェクトに実行したい関数を渡してプロセスを生成する。API は ``threading.Thread`` とよく似ており、``start()`` で開始し ``join()`` で終了を待つ。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def worker(name):
       print(f"{name}: 開始")

   if __name__ == "__main__":
       p = mp.Process(target=worker, args=("process-1",))
       p.start()
       p.join()
   # 出力: process-1: 開始

子プロセスの生成方式（start method）
--------------------------------------

子プロセスの生成方式には ``spawn``・``fork``・``forkserver`` の 3 種類があり、デフォルトはプラットフォームによって異なる。

.. list-table::
   :header-rows: 1

   * - プラットフォーム
     - デフォルトの生成方式
   * - Windows
     - ``spawn``
   * - macOS
     - ``spawn``
   * - Linux などその他の POSIX
     - ``forkserver``\ （3.14 以降。3.13 以前は ``fork``）

``spawn`` は新しいインタプリタを起動し、``forkserver`` はあらかじめ起動しておいたサーバープロセスから子プロセスを fork する。どちらの方式でも、子プロセスはメインモジュールを import し直し、実行する関数や引数は pickle して受け渡される。そのため、次の 2 点に注意する必要がある。

- プロセス生成のコードは ``if __name__ == "__main__":`` の中に書く。書かないと、子プロセスがモジュールを再 import した際にさらにプロセスを生成しようとしてしまい、エラーになる。
- ``Process`` や ``Pool.map()`` に渡す関数は pickle 可能である必要があり、そのためにはモジュールのトップレベルで定義された（import 可能な）関数でなければならない。ラムダ式や関数内で定義したクロージャ、対話モード（REPL）でその場に定義した関数は使えず、``PicklingError`` や ``AttributeError`` などのエラーになる。これは ``multiprocessing`` を使う際にもっともよく遭遇するエラーの一つである。

親プロセスの状態をそのまま複製する ``fork`` は、スレッドを使っているプロセスで使うとデッドロックの原因になり得るため、3.14 で Linux のデフォルトが ``forkserver`` に変更された。生成方式を明示したい場合は ``mp.get_context("spawn")`` のようにコンテキストを取得し、そのメソッド（``ctx.Process`` や ``ctx.Pool`` など）を使う。どのプラットフォームでも同じように動作させたい場合は、上記の 2 点を常に守っておくとよい。

なぜ GIL を回避できるのか
--------------------------

前述のとおり各プロセスが独立した GIL を持つのは、``multiprocessing`` が OS のプロセスを個別に起動するためである。GIL（Global Interpreter Lock）は 1 つのプロセス内で 1 つのインタプリタがバイトコードを実行することを保証する仕組みであり、そもそもプロセスをまたいで共有されるものではないため、プロセスを分ければ複数コアを並列に使うことができる。

multiprocessing.Pool
----------------------

``Pool`` はワーカープロセスの集団を管理し、``map()`` でイテラブルの各要素に関数を適用する処理を各プロセスに分配してくれる。CPU バウンドな処理を並列化する際によく使われる。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def square(x):
       return x * x

   if __name__ == "__main__":
       with mp.Pool(processes=4) as pool:
           results = pool.map(square, range(10))
       print(results)
   # 出力: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

``map()`` の他にも、目的に応じて使い分けられるメソッドがある。

- ``starmap()``: ``map()`` は単一引数の関数しか渡せないが、``starmap()`` は ``(引数1, 引数2, ...)`` のタプルのイテラブルを渡すことで、複数引数を取る関数を並列化できる。
- ``apply_async()``: 1 回だけ非同期に関数を呼び出し、``Future`` に似た結果オブジェクトを返す。``callback`` 引数に関数を渡すと、結果が得られた時点でそれを自動的に呼び出せる。
- ``imap()`` / ``imap_unordered()``: ``map()`` はすべての結果が揃うまでブロックしてリストを返すが、これらは結果を 1 件ずつ遅延的に返すイテレータを返す。大量データを扱う場合や、結果が出るたびに進捗を表示したい場合に向く（``imap_unordered`` は結果が出た順に返すため、入力順を保持する ``imap`` より速く結果を得られることがある）。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def power(base, exp):
       return base ** exp

   if __name__ == "__main__":
       with mp.Pool(processes=4) as pool:
           results = pool.starmap(power, [(2, 3), (3, 2), (5, 2)])
       print(results)
   # 出力: [8, 9, 25]

``apply_async()`` に ``callback`` を渡す例は以下の通り。結果を待たずに処理を続け、結果が得られた時点で ``callback`` に指定した関数が親プロセス内で呼ばれる。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def square(x):
       return x * x

   results = []

   def store_result(value):
       results.append(value)

   if __name__ == "__main__":
       with mp.Pool(processes=4) as pool:
           pool.apply_async(square, args=(10,), callback=store_result)
           pool.close()
           pool.join()  # コールバックの完了を含めて待つ
       print(results)
   # 出力: [100]

multiprocessing.Queue
------------------------

プロセスはメモリ空間を共有しないため、変数を直接共有することはできない。プロセス間通信（IPC）には ``Queue`` を使うのが基本的な方法で、内部でデータを pickle によりシリアライズしてやり取りする。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def producer(q):
       for i in range(5):
           q.put(i)
       q.put(None)  # 終了の合図

   def consumer(q):
       while True:
           item = q.get()
           if item is None:
               break
           print(f"受信: {item}")

   if __name__ == "__main__":
       q = mp.Queue()
       p1 = mp.Process(target=producer, args=(q,))
       p2 = mp.Process(target=consumer, args=(q,))
       p1.start()
       p2.start()
       p1.join()
       p2.join()
   # 出力:
   # 受信: 0
   # 受信: 1
   # 受信: 2
   # 受信: 3
   # 受信: 4

Value / Array / Manager による状態共有
------------------------------------------

``Queue`` によるメッセージのやり取りとは別に、単純な値や配列を複数のプロセス間で直接共有したい場合は ``multiprocessing.Value``・``multiprocessing.Array`` が使える。内部で共有メモリを使い、``threading.Lock`` と同様に使える ``multiprocessing.Lock`` を介して安全に更新できる。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   def increment(counter, lock):
       for _ in range(1000):
           with lock:
               counter.value += 1

   if __name__ == "__main__":
       counter = mp.Value("i", 0)  # "i" は int を表す型コード
       lock = mp.Lock()
       procs = [mp.Process(target=increment, args=(counter, lock))
                for _ in range(4)]
       for p in procs:
           p.start()
       for p in procs:
           p.join()
       print(counter.value)
   # 出力: 4000

リストや辞書のような、より複雑なデータ構造を共有したい場合は、``multiprocessing.Manager()`` が返す ``dict``/``list`` 風のプロキシオブジェクトを使うと簡単に扱える。

.. code-block:: python
   :linenos:

   import multiprocessing as mp

   if __name__ == "__main__":
       with mp.Manager() as manager:
           shared_dict = manager.dict()
           shared_dict["count"] = 0
           # shared_dict を各プロセスに渡して更新できる

.. note::

   より高レベルな ``Pool``/``Executor`` 風の API を使いたい場合は :doc:`concurrent_futures` の ``ProcessPoolExecutor`` も検討するとよい。一方、並列化したい処理が CPU バウンドではなく I/O 待ちが中心の場合は、プロセスを起動するオーバーヘッドをかけずに :doc:`threading` を使う方が適していることが多い。
