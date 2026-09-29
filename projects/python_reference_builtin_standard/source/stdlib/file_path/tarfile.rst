tarfile
=======

tar 形式のアーカイブファイルを作成・展開するためのモジュール。gzip や bzip2、lzma による圧縮にも対応しており、``open()`` に渡すモード文字列（``"r:gz"`` など）によって圧縮形式を切り替えられる。中心となる :class:`TarFile` クラスは ``zipfile.ZipFile`` と似た使い方ができる。

tarfile.open によるアーカイブのオープン
--------------------------------------------

モード文字列の ``:`` の後ろに圧縮形式を指定する。``"r:gz"`` は gzip 圧縮された tar アーカイブ（``.tar.gz`` / ``.tgz``）を、``"r:bz2"`` は bzip2 圧縮のアーカイブを開く。圧縮形式を自動判別させたい場合は ``"r:*"`` を使う。

.. code-block:: python

   >>> import tarfile
   >>> with tarfile.open("archive.tar.gz", "r:gz") as tf:
   ...     tf.getnames()
   ['README.txt', 'data/values.csv']

同様に、``"w:bz2"`` や ``"w:xz"`` を指定すればそれぞれ bzip2・lzma 圧縮のアーカイブを作成できる。

.. code-block:: python

   >>> with tarfile.open("archive.tar.xz", "w:xz") as tf:
   ...     tf.add("report.txt")

getnames / extractall による読み取り
----------------------------------------

``getnames()`` はアーカイブ内のファイル名一覧を、``extractall()`` はすべてのエントリを指定ディレクトリへ展開する。

.. code-block:: python

   >>> import tarfile
   >>> with tarfile.open("archive.tar.gz", "r:gz") as tf:
   ...     tf.extractall("output")

add によるアーカイブの作成
------------------------------

モード ``"w:gz"`` などで新規に開き、``add()`` でファイルやディレクトリを追加する。ディレクトリを指定すると、その配下も再帰的に格納される。

.. code-block:: python

   >>> import tarfile
   >>> with tarfile.open("new_archive.tar.gz", "w:gz") as tf:
   ...     tf.add("report.txt")
   ...     tf.add("data", recursive=True)

.. warning::

   信頼できない配布元から入手した tar アーカイブに対して ``extractall()`` をそのまま実行すると、アーカイブ内のエントリ名に ``../`` などが含まれている場合、展開先ディレクトリの外側にファイルが書き出されてしまう（パストラバーサル）危険がある。Python 3.12 以降では、``filter="data"`` を指定することでパストラバーサルなどの問題を回避できる（:pep:`706`）。Python 3.14 以降では、``filter`` を省略した場合でも安全な ``data`` フィルタが暗黙的に適用されるようになったが、意図を明確にするため明示的に指定することが推奨される。

   .. code-block:: python

      >>> with tarfile.open("untrusted.tar.gz", "r:gz") as tf:
      ...     tf.extractall("output", filter="data")
