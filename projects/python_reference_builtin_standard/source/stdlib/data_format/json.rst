json
====

Python のオブジェクトと JSON（JavaScript Object Notation）形式の文字列との間で
相互変換を行うモジュール。設定ファイルや Web API のレスポンスなど、
データ交換フォーマットとして広く使われている。

json.dumps / json.loads
-------------------------

``dumps`` は Python オブジェクトを JSON 文字列に変換し、``loads`` は JSON 文字列を Python オブジェクトに変換する。

.. code-block:: python

   >>> import json
   >>> data = {"name": "Alice", "age": 30, "tags": ["admin", "user"]}
   >>> s = json.dumps(data)
   >>> s
   '{"name": "Alice", "age": 30, "tags": ["admin", "user"]}'
   >>> json.loads(s)
   {'name': 'Alice', 'age': 30, 'tags': ['admin', 'user']}

json.dump / json.load
-----------------------

ファイルオブジェクトに対して直接 JSON の書き込み・読み込みを行う。
文字列を経由しない分、大きなデータを扱う際に便利。

.. code-block:: python

   >>> with open("data.json", "w", encoding="utf-8") as f:
   ...     json.dump(data, f)
   ...
   >>> with open("data.json", encoding="utf-8") as f:
   ...     loaded = json.load(f)
   ...
   >>> loaded
   {'name': 'Alice', 'age': 30, 'tags': ['admin', 'user']}

ensure_ascii と indent
------------------------

``ensure_ascii=False`` を指定すると非 ASCII 文字（日本語など）を
エスケープせずそのまま出力できる。``indent`` を指定すると人間が読みやすい
整形済みの出力になる。

.. code-block:: python

   >>> print(json.dumps({"名前": "太郎"}))
   {"\u540d\u524d": "\u592a\u90ce"}
   >>> print(json.dumps({"名前": "太郎"}, ensure_ascii=False))
   {"名前": "太郎"}
   >>> print(json.dumps({"a": 1, "b": [1, 2]}, indent=2))
   {
     "a": 1,
     "b": [
       1,
       2
     ]
   }

default によるカスタムエンコード
----------------------------------

``datetime`` オブジェクトなど、標準では JSON にシリアライズできない型は
そのまま ``dumps`` に渡すと ``TypeError`` になる。``default`` 引数に
変換用の関数を渡すことで対応できる。

.. code-block:: python

   >>> from datetime import datetime
   >>> def default(o):
   ...     if isinstance(o, datetime):
   ...         return o.isoformat()
   ...     raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")
   ...
   >>> json.dumps({"created_at": datetime(2024, 1, 1)}, default=default)
   '{"created_at": "2024-01-01T00:00:00"}'

.. note::

   ``default`` を指定しないまま非対応の型を渡すと ``TypeError: Object of type ... is not JSON serializable`` が送出される。

object_hook によるカスタムデコード
--------------------------------------

``default`` がエンコード時にカスタム型を JSON に変換するのに対し、デコード時に JSON オブジェクト（辞書）から独自クラスのインスタンスを復元したい場合は ``loads``/``load`` の ``object_hook`` 引数を使う。``object_hook`` にはデコードされた辞書を受け取り、任意の値（そのままの辞書でも、独自オブジェクトでもよい）を返す関数を渡す。

.. code-block:: python

   >>> class Point:
   ...     def __init__(self, x, y):
   ...         self.x = x
   ...         self.y = y
   ...     def __repr__(self):
   ...         return f"Point({self.x}, {self.y})"
   ...
   >>> def as_point(d):
   ...     if "x" in d and "y" in d:
   ...         return Point(d["x"], d["y"])
   ...     return d
   ...
   >>> json.loads('{"x": 1, "y": 2}', object_hook=as_point)
   Point(1, 2)

.. note::

   不正な形式の JSON 文字列を ``loads``/``load`` に渡すと ``json.JSONDecodeError`` が送出される。外部から受け取った文字列をデコードする場合は、``try`` / ``except json.JSONDecodeError`` で囲んでおくと安全。
