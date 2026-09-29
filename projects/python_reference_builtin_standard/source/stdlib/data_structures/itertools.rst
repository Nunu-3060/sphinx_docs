itertools
=========

効率のよいループ処理のためのイテレータを生成する関数群を提供するモジュール。
組み込みの ``map`` や ``filter`` と同様、要素を必要になった時点で
遅延評価するため、大きな（あるいは無限の）データ列もメモリを圧迫せずに
扱える。

itertools.chain
----------------

複数のイテラブルを、あたかも 1 つの連続したイテラブルであるかのように
つなげて反復する。

.. code-block:: python

   >>> from itertools import chain
   >>> list(chain([1, 2], (3, 4), "56"))
   [1, 2, 3, 4, '5', '6']

itertools.product
------------------

複数のイテラブルの直積（デカルト積）を生成する。入れ子の ``for`` ループを
書く代わりに使える。

.. code-block:: python

   >>> from itertools import product
   >>> list(product([1, 2], ["a", "b"]))
   [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
   >>> list(product([0, 1], repeat=2))
   [(0, 0), (0, 1), (1, 0), (1, 1)]

itertools.combinations / itertools.permutations
-------------------------------------------------

``combinations`` は順序を無視した組み合わせ、``permutations`` は
順序を考慮した並びを列挙する。

.. code-block:: python

   >>> from itertools import combinations, permutations
   >>> list(combinations("ABC", 2))
   [('A', 'B'), ('A', 'C'), ('B', 'C')]
   >>> list(permutations("ABC", 2))
   [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

itertools.groupby
------------------

隣接する要素をキー関数の値でグループ化する。事前に同じキーの要素が
隣り合うようソート済みであることが前提となる点に注意。

.. code-block:: python

   >>> from itertools import groupby
   >>> data = sorted(["apple", "banana", "avocado", "blueberry"], key=lambda s: s[0])
   >>> for key, group in groupby(data, key=lambda s: s[0]):
   ...     print(key, list(group))
   ...
   a ['apple', 'avocado']
   b ['banana', 'blueberry']

itertools.islice
-----------------

イテレータに対してスライスのような範囲指定を行う。通常のスライス構文
（``[start:stop:step]``）はイテレータには使えないため、代わりに用いる。

.. code-block:: python

   >>> from itertools import islice, count
   >>> list(islice(range(10), 2, 8, 2))
   [2, 4, 6]
   >>> list(islice(count(10), 3))
   [10, 11, 12]

itertools.count / itertools.cycle
------------------------------------

``count`` は指定した開始値から無限に増加する数列を、``cycle`` は
イテラブルの要素を無限に繰り返す。どちらも ``islice`` などと組み合わせて
必要な分だけ取り出すのが基本パターン。

.. code-block:: python

   >>> from itertools import count, cycle, islice
   >>> list(islice(count(0, 2), 5))
   [0, 2, 4, 6, 8]
   >>> list(islice(cycle(["a", "b", "c"]), 7))
   ['a', 'b', 'c', 'a', 'b', 'c', 'a']

itertools.accumulate
----------------------

要素を左から順に累積的に関数へ適用し、その途中経過をすべてイテレータ
として返す。:doc:`functools` の ``functools.reduce`` が最終結果だけを
返すのに対し、``accumulate`` は累積和・累積積のような「途中の値」を
順に得られる。

.. code-block:: python

   >>> from itertools import accumulate
   >>> list(accumulate([1, 2, 3, 4]))
   [1, 3, 6, 10]
   >>> list(accumulate([1, 2, 3, 4], lambda a, b: a * b))
   [1, 2, 6, 24]

itertools.zip_longest
------------------------

組み込みの ``zip`` は最も短いイテラブルの長さで結果が切り詰められるのに対し、``zip_longest`` は最も長いイテラブルの長さに合わせ、足りない要素は ``fillvalue`` （デフォルトは ``None``）で埋める。

.. code-block:: python

   >>> from itertools import zip_longest
   >>> list(zip_longest(["a", "b", "c"], [1, 2], fillvalue="?"))
   [('a', 1), ('b', 2), ('c', '?')]
