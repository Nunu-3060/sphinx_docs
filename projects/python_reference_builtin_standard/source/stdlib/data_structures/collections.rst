collections
===========

組み込みの ``dict``、``list``、``tuple`` を補完する、特殊な用途向けのコンテナデータ型を提供するモジュール。頻度カウントや順序保持、固定フィールドの軽量オブジェクトなど、よくあるパターンをすっきり書ける。

collections.Counter
--------------------

要素の出現回数を数えるための ``dict`` のサブクラス。存在しないキーに
アクセスしても ``KeyError`` にならず ``0`` を返す。

.. code-block:: python

   >>> from collections import Counter
   >>> c = Counter("abracadabra")
   >>> c
   Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
   >>> c.most_common(2)
   [('a', 5), ('b', 2)]
   >>> c["z"]
   0

collections.defaultdict
------------------------

キーが存在しない場合に、指定したファクトリ関数でデフォルト値を自動生成
する辞書。グルーピング処理を書くときに ``setdefault`` より簡潔になる。

.. code-block:: python

   >>> from collections import defaultdict
   >>> groups = defaultdict(list)
   >>> for name in ["apple", "banana", "avocado", "blueberry"]:
   ...     groups[name[0]].append(name)
   ...
   >>> dict(groups)
   {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry']}

collections.OrderedDict
------------------------

挿入順を保持する辞書。組み込みの ``dict`` も挿入順を保持するため差は小さくなったが、``move_to_end`` のような順序操作専用のメソッドが必要な場合はこちらを使う。

.. code-block:: python

   >>> from collections import OrderedDict
   >>> od = OrderedDict(a=1, b=2, c=3)
   >>> od.move_to_end("a")
   >>> od
   OrderedDict({'b': 2, 'c': 3, 'a': 1})

collections.namedtuple
-----------------------

フィールド名でアクセスできる軽量なタプルのサブクラスを生成する。
少数の属性を持つ値オブジェクトを、クラスを定義せずに手早く作れる。

.. code-block:: python

   >>> from collections import namedtuple
   >>> Point = namedtuple("Point", ["x", "y"])
   >>> p = Point(1, 2)
   >>> p.x, p.y
   (1, 2)
   >>> p._replace(x=10)
   Point(x=10, y=2)

collections.ChainMap
---------------------

複数の辞書を、コピーを作らずに 1 つの辞書のように重ねて参照できる。
先に指定した辞書ほど優先され、キーが見つからない場合は後続の辞書へ
フォールバックする。ユーザー設定とデフォルト設定を組み合わせる場合など
に便利。

.. code-block:: python

   >>> from collections import ChainMap
   >>> defaults = {"color": "blue", "size": "M"}
   >>> user_config = {"color": "red"}
   >>> settings = ChainMap(user_config, defaults)
   >>> settings["color"]
   'red'
   >>> settings["size"]
   'M'
   >>> dict(settings)
   {'color': 'red', 'size': 'M'}

collections.deque
------------------

両端からの追加・削除を高速に行える両端キュー。リストの先頭への
挿入・削除が O(n) になるのに対し、``deque`` は O(1) で行える。

.. code-block:: python

   >>> from collections import deque
   >>> dq = deque([1, 2, 3])
   >>> dq.appendleft(0)
   >>> dq.append(4)
   >>> dq
   deque([0, 1, 2, 3, 4])
   >>> dq.popleft()
   0
