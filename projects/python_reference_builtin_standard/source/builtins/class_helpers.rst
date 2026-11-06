クラス設計支援
==============

クラス定義時に使用する組み込み関数群。

super
-----

親クラス（スーパークラス）のメソッドを呼び出すためのプロキシオブジェクトを返す。正確には、メソッド解決順序（MRO）上で次に位置するクラスへ属性の探索を委譲する。

.. code-block:: python
   :linenos:

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
   :linenos:

   class Circle:
       def __init__(self, radius):
           self._radius = radius

       @property
       def radius(self):
           return self._radius

       @radius.setter
       def radius(self, value):
           if value < 0:
               raise ValueError("radius must be non-negative")
           self._radius = value

       @property
       def area(self):
           return 3.14 * self._radius ** 2

   >>> c = Circle(2)
   >>> c.area
   12.56
   >>> c.radius = 3
   >>> c.radius
   3

staticmethod
------------

インスタンスやクラスに依存しない、クラスの名前空間に属するメソッドを定義する。

.. code-block:: python
   :linenos:

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
   :linenos:

   class Point:
       def __init__(self, x, y):
           self.x, self.y = x, y

       @classmethod
       def origin(cls):
           return cls(0, 0)

   >>> p = Point.origin()
   >>> p.x, p.y
   (0, 0)
