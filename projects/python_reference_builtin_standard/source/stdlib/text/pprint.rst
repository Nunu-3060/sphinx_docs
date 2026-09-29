pprint
======

ネストしたリストや辞書などのデータ構造を、人間が読みやすい形に整形して
出力するモジュール。組み込みの ``print()`` は複雑な構造を1行に詰め込んで
しまい読みにくいのに対し、``pprint`` は適度な位置で改行し、インデントを
揃えて出力する。

print() との比較
------------------

実際にどのような違いが出るか、深くネストしたデータ構造を例に見て
みる。``pprint()`` は同じデータを複数行に
分けて整形して出力する。

.. code-block:: python

   >>> data = {
   ...     "name": "太郎",
   ...     "age": 30,
   ...     "children": [
   ...         {"name": "花子", "age": 5, "hobbies": ["絵", "音楽"]},
   ...         {"name": "次郎", "age": 3, "hobbies": ["ブロック"]},
   ...     ],
   ... }
   >>> print(data)
   {'name': '太郎', 'age': 30, 'children': [{'name': '花子', 'age': 5, 'hobbies': ['絵', '音楽']}, {'name': '次郎', 'age': 3, 'hobbies': ['ブロック']}]}

   >>> from pprint import pprint
   >>> pprint(data)
   {'age': 30,
    'children': [{'age': 5, 'hobbies': ['絵', '音楽'], 'name': '花子'},
                 {'age': 3, 'hobbies': ['ブロック'], 'name': '次郎'}],
    'name': '太郎'}

width / indent / sort_dicts パラメータ
----------------------------------------

``pprint()`` の出力は、いくつかの引数で調整できる。``width`` は1行の
最大文字数（これを超えそうな場合に改行される）、``indent`` はネストの
深さごとに追加するインデント幅、``sort_dicts`` は辞書のキーをソートして
表示するかどうかを制御する（デフォルトは ``True`` で、``False`` にすると
元の挿入順で表示される）。

.. code-block:: python

   >>> from pprint import pprint
   >>> data = {"b": [1, 2, 3, 4, 5, 6, 7, 8], "a": {"x": 1, "y": 2}}
   >>> pprint(data, width=20)
   {'a': {'x': 1,
          'y': 2},
    'b': [1,
          2,
          3,
          4,
          5,
          6,
          7,
          8]}
   >>> pprint(data, indent=4, sort_dicts=False)
   {'b': [1, 2, 3, 4, 5, 6, 7, 8], 'a': {'x': 1, 'y': 2}}

pformat()
---------

``pprint()`` は結果を標準出力にそのまま表示するが、画面に表示せず、
整形済みの文字列として受け取りたい場合は ``pformat()`` を使う。ログ出力や、別の
文字列に組み込みたい場合に便利。

.. code-block:: python

   >>> from pprint import pformat
   >>> data = {"status": "ok", "items": [1, 2, 3]}
   >>> formatted = pformat(data)
   >>> formatted
   "{'items': [1, 2, 3], 'status': 'ok'}"
   >>> import logging
   >>> logging.info("受信データ:\n%s", pformat(data))  # doctest: +SKIP

.. note::

   ``pprint`` は主に開発時のデバッグや、ログ・対話環境での確認用途で使われる。``pprint`` は他システムとのデータ交換や永続化を目的とせず、あくまで人間が読む画面上での整形表示を目的とする。構造化データをプログラムの出力として扱いたい場合は、``pprint`` の出力形式（Pythonリテラル風）ではなく :doc:`../data_format/json` を使うのが適切である。
