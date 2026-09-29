dict
====

Python の辞書型 ``dict`` が持つメソッド群。キーと値の組を保持するミュータブル（変更可能）なオブジェクトであり、キーには文字列や数値、タプルなどハッシュ可能な値を使用できる。

dict.get
--------

指定したキーに対応する値を取得する。``dict[key]`` と異なり、キーが存在しない場合に ``KeyError`` を発生させず、第 2 引数で指定したデフォルト値（省略時は ``None``）を返す。

.. code-block:: python

   >>> config = {"host": "localhost", "port": 8080}
   >>> config["timeout"]
   Traceback (most recent call last):
       ...
   KeyError: 'timeout'
   >>> config.get("timeout")
   >>> config.get("timeout", 30)
   30
   >>> config.get("host", "0.0.0.0")
   'localhost'

dict.keys / dict.values / dict.items
---------------------------------------

``keys`` はキーの集合、``values`` は値の集合、``items`` はキーと値の組（タプル）の集合を、それぞれビューオブジェクトとして返す。ビューは元の辞書と連動しており、辞書が更新されると内容も自動的に反映される。辞書を直接反復（``for key in d``）した場合は、``keys()`` を反復した場合と同じキーが得られる。

.. code-block:: python

   >>> scores = {"alice": 90, "bob": 75}
   >>> list(scores.keys())
   ['alice', 'bob']
   >>> list(scores.values())
   [90, 75]
   >>> list(scores.items())
   [('alice', 90), ('bob', 75)]
   >>> for name in scores:
   ...     print(name)
   alice
   bob
   >>> for name, score in scores.items():
   ...     print(name, score)
   alice 90
   bob 75

dict.update
-----------

別の辞書やキーワード引数の内容を、既存の辞書に取り込む。同じキーが存在する場合は値が上書きされ、存在しないキーは新たに追加される。

.. code-block:: python

   >>> defaults = {"host": "localhost", "port": 8080, "debug": False}
   >>> defaults.update({"port": 9090, "timeout": 30})
   >>> defaults
   {'host': 'localhost', 'port': 9090, 'debug': False, 'timeout': 30}
   >>> defaults.update(debug=True)
   >>> defaults["debug"]
   True

dict.setdefault
---------------

キーが存在する場合はその値を返し、存在しない場合は指定したデフォルト値をそのキーに設定した上で、そのデフォルト値を返す。キーごとのリストをまとめるような、値の初期化を伴う集計処理でよく使われる。

.. code-block:: python

   >>> groups = {}
   >>> groups.setdefault("fruits", []).append("apple")
   >>> groups.setdefault("fruits", []).append("banana")
   >>> groups.setdefault("vegetables", []).append("carrot")
   >>> groups
   {'fruits': ['apple', 'banana'], 'vegetables': ['carrot']}

.. note::

   同様の集計処理は、標準ライブラリの :class:`collections.defaultdict` を使うことでも実現できる。

辞書のマージ演算子 ``|`` / ``|=``
------------------------------------

``|`` 演算子で 2 つの辞書をマージした新しい辞書を作成できる。同じキーが両方に存在する場合は、右側（後ろ）の辞書の値が優先される。``dict.update`` は既存の辞書をその場で書き換えるのに対し、``|`` は新しい辞書を返し、元の辞書はどちらも変更されない点が異なる。

.. code-block:: python

   >>> defaults = {"host": "localhost", "port": 8080}
   >>> overrides = {"port": 9090, "debug": True}
   >>> defaults | overrides
   {'host': 'localhost', 'port': 9090, 'debug': True}
   >>> defaults
   {'host': 'localhost', 'port': 8080}

その場でマージしたい場合は ``|=`` を使う。これは ``update`` とほぼ同じ結果になるが、右辺には辞書（またはキーと値の組を返すイテラブル）をそのまま書ける。

.. code-block:: python

   >>> defaults |= overrides
   >>> defaults
   {'host': 'localhost', 'port': 9090, 'debug': True}

その他の便利なメソッド
--------------------------

``copy`` は辞書の浅いコピー（shallow copy）を作成する。トップレベルのキーと値の組は新しい辞書にコピーされるが、値自体がミュータブルなオブジェクトの場合はそのオブジェクトが共有される点に注意する。

.. code-block:: python

   >>> original = {"name": "Alice", "tags": ["admin"]}
   >>> copied = original.copy()
   >>> copied["name"] = "Bob"
   >>> original["name"]
   'Alice'
   >>> copied["tags"].append("user")
   >>> original["tags"]        # リストは共有されているため変化する
   ['admin', 'user']

``fromkeys(iterable, value)`` はクラスメソッドで、指定したイテラブルの各要素をキーとし、すべて同じ値（省略時は ``None``）を持つ新しい辞書を作成する。

.. code-block:: python

   >>> dict.fromkeys(["a", "b", "c"], 0)
   {'a': 0, 'b': 0, 'c': 0}
   >>> dict.fromkeys(["x", "y"])
   {'x': None, 'y': None}

.. warning::

   ``fromkeys`` にミュータブルな値（リストなど）を渡すと、すべてのキーが **同じオブジェクト**\ を値として共有してしまうため注意が必要。キーごとに独立したリストが欲しい場合は、:doc:`辞書内包表記 <comprehension>` ``{k: [] for k in keys}`` を使う。

dict.pop / dict.popitem
------------------------

``pop`` は指定したキーの値を辞書から取り除いて返す。キーが存在しない場合、第 2 引数のデフォルト値を指定していなければ ``KeyError`` が発生する。``popitem`` は最後に挿入されたキーと値の組を取り除いて返す。

.. code-block:: python

   >>> inventory = {"apple": 10, "banana": 5, "cherry": 20}
   >>> inventory.pop("banana")
   5
   >>> inventory.pop("grape", 0)
   0
   >>> inventory
   {'apple': 10, 'cherry': 20}
   >>> inventory.popitem()
   ('cherry', 20)
   >>> inventory
   {'apple': 10}

.. note::

   辞書操作に関する補足として、新しい辞書を作る際は、``{k: v for k, v in ...}`` の形式で書ける :doc:`辞書内包表記 <comprehension>` を使うと簡潔に書ける。また、辞書は挿入順を保持することが言語仕様として保証されており、``keys`` や ``items`` などで反復した際も、キーを追加した順序で値が得られる。

   .. code-block:: python

      >>> numbers = [1, 2, 3, 4, 5]
      >>> {n: n ** 2 for n in numbers if n % 2 == 0}
      {2: 4, 4: 16}
