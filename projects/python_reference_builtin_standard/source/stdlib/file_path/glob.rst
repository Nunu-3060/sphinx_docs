glob
====

シェルのワイルドカードパターンに従って、パターンにマッチするファイルパスを列挙するモジュール。

glob.glob
---------

パターンにマッチするパスの一覧をリストとして返す。このページの出力例は Linux / macOS でのものであり、Windows では返されるパスの一部の区切り文字が ``\`` になる。

.. code-block:: python
   :linenos:

   >>> import glob
   >>> glob.glob("source/stdlib/file_path/*.rst")  # doctest: +SKIP
   ['source/stdlib/file_path/os.rst', 'source/stdlib/file_path/pathlib.rst', 'source/stdlib/file_path/glob.rst']

パターン構文の基本
------------------

``*`` は区切り文字（``/``）を除く任意の文字列、``?`` は任意の 1 文字、``[abc]`` はいずれか 1 文字にマッチする。

.. code-block:: python
   :linenos:

   >>> glob.glob("source/stdlib/file_path/?s.rst")
   ['source/stdlib/file_path/os.rst']
   >>> glob.glob("source/stdlib/file_path/[gs]*.rst")  # doctest: +SKIP
   ['source/stdlib/file_path/shutil.rst', 'source/stdlib/file_path/glob.rst']

結果の順序は保証されないため、順序が必要な場合は ``sorted()`` で並べ替える。また、``*`` や ``?`` はドット（``.``）で始まる隠しファイルにはマッチしない。隠しファイルも対象にしたい場合は ``include_hidden=True``\ （Python 3.11 以降）を指定する。

glob.iglob
----------

結果をリストではなくイテレータとして返す。マッチ件数が多い場合にメモリを節約できる。

.. code-block:: python
   :linenos:

   >>> for path in glob.iglob("source/stdlib/file_path/*.rst"):
   ...     print(path)  # doctest: +SKIP
   source/stdlib/file_path/os.rst
   source/stdlib/file_path/pathlib.rst
   source/stdlib/file_path/glob.rst

recursive=True と ** による再帰検索
------------------------------------

``recursive=True`` を指定すると、``**`` がディレクトリを再帰的にたどるワイルドカードとして機能する。

.. code-block:: python
   :linenos:

   >>> glob.glob("source/**/*.rst", recursive=True)  # doctest: +SKIP
   ['source/index.rst', 'source/builtins/type_conversion.rst', 'source/stdlib/file_path/os.rst']

.. note::

   ``glob.glob()`` は結果を ``str`` のリストとして返すのに対し、:doc:`pathlib` の ``Path.glob`` は ``Path`` オブジェクトのイテレータを返す（``Path.glob`` では ``recursive=True`` を指定しなくても ``**`` が再帰的に機能する）。パスをオブジェクトとして扱う新しいコードでは ``Path.glob`` の使用が推奨されることが多い。

glob.translate
--------------

``glob.translate()``\ （Python 3.13 以降）は、glob パターンを同等の正規表現文字列に変換する。ファイルシステムを走査せずに、手元のパス文字列の一覧をパターンで絞り込みたい場合に使える。

.. code-block:: python
   :linenos:

   >>> import re
   >>> regex = glob.translate("src/**/*.py", recursive=True)
   >>> paths = ["src/main.py", "src/pkg/util.py", "docs/index.rst"]
   >>> [p for p in paths if re.match(regex, p)]
   ['src/main.py', 'src/pkg/util.py']
