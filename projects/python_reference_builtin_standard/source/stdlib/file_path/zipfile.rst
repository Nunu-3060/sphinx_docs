zipfile
=======

ZIP 形式のアーカイブファイルを作成・展開・検査するためのモジュール。中心となる :class:`ZipFile` クラスは、モード ``"r"`` で開けば既存の ZIP ファイルの読み取りに、モード ``"w"`` で開けば新規作成や書き込みに使える。ほかに、既存のアーカイブに追記する ``"a"`` （append）モードや、ファイルが存在しない場合のみ新規作成する ``"x"`` （exclusive create）モードもある。

ZipFile によるアーカイブのオープン
-------------------------------------

``ZipFile`` はコンテキストマネージャとして使えるため、``with`` 文を使うと確実にファイルを閉じることができる。

.. code-block:: python

   >>> import zipfile
   >>> with zipfile.ZipFile("archive.zip", "r") as zf:
   ...     zf.namelist()
   ['README.txt', 'data/values.csv']

namelist / extractall による読み取り
---------------------------------------

``namelist()`` はアーカイブ内のファイル名一覧を返し、``extractall()`` は指定したディレクトリへすべてのエントリを展開する。

.. code-block:: python

   >>> import zipfile
   >>> with zipfile.ZipFile("archive.zip", "r") as zf:
   ...     print(zf.namelist())
   ...     zf.extractall("output")
   ['README.txt', 'data/values.csv']

read によるメモリ上への読み込み
-----------------------------------

展開せずに、アーカイブ内の特定ファイルの内容だけをメモリ上に読み込むこともできる。

.. code-block:: python

   >>> import zipfile
   >>> with zipfile.ZipFile("archive.zip", "r") as zf:
   ...     content = zf.read("README.txt")
   ...     print(content.decode("utf-8"))
   This is a sample archive.

write / writestr によるアーカイブの作成
--------------------------------------------

モード ``"w"`` で開くと新しい ZIP ファイルを作成できる。``write()`` は既存のファイルをアーカイブに追加し、``writestr()`` は文字列やバイト列を直接エントリとして書き込む。

.. code-block:: python

   >>> import zipfile
   >>> with zipfile.ZipFile("new_archive.zip", "w",
   ...                      compression=zipfile.ZIP_DEFLATED) as zf:
   ...     zf.write("report.txt")
   ...     zf.writestr("memo.txt", "これはメモです。\n")

.. note::

   ``compression=zipfile.ZIP_DEFLATED`` を指定すると圧縮されたアーカイブになる。省略した場合は無圧縮（``ZIP_STORED``）で保存される。
