time
====

時刻の取得や時間計測、スリープなど、システムクロックに関する低レベルな機能を提供するモジュール。エポック（1970-01-01 UTC）からの経過秒数を扱う場面や、処理時間の計測に用いる。

time.time
---------

エポックからの経過秒数を浮動小数点数で返す。

.. code-block:: python

   >>> import time
   >>> time.time()  # doctest: +SKIP
   1789516800.123456

time.sleep
----------

指定した秒数だけ処理を一時停止する。

.. code-block:: python

   >>> import time
   >>> print("start")
   start
   >>> time.sleep(1.5)
   >>> print("end")
   end

time.perf_counter
------------------

処理時間の計測に特化した高精度なカウンタを返す。基準点は不定なので、差分（経過時間）を求める用途にのみ使う。ベンチマークには ``time.time()`` よりもこちらが適している。

.. code-block:: python

   >>> import time
   >>> start = time.perf_counter()
   >>> total = sum(range(1_000_000))
   >>> elapsed = time.perf_counter() - start
   >>> elapsed  # doctest: +SKIP
   0.021345

time.strftime / time.localtime
---------------------------------

``localtime`` はエポック秒をローカルタイムの ``struct_time`` に変換し、``strftime`` はそれを書式文字列に変換する。

.. code-block:: python

   >>> import time
   >>> t = time.localtime()
   >>> time.strftime("%Y-%m-%d %H:%M:%S", t)  # doctest: +SKIP
   '2026-09-16 13:45:30'

.. note::

   カレンダー計算（日付の加減算、曜日の取得、タイムゾーン変換など）を伴う処理では :doc:`datetime` を使う方が扱いやすい。一方、処理時間の計測や単純なスリープ、OS レベルのエポック秒が必要な場面では ``time`` モジュールが適している。両者は目的に応じて使い分けるとよい。
