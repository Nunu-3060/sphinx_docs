配列の作成
==========

``ndarray`` を作成するには、いくつかの方法があります。

list からの作成
----------------

``np.array`` に Python の ``list``\ （入れ子の list でも可）を渡すことで ``ndarray`` を作成できます。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.array([1, 2, 3])
   print(a)
   # [1 2 3]

   b: np.ndarray = np.array([[1, 2, 3], [4, 5, 6]])
   print(b)
   # [[1 2 3]
   #  [4 5 6]]

初期値を指定した作成
---------------------

決まった値で埋めた配列を作成する関数も用意されています。

.. code-block:: python

   np.zeros((2, 3))
   # 0 で埋めた 2x3 の配列

   np.ones((2, 3))
   # 1 で埋めた 2x3 の配列

   np.full((2, 3), 7)
   # 7 で埋めた 2x3 の配列

連続した値の作成
----------------

.. code-block:: python

   np.arange(0, 10, 2)
   # array([0, 2, 4, 6, 8])
   # Python 標準の range と同様に、開始・終了（含まない）・間隔を指定する

   np.linspace(0, 1, 5)
   # array([0.  , 0.25, 0.5 , 0.75, 1.  ])
   # 開始から終了（含む）までを等間隔で分割した個数を指定する

dtype の指定
------------

``ndarray`` の要素はすべて同じ型（``dtype``）を持ちます。作成時に明示的に指定することもできます。

.. code-block:: python

   import numpy as np
   import numpy.typing as npt

   a: npt.NDArray[np.float64] = np.array([1, 2, 3], dtype=np.float64)
   print(a)
   # [1. 2. 3.]
   print(a.dtype)
   # float64

dtype を指定しない場合は、渡した値から自動的に適切な型が推定されます。

.. note::

   ``np.ndarray`` は要素の型を問わない型ヒントですが、``numpy.typing.NDArray`` を使うと ``NDArray[np.float64]`` のように要素の型まで含めて表現できます。要素の型（dtype）を意識するこのページのような場面では、こちらを使うとより正確な型ヒントになります。
