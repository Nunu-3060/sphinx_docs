functools
=========

高階関数（関数を引数に取ったり返したりする関数）や、関数・呼び出し可能
オブジェクトに対する操作をまとめたモジュール。

functools.reduce
------------------

イテラブルの要素を左から順に累積的に関数へ適用し、単一の値にまとめる。

.. code-block:: python

   >>> from functools import reduce
   >>> reduce(lambda acc, x: acc + x, [1, 2, 3, 4])
   10
   >>> reduce(lambda acc, x: acc * x, [1, 2, 3, 4], 1)
   24

functools.partial
--------------------

既存の関数の一部の引数をあらかじめ固定した、新しい呼び出し可能
オブジェクトを生成する。コールバック関数に引数を渡したい場合などに便利。

.. code-block:: python

   >>> from functools import partial
   >>> def power(base, exponent):
   ...     return base ** exponent
   ...
   >>> square = partial(power, exponent=2)
   >>> square(5)
   25

functools.lru_cache / functools.cache
----------------------------------------

関数の呼び出し結果をキャッシュし、同じ引数での再計算を避けるデコレータ。``lru_cache`` は保持件数の上限を指定でき、``cache`` は上限なしでキャッシュする ``lru_cache(maxsize=None)`` の簡易版。

.. code-block:: python

   >>> from functools import lru_cache
   >>> @lru_cache(maxsize=None)
   ... def fib(n):
   ...     return n if n < 2 else fib(n - 1) + fib(n - 2)
   ...
   >>> fib(30)
   832040
   >>> fib.cache_info()
   CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)

functools.wraps
-----------------

デコレータを書く際に、ラップ対象の関数が持つ ``__name__`` や ``__doc__`` などのメタデータを、生成される wrapper 関数へコピーする。

.. code-block:: python

   >>> from functools import wraps
   >>> def logged(func):
   ...     @wraps(func)
   ...     def wrapper(*args, **kwargs):
   ...         print(f"call {func.__name__}")
   ...         return func(*args, **kwargs)
   ...     return wrapper
   ...
   >>> @logged
   ... def greet(name):
   ...     """挨拶を返す。"""
   ...     return f"Hello, {name}"
   ...
   >>> greet.__name__
   'greet'
   >>> greet.__doc__
   '挨拶を返す。'

functools.singledispatch
--------------------------

第一引数の型に応じて呼び出す実装を切り替える関数を作成するデコレータ。``if isinstance(...)`` を連ねる代わりに、型ごとの処理を ``register()`` で個別の関数として追加していける。

.. code-block:: python

   >>> from functools import singledispatch
   >>> @singledispatch
   ... def describe(obj):
   ...     return f"object: {obj!r}"
   ...
   >>> @describe.register
   ... def _(obj: int):
   ...     return f"int: {obj}"
   ...
   >>> @describe.register
   ... def _(obj: list):
   ...     return f"list of {len(obj)} items"
   ...
   >>> describe(42)
   'int: 42'
   >>> describe([1, 2, 3])
   'list of 3 items'
   >>> describe(3.14)
   'object: 3.14'

functools.cmp_to_key
----------------------

2 引数を取り、負・0・正の値を返す旧スタイルの比較関数を、``sorted`` や ``list.sort`` の ``key`` に渡せる形式に変換する。

.. code-block:: python

   >>> from functools import cmp_to_key
   >>> def compare(a, b):
   ...     return (a > b) - (a < b)
   ...
   >>> sorted([3, 1, 2], key=cmp_to_key(lambda a, b: compare(b, a)))
   [3, 2, 1]
