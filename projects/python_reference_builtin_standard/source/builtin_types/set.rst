set
===

Python の集合型 ``set`` が持つメソッド群。``set`` は重複を許さない要素の集まりで、順序を持たない。要素の追加・削除や、和集合・積集合といった集合演算を高速に行えるのが特徴。既存のイテラブルから新しい ``set`` を生成する構文については :doc:`comprehension` を参照。

set.add / set.remove / set.discard
-------------------------------------

``add`` は集合に要素を 1 つ追加する。すでに同じ要素があれば何も起こらない。``remove`` と ``discard`` はどちらも要素を取り除くが、指定した要素が存在しない場合の挙動が異なる。``remove`` は ``KeyError`` を発生させるのに対し、``discard`` はエラーにならず何もしない。

.. code-block:: python

   >>> fruits = {"apple", "banana"}
   >>> fruits.add("cherry")
   >>> fruits
   {'apple', 'banana', 'cherry'}
   >>> fruits.remove("banana")
   >>> fruits
   {'apple', 'cherry'}
   >>> fruits.remove("melon")
   Traceback (most recent call last):
       ...
   KeyError: 'melon'
   >>> fruits.discard("melon")
   >>> fruits
   {'apple', 'cherry'}

.. note::

   存在しないかもしれない要素を取り除く場合は ``discard`` を使うと、``KeyError`` を気にせずに済む。

set.union / set.intersection / set.difference
--------------------------------------------------

複数の集合に対する集合演算を行う。``union`` は和集合（いずれかに含まれる要素）、``intersection`` は積集合（両方に含まれる要素）、``difference`` は差集合（片方にのみ含まれる要素）を返す。それぞれ演算子 ``|``、``&``、``-`` でも同じ結果が得られる。

.. code-block:: python

   >>> a = {1, 2, 3, 4}
   >>> b = {3, 4, 5, 6}
   >>> a.union(b)
   {1, 2, 3, 4, 5, 6}
   >>> a | b
   {1, 2, 3, 4, 5, 6}
   >>> a.intersection(b)
   {3, 4}
   >>> a & b
   {3, 4}
   >>> a.difference(b)
   {1, 2}
   >>> a - b
   {1, 2}

set.symmetric_difference / ``^``
------------------------------------

``symmetric_difference`` は対称差集合（どちらか一方にのみ含まれる要素）を返す。演算子 ``^`` でも同じ結果が得られる。``difference``\ （\ ``-``\ ）\ が一方向の差だけを見るのに対し、対称差は両方向の差を合わせたものになる。

.. code-block:: python

   >>> a = {1, 2, 3, 4}
   >>> b = {3, 4, 5, 6}
   >>> a.symmetric_difference(b)
   {1, 2, 5, 6}
   >>> a ^ b
   {1, 2, 5, 6}

set.update / set.intersection_update / set.difference_update / set.symmetric_difference_update
------------------------------------------------------------------------------------------------

これまでに紹介した ``union`` ``intersection`` ``difference`` ``symmetric_difference`` はいずれも **新しい集合を返し、元の集合を変更しない**。これに対して、末尾に ``_update`` が付くメソッド群は、辞書の ``update`` やリストの ``append`` / ``extend`` と同様に、**その場（in-place）で元の集合を書き換える**。

.. code-block:: python

   >>> a = {1, 2, 3, 4}
   >>> b = {3, 4, 5, 6}
   >>> a.update(b)              # a |= b と同じ
   >>> a
   {1, 2, 3, 4, 5, 6}

   >>> a = {1, 2, 3, 4}
   >>> a.intersection_update(b)  # a &= b と同じ
   >>> a
   {3, 4}

   >>> a = {1, 2, 3, 4}
   >>> a.difference_update(b)    # a -= b と同じ
   >>> a
   {1, 2}

   >>> a = {1, 2, 3, 4}
   >>> a.symmetric_difference_update(b)  # a ^= b と同じ
   >>> a
   {1, 2, 5, 6}

set.pop / set.clear
-----------------------

``pop`` は集合から要素を 1 つ取り除いて返す。``set`` は順序を持たないため、どの要素が取り除かれるかは決まっていない。空の集合に対して呼び出すと ``KeyError`` が発生する。``clear`` は集合の要素をすべて取り除き、空にする。

.. code-block:: python

   >>> fruits = {"apple", "banana", "cherry"}
   >>> fruits.pop()          # どの要素が返るかは不定
   'apple'
   >>> fruits.clear()
   >>> fruits
   set()
   >>> fruits.pop()
   Traceback (most recent call last):
       ...
   KeyError: 'pop from an empty set'

set.issubset / set.issuperset
---------------------------------

``issubset`` はある集合が別の集合の部分集合かどうか、``issuperset`` は逆にある集合が別の集合を包含しているかどうかを判定する。演算子 ``<=`` と ``>=`` でも同じ判定ができる。

.. code-block:: python

   >>> a = {1, 2}
   >>> b = {1, 2, 3, 4}
   >>> a.issubset(b)
   True
   >>> a <= b
   True
   >>> b.issuperset(a)
   True
   >>> b >= a
   True

.. note::

   ``set`` はミュータブル（変更可能）だが、イミュータブルな対をなす型として :doc:`../builtins/type_conversion` で紹介した ``frozenset`` がある。辞書のキーや別の集合の要素として使いたい場合は ``frozenset`` を選ぶ。また、``set`` はリストなどから重複を取り除く用途や、``in`` 演算子による高速なメンバーシップテストにもよく利用される。
