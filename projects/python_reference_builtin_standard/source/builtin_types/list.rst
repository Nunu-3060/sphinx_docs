list
====

``list`` はミュータブル（変更可能）なシーケンス型で、要素の追加・削除・並べ替えなど、その場（in-place）でデータを操作するためのメソッドを豊富に備えている。ここでは、それらのメソッドをよく使うグループごとに解説する。既存のイテラブルから新しい ``list`` を生成する構文については :doc:`comprehension` を参照。

list.append / list.extend
--------------------------

``append`` はリストの末尾に要素を 1 つだけ追加する。``extend`` はイテラブル（別のリストやタプルなど）を受け取り、その要素をすべて末尾に追加する。

.. code-block:: python

   >>> nums = [1, 2, 3]
   >>> nums.append(4)
   >>> nums
   [1, 2, 3, 4]
   >>> nums.extend([5, 6])
   >>> nums
   [1, 2, 3, 4, 5, 6]

よくある間違いとして、複数の要素を追加したいのに ``append`` を使ってしまい、リストそのものが 1 つの要素として追加されてしまうケースがある。

.. code-block:: python

   >>> nums = [1, 2, 3]
   >>> nums.append([4, 5])
   >>> nums
   [1, 2, 3, [4, 5]]
   >>> nums = [1, 2, 3]
   >>> nums.extend([4, 5])
   >>> nums
   [1, 2, 3, 4, 5]

「複数の要素をまとめて追加したい」場合は ``extend`` を、「1 つの要素（リストそのものを含む）を追加したい」場合は ``append`` を使う、と区別すると分かりやすい。

list.insert
-----------

``insert(index, value)`` は指定したインデックスの位置に要素を挿入する。それ以降の要素は 1 つずつ後ろにずれる。

.. code-block:: python

   >>> fruits = ["apple", "banana", "cherry"]
   >>> fruits.insert(1, "blueberry")
   >>> fruits
   ['apple', 'blueberry', 'banana', 'cherry']
   >>> fruits.insert(0, "avocado")
   >>> fruits
   ['avocado', 'apple', 'blueberry', 'banana', 'cherry']

list.remove / list.pop
-----------------------

``remove(value)`` は指定した値と最初に一致する要素を削除する。値そのもので指定するため、リスト内に見つからない場合は ``ValueError`` が発生する。一方 ``pop(index)`` はインデックスで指定した要素を削除し、その値を返す。引数を省略すると末尾の要素を取り出す。

.. code-block:: python

   >>> nums = [10, 20, 30, 20]
   >>> nums.remove(20)
   >>> nums
   [10, 30, 20]
   >>> nums.remove(999)
   Traceback (most recent call last):
       ...
   ValueError: list.remove(x): x not in list

   >>> nums = [10, 20, 30]
   >>> nums.pop()
   30
   >>> nums
   [10, 20]
   >>> nums.pop(0)
   10
   >>> nums
   [20]

list.sort / list.reverse
--------------------------

``sort`` はリストの要素をその場で並べ替える。``reverse`` はリストの要素の順序をその場で反転する。いずれも戻り値は ``None`` で、元のリスト自体が変更される点に注意する。新しい並べ替え済みのリストを別に得たい場合は、組み込み関数 ``sorted()`` を使う（こちらは元のリストを変更せず、並べ替えた新しいリストを返す）。

.. code-block:: python

   >>> nums = [3, 1, 4, 1, 5, 9, 2, 6]
   >>> nums.sort()
   >>> nums
   [1, 1, 2, 3, 4, 5, 6, 9]
   >>> nums.reverse()
   >>> nums
   [9, 6, 5, 4, 3, 2, 1, 1]

   >>> original = [3, 1, 2]
   >>> new_list = sorted(original)
   >>> new_list
   [1, 2, 3]
   >>> original
   [3, 1, 2]

``sort`` には ``key`` と ``reverse`` というキーワード引数がある。``key`` には各要素から並べ替えの基準となる値を取り出す関数を渡し、``reverse=True`` を指定すると降順に並べ替える。

.. code-block:: python

   >>> words = ["banana", "kiwi", "apple", "fig"]
   >>> words.sort(key=len)
   >>> words
   ['fig', 'kiwi', 'apple', 'banana']
   >>> words.sort(key=len, reverse=True)
   >>> words
   ['banana', 'apple', 'kiwi', 'fig']

list.index / list.count
--------------------------

``index(value)`` は指定した値と最初に一致する要素のインデックスを返す。見つからない場合は ``ValueError`` が発生する。``count(value)`` は指定した値がリスト中に出現する回数を返す。

.. code-block:: python

   >>> letters = ["a", "b", "c", "b", "a"]
   >>> letters.index("b")
   1
   >>> letters.index("z")
   Traceback (most recent call last):
       ...
   ValueError: 'z' is not in list
   >>> letters.count("a")
   2
   >>> letters.count("z")
   0

list.clear / list.copy
------------------------

``clear`` はリストの要素をすべて削除し、空のリストにする。``copy`` はリストの浅いコピー（shallow copy）を作成して返す。スライス ``lst[:]`` でも同じ結果が得られるが、``copy`` の方が意図が明確になる。

.. code-block:: python

   >>> nums = [1, 2, 3]
   >>> nums.clear()
   >>> nums
   []

   >>> original = [1, 2, 3]
   >>> copied = original.copy()
   >>> copied.append(4)
   >>> copied
   [1, 2, 3, 4]
   >>> original          # コピー先への変更は元のリストに影響しない
   [1, 2, 3]

.. warning::

   ``copy`` は浅いコピーであるため、リストの要素自体がミュータブルなオブジェクト（別のリストなど）の場合、そのオブジェクトは元のリストと共有される。要素も含めて完全に独立させたい場合は、標準ライブラリの :func:`copy.deepcopy` を使う。

スライス操作
------------

``lst[start:stop:step]`` の形式でリストの一部分を取り出すことができる。スライスは元のリストを変更せず、新しいリストを返す点に注意する。

.. code-block:: python

   >>> nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
   >>> nums[2:5]
   [2, 3, 4]
   >>> nums[:3]
   [0, 1, 2]
   >>> nums[7:]
   [7, 8, 9]
   >>> nums[::2]
   [0, 2, 4, 6, 8]
   >>> nums[::-1]
   [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

一方、スライスに対して代入を行うと、元のリストの該当部分をその場で置き換えることができる。置き換える要素の個数は、元の範囲の長さと一致していなくてもよい。

.. code-block:: python

   >>> nums = [0, 1, 2, 3, 4]
   >>> nums[1:3] = [10, 20, 30]
   >>> nums
   [0, 10, 20, 30, 3, 4]
   >>> nums[1:4] = []
   >>> nums
   [0, 3, 4]
