collections.abc
================

コンテナ型（``list``、``dict``、``set`` など）が備えるべき振る舞いを、
抽象基底クラス（ABC: Abstract Base Class）として定義したモジュール。
「イテレートできる」「要素数を持つ」「キーで値を取り出せる」といった
性質を、具体的な型を問わずに ``isinstance()`` で判定したり、関数の
引数や戻り値の型ヒントとして表現したりするのに使う。

ABC とは何のためにあるのか
--------------------------

Python では「``list`` かどうか」より「イテレート可能かどうか」のように、振る舞い（プロトコル）に着目したダックタイピングが好まれる。``collections.abc`` の ABC は、``__iter__`` や ``__len__`` のような特殊メソッドを実装しているオブジェクトを、継承関係なしに「その性質を持つ」と認識できるようにする。

.. code-block:: python

   >>> from collections.abc import Iterable
   >>> isinstance([1, 2, 3], Iterable)
   True
   >>> isinstance("abc", Iterable)
   True
   >>> isinstance(42, Iterable)
   False

Iterable と Iterator
---------------------

``Iterable`` は ``__iter__`` を持つ（for 文で反復できる）オブジェクトを、``Iterator`` はさらに ``__next__`` を持つ（``next()`` で1つずつ値を取り出せる）オブジェクトを表す。自作クラスがこれらの性質を満たすかを継承関係に依らず判定できる。

.. code-block:: python

   >>> from collections.abc import Iterable, Iterator
   >>>
   >>> class Countdown:
   ...     def __init__(self, start):
   ...         self.start = start
   ...     def __iter__(self):
   ...         return self
   ...     def __next__(self):
   ...         if self.start <= 0:
   ...             raise StopIteration
   ...         self.start -= 1
   ...         return self.start + 1
   ...
   >>> c = Countdown(3)
   >>> isinstance(c, Iterable)
   True
   >>> isinstance(c, Iterator)
   True
   >>> list(c)
   [3, 2, 1]

Sequence と Mapping
--------------------

``Sequence`` はインデックスアクセス（``__getitem__``）と順序を持つコンテナ（``list``、``tuple``、``str`` など）を、``Mapping`` はキーで値を取り出せるコンテナ（``dict`` など）を表す。``isinstance()`` による判定に使えるほか、``Sequence[int]`` のように要素の型を指定したジェネリック型ヒントとしても使える。

.. code-block:: python

   >>> from collections.abc import Sequence, Mapping
   >>> isinstance([1, 2, 3], Sequence)
   True
   >>> isinstance({"a": 1}, Mapping)
   True
   >>> isinstance({"a": 1}, Sequence)
   False

   >>> def first_item(items: Sequence[int]) -> int:
   ...     return items[0]
   ...
   >>> def get_value(data: Mapping[str, int], key: str) -> int:
   ...     return data[key]
   ...
   >>> first_item([10, 20, 30])
   10
   >>> get_value({"x": 1, "y": 2}, "y")
   2

Callable による型ヒント
------------------------

``Callable`` は、関数やメソッドのような呼び出し可能オブジェクトを表す。``Callable[[引数の型...], 戻り値の型]`` の形式でパラメータ化できる。これは、組み込み型や ABC を添字表記でパラメータ化できるようにしたPEP 585 により、かつて ``typing.Callable`` が担っていた役割を置き換えるもので、新しいコードでは ``typing.Callable`` の代わりにこちらを使うのが推奨される（詳細は :doc:`../misc/typing` を参照）。

.. code-block:: python

   >>> from collections.abc import Callable
   >>>
   >>> def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
   ...     return func(a, b)
   ...
   >>> apply(lambda x, y: x + y, 3, 4)
   7

自作クラスを ABC に適合させる
------------------------------

``__iter__`` や ``__len__`` などの必要なメソッドを実装していれば、
そのクラスは明示的に継承しなくても対応する ABC の「サブクラス」として
認識される（これを構造的サブクラス化と呼ぶ）。また、継承関係を持たない
まま、明示的にサブクラスとして登録する ``register()`` という方法も
用意されている。

.. code-block:: python

   >>> from collections.abc import Sized
   >>>
   >>> class Basket:
   ...     def __init__(self, items):
   ...         self._items = items
   ...     def __len__(self):
   ...         return len(self._items)
   ...
   >>> isinstance(Basket([1, 2, 3]), Sized)
   True

MutableMapping を継承した独自クラスの作成
--------------------------------------------

前節の構造的サブクラス化は ``isinstance()`` による判定を可能にするだけで、``update()`` や ``get()`` のような便利メソッドを自動的に使えるようにはしない。これらを利用したい場合は、実際に ABC を継承する必要がある。``collections.abc`` の最も実用的な使い方は、ABC を継承して独自のコンテナクラスを作ることである。``MutableMapping`` を継承する場合、``__getitem__``、``__setitem__``、``__delitem__``、``__iter__``、``__len__`` の 5 つの抽象メソッドだけを実装すれば、``update()``、``get()``、``pop()``、``keys()``、``items()`` などの残りのメソッドは ABC 側の実装から「無料で」手に入る。

.. code-block:: python

   >>> from collections.abc import MutableMapping
   >>>
   >>> class CaseInsensitiveDict(MutableMapping):
   ...     def __init__(self):
   ...         self._data = {}
   ...     def __getitem__(self, key):
   ...         return self._data[key.lower()]
   ...     def __setitem__(self, key, value):
   ...         self._data[key.lower()] = value
   ...     def __delitem__(self, key):
   ...         del self._data[key.lower()]
   ...     def __iter__(self):
   ...         return iter(self._data)
   ...     def __len__(self):
   ...         return len(self._data)
   ...
   >>> d = CaseInsensitiveDict()
   >>> d["Content-Type"] = "text/html"
   >>> d["content-type"]
   'text/html'
   >>> d.update({"Accept": "*/*"})
   >>> d.get("accept")
   '*/*'
   >>> list(d.keys())
   ['content-type', 'accept']

.. note::

   ``collections.abc`` の ABC は、``isinstance()`` / ``issubclass()`` によるダックタイピングの判定と、``list[int]`` などの組み込みジェネリック型と同様の型ヒントの記述という、2 つの役割を兼ねている。型ヒントとしてコンテナ系の抽象型（``Iterable``、``Sequence``、``Mapping``、``Callable`` など）を書く場合は、``typing`` モジュールの対応する型ではなく、こちらを使うのが現在の標準的なスタイルである。
