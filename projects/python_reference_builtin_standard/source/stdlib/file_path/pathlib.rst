pathlib
=======

ファイルシステムパスをオブジェクトとして扱うモジュール。文字列操作の代わりに ``Path`` オブジェクトのメソッドや演算子でパスを組み立てられ、コードの可読性が向上する。

Path の生成
-----------

``Path`` にパス文字列を渡してオブジェクトを生成する。引数なしで呼ぶとカレントディレクトリを表す。

.. code-block:: python
   :linenos:

   >>> from pathlib import Path
   >>> p = Path("source/index.rst")
   >>> p
   WindowsPath('source/index.rst')
   >>> Path.cwd()
   WindowsPath('G:/python/standard')

/ 演算子によるパスの結合
------------------------

``/`` 演算子でパスを結合できる。``os.path.join`` より直感的に書ける。

.. code-block:: python
   :linenos:

   >>> base = Path("source")
   >>> base / "stdlib" / "os.rst"
   WindowsPath('source/stdlib/os.rst')

joinpath
--------

``joinpath`` メソッドでもパスを結合できる。``/`` 演算子と異なり、複数のセグメントを一度の呼び出しでまとめて渡せる。

.. code-block:: python
   :linenos:

   >>> base = Path("source")
   >>> base.joinpath("stdlib", "os.rst")
   WindowsPath('source/stdlib/os.rst')

exists / is_file / is_dir
--------------------------

パスの存在確認や、ファイル・ディレクトリの種別判定を行う。

.. code-block:: python
   :linenos:

   >>> p = Path("source/stdlib/os.rst")
   >>> p.exists()
   True
   >>> p.is_file()
   True
   >>> p.is_dir()
   False

iterdir によるディレクトリ内一覧
----------------------------------

``iterdir`` はディレクトリ直下のエントリを ``Path`` オブジェクトのイテレータとして返す。``os.listdir`` や ``os.scandir`` に対応する pathlib の機能。

.. code-block:: python
   :linenos:

   >>> [p.name for p in Path("source").iterdir() if p.is_dir()]  # doctest: +SKIP
   ['stdlib']

walk によるディレクトリツリーの再帰的な走査
------------------------------------------------

``Path.walk()``\ （Python 3.12 以降）は ``os.walk`` に対応する pathlib のメソッドで、ディレクトリツリーを再帰的にたどりながら ``(ディレクトリパス, サブディレクトリ名のリスト, ファイル名のリスト)`` のタプルを生成する。``os.walk`` と異なり、ディレクトリパスは文字列ではなく ``Path`` オブジェクトとして得られる。

.. code-block:: python
   :linenos:

   >>> for dirpath, dirnames, filenames in Path("source/stdlib").walk():
   ...     print(dirpath, len(filenames))  # doctest: +SKIP

glob によるパターン検索
------------------------

``glob`` でワイルドカードにマッチするパスを ``Path`` オブジェクトのイテレータとして列挙する。``**`` を使うと再帰的に検索できる。パターンの先頭に ``**/`` を付ける代わりに ``rglob`` を使うこともできる。パターン構文の詳細は :doc:`glob` を参照。

.. code-block:: python
   :linenos:

   >>> sorted(Path("source/stdlib").glob("*.rst"))  # doctest: +SKIP
   [WindowsPath('source/stdlib/os.rst'), WindowsPath('source/stdlib/pathlib.rst')]
   >>> list(Path("source").glob("**/*.rst"))  # doctest: +SKIP
   >>> list(Path("source").rglob("*.rst"))  # 上と同じ  # doctest: +SKIP

read_text / write_text
-----------------------

ファイルを開いてから閉じるまでの一連の処理を 1 行で行える。

.. code-block:: python
   :linenos:

   >>> p = Path("memo.txt")
   >>> p.write_text("hello\n", encoding="utf-8")
   6
   >>> p.read_text(encoding="utf-8")
   'hello\n'

mkdir / unlink / rmdir / rename によるパスの作成・変更
----------------------------------------------------------

ディレクトリやファイルの作成・削除・改名も ``Path`` のメソッドとして行える。それぞれ ``os.makedirs`` / ``os.remove`` / ``os.rmdir`` / ``os.rename`` に対応する。``mkdir`` は ``parents=True`` で中間ディレクトリも含めて作成し、``exist_ok=True`` で既に存在していてもエラーにしない。

.. code-block:: python
   :linenos:

   >>> p = Path("a/b/c")
   >>> p.mkdir(parents=True, exist_ok=True)
   >>> f = p / "file.txt"
   >>> f.write_text("hello\n", encoding="utf-8")
   6
   >>> f.rename(p / "renamed.txt")
   WindowsPath('a/b/c/renamed.txt')
   >>> (p / "renamed.txt").unlink()
   >>> p.rmdir()

``rename`` は移動先に同名のファイルが存在すると、Windows では ``FileExistsError`` になる（POSIX では黙って上書きされる）。OS を問わず上書きしたい場合は ``replace`` を使う。

copy / move によるコピー・移動
------------------------------

Python 3.14 以降では、``Path.copy()`` / ``Path.move()`` でファイルやディレクトリ（ツリー全体）のコピー・移動を行える。従来はこうした処理に :doc:`shutil` を併用する必要があった。いずれも新しいパスを表す ``Path`` オブジェクトを返す。指定したディレクトリの中へコピー・移動する ``copy_into()`` / ``move_into()`` もある。なお、コピー先・移動先の親ディレクトリはあらかじめ存在している必要がある。

.. code-block:: python
   :linenos:

   >>> src = Path("memo.txt")
   >>> src.copy("backup/memo.txt")  # doctest: +SKIP
   WindowsPath('backup/memo.txt')
   >>> src.move_into("archive")  # doctest: +SKIP
   WindowsPath('archive/memo.txt')

parent / name / suffix
-----------------------

パスを構成要素に分解して参照する属性。

.. code-block:: python
   :linenos:

   >>> p = Path("source/stdlib/os.rst")
   >>> p.parent
   WindowsPath('source/stdlib')
   >>> p.name
   'os.rst'
   >>> p.stem
   'os'
   >>> p.suffix
   '.rst'

with_name / with_suffix / with_stem
-------------------------------------

パスの一部だけを置き換えた新しい ``Path`` オブジェクトを返す。元のオブジェクトは変更されない（イミュータブル）。

.. code-block:: python
   :linenos:

   >>> p = Path("source/stdlib/os.rst")
   >>> p.with_name("pathlib.rst")
   WindowsPath('source/stdlib/pathlib.rst')
   >>> p.with_suffix(".txt")
   WindowsPath('source/stdlib/os.txt')
   >>> p.with_stem("index")
   WindowsPath('source/stdlib/index.rst')

resolve
-------

相対パスを絶対パスに変換する。``..`` やシンボリックリンクも解決される。

.. code-block:: python
   :linenos:

   >>> p = Path("source/../source/index.rst")
   >>> p.resolve()  # doctest: +SKIP
   WindowsPath('G:/python/standard/source/index.rst')

as_posix
--------

区切り文字を OS に依存せず ``/`` に統一した文字列を返す。Windows でも ``/`` 区切りの文字列を得たい場合に使う。

.. code-block:: python
   :linenos:

   >>> p = Path("source") / "stdlib" / "os.rst"
   >>> p.as_posix()
   'source/stdlib/os.rst'

.. note::

   :doc:`os` の ``os.path`` は文字列に対する関数群としてパスを扱うのに対し、``pathlib`` はパスをオブジェクトとして扱うオブジェクト指向インタフェースを提供する。新しいコードでは ``pathlib`` の使用が推奨されることが多い。
