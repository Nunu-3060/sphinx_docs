shutil
======

ファイルやディレクトリ単位でのコピー・移動・削除など、高水準のファイル操作を提供するモジュール。``os`` モジュールより一段抽象的な操作をまとめて行える。

shutil.copy / shutil.copy2
---------------------------

ファイルをコピーし、コピー先のパスを返す。コピー先にディレクトリを指定した場合は、その中に同名のファイルとしてコピーされる。``copy`` はファイルの内容とパーミッションのみをコピーし、``copy2`` はさらに更新日時などのメタデータも可能な限り保持する。

.. code-block:: python
   :linenos:

   >>> import shutil
   >>> shutil.copy("source/index.rst", "backup/index.rst")
   'backup/index.rst'
   >>> shutil.copy2("source/index.rst", "backup/index_meta.rst")
   'backup/index_meta.rst'

shutil.copytree
----------------

ディレクトリツリーを再帰的にまるごとコピーする。既定ではコピー先のディレクトリが既に存在すると ``FileExistsError`` になるため、既存のディレクトリにコピーしたい場合は ``dirs_exist_ok=True`` を指定する。

.. code-block:: python
   :linenos:

   >>> shutil.copytree("source/stdlib", "backup/stdlib")
   'backup/stdlib'

shutil.move
------------

ファイルやディレクトリを移動する。移動先が既存のディレクトリの場合は、その中に移動される。

.. code-block:: python
   :linenos:

   >>> shutil.move("backup/index.rst", "archive/index.rst")
   'archive/index.rst'

shutil.rmtree
--------------

ディレクトリを内容ごと再帰的に削除する。``os.rmdir`` と異なり空でなくても削除できる。削除したファイルは元に戻せないため、パスの指定には注意が必要である。削除に失敗したときの処理は ``onexc`` 引数（Python 3.12 以降。従来の ``onerror`` 引数は非推奨）で指定できる。

.. code-block:: python
   :linenos:

   >>> shutil.rmtree("backup/stdlib")

shutil.which
-------------

実行可能ファイルが ``PATH`` 上のどこにあるかを調べる。見つからない場合は ``None`` を返す。

.. code-block:: python
   :linenos:

   >>> shutil.which("python")  # doctest: +SKIP
   'C:\\Python312\\python.exe'
   >>> shutil.which("no-such-command") is None
   True

shutil.disk_usage
-------------------

指定したパスが存在するディスクの総容量・使用量・空き容量を取得する。

.. code-block:: python
   :linenos:

   >>> usage = shutil.disk_usage("G:/")
   >>> usage.total > usage.used
   True

shutil.make_archive / shutil.unpack_archive
----------------------------------------------

ディレクトリを ``zip``・``tar``・``gztar`` などの形式でアーカイブ化したり、アーカイブを展開したりする。形式名を指定するだけで使えるため、アーカイブ処理を 1 行で済ませたい場合に便利である（Python 3.14 以降では Zstandard 圧縮の ``zstdtar`` 形式も使える）。``unpack_archive`` で tar アーカイブを展開する際は ``tarfile`` と同じ展開フィルタが適用され、Python 3.14 以降の既定は安全な ``data`` フィルタである（:doc:`tarfile` を参照）。

.. code-block:: python
   :linenos:

   >>> shutil.make_archive("backup", "zip", "source/stdlib")
   'G:\\python\\standard\\backup.zip'
   >>> shutil.unpack_archive("backup.zip", "restored")

.. note::

   ``make_archive`` / ``unpack_archive`` は :doc:`zipfile` や :doc:`tarfile` を内部で利用した高水準の一括処理用インタフェースである。個々のファイルを選んで圧縮したり、圧縮中にファイル内容を加工したりといった細かい制御が必要な場合は、``zipfile`` / ``tarfile`` を直接使う。
