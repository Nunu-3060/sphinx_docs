型変換・生成
============

他の型のオブジェクトから、目的の型のオブジェクトを生成する関数群。

int
---

整数、または整数に変換可能な文字列・数値から ``int`` オブジェクトを生成する。

.. code-block:: python

   >>> int("42")
   42
   >>> int(3.9)
   3
   >>> int("ff", 16)
   255

float
-----

浮動小数点数、または変換可能な文字列・数値から ``float`` オブジェクトを生成する。

.. code-block:: python

   >>> float("3.14")
   3.14
   >>> float(10)
   10.0

complex
-------

実部と虚部から、または変換可能な文字列から ``complex`` オブジェクト（複素数）を生成する。

.. code-block:: python

   >>> complex(1, 2)
   (1+2j)
   >>> complex("1+2j")
   (1+2j)

chr
---

Unicode コードポイント（整数）から、対応する1文字の文字列を生成する。

.. code-block:: python

   >>> chr(65)
   'A'
   >>> chr(0x3042)
   'あ'

ord
---

1文字の文字列から、対応する Unicode コードポイント（整数）を返す。``chr`` の逆演算にあたる。

.. code-block:: python

   >>> ord('A')
   65
   >>> ord('あ')
   12354

str
---

オブジェクトの人間可読な文字列表現を返す。引数を省略すると空文字列 ``''`` を返す。``repr`` との違いなど、文字列表現の詳細は :doc:`string_repr` を参照。

.. code-block:: python

   >>> str(123)
   '123'
   >>> str([1, 2, 3])
   '[1, 2, 3]'

bool
----

オブジェクトの真偽値（``True`` / ``False``）を返す。

.. code-block:: python

   >>> bool(0)
   False
   >>> bool("")
   False
   >>> bool([1])
   True

list
----

イテラブルの要素から新しい ``list`` オブジェクトを生成する。

.. code-block:: python

   >>> list("abc")
   ['a', 'b', 'c']
   >>> list(range(3))
   [0, 1, 2]

tuple
-----

イテラブルの要素から新しい ``tuple`` オブジェクトを生成する。

.. code-block:: python

   >>> tuple([1, 2, 3])
   (1, 2, 3)

dict
----

キーと値のペアから新しい ``dict`` オブジェクトを生成する。

.. code-block:: python

   >>> dict(a=1, b=2)
   {'a': 1, 'b': 2}
   >>> dict([("x", 1), ("y", 2)])
   {'x': 1, 'y': 2}

set
---

イテラブルの要素から重複のない ``set`` オブジェクトを生成する。

.. code-block:: python

   >>> set([1, 2, 2, 3])
   {1, 2, 3}

frozenset
---------

``set`` をイミュータブル（変更不可）にしたもの。ハッシュ可能なので辞書のキーや集合の要素として使用できる（ハッシュ可能性については :doc:`introspection` の ``hash()`` の項を参照）。

.. code-block:: python

   >>> frozenset([1, 2, 2, 3])
   frozenset({1, 2, 3})

bytes
-----

イミュータブルなバイト列を生成する。

.. code-block:: python

   >>> bytes("abc", encoding="utf-8")
   b'abc'
   >>> bytes([65, 66, 67])
   b'ABC'

bytearray
---------

ミュータブル（変更可能）なバイト列を生成する。

.. code-block:: python

   >>> ba = bytearray("abc", encoding="utf-8")
   >>> ba[0] = 65
   >>> ba
   bytearray(b'Abc')
