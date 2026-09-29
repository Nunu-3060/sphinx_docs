operator
========

``+`` や ``[]`` などの演算子と等価な処理を行う関数群を提供するモジュール。``lambda`` を書く代わりに使うことで、意図が明確になり実行速度も有利になることが多い。

operator.itemgetter
----------------------

指定したインデックスやキーで要素を取得する呼び出し可能オブジェクトを
生成する。``sorted`` の ``key`` 引数としてよく利用される。

.. code-block:: python

   >>> from operator import itemgetter
   >>> people = [{"name": "b", "age": 30}, {"name": "a", "age": 25}]
   >>> sorted(people, key=itemgetter("age"))
   [{'name': 'a', 'age': 25}, {'name': 'b', 'age': 30}]
   >>> pair = ("x", "y", "z")
   >>> itemgetter(0, 2)(pair)
   ('x', 'z')

operator.attrgetter
----------------------

指定した属性を取得する呼び出し可能オブジェクトを生成する。オブジェクトの
リストを属性値でソートする際などに使う。

.. code-block:: python

   >>> from operator import attrgetter
   >>> class Person:
   ...     def __init__(self, name, age):
   ...         self.name = name
   ...         self.age = age
   ...
   >>> people = [Person("b", 30), Person("a", 25)]
   >>> sorted(people, key=attrgetter("age"))[0].name
   'a'

operator.add / operator.mul などの演算子関数
------------------------------------------------

``+`` や ``*`` といった演算子を、関数として呼び出せる形にしたもの。``functools.reduce`` のように関数を引数として渡す必要がある場面で ``lambda`` の代わりに使える。

.. code-block:: python

   >>> from operator import add, mul
   >>> add(2, 3)
   5
   >>> mul(2, 3)
   6

functools.reduce との組み合わせ
------------------------------------

演算子関数は :doc:`functools` の ``functools.reduce`` と組み合わせる
ことで、累積計算を簡潔に書ける。

.. code-block:: python

   >>> from functools import reduce
   >>> from operator import add, mul
   >>> reduce(add, [1, 2, 3, 4])
   10
   >>> reduce(mul, [1, 2, 3, 4])
   24
