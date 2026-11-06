enum
====

名前の付いた定数の集合（列挙型）を定義するためのモジュール。文字列やマジックナンバーを直接使う代わりに列挙型を使うことで、意図が明確になり、誤った値の使用を型チェッカや実行時エラーで検出しやすくなる。

Enum の基本
-----------

``Enum`` を継承したクラスに、メンバーとその値を定義する。

.. code-block:: python
   :linenos:

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
   :linenos:

   from enum import Enum, auto

   class Status(Enum):
       PENDING = auto()
       RUNNING = auto()
       DONE = auto()

   >>> Status.RUNNING.value
   2

IntEnum
-------

``IntEnum`` はメンバーが ``int`` としても振る舞う列挙型。整数との比較や演算が必要な場面で使う。

.. code-block:: python
   :linenos:

   from enum import IntEnum

   class Priority(IntEnum):
       LOW = 1
       MEDIUM = 2
       HIGH = 3

   >>> Priority.HIGH == 3
   True
   >>> Priority.HIGH > Priority.LOW
   True
   >>> str(Priority.HIGH)
   '3'

.. note::

   Python 3.11 から、``IntEnum`` のメンバーの ``str()`` や ``format()``\ （f-string での埋め込みを含む）の結果は、``'Priority.HIGH'`` ではなく ``'3'`` のように値そのものを表す文字列になった。通常の ``Enum`` の ``str()`` は従来どおり ``'Color.RED'`` の形式である。

メンバーの比較
--------------

同じ列挙型のメンバー同士は ``==`` や ``is`` で比較できる。異なる列挙型や単純な値とは、``IntEnum`` などの特殊なケースを除き等しくならない。

.. code-block:: python
   :linenos:

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
   :linenos:

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

   誤って同じ値を持つメンバー（エイリアス）を定義してしまうミスを防ぎたい場合は、クラスに ``@unique`` デコレータを付けると、値が重複している場合にクラス定義の時点で ``ValueError`` が発生するようになる。

StrEnum
-------

Python 3.11 で追加された ``StrEnum`` は、メンバーが ``str`` としても振る舞う列挙型である。``IntEnum`` の文字列版にあたり、文字列との比較や、文字列を受け取る API への受け渡しをそのまま行える。``auto()`` を使うと、メンバー名を小文字にした文字列が値になる。

.. code-block:: python
   :linenos:

   from enum import StrEnum, auto

   class Method(StrEnum):
       GET = auto()
       POST = auto()

   >>> Method.GET
   <Method.GET: 'get'>
   >>> Method.GET == "get"
   True
   >>> f"method={Method.POST}"
   'method=post'

Enum の反復処理
----------------

列挙型クラス自体をイテレートすると、定義順にすべてのメンバーを取得できる。

.. code-block:: python
   :linenos:

   >>> for c in Color:
   ...     print(c.name, c.value)
   RED 1
   GREEN 2
   BLUE 3
