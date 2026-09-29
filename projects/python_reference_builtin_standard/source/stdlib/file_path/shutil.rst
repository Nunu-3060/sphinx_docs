shutil
======

ファイルやディレクトリ単位でのコピー・移動・削除など、高水準のファイル操作を提供するモジュール。``os`` モジュールより一段抽象的な操作をまとめて行える。

shutil.copy / shutil.copy2
---------------------------

ファイルをコピーする。``copy2`` は更新日時などのメタデータも保持する。

.. code-block:: python

   >>> import shutil
   >>> shutil.copy("source/index.rst", "backup/index.rst")
   'backup/index.rst'
   >>> shutil.copy2("source/index.rst", "backup/index_meta.rst")
   'backup/index_meta.rst'

shutil.copytree
----------------

ディレクトリツリーを再帰的にまるごとコピーする。

.. code-block:: python

   >>> shutil.copytree("source/stdlib", "backup/stdlib")
   'backup/stdlib'

shutil.move
------------

ファイルやディレクトリを移動する。移動先が既存のディレクトリの場合は、その中に移動される。

.. code-block:: python

   >>> shutil.move("backup/index.rst", "archive/index.rst")
   'archive/index.rst'

shutil.rmtree
--------------

ディレクトリを内容ごと再帰的に削除する。``os.rmdir`` と異なり空でなくても削除できる。

.. code-block:: python

   >>> shutil.rmtree("backup/stdlib")

shutil.which
-------------

実行可能ファイルが ``PATH`` 上のどこにあるかを調べる。見つからない場合は ``None`` を返す。

.. code-block:: python

   >>> shutil.which("python")  # doctest: +SKIP
   'C:\\Python312\\python.exe'
   >>> shutil.which("no-such-command")
   None

shutil.disk_usage
-------------------

指定したパスが存在するディスクの総容量・使用量・空き容量を取得する。

.. code-block:: python

   >>> usage = shutil.disk_usage("G:/")
   >>> usage.total > usage.used
   True

shutil.make_archive / shutil.unpack_archive
----------------------------------------------

ディレクトリを ``zip``・``tar``・``gztar`` などの形式でアーカイブ化したり、アーカイブを展開したりする。形式名を指定するだけで使えるため、アーカイブ処理を 1 行で済ませたい場合に便利。

.. code-block:: python

   >>> shutil.make_archive("backup", "zip", "source/stdlib")
   'G:\\python\\standard\\backup.zip'
   >>> shutil.unpack_archive("backup.zip", "restored")

.. note::

   ``make_archive``/``unpack_archive`` は :doc:`zipfile` や :doc:`tarfile` を内部で利用した高水準の一括処理用インタフェース。個々のファイルを選んで圧縮したり、圧縮中にファイル内容を加工したりといった細かい制御が必要な場合は、``zipfile``/``tarfile`` を直接使う。
