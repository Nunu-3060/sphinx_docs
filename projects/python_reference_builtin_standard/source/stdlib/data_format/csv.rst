csv
====

CSV（Comma-Separated Values）形式のファイルを読み書きするためのモジュール。Excel などで作成された CSV ファイルとの区切り文字やクォートの扱いの違いにも対応できる。

csv.reader / csv.writer
--------------------------

``reader`` は各行をリストとして返すイテレータを、``writer`` は行を書き込むためのオブジェクトを生成する。``writer`` の ``writerow()`` は 1 行を、``writerows()`` は複数行をまとめて書き込む。読み込んだ値は、元が数値であってもすべて文字列になる点に注意。

.. code-block:: python
   :linenos:

   >>> import csv
   >>> with open("users.csv", "w", newline="", encoding="utf-8") as f:
   ...     writer = csv.writer(f)
   ...     writer.writerows([["name", "age"], ["Alice", 30], ["Bob", 25]])
   ...
   >>> with open("users.csv", newline="", encoding="utf-8") as f:
   ...     reader = csv.reader(f)
   ...     for row in reader:
   ...         print(row)
   ...
   ['name', 'age']
   ['Alice', '30']
   ['Bob', '25']

csv.DictReader / csv.DictWriter
-----------------------------------

先頭行をヘッダとして扱い、各行を辞書として読み書きできる。列の対応関係をインデックスではなくキー名で管理できるため、列の順序に依存しないコードが書ける。なお ``writerow()`` と ``writeheader()`` は書き込んだ文字数を返すため、対話環境では下の例のようにその値が表示される。

.. code-block:: python
   :linenos:

   >>> with open("users.csv", newline="", encoding="utf-8") as f:
   ...     reader = csv.DictReader(f)
   ...     for row in reader:
   ...         print(row["name"], row["age"])
   ...
   Alice 30
   Bob 25

   >>> with open("out.csv", "w", newline="", encoding="utf-8") as f:
   ...     writer = csv.DictWriter(f, fieldnames=["name", "age"])
   ...     writer.writeheader()
   ...     writer.writerows([{"name": "Carol", "age": 40}])
   ...
   10

delimiter オプション
----------------------

区切り文字を変更することで、タブ区切り（TSV）やセミコロン区切りなど CSV 以外の形式にも対応できる。読み込み時と書き込み時の両方で、``csv.reader`` / ``csv.writer`` に同じ ``delimiter`` を渡す必要がある。

.. code-block:: python
   :linenos:

   >>> with open("users.tsv", "w", newline="", encoding="utf-8") as f:
   ...     writer = csv.writer(f, delimiter="\t")
   ...     writer.writerows([["name", "age"], ["Alice", 30], ["Bob", 25]])
   ...
   >>> with open("users.tsv", newline="", encoding="utf-8") as f:
   ...     reader = csv.reader(f, delimiter="\t")
   ...     for row in reader:
   ...         print(row)
   ...
   ['name', 'age']
   ['Alice', '30']
   ['Bob', '25']

newline='' を指定する理由
----------------------------

CSV ファイルを開く際は、読み込み・書き込みのいずれも ``open(..., newline="")`` を指定するのが公式に推奨されている。これを省略すると、改行コードの変換により、埋め込まれた改行を含むフィールドの扱いが環境によって崩れることがある。

.. code-block:: python
   :linenos:

   >>> # 誤り: newline を指定しないと Windows 環境で余分な空行が
   >>> # 挿入されることがある
   >>> f = open("users.csv", "w", encoding="utf-8")
   >>>
   >>> # 正しい書き方
   >>> f = open("users.csv", "w", newline="", encoding="utf-8")

.. note::

   この挙動は ``csv`` モジュール自身が改行の処理を行うために生じる。詳細は `Python 公式ドキュメントの csv モジュールの説明 <https://docs.python.org/ja/3/library/csv.html>`_ を参照。

.. note::

   Excel で作成された UTF-8 の CSV ファイルは、先頭に BOM（バイト順マーク）が付いていることが多い。``encoding="utf-8"`` のまま読み込むと、最初の列名の先頭に ``\ufeff`` が混入するため、``encoding="utf-8-sig"`` を指定する。Excel で開く CSV ファイルを書き出す場合も、``utf-8-sig`` を指定すると文字化けを防げる。
