クラス設計支援
==============

クラス定義時に使用する組み込み関数群。

super
-----

親クラス（スーパークラス）のメソッド呼び出しを委譲するためのプロキシオブジェクトを返す。

.. code-block:: python

   class Base:
       def greet(self):
           return "Hello"

   class Derived(Base):
       def greet(self):
           return super().greet() + ", World"

property
--------

メソッドを属性のようにアクセスできるようにする（ゲッター・セッターの定義）。

.. code-block:: python

   class Circle:
       def __init__(self, radius):
           self._radius = radius

       @property
       def area(self):
           return 3.14 * self._radius ** 2

   >>> Circle(2).area
   12.56

staticmethod
------------

インスタンスやクラスに依存しない、クラスの名前空間に属するメソッドを定義する。

.. code-block:: python

   class Math:
       @staticmethod
       def add(a, b):
           return a + b

   >>> Math.add(1, 2)
   3

classmethod
-----------

第一引数にクラス自身を受け取るメソッドを定義する。代替コンストラクタなどでよく使われる。

.. code-block:: python

   class Point:
       def __init__(self, x, y):
           self.x, self.y = x, y

       @classmethod
       def origin(cls):
           return cls(0, 0)

   >>> p = Point.origin()
   >>> p.x, p.y
   (0, 0)
