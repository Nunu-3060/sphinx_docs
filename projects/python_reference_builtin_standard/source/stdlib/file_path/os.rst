os
==

オペレーティングシステムに依存する機能（ファイル操作、環境変数、プロセス管理など）へのポータブルなインタフェースを提供するモジュール。

os.getcwd / os.chdir
---------------------

カレントディレクトリの取得・変更を行う。

.. code-block:: python

   >>> import os
   >>> os.getcwd()
   'G:\\python\\standard'
   >>> os.chdir("source")
   >>> os.getcwd()
   'G:\\python\\standard\\source'
   >>> os.chdir("..")

os.listdir / os.scandir
-------------------------

ディレクトリ内のエントリ一覧を取得する。``scandir`` はファイル種別などの情報を保持したまま反復できるため、大量のファイルを扱う際は高速。

.. code-block:: python

   >>> os.listdir(".")  # doctest: +SKIP
   ['source', 'Makefile', 'build_html.bat']
   >>> [e.name for e in os.scandir(".") if e.is_dir()]  # doctest: +SKIP
   ['source']

os.walk
-------

ディレクトリツリーを再帰的にたどり、各ディレクトリについて ``(ディレクトリパス, サブディレクトリ名のリスト, ファイル名のリスト)`` のタプルを生成する。ディレクトリ配下を丸ごと処理したい場合に最もよく使う関数。

.. code-block:: python

   >>> for dirpath, dirnames, filenames in os.walk("source/stdlib"):
   ...     print(dirpath, len(filenames))  # doctest: +SKIP

.. note::

   Python 3.12 以降では、:doc:`pathlib` の ``Path.walk()`` が ``os.walk`` と同様の機能をオブジェクト指向インタフェースで提供する。

os.makedirs / os.remove / os.rmdir
------------------------------------

ディレクトリ・ファイルの作成や削除を行う。

.. code-block:: python

   >>> os.makedirs("a/b/c", exist_ok=True)
   >>> open("a/b/c/file.txt", "w").close()
   >>> os.remove("a/b/c/file.txt")
   >>> os.rmdir("a/b/c")

os.environ
----------

環境変数を辞書のように参照・設定する。

.. code-block:: python

   >>> os.environ["PATH"]  # doctest: +SKIP
   >>> os.environ.get("MY_APP_ENV", "development")
   'development'

os.getpid / os.system / os.kill
--------------------------------

実行中のプロセスに関する情報の取得や、他プロセスの起動・制御も ``os`` モジュールの役割の一つ。``os.getpid()`` は現在のプロセス ID を返す。シェルコマンドを実行したい場合は ``os.system()``、他プロセスにシグナルを送りたい場合は ``os.kill()`` が使えるが、いずれもより高機能な :mod:`subprocess` モジュールで代替できることが多い。

.. code-block:: python

   >>> os.getpid()  # doctest: +SKIP
   12345
   >>> os.system("echo hello")  # doctest: +SKIP
   0
   >>> import signal
   >>> pid = 12345  # 実在するプロセスの ID を指定する必要がある
   >>> os.kill(pid, signal.SIGTERM)  # doctest: +SKIP

os.path
-------

パス文字列を操作するサブモジュール。パスの結合や存在確認などによく使う。

.. code-block:: python

   >>> os.path.join("source", "index.rst")
   'source\\index.rst'
   >>> os.path.exists("source/index.rst")
   True
   >>> os.path.splitext("index.rst")
   ('index', '.rst')
   >>> os.path.dirname("source/stdlib/os.rst")
   'source/stdlib'
   >>> os.path.basename("source/stdlib/os.rst")
   'os.rst'
   >>> os.path.abspath("source/index.rst")  # doctest: +SKIP
   'G:\\python\\standard\\source\\index.rst'

.. note::

   新しいコードでは、オブジェクト指向インタフェースを持つ :doc:`pathlib` の使用が推奨されることが多い。
