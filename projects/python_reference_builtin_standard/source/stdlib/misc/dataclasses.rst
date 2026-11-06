dataclasses
===========

データを保持することを主目的としたクラスを、少ないコード量で定義するためのモジュール。``@dataclass`` デコレータを付けるだけで、``__init__`` や ``__repr__`` などの定型的なメソッドが自動生成される。

@dataclass の基本
-----------------

クラス変数に型注釈を付けて属性を宣言すると、それらを受け取る ``__init__`` が自動生成される。

.. code-block:: python
   :linenos:

   from dataclasses import dataclass

   @dataclass
   class Point:
       x: int
       y: int

   >>> p = Point(1, 2)
   >>> p
   Point(x=1, y=2)
   >>> p.x
   1

自動生成される __repr__ / __eq__
-----------------------------------

通常のクラスでは自前で定義する必要がある ``__repr__``\ （デバッグ用の表示）や ``__eq__``\ （属性値による等価比較）が、デフォルトで生成される。

.. code-block:: python
   :linenos:

   @dataclass
   class Point:
       x: int
       y: int

   >>> Point(1, 2) == Point(1, 2)
   True
   >>> Point(1, 2) == Point(3, 4)
   False

field() と default_factory
-----------------------------

リストや辞書のようなミュータブルな値をデフォルト値にしたい場合、そのまま ``= []`` と書くとエラーになる。``field(default_factory=...)`` を使うことで、インスタンスごとに新しいオブジェクトを生成できる。

.. code-block:: python
   :linenos:

   from dataclasses import dataclass, field

   @dataclass
   class Cart:
       items: list[str] = field(default_factory=list)

   >>> c1 = Cart()
   >>> c1.items.append("apple")
   >>> c2 = Cart()
   >>> c2.items
   []

frozen=True によるイミュータブル化
-------------------------------------

``@dataclass(frozen=True)`` を指定すると、属性の再代入ができなくなり、イミュータブル（変更不可）なオブジェクトとして扱える。

.. code-block:: python
   :linenos:

   @dataclass(frozen=True)
   class Point:
       x: int
       y: int

   >>> p = Point(1, 2)
   >>> p.x = 10
   Traceback (most recent call last):
       ...
   dataclasses.FrozenInstanceError: cannot assign to field 'x'

order=True による比較演算子の生成
-------------------------------------

``@dataclass(order=True)`` を指定すると、フィールドを先頭から順に比較する ``<``/``<=``/``>``/``>=`` が自動生成され、インスタンス同士を並べ替え（``sorted()`` など）に使えるようになる。

.. code-block:: python
   :linenos:

   @dataclass(order=True)
   class Point:
       x: int
       y: int

   >>> Point(1, 2) < Point(3, 4)
   True
   >>> sorted([Point(3, 0), Point(1, 0)])
   [Point(x=1, y=0), Point(x=3, y=0)]

asdict() / astuple() による変換
-----------------------------------

``dataclasses.asdict()``/``dataclasses.astuple()`` を使うと、インスタンスを（ネストした dataclass も再帰的に変換した）普通の ``dict``/``tuple`` に変換できる。JSON への変換など、dataclass 以外の形式で扱いたい場合に使う。

.. code-block:: python
   :linenos:

   from dataclasses import asdict, astuple

   @dataclass
   class Point:
       x: int
       y: int

   >>> p = Point(1, 2)
   >>> asdict(p)
   {'x': 1, 'y': 2}
   >>> astuple(p)
   (1, 2)

fields() によるフィールドの取得
-----------------------------------

``dataclasses.fields()`` に dataclass のインスタンスまたはクラスを渡すと、各フィールドの名前や型などの定義情報を ``Field`` オブジェクトとして取得できる。フィールド定義を動的に調べたいツールなどで使われる。

.. code-block:: python
   :linenos:

   from dataclasses import fields

   >>> for f in fields(Point):
   ...     print(f.name, f.type.__name__)
   x int
   y int

__post_init__ による後処理
-------------------------------

``__init__`` が自動生成されるため、初期化直後にバリデーションや派生値の計算を行いたい場合は、``__post_init__`` メソッドを定義する。自動生成された ``__init__`` は、すべての属性を設定した最後にこのメソッドを呼び出す。

.. code-block:: python
   :linenos:

   from dataclasses import field

   @dataclass
   class Circle:
       radius: float
       area: float = field(init=False)

       def __post_init__(self):
           self.area = 3.14159 * self.radius ** 2

   >>> c = Circle(2.0)
   >>> c.area
   12.56636

slots=True / kw_only=True
----------------------------

``@dataclass(slots=True)`` を指定すると、``__slots__`` を持つクラスが生成される。インスタンスごとの ``__dict__`` が作られないためメモリ使用量が減り、属性アクセスもわずかに速くなるほか、定義されていない属性への代入（タイプミスなど）が ``AttributeError`` になる。

``@dataclass(kw_only=True)`` を指定すると、すべてのフィールドがキーワード専用引数になり、``User(name="Alice")`` のように名前を指定して渡す必要がある。フィールドが多いクラスで引数の順序の取り違えを防げるほか、デフォルト値を持つフィールドの後にデフォルト値のないフィールドを定義できないという制約も気にしなくてよくなる。一部のフィールドだけをキーワード専用にしたい場合は、``field(kw_only=True)`` や、区切りとなる疑似フィールド ``_: KW_ONLY`` を使う。

.. code-block:: python
   :linenos:

   @dataclass(slots=True, kw_only=True)
   class User:
       name: str
       age: int = 0

   >>> u = User(name="Alice", age=30)
   >>> u
   User(name='Alice', age=30)
   >>> User("Alice")
   Traceback (most recent call last):
       ...
   TypeError: User.__init__() takes 1 positional argument but 2 were given
   >>> u.email = "alice@example.com"
   Traceback (most recent call last):
       ...
   AttributeError: 'User' object has no attribute 'email' and no __dict__ for setting new attributes

.. note::

   一部のフィールドだけを変更した新しいインスタンスを作りたい場合は、``dataclasses.replace(インスタンス, フィールド名=新しい値)`` を使う（Python 3.13 以降は :doc:`copy` の ``copy.replace()`` も使える）。``frozen=True`` のインスタンスでも使えるため、イミュータブルなオブジェクトを「更新」する際の定番の方法である。

.. note::

   フィールドに型注釈が必須である点に注意する。型注釈のない変数はクラス属性としては扱われても、``dataclass`` が生成するフィールドの対象にはならない。
