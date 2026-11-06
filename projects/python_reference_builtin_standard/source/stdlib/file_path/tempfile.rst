tempfile
========

一時的なファイルやディレクトリを安全に作成・削除するためのモジュール。後片付け忘れによるゴミファイルの残留を防げる。

tempfile.TemporaryFile
------------------------

ファイルシステム上の名前を持たない一時ファイルを作成する（POSIX 環境の場合。Windows では ``NamedTemporaryFile`` と同じ動作になる）。``with`` ブロックを抜けると自動的に閉じられ、ファイルは削除される。既定のモードは ``"w+b"``\ （バイナリ）なので、文字列を扱う場合は例のように ``mode="w+t"`` を指定する。

.. code-block:: python
   :linenos:

   >>> import tempfile
   >>> with tempfile.TemporaryFile(mode="w+t") as f:
   ...     _ = f.write("hello")
   ...     _ = f.seek(0)
   ...     f.read()
   'hello'

tempfile.NamedTemporaryFile
------------------------------

ファイルシステム上に名前（パス）を持つ一時ファイルを作成する。他のプロセスやライブラリにパスを渡して使わせたい場合に便利である。既定（``delete=True``）ではファイルを閉じた時点で削除される。例のように ``delete=False`` を指定するとファイルは残るため、不要になったら呼び出し側で削除する。

.. code-block:: python
   :linenos:

   >>> with tempfile.NamedTemporaryFile(mode="w+t", suffix=".txt", delete=False) as f:
   ...     _ = f.write("data")
   ...     path = f.name
   >>> path  # doctest: +SKIP
   'C:\\Users\\...\\Temp\\tmpabcd1234.txt'

.. note::

   Windows では、既定の設定で作成した一時ファイルを開いたまま、そのパスで別途開き直すことはできない。Python 3.12 以降では ``delete_on_close=False`` を指定すると、``with`` ブロック内でファイルを閉じても削除されず、ブロックを抜けた時点で削除される。これにより、いったん書き込んで閉じたファイルのパスを他のプログラムに渡し、後片付けは ``with`` 文に任せるという使い方が OS を問わずできる。

   .. code-block:: python
      :linenos:

      >>> with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete_on_close=False) as f:
      ...     _ = f.write("data")
      ...     f.close()
      ...     # ここで f.name を他のプログラムに渡して読ませられる

tempfile.TemporaryDirectory
------------------------------

一時ディレクトリを作成する。``with`` ブロックを抜けると、中身ごと再帰的に削除される。

.. code-block:: python
   :linenos:

   >>> with tempfile.TemporaryDirectory() as tmpdir:
   ...     print(tmpdir)  # doctest: +SKIP
   ...     # tmpdir 以下に自由にファイルを作成できる
   C:\Users\...\Temp\tmpxyz9876

tempfile.mkstemp / tempfile.mkdtemp
--------------------------------------

より低水準な API。``mkstemp`` はファイルディスクリプタとパスのタプルを、``mkdtemp`` はディレクトリパスを返すだけで、後片付け（クローズや削除）は呼び出し側が行う必要がある。

.. code-block:: python
   :linenos:

   >>> fd, path = tempfile.mkstemp(suffix=".txt")
   >>> import os
   >>> os.close(fd)
   >>> os.remove(path)
   >>> dirpath = tempfile.mkdtemp()
   >>> os.rmdir(dirpath)
