pickle
=======

Python のオブジェクトをバイト列にシリアライズ（直列化）し、そこから元のオブジェクトを復元するためのモジュール。JSON と異なり、ほぼ任意の Python オブジェクト（カスタムクラスのインスタンスなど）をそのまま保存・復元できる。

pickle.dump / pickle.load
----------------------------

``dump`` はオブジェクトをファイルに書き込み、``load`` はファイルからオブジェクトを復元する。ファイルはバイナリモード（``"wb"`` / ``"rb"``）で開く必要がある。

.. code-block:: python
   :linenos:

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

``dump`` / ``dumps`` が使う pickle プロトコル（データ形式のバージョン）のデフォルトは ``pickle.DEFAULT_PROTOCOL`` で、Python 3.14 以降は 5、3.13 以前は 4 である。読み込み側はプロトコルを自動判別するが、古い Python で読み込む必要がある場合は ``protocol`` 引数で明示的に指定する。

.. code-block:: python
   :linenos:

   >>> b = pickle.dumps(data)
   >>> b[:2]  # 先頭はプロトコル番号を表すヘッダ（Python 3.13 以前では b'\x80\x04'）
   b'\x80\x05'
   >>> pickle.loads(b)
   {'name': 'Alice', 'scores': [90, 85, 100]}

カスタムクラスのシリアライズ
--------------------------------

インスタンス属性を持つ独自クラスのオブジェクトも、追加の設定なしでそのまま保存・復元できる。

.. code-block:: python
   :linenos:

   >>> class Point:
   ...     def __init__(self, x, y):
   ...         self.x = x
   ...         self.y = y
   ...
   >>> p = pickle.loads(pickle.dumps(Point(1, 2)))
   >>> p.x, p.y
   (1, 2)

.. note::

   pickle はクラスの定義（コード）そのものではなく、クラスがどのモジュールのどの名前で定義されているかという「パス」だけを保存する。そのため、unpickle 時にはそのクラスが同じモジュールパスから import 可能である必要がある。上記の例は対話環境の同一スコープ内で実行しているため問題なく動くが、実際のプログラムでファイルやネットワーク経由で pickle データをやり取りする場合、保存後にクラスを別のモジュールへ移動したり、クラスやモジュールを削除・改名したりすると、復元時に ``AttributeError`` や ``ModuleNotFoundError`` になるので注意。

.. warning::

   信頼できない、または改ざんされている可能性のあるデータを ``pickle.load`` / ``pickle.loads`` で復元してはならない。pickle 形式はデータの復元過程で任意のコードを実行できてしまうため、悪意のある pickle データを読み込むとシステムが侵害される危険がある。外部から受け取ったデータには :doc:`json` など、より安全な形式を使用すること。
