tarfile
=======

tar 形式のアーカイブファイルを作成・展開するためのモジュール。gzip や bzip2、lzma による圧縮にも対応しており、``open()`` に渡すモード文字列（``"r:gz"`` など）によって圧縮形式を切り替えられる。Python 3.14 以降では Zstandard 圧縮（``"r:zst"`` / ``"w:zst"``）にも対応している。``tarfile.open()`` が返す ``TarFile`` オブジェクトは、:doc:`zipfile` の ``ZipFile`` と似た使い方ができる。

tarfile.open によるアーカイブのオープン
--------------------------------------------

モード文字列の ``:`` の後ろに圧縮形式を指定する。``"r:gz"`` は gzip 圧縮された tar アーカイブ（``.tar.gz`` / ``.tgz``）を、``"r:bz2"`` は bzip2 圧縮のアーカイブを開く。圧縮形式を自動判別させたい場合は ``"r:*"`` を使う。

.. code-block:: python
   :linenos:

   >>> import tarfile
   >>> with tarfile.open("archive.tar.gz", "r:gz") as tf:
   ...     tf.getnames()
   ['README.txt', 'data/values.csv']

同様に、``"w:bz2"`` や ``"w:xz"`` を指定すればそれぞれ bzip2・lzma 圧縮のアーカイブを作成できる。

.. code-block:: python
   :linenos:

   >>> with tarfile.open("archive.tar.xz", "w:xz") as tf:
   ...     tf.add("report.txt")

getnames / extractall による読み取り
----------------------------------------

``getnames()`` はアーカイブ内のファイル名一覧を、``extractall()`` はすべてのエントリを指定ディレクトリへ展開する。``filter`` 引数については後述の警告を参照。

.. code-block:: python
   :linenos:

   >>> import tarfile
   >>> with tarfile.open("archive.tar.gz", "r:gz") as tf:
   ...     tf.extractall("output", filter="data")

add によるアーカイブの作成
------------------------------

モード ``"w:gz"`` などで新規に開き、``add()`` でファイルやディレクトリを追加する。ディレクトリを指定すると、その配下も再帰的に格納される（``recursive=False`` を指定するとディレクトリ自体のエントリのみを格納する）。

.. code-block:: python
   :linenos:

   >>> import tarfile
   >>> with tarfile.open("new_archive.tar.gz", "w:gz") as tf:
   ...     tf.add("report.txt")
   ...     tf.add("data")

.. warning::

   信頼できない配布元から入手した tar アーカイブに対して、Python 3.13 以前で ``filter`` を指定せずに ``extractall()`` を実行すると、アーカイブ内のエントリ名に ``../`` などが含まれている場合、展開先ディレクトリの外側にファイルが書き出されてしまう（パストラバーサル）危険がある。``filter="data"`` を指定すると、展開先の外側に書き出されるエントリや外側を指すリンク、デバイスファイルなどの特殊ファイルが拒否され、パストラバーサルなどの問題を回避できる（:pep:`706`。Python 3.12 で追加され、3.11 でも 3.11.4 以降で利用できる）。Python 3.12・3.13 では ``filter`` を省略すると ``DeprecationWarning`` が出たうえで従来どおり無制限に展開されるが、Python 3.14 以降では省略時の既定が ``data`` フィルタになった。動作するバージョンを問わず安全に展開できるよう、明示的に指定するのがよい。

   .. code-block:: python
      :linenos:

      >>> with tarfile.open("untrusted.tar.gz", "r:gz") as tf:
      ...     tf.extractall("output", filter="data")
