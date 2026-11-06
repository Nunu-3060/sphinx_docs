typing
======

型ヒント（type hint）を記述するための機能を提供するモジュール。Python は動的型付け言語であり、型ヒントを書いても実行時に強制されるわけではないが、エディタの補完や静的型チェッカ（mypy など）による誤り検出、コードの可読性向上に役立つ。

基本的な型ヒント
----------------

変数や引数、戻り値には、対応する型をそのまま注釈として書ける。

.. code-block:: python
   :linenos:

   def greet(name: str) -> str:
       return f"Hello, {name}"

   age: int = 25
   price: float = 19.8

組み込みジェネリック型（list[int] など）
-----------------------------------------

Python 3.8 以前は ``typing.List`` や ``typing.Dict`` を使う必要があったが、Python 3.9 以降は組み込みの ``list`` や ``dict`` に直接要素の型を指定できる（PEP 585）。``typing.List`` などは互換性のために残されている非推奨の別名にすぎないため、新しいコードでは組み込み型を使う。

.. code-block:: python
   :linenos:

   def total(values: list[int]) -> int:
       return sum(values)

   def counts(data: dict[str, int]) -> None:
       for key, value in data.items():
           print(key, value)

   >>> total([1, 2, 3])
   6

X | Y による Union 型（Optional / Union）
--------------------------------------------

``X | Y`` は「``X`` または ``Y``」を表し、``X | None`` は「``X`` または ``None``」を表す（Python 3.10 で導入された記法、PEP 604）。

.. code-block:: python
   :linenos:

   def find_user(user_id: int) -> str | None:
       """見つからなければ None を返す"""
       return None

   def parse(value: int | str) -> int:
       return int(value)

古いコードでは、同じ意味を ``typing.Optional[X]`` や ``typing.Union[X, Y]`` を使って書いていることが多い。意味は同じだが、新しいコードでは ``|`` を使う記法が推奨される。

.. code-block:: python
   :linenos:

   from typing import Optional, Union

   # 従来の書き方（上の例と同じ意味）
   def find_user(user_id: int) -> Optional[str]:
       return None

   def parse(value: Union[int, str]) -> int:
       return int(value)

Callable
--------

関数やメソッドなど、呼び出し可能なオブジェクトの型を表す。``Callable[[引数の型...], 戻り値の型]`` の形式で書く。

``typing.Callable`` ではなく ``collections.abc.Callable`` を使うのが推奨される（``list[int]`` などの組み込みジェネリック型と同様、PEP 585 により標準ライブラリの ABC も直接パラメータ化できるようになったため）。この使い分けについては :doc:`../data_structures/collections_abc` も参照。

.. code-block:: python
   :linenos:

   from collections.abc import Callable

   def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
       return func(a, b)

   >>> apply(lambda x, y: x + y, 3, 4)
   7

型パラメータによるジェネリック関数
------------------------------------

関数名の後ろに ``[T]`` のように型パラメータを書くと、引数と戻り値の型が「同じ型である」ことを表現できるジェネリックな関数を定義できる（Python 3.12 で導入された構文、PEP 695）。

.. code-block:: python
   :linenos:

   def first[T](items: list[T]) -> T:
       return items[0]

   >>> first([1, 2, 3])
   1
   >>> first(["a", "b"])
   'a'

``[T: str]`` のように書くと上限（``str`` またはそのサブクラス）を、``[T: (int, float)]`` のように書くと取り得る型の候補を制約として指定できる。

Python 3.11 をサポートする必要があるコードでは、この構文は使えない。その場合は従来どおり ``TypeVar`` で型変数を定義しておく。

.. code-block:: python
   :linenos:

   from typing import TypeVar

   T = TypeVar("T")

   def first(items: list[T]) -> T:
       return items[0]

ジェネリッククラス
------------------

型パラメータの構文はクラスにも使える。クラス名の後ろに ``[T]`` を書くと、インスタンスごとに扱う要素の型を指定できるジェネリックなクラスを定義できる。

.. code-block:: python
   :linenos:

   class Box[T]:
       def __init__(self, item: T) -> None:
           self.item = item

       def get(self) -> T:
           return self.item

   >>> box = Box(42)
   >>> box.get()
   42
   >>> str_box: Box[str] = Box("hello")
   >>> str_box.get()
   'hello'

Python 3.11 以前の書き方では、``TypeVar`` で定義した型変数を使い、``Generic[T]`` を継承する。

.. code-block:: python
   :linenos:

   from typing import Generic, TypeVar

   T = TypeVar("T")

   class Box(Generic[T]):
       ...

type 文による型エイリアス
--------------------------

複雑な型に名前を付けて再利用したい場合は、Python 3.12 で導入された ``type`` 文で型エイリアスを定義する。型パラメータを持つエイリアスも定義でき、右辺は実際に使われるまで評価されないため、まだ定義されていない型を参照することもできる。

.. code-block:: python
   :linenos:

   type Point = tuple[float, float]
   type Pair[T] = tuple[T, T]

   def distance(p: Point, q: Point) -> float:
       return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5

Python 3.11 では、``Point = tuple[float, float]`` のような単純な代入や、``typing.TypeAlias`` を使った ``Point: TypeAlias = tuple[float, float]`` という書き方で型エイリアスを定義する。

Any
---

``Any`` は「どんな型でもよい」ことを表す型で、その値に対する型チェックを静的型チェッカが事実上行わなくなる。段階的に型注釈を導入する際の逃げ道として使えるが、多用すると型ヒントによる誤り検出の恩恵が失われるため注意する。

