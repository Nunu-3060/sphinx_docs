math
====

C 言語の数学関数群を利用できるようにするモジュール。三角関数や対数関数、定数など、主に浮動小数点数を対象とした数値計算のための機能を提供する（``gcd`` や ``factorial`` など整数向けの関数も含む）。

math.sqrt
---------

平方根を計算する。負の数を渡すと ``ValueError`` が送出される。

.. code-block:: python
   :linenos:

   >>> import math
   >>> math.sqrt(2)
   1.4142135623730951
   >>> math.sqrt(16)
   4.0

math.floor / math.ceil
-----------------------

数値を切り捨て（``floor``）・切り上げ（``ceil``）て整数にする。

.. code-block:: python
   :linenos:

   >>> math.floor(3.7)
   3
   >>> math.ceil(3.2)
   4
   >>> math.floor(-3.2)
   -4

math.pi / math.e
-----------------

円周率や自然対数の底など、数学的によく使われる定数を提供する。

.. code-block:: python
   :linenos:

   >>> math.pi
   3.141592653589793
   >>> math.e
   2.718281828459045
   >>> math.pi * 5 ** 2  # 半径 5 の円の面積
   78.53981633974483

math.log
--------

対数を計算する。第 2 引数で底を指定でき、省略時は自然対数（底 ``e``）となる。底が 2 や 10 の場合は、より精度の高い専用関数 ``math.log2`` / ``math.log10`` を使うとよい。

.. code-block:: python
   :linenos:

   >>> math.log(math.e)
   1.0
   >>> math.log(100, 10)
   2.0
   >>> math.log2(8)
   3.0
   >>> math.log10(1000)
   3.0

math.sin / math.cos / math.tan
--------------------------------

三角関数を計算する。引数はラジアンで指定する。度数からラジアンへの変換には ``math.radians`` を使う。

.. code-block:: python
   :linenos:

   >>> math.sin(math.pi / 2)
   1.0
   >>> math.cos(0)
   1.0
   >>> math.tan(math.radians(45))
   0.9999999999999999

math.asin / math.acos / math.atan / math.atan2
--------------------------------------------------

逆三角関数を計算する。戻り値はラジアンで表される。``atan2(y, x)`` は ``atan(y / x)`` と異なり、``x`` と ``y`` それぞれの符号から正しい象限の角度を判定できる。

.. code-block:: python
   :linenos:

   >>> math.asin(1.0)
   1.5707963267948966
   >>> math.acos(1.0)
   0.0
   >>> math.atan(1.0)
   0.7853981633974483
   >>> math.atan2(1, -1)
   2.356194490192345
   >>> math.atan(1 / -1)  # atan だけでは象限を区別できない
   -0.7853981633974483

math.gcd
--------

複数の整数の最大公約数を求める。

.. code-block:: python
   :linenos:

   >>> math.gcd(12, 18)
   6
   >>> math.gcd(24, 36, 60)
   12

math.factorial
--------------

階乗（``n!``）を計算する。負の数を渡すと ``ValueError`` が、整数以外（``float`` など）を渡すと ``TypeError`` が送出される。

.. code-block:: python
   :linenos:

   >>> math.factorial(5)
   120
   >>> math.factorial(0)
   1

math.isclose
------------

2 つの浮動小数点数がほぼ等しいかを判定する。浮動小数点数は演算誤差を持つため、``==`` による厳密な比較ではなく本関数を使うのが安全である。

.. code-block:: python
   :linenos:

   >>> 0.1 + 0.2 == 0.3
   False
   >>> math.isclose(0.1 + 0.2, 0.3)
   True
   >>> math.isclose(1.0, 1.0001, rel_tol=1e-3)
   True

.. note::

   ``rel_tol`` の既定値は ``1e-09`` で、相対誤差で比較する。そのため ``0.0`` との比較では ``abs_tol`` を指定しないと、ごく小さな値でも ``False`` になる点に注意する（例: ``math.isclose(1e-10, 0.0)`` は ``False``）。

Python 3.11 以降に追加された主な関数
------------------------------------

近年のバージョンでは、次のような関数が追加されている。

- ``math.cbrt(x)``: 立方根（3.11）
- ``math.exp2(x)``: 2 の ``x`` 乗（3.11）
- ``math.sumprod(p, q)``: 2 つのイテラブルの積和（内積）を高精度に計算する（3.12）
- ``math.fma(x, y, z)``: ``x * y + z`` を途中で丸めずに 1 回の丸めで計算する（3.13）

.. code-block:: python
   :linenos:

   >>> math.cbrt(27)
   3.0
   >>> math.exp2(10)
   1024.0
   >>> math.sumprod([1, 2, 3], [4, 5, 6])
   32
   >>> math.fma(2.0, 3.0, 4.0)
   10.0
