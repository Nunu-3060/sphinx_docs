配列の属性
==========

``ndarray`` は自身の形状や型に関する情報を属性として持っています。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.array([[1, 2, 3], [4, 5, 6]])

   a.shape
   # (2, 3)  各次元の要素数

   a.ndim
   # 2  次元数

   a.size
   # 6  全要素数

   a.dtype
   # dtype('int64')  要素の型

.. note::

   ``dtype`` の表示は環境によって異なる場合があります。たとえば整数の配列は、numpy 2.0 より前のバージョンを Windows で使用すると、``int64`` ではなく ``int32`` と表示されます（numpy 2.0 以降は Windows でも ``int64`` が既定です）。表示される具体的な型名よりも、「同じ型で統一されている」という点を理解することが重要です。

1 次元配列と 2 次元配列
--------------------------

``shape`` を見ると配列の構造がわかります。

.. code-block:: python

   v: np.ndarray = np.array([1, 2, 3])
   v.shape
   # (3,)  1 次元（ベクトル）

   m: np.ndarray = np.array([[1, 2, 3], [4, 5, 6]])
   m.shape
   # (2, 3)  2 次元（行列）。2 行 3 列。

2 次元配列は「行列」としてイメージすると理解しやすく、``shape`` の 1 つ目の値が行数、2 つ目の値が列数に対応します。
