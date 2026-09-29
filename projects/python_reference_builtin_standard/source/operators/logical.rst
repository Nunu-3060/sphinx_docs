論理演算子
==========

真偽値（あるいは真偽値として評価できるオブジェクト）を組み合わせて論理演算を行うための演算子。``and`` ``or`` ``not`` の3つがある。

``and`` / ``or``
------------------

``and`` は両方の値が真であるときに真、``or`` はいずれかの値が真であるときに真となる。

.. code-block:: python

   >>> True and False
   False
   >>> True or False
   True
   >>> (1 < 2) and (2 < 3)
   True

.. note::

   ``and`` ``or`` は ``True`` / ``False`` を返すわけではなく、実際に評価したオペランドの値そのものを返す。また、左のオペランドで結果が確定する場合、右のオペランドは評価されない（短絡評価）。この性質はデフォルト値の指定などによく利用される。

   .. code-block:: python

      >>> 0 or "default"
      'default'
      >>> "" or "default"
      'default'
      >>> "value" or "default"
      'value'
      >>> [] and "not reached"
      []

``not``
--------

オペランドの真偽値を反転する単項演算子。

.. code-block:: python

   >>> not True
   False
   >>> not 0
   True
   >>> not [1, 2, 3]
   False

真偽値としての評価（truthiness）
--------------------------------

``and`` ``or`` ``not`` や ``if`` 文は、オペランドを ``bool()`` に渡した結果（真偽値）に基づいて動作する。``0`` や空のコレクションなど、以下のような値は偽（falsy）として扱われる。

- ``False``
- ``None``
- 数値の ``0`` （``0``、``0.0``、``0j`` など）
- 空の文字列 ``""``
- 空のリスト ``[]``、空のタプル ``()``
- 空の辞書 ``{}``、空の集合 ``set()``

これら以外のオブジェクトは真（truthy）として扱われる。

.. code-block:: python

   >>> bool(0)
   False
   >>> bool("")
   False
   >>> bool([])
   False
   >>> bool({})
   False
   >>> bool(None)
   False
   >>> bool("0")
   True
   >>> if []:
   ...     print("truthy")
   ... else:
   ...     print("falsy")
   falsy
