pickle
=======

Python のオブジェクトをバイト列にシリアライズ（直列化）し、そこから元のオブジェクトを復元するためのモジュール。JSON と異なり、ほぼ任意の Python オブジェクト（カスタムクラスのインスタンスなど）をそのまま保存・復元できる。

pickle.dump / pickle.load
----------------------------

``dump`` はオブジェクトをファイルに書き込み、``load`` はファイルから
オブジェクトを復元する。ファイルはバイナリモード（``"wb"`` / ``"rb"``）
で開く必要がある。

.. code-block:: python

   >>> import pickle
   >>> data = {"name": "Alice", "scores": [90, 85, 100]}
   >>> with open("data.pkl", "wb") as f:
   ...     pickle.dump(data, f)
   ...
   >>> with open("data.pkl", "rb") as f:
   ...     loaded = pickle.load(f)
   ...
   >>> loaded
   {'name': 'Alice', 'scores': [90, 85, 100]}

pickle.dumps / pickle.loads
--------------------------------

ファイルを経由せず、バイト列として直接シリアライズ・復元したい場合は ``dumps`` / ``loads`` を使う。

.. code-block:: python

   >>> b = pickle.dumps(data)
   >>> b[:10]
   b'\x80\x05\x95...'
   >>> pickle.loads(b)
   {'name': 'Alice', 'scores': [90, 85, 100]}

カスタムクラスのシリアライズ
--------------------------------

インスタンス属性を持つ独自クラスのオブジェクトも、追加の設定なしで
そのまま保存・復元できる。

.. code-block:: python

   >>> class Point:
   ...     def __init__(self, x, y):
   ...         self.x = x
   ...         self.y = y
   ...
   >>> p = pickle.loads(pickle.dumps(Point(1, 2)))
   >>> p.x, p.y
   (1, 2)

.. note::

   pickle はクラスの定義そのものではなく、クラスがどのモジュールのどの名前で定義されているかという「パス」だけを保存する。そのため、unpickle 時にはそのクラスが同じモジュールパスから import 可能である必要がある。上記の例は対話環境の同一スコープ内で実行しているため問題なく動くが、実際のプログラムでファイルやネットワーク経由で pickle データをやり取りする場合、保存時と復元時でクラスのモジュールを移動・削除・改名すると ``AttributeError: Can't get attribute 'Point' on <module ...>`` のようなエラーになるので注意。

.. warning::

   信頼できない、または改ざんされている可能性のあるデータを ``pickle.load`` / ``pickle.loads`` で復元してはならない。pickle 形式はデータの復元過程で任意のコードを実行できてしまうため、悪意のある pickle データを読み込むとシステムが侵害される危険がある。外部から受け取ったデータには :doc:`json` など、より安全な形式を使用すること。
