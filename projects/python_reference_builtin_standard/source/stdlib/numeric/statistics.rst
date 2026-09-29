statistics
==========

数値データに対する基本的な統計量を計算するためのモジュール。平均や
中央値、分散といった代表値を、外部ライブラリを使わずに標準ライブラリ
だけで求めたい場合に利用する。

statistics.mean
----------------

データの算術平均（相加平均）を計算する。

.. code-block:: python

   >>> import statistics
   >>> data = [1, 2, 3, 4, 5]
   >>> statistics.mean(data)
   3

statistics.median
------------------

データを昇順に並べたときの中央値を返す。データ数が偶数の場合は、
中央2つの値の平均となる。外れ値の影響を受けにくいのが特徴。

.. code-block:: python

   >>> statistics.median([1, 2, 3, 4, 5])
   3
   >>> statistics.median([1, 2, 3, 4])
   2.5

statistics.mode
----------------

データの中で最も頻繁に現れる値（最頻値）を返す。

.. code-block:: python

   >>> statistics.mode([1, 1, 2, 3, 3, 3, 4])
   3
   >>> statistics.mode(["a", "b", "b", "c"])
   'b'

statistics.stdev / statistics.variance
-----------------------------------------

標本標準偏差・標本分散を計算する。これらはデータのばらつきの度合いを
表す指標である。
母集団全体に対して計算したい場合は ``pstdev`` / ``pvariance`` を使う。

.. code-block:: python

   >>> data = [2, 4, 4, 4, 5, 5, 7, 9]
   >>> statistics.variance(data)
   4.571428571428571
   >>> statistics.stdev(data)
   2.138089935299395
