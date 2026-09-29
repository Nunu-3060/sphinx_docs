形状操作
========

reshape
-------

``reshape`` を使うと、要素数を変えずに配列の形状を変更できます。

.. code-block:: python

   import numpy as np

   a: np.ndarray = np.arange(6)
   print(a)
   # [0 1 2 3 4 5]

   b: np.ndarray = a.reshape(2, 3)
   print(b)
   # [[0 1 2]
   #  [3 4 5]]

要素数が一致しない形状を指定するとエラーになります。次元の 1 箇所だけ ``-1`` を指定すると、残りの次元から自動的に要素数を計算してくれます。

.. code-block:: python

   a.reshape(3, -1)
   # array([[0, 1],
   #        [2, 3],
   #        [4, 5]])

transpose と flatten
----------------------

.. code-block:: python

   b: np.ndarray = np.array([[1, 2, 3], [4, 5, 6]])

   b.T
   # array([[1, 4],
   #        [2, 5],
   #        [3, 6]])
   # 行と列を入れ替える（転置）

   b.flatten()
   # array([1, 2, 3, 4, 5, 6])
   # 1 次元配列に変換する

.. note::

   1 次元に変換する方法には ``ravel`` もあります。``flatten`` は必ずコピーを返すのに対し、``ravel`` は可能な場合は元の配列と同じメモリを共有する「ビュー」を返します。そのため ``ravel`` の方が高速な場合がありますが、返された配列を変更すると元の配列にも影響が及ぶことがあるので注意してください。挙動を確実にコピーにしたい場合は ``flatten`` を使ってください。

配列の結合
------------

複数の配列を結合するには ``concatenate`` や ``stack`` を使います。

.. code-block:: python

   a: np.ndarray = np.array([1, 2, 3])
   b: np.ndarray = np.array([4, 5, 6])

   np.concatenate([a, b])
   # array([1, 2, 3, 4, 5, 6])  既存の次元に沿って連結する

   np.stack([a, b])
   # array([[1, 2, 3],
   #        [4, 5, 6]])  新しい次元を追加して積み重ねる

2 次元配列の場合は、``axis`` 引数でどの方向に連結するかを指定できます。

.. code-block:: python

   a2: np.ndarray = np.array([[1, 2, 3], [4, 5, 6]])
   b2: np.ndarray = np.array([[7, 8, 9], [10, 11, 12]])

   np.concatenate([a2, b2], axis=0)
   # array([[ 1,  2,  3],
   #        [ 4,  5,  6],
   #        [ 7,  8,  9],
   #        [10, 11, 12]])  縦方向（行を追加する方向）に連結する

   np.concatenate([a2, b2], axis=1)
   # array([[ 1,  2,  3,  7,  8,  9],
   #        [ 4,  5,  6, 10, 11, 12]])  横方向（列を追加する方向）に連結する

``axis`` を省略した場合は既定値の ``0`` が使われるため、最初の例の ``np.concatenate([a, b])`` は ``axis=0`` を指定したのと同じ結果になります。

次元の追加（newaxis / expand_dims）
--------------------------------------

既存の配列に、サイズ 1 の次元を新しく追加したい場合は ``np.newaxis`` または ``np.expand_dims`` を使います。たとえば 1 次元のベクトルを、行が 1 つの 2 次元配列（あるいは列が 1 つの 2 次元配列）として扱いたい場合に使われます。

.. code-block:: python

   v: np.ndarray = np.array([1, 2, 3])
   v.shape
   # (3,)

   v[:, np.newaxis]
   # array([[1],
   #        [2],
   #        [3]])
   v[:, np.newaxis].shape
   # (3, 1)  列方向に次元を追加する

   np.expand_dims(v, axis=0)
   # array([[1, 2, 3]])
   np.expand_dims(v, axis=0).shape
   # (1, 3)  行方向に次元を追加する

``np.newaxis`` はスライスの中で使う書き方、``np.expand_dims`` は関数として ``axis`` を指定する書き方です。どちらも同じ結果を得られるので、読みやすいと感じる方を使ってください。
