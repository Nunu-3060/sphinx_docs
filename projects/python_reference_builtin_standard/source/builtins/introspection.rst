オブジェクト検査・リフレクション
================================

オブジェクトの型や属性を実行時に調べる・操作するための関数群。

type
----

オブジェクトの型を返す。

.. code-block:: python

   >>> type(42)
   <class 'int'>
   >>> type("abc")
   <class 'str'>

3引数版 ``type(name, bases, namespace)`` を使うと、``class`` 文を使わずに動的にクラスを生成できる。

.. code-block:: python

   >>> Point = type("Point", (), {"x": 0, "y": 0})
   >>> p = Point()
   >>> p.x
   0

isinstance
----------

オブジェクトが指定した型（またはそのサブクラス）のインスタンスかどうかを判定する。

.. code-block:: python

   >>> isinstance(42, int)
   True
   >>> isinstance(42, (int, float))
   True

issubclass
----------

クラスが指定したクラス（またはそのサブクラス）かどうかを判定する。

.. code-block:: python

   >>> issubclass(bool, int)
   True

id
--

オブジェクトの識別値（CPythonではメモリアドレス相当）を返す。

.. code-block:: python

   >>> a = [1, 2, 3]
   >>> b = a
   >>> c = [1, 2, 3]
   >>> id(a) == id(b)
   True
   >>> id(a) == id(c)
   False

``b`` は ``a`` と同じオブジェクトを指しているため識別値が一致するが、``c`` は値が等しくても別のオブジェクトなので識別値は異なる。

hasattr / getattr / setattr / delattr
--------------------------------------

オブジェクトの属性の有無を調べたり、取得・設定・削除したりする。

.. code-block:: python

   >>> class Point:
   ...     x = 1
   ...
   >>> p = Point()
   >>> hasattr(p, "x")
   True
   >>> getattr(p, "x")
   1
   >>> setattr(p, "y", 2)
   >>> p.y
   2
   >>> delattr(p, "y")

dir
---

オブジェクトが持つ属性・メソッドの名前一覧を返す。引数を省略すると現在のスコープの名前一覧を返す。また、:doc:`class_helpers` で説明する ``super`` や ``property`` などの機能を使って定義したクラスの属性も、``dir`` で確認できる。

.. code-block:: python

   >>> dir([])[:3]
   ['__add__', '__class__', '__contains__']

vars
----

オブジェクトの ``__dict__`` 属性を返す。引数を省略すると現在のローカル変数の辞書を返し、これは ``locals()`` と等価である（モジュールレベルの変数一覧を得るには ``globals()`` を使う）。

.. code-block:: python

   >>> class Point:
   ...     def __init__(self):
   ...         self.x = 1
   ...
   >>> vars(Point())
   {'x': 1}

hash
----

オブジェクトのハッシュ値（整数）を返す。ハッシュ可能なオブジェクトのみ辞書のキーや集合（``set`` / ``frozenset``）の要素にできる（:doc:`type_conversion` の ``frozenset`` の項も参照）。リストや辞書のようなミュータブルなオブジェクトはハッシュ可能ではない。

.. code-block:: python

   >>> hash(42)
   42
   >>> hash("abc")  # 実行毎にランダム化されるため値は環境によって異なる
   -4044789205657692274

callable
--------

オブジェクトが呼び出し可能（関数のように ``()`` で呼べる）かどうかを判定する。

.. code-block:: python

   >>> callable(len)
   True
   >>> callable(42)
   False
