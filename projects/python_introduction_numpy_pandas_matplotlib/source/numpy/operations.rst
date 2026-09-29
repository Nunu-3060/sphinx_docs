配列の演算
============

要素ごとの演算
----------------

``ndarray`` 同士の四則演算は、Python の list とは異なり、要素ごとに計算されます。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.array([1, 2, 3])
   b: np.ndarray = np.array([10, 20, 30])

   a + b
   # array([11, 22, 33])

   a * b
   # array([10, 40, 90])

   a * 2
   # array([2, 4, 6])

比較演算子も同様に要素ごとに適用され、真偽値の配列が返されます。

.. code-block:: python

   a == np.array([1, 0, 3])
   # array([ True, False,  True])

行列の掛け算
--------------

これまで見てきた ``*`` は、あくまで要素ごとの掛け算（アダマール積）です。数学的な意味での行列の掛け算（行列積）を行いたい場合は、``*`` ではなく ``@`` 演算子（または ``np.matmul``）を使います。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.array([[1, 2], [3, 4]])
   b: np.ndarray = np.array([[5, 6], [7, 8]])

   a * b
   # array([[ 5, 12],
   #        [21, 32]])
   # 要素ごとの掛け算（アダマール積）

   a @ b
   # array([[19, 22],
   #        [43, 50]])
   # 行列積（1 行目・1 列目: 1*5 + 2*7 = 19 など）

   np.matmul(a, b)
   # a @ b と同じ結果

.. note::

   ``*`` は「同じ形状の配列同士を要素ごとに掛け合わせる」演算であるのに対し、``@`` は「行列として掛け合わせる」演算です。数式の行列積をそのままコードにしたい場合に ``*`` を使ってしまうと、意図しない結果になるので注意してください。

数学関数（ユニバーサル関数）
------------------------------

``np.sin`` / ``np.cos`` / ``np.tan`` / ``np.exp`` / ``np.log`` / ``np.sqrt`` のような数学関数も、配列を渡すと要素ごとに計算されます。このように配列の要素ごとに処理を行う関数は「ユニバーサル関数（ufunc）」と呼ばれます。

.. code-block:: python

   import numpy as np

   angles_deg: np.ndarray = np.array([0, 30, 90])
   angles_rad: np.ndarray = np.deg2rad(angles_deg)
   # np.deg2rad で度数法から弧度法（ラジアン）に変換する

   np.sin(angles_rad)
   # array([0. , 0.5, 1. ])

   np.log(np.array([1.0, np.e, 10.0]))
   # array([0.        , 1.        , 2.30258509])
   # np.log は自然対数（底が e の対数）

   np.sqrt(np.array([1, 4, 9, 16]))
   # array([1., 2., 3., 4.])

Python 標準の ``math`` モジュールにも同名の関数（``math.sin`` など）がありますが、``math`` の関数はスカラー（単一の値）にしか使えません。配列全体にまとめて適用したい場合は、``for`` ループで ``math.sin`` を繰り返し呼び出すのではなく、numpy の ufunc を使うことで、より簡潔かつ高速に計算できます。
