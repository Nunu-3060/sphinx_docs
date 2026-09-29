enum
====

名前の付いた定数の集合（列挙型）を定義するためのモジュール。
文字列やマジックナンバーを直接使う代わりに列挙型を使うことで、
意図が明確になり、誤った値の使用を型チェッカや実行時エラーで
検出しやすくなる。

Enum の基本
-----------

``Enum`` を継承したクラスに、メンバーとその値を定義する。

.. code-block:: python

   from enum import Enum

   class Color(Enum):
       RED = 1
       GREEN = 2
       BLUE = 3

   >>> Color.RED
   <Color.RED: 1>
   >>> Color.RED.name
   'RED'
   >>> Color.RED.value
   1

auto() による自動採番
------------------------

値そのものに意味がなく、区別さえできればよい場合は ``auto()`` を使うと、1 から始まる連番などが自動的に割り当てられる。

.. code-block:: python

   from enum import Enum, auto

   class Status(Enum):
       PENDING = auto()
       RUNNING = auto()
       DONE = auto()

   >>> Status.RUNNING.value
   2

IntEnum
-------

``IntEnum`` はメンバーが ``int`` としても振る舞う列挙型。整数との比較や
演算が必要な場面で使う。

.. code-block:: python

   from enum import IntEnum

   class Priority(IntEnum):
       LOW = 1
       MEDIUM = 2
       HIGH = 3

   >>> Priority.HIGH == 3
   True
   >>> Priority.HIGH > Priority.LOW
   True

メンバーの比較
--------------

同じ列挙型のメンバー同士は ``==`` や ``is`` で比較できる。異なる列挙型や
単純な値とは、``IntEnum`` などの特殊なケースを除き等しくならない。

.. code-block:: python

   >>> Color.RED == Color.RED
   True
   >>> Color.RED is Color.RED
   True
   >>> Color.RED == 1
   False

Flag と IntFlag によるビットフラグ
--------------------------------------

``Flag``/``IntFlag`` は、``|`` 演算子でメンバーを組み合わせられる列挙型。権限フラグなど、複数の値を同時に持たせたい場合に使う。``IntFlag`` は ``IntEnum`` と同様に ``int`` としても振る舞う。

.. code-block:: python

   from enum import Flag, auto

   class Permission(Flag):
       READ = auto()
       WRITE = auto()
       EXECUTE = auto()

   >>> perm = Permission.READ | Permission.WRITE
   >>> perm
   <Permission.READ|WRITE: 3>
   >>> Permission.READ in perm
   True
   >>> Permission.EXECUTE in perm
   False

.. note::

   Python 3.11 以降では、値が文字列となる列挙型として ``StrEnum`` も
   利用できる（メンバーがそのまま ``str`` としても振る舞う）。また、
   誤って同じ値を持つメンバー（エイリアス）を定義してしまうミスを
   防ぎたい場合は、クラスに ``@unique`` デコレータを付けると、値が
   重複した時点で ``ValueError`` が発生するようになる。

Enum の反復処理
----------------

列挙型クラス自体をイテレートすると、定義順にすべてのメンバーを取得できる。

.. code-block:: python

   >>> for c in Color:
   ...     print(c.name, c.value)
   RED 1
   GREEN 2
   BLUE 3
