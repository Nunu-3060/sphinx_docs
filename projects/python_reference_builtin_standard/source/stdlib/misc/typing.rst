typing
======

型ヒント（type hint）を記述するための機能を提供するモジュール。Python は動的型付け言語であり、型ヒントを書いても実行時に強制されるわけではないが、エディタの補完や静的型チェッカ（mypy など）による誤り検出、コードの可読性向上に役立つ。

基本的な型ヒント
----------------

変数や引数、戻り値には、対応する型をそのまま注釈として書ける。

.. code-block:: python

   def greet(name: str) -> str:
       return f"Hello, {name}"

   age: int = 25
   price: float = 19.8

組み込みジェネリック型（list[int] など）
-----------------------------------------

従来は ``typing.List`` や ``typing.Dict`` を使う必要があったが、現在は組み込みの ``list`` や ``dict`` に直接要素の型を指定できる。新しいコードではこちらが推奨される。

.. code-block:: python

   def total(values: list[int]) -> int:
       return sum(values)

   def counts(data: dict[str, int]) -> None:
       for key, value in data.items():
           print(key, value)

   >>> total([1, 2, 3])
   6

Optional と Union
-----------------

``Optional[X]`` は ``X`` または ``None`` を、``Union[X, Y]`` は ``X`` または ``Y`` を表す。``X | Y`` という記法でも同じ意味を表せ、新しいコードではこちらが好まれることが多い。

.. code-block:: python

   from typing import Optional, Union

   def find_user(user_id: int) -> Optional[str]:
       """見つからなければ None を返す"""
       return None

   def parse(value: Union[int, str]) -> int:
       return int(value)

   # | 演算子を使うと次のようにも書ける
   def find_user2(user_id: int) -> str | None:
       return None

Callable
--------

関数やメソッドなど、呼び出し可能なオブジェクトの型を表す。``Callable[[引数の型...], 戻り値の型]`` の形式で書く。

``typing.Callable`` ではなく ``collections.abc.Callable`` を使うのが推奨される（``list[int]`` などの組み込みジェネリック型と同様、PEP 585 により標準ライブラリの ABC も直接パラメータ化できるようになったため）。
この使い分けについては :doc:`../data_structures/collections_abc` も参照。

.. code-block:: python

   from collections.abc import Callable

   def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
       return func(a, b)

   >>> apply(lambda x, y: x + y, 3, 4)
   7

TypeVar によるジェネリック関数
--------------------------------

``TypeVar`` を使うと、引数と戻り値の型が「同じ型である」ことを表現できる
ジェネリックな関数を定義できる。

.. code-block:: python

   from typing import TypeVar

   T = TypeVar("T")

   def first(items: list[T]) -> T:
       return items[0]

   >>> first([1, 2, 3])
   1
   >>> first(["a", "b"])
   'a'

Generic によるジェネリッククラス
------------------------------------

``TypeVar`` は関数だけでなくクラスにも使える。``Generic[T]`` を継承すると、
インスタンスごとに扱う要素の型を指定できるジェネリックなクラスを定義できる。

.. code-block:: python

   from typing import Generic, TypeVar

   T = TypeVar("T")

   class Box(Generic[T]):
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

Any
---

``Any`` は「どんな型でもよい」ことを表す型で、その値に対する型チェックを
静的型チェッカが事実上行わなくなる。段階的に型注釈を導入する際の
逃げ道として使えるが、多用すると型ヒントによる誤り検出の恩恵が
失われるため注意する。

.. code-block:: python

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

``TypedDict`` を使うと、キーとその値の型が決まった辞書の「形」を型として
表現できる。実行時には通常の ``dict`` と変わらないが、静的型チェッカが
キーの誤字や値の型の不一致を検出できるようになる。

.. code-block:: python

   from typing import TypedDict

   class Movie(TypedDict):
       title: str
       year: int

   >>> movie: Movie = {"title": "Blade Runner", "year": 1982}
   >>> movie["title"]
   'Blade Runner'

cast() による型情報の指定
------------------------------

``cast(型, 値)`` は実行時には何もせず値をそのまま返すが、静的型チェッカに
対して「この値をこの型として扱ってよい」と伝える。型チェッカが式の型を
正しく推論できない場合に、注釈を補うための手段として使う。

.. code-block:: python

   from typing import cast

   def get_config() -> dict:
       return {"timeout": 30}

   timeout = cast(int, get_config()["timeout"])

   >>> timeout
   30

.. note::

   型ヒントはあくまでヒントであり、誤った型を渡してもエラーにはならない
   点に注意する。

   この性質を踏まえると、``typing`` と ``collections.abc`` のどちらを使うべきか迷うこともあるだろう。現在の使い分けの目安は次の通りである。``list``/``dict``/``tuple``/``set`` のようなコンテナ型や ``Iterable``/``Sequence``/``Mapping``/``Callable`` のような抽象基底クラスには組み込み型や ``collections.abc`` を使う。一方、``Optional``/``Union``（または ``X | Y``）・``TypeVar``・``Generic``・ ``Protocol``・``Any``・``TypedDict``・``cast`` のように ``collections.abc`` に存在しない型ヒント専用の機能には、引き続き ``typing`` を使うとよい。
