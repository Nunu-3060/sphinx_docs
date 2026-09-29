tempfile
========

一時的なファイルやディレクトリを安全に作成・削除するためのモジュール。後片付け忘れによるゴミファイルの残留を防げる。

tempfile.TemporaryFile
------------------------

名前を持たない一時ファイルを作成する。``with`` ブロックを抜けると自動的に閉じられ、ファイルは削除される。

.. code-block:: python

   >>> import tempfile
   >>> with tempfile.TemporaryFile(mode="w+t") as f:
   ...     f.write("hello")
   ...     _ = f.seek(0)
   ...     f.read()
   'hello'

tempfile.NamedTemporaryFile
------------------------------

ファイルシステム上に名前（パス）を持つ一時ファイルを作成する。他のプロセスやライブラリにパスを渡して使わせたい場合に便利。

.. code-block:: python

   >>> with tempfile.NamedTemporaryFile(mode="w+t", suffix=".txt", delete=False) as f:
   ...     f.write("data")
   ...     path = f.name
   >>> path  # doctest: +SKIP
   'C:\\Users\\...\\Temp\\tmpabcd1234.txt'

tempfile.TemporaryDirectory
------------------------------

一時ディレクトリを作成する。``with`` ブロックを抜けると、中身ごと再帰的に削除される。

.. code-block:: python

   >>> with tempfile.TemporaryDirectory() as tmpdir:
   ...     print(tmpdir)  # doctest: +SKIP
   ...     # tmpdir 以下に自由にファイルを作成できる
   C:\Users\...\Temp\tmpxyz9876

tempfile.mkstemp / tempfile.mkdtemp
--------------------------------------

より低水準な API。``mkstemp`` はファイルディスクリプタとパスのタプルを、``mkdtemp`` はディレクトリパスを返すだけで、後片付け（クローズや削除）は呼び出し側が行う必要がある。

.. code-block:: python

   >>> fd, path = tempfile.mkstemp(suffix=".txt")
   >>> import os
   >>> os.close(fd)
   >>> os.remove(path)
   >>> dirpath = tempfile.mkdtemp()
   >>> os.rmdir(dirpath)
