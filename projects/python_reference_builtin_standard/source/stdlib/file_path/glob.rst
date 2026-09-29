glob
====

シェルのワイルドカードパターンに従って、パターンにマッチするファイルパスを列挙するモジュール。

glob.glob
---------

パターンにマッチするパスの一覧をリストとして返す。

.. code-block:: python

   >>> import glob
   >>> glob.glob("source/stdlib/*.rst")  # doctest: +SKIP
   ['source/stdlib/os.rst', 'source/stdlib/pathlib.rst', 'source/stdlib/glob.rst']

パターン構文の基本
------------------

``*`` は区切り文字（``/``）を除く任意の文字列、``?`` は任意の 1 文字、``[abc]`` はいずれか 1 文字にマッチする。

.. code-block:: python

   >>> glob.glob("source/stdlib/?s.rst")
   ['source/stdlib/os.rst']
   >>> glob.glob("source/stdlib/[gs]*.rst")  # doctest: +SKIP
   ['source/stdlib/shutil.rst', 'source/stdlib/glob.rst']

glob.iglob
----------

結果をリストではなくイテレータとして返す。マッチ件数が多い場合にメモリを節約できる。

.. code-block:: python

   >>> for path in glob.iglob("source/stdlib/*.rst"):
   ...     print(path)
   source/stdlib/os.rst
   source/stdlib/pathlib.rst
   source/stdlib/glob.rst

recursive=True と ** による再帰検索
------------------------------------

``recursive=True`` を指定すると、``**`` がディレクトリを再帰的にたどるワイルドカードとして機能する。

.. code-block:: python

   >>> glob.glob("source/**/*.rst", recursive=True)  # doctest: +SKIP
   ['source/index.rst', 'source/stdlib/os.rst', 'source/builtins/type_conversion.rst']

.. note::

   ``glob.glob()`` は結果を ``str`` のリストとして返すのに対し、:doc:`pathlib` の ``Path.glob`` は ``Path`` オブジェクトのイテレータを返す。パスをオブジェクトとして扱う新しいコードでは ``Path.glob`` の使用が推奨されることが多い。
