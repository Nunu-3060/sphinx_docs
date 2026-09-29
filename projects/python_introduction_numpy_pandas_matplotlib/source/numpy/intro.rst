numpy とは
==========

numpy (Numerical Python) は、Python で数値計算を効率的に行うためのライブラリです。numpy が提供する多次元配列 ``ndarray`` は、pandas や matplotlib をはじめ多くのライブラリの基盤としても使われています。

公式サイト: `numpy <https://numpy.org/>`_

なぜ numpy を使うのか
----------------------

- Python 標準の ``list`` よりも高速に大量の数値データを扱える
- 同じ型のデータをまとめて扱うことでメモリ効率がよい
- 数学関数、線形代数、乱数生成など、数値計算に必要な機能が揃っている

list と ndarray の違い
------------------------

Python の ``list`` は要素ごとに異なる型を格納できる汎用的なコンテナですが、その分オーバーヘッドがあります。numpy の ``ndarray`` は同じ型のデータを連続したメモリ領域に格納するため、要素ごとの演算をまとめて高速に実行できます。

.. code-block:: python

   import numpy as np

   data: list[int] = [1, 2, 3]
   # list を 2 倍しても、要素が繰り返されるだけ
   print(data * 2)  # [1, 2, 3, 1, 2, 3]

   arr: np.ndarray = np.array(data)
   # ndarray は要素ごとに 2 倍される
   print(arr * 2)  # [2 4 6]

このように、``ndarray`` を使うと「配列全体に対する演算」を直感的に書くことができます。次のページから、``ndarray`` の作成方法を見ていきます。
