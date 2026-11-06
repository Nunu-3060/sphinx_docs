statistics
==========

数値データに対する基本的な統計量を計算するためのモジュール。平均や中央値、分散といった代表値を、外部ライブラリを使わずに標準ライブラリだけで求めたい場合に利用する。

statistics.mean / statistics.fmean
------------------------------------

データの算術平均（相加平均）を計算する。``mean`` は入力の型を保とうとするため、整数のリストに対しては結果が割り切れれば ``int`` を返す。常に ``float`` で高速に計算したい場合は ``fmean`` を使う（3.11 以降は ``weights`` 引数で重み付き平均も計算できる）。

.. code-block:: python
   :linenos:

   >>> import statistics
   >>> data = [1, 2, 3, 4, 5]
   >>> statistics.mean(data)
   3
   >>> statistics.fmean(data)
   3.0
   >>> statistics.fmean([1, 2, 3], weights=[3, 1, 1])
   1.6

statistics.median
------------------

データを昇順に並べたときの中央値を返す。データ数が偶数の場合は、中央 2 つの値の平均となる。外れ値の影響を受けにくいのが特徴。

.. code-block:: python
   :linenos:

   >>> statistics.median([1, 2, 3, 4, 5])
   3
   >>> statistics.median([1, 2, 3, 4])
   2.5

statistics.mode / statistics.multimode
----------------------------------------

データの中で最も頻繁に現れる値（最頻値）を返す。最頻値が複数ある場合は最初に現れたものを返す。すべての最頻値をリストで得たい場合は ``multimode`` を使う。

.. code-block:: python
   :linenos:

   >>> statistics.mode([1, 1, 2, 3, 3, 3, 4])
   3
   >>> statistics.mode(["a", "b", "b", "c"])
   'b'
   >>> statistics.multimode([1, 1, 2, 2, 3])
   [1, 2]

statistics.stdev / statistics.variance
-----------------------------------------

標本標準偏差・標本分散を計算する。これらはデータのばらつきの度合いを表す指標である。母集団全体に対して計算したい場合は ``pstdev`` / ``pvariance`` を使う。

.. code-block:: python
   :linenos:

   >>> data = [2, 4, 4, 4, 5, 5, 7, 9]
   >>> statistics.variance(data)
   4.571428571428571
   >>> statistics.stdev(data)
   2.138089935299395

相関と回帰
----------

2 つのデータ列の関係を調べる関数も用意されている。``correlation`` はピアソンの相関係数（3.12 以降は ``method="ranked"`` でスピアマンの順位相関係数）を、``linear_regression`` は単回帰（最小二乗法）の傾きと切片を返す。

.. code-block:: python
   :linenos:

   >>> x = [1, 2, 3, 4, 5]
   >>> statistics.correlation(x, [2, 4, 6, 8, 10])
   1.0
   >>> statistics.linear_regression(x, [3, 5, 7, 9, 11])
   LinearRegression(slope=2.0, intercept=1.0)

.. note::

   Python 3.13 以降では、カーネル密度推定を行う ``statistics.kde`` と、推定した分布から乱数を生成する ``statistics.kde_random`` も追加されている。より本格的な数値計算やデータ分析には、NumPy や pandas などのサードパーティライブラリの利用を検討するとよい。