.. code-block:: python
   :linenos:

   from typing import Any

   def process(data: Any) -> None:
       print(data)  # data がどんな型でも静的型チェッカはエラーを出さない

   >>> process(123)
   123
   >>> process("text")
   text

Protocol による構造的サブタイピング
---------------------------------------

``Protocol`` を継承したクラスは、特定のメソッドや属性を持っているかどうか（構造）だけで型の適合を判定する「構造的サブタイピング」を表現できる。明示的な継承関係がなくても、必要なメソッドを実装していればその ``Protocol`` を満たしているとみなされる。

.. code-block:: python
   :linenos:

   from typing import Protocol

   class Greeter(Protocol):
       def greet(self) -> str:
           ...

   class Cat:  # Greeter を継承していないが、greet() を実装している
       def greet(self) -> str:
           return "にゃー"

   def say_hello(g: Greeter) -> None:
       print(g.greet())

   >>> say_hello(Cat())
   にゃー

TypedDict による辞書のスキーマ定義
---------------------------------------

``TypedDict`` を使うと、キーとその値の型が決まった辞書の「形」を型として表現できる。実行時には通常の ``dict`` と変わらないが、静的型チェッカがキーの誤字や値の型の不一致を検出できるようになる。

.. code-block:: python
   :linenos:

   from typing import TypedDict

   class Movie(TypedDict):
       title: str
       year: int

   >>> movie: Movie = {"title": "Blade Runner", "year": 1982}
   >>> movie["title"]
   'Blade Runner'

cast() による型情報の指定
------------------------------

``cast(型, 値)`` は実行時には何もせず値をそのまま返すが、静的型チェッカに対して「この値をこの型として扱ってよい」と伝える。型チェッカが式の型を正しく推論できない場合に、注釈を補うための手段として使う。

.. code-block:: python
   :linenos:

   from typing import cast

   def get_config() -> dict[str, object]:
       return {"timeout": 30}

   timeout = cast(int, get_config()["timeout"])

   >>> timeout
   30

Python 3.11 以降に追加された主な機能
--------------------------------------

Python 3.11 以降も、``typing`` には型をより正確に表現するための機能が追加され続けている。主なものを以下にまとめる。

.. list-table::
   :header-rows: 1

   * - 機能
     - 追加されたバージョン
     - 概要
   * - ``Self``
     - 3.11
     - メソッドの戻り値などで「そのクラス自身（サブクラスから呼ばれた場合はそのサブクラス）」を表す
   * - ``Never`` / ``assert_never()``
     - 3.11
     - 値が存在し得ない型を表す。``match`` 文や ``if`` 文ですべてのケースを網羅したかを型チェッカに検査させる際に使う
   * - ``LiteralString``
     - 3.11
     - ソースコード中のリテラルだけから作られた文字列を表す。SQL インジェクション対策などに使う
   * - ``Required`` / ``NotRequired``
     - 3.11
     - ``TypedDict`` の個々のキーを必須または省略可能として指定する
   * - ``@override``
     - 3.12
     - メソッドが親クラスのメソッドをオーバーライドしていることを明示する。親クラス側に同名のメソッドがない場合に型チェッカが警告する
   * - ``TypeIs``
     - 3.13
     - ``isinstance()`` のように引数の型を絞り込む関数の戻り値に使う
   * - ``ReadOnly``
     - 3.13
     - ``TypedDict`` のキーを読み取り専用として指定する

以下は ``Self`` と ``@override`` の使用例である。

.. code-block:: python
   :linenos:

   from typing import Self, override

   class Shape:
       def scale(self, factor: float) -> Self:
           return self

       def area(self) -> float:
           return 0.0

   class Square(Shape):
       def __init__(self, size: float) -> None:
           self.size = size

       @override
       def scale(self, factor: float) -> Self:
           self.size *= factor
           return self

       @override
       def area(self) -> float:
           return self.size ** 2

アノテーションの評価タイミング（Python 3.14）
------------------------------------------------

Python 3.14 では、関数やクラスのアノテーションは定義時には評価されず、``__annotations__`` などで実際に参照されたときに初めて評価されるようになった（PEP 649 / PEP 749）。そのため、後で定義されるクラスを参照する場合でも、``"Node"`` のように文字列で囲んだり、``from __future__ import annotations`` を書いたりする必要がなくなった。

.. code-block:: python
   :linenos:

   class Node:
       def __init__(self, next: Node | None = None) -> None:  # 3.14 ではそのまま書ける
           self.next = next

実行時にアノテーションを調べるツールを作る場合は、新しく追加された ``annotationlib`` モジュールの ``get_annotations()`` を使うと、未定義の名前を含むアノテーションも ``ForwardRef`` として安全に取得できる。なお Python 3.13 以前を対象とするコードでは、従来どおり文字列や ``from __future__ import annotations`` を使う。

.. note::

   型ヒントはあくまでヒントであり、誤った型を渡しても実行時にエラーにはならない点に注意する。

   ``typing`` と ``collections.abc`` のどちらを使うべきか迷った場合の目安は次の通りである。``list``/``dict``/``tuple``/``set`` のようなコンテナ型や ``Iterable``/``Sequence``/``Mapping``/``Callable`` のような抽象基底クラスには組み込み型や ``collections.abc`` を使う。``Union``/``Optional`` の代わりには ``X | Y`` を使う。一方、``TypeVar``\ （3.12 以降は型パラメータ構文で代替可能）・``Protocol``・``Any``・``TypedDict``・``Self``・``cast`` のように組み込み型や ``collections.abc`` に存在しない型ヒント専用の機能には、引き続き ``typing`` を使う。
