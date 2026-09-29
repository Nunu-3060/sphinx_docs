csv
====

CSV（Comma-Separated Values）形式のファイルを読み書きするためのモジュール。Excel などで作成された CSV ファイルとの区切り文字やクォートの扱いの違いにも対応できる。

csv.reader / csv.writer
--------------------------

``reader`` は各行をリストとして返すイテレータを、``writer`` は行を
書き込むためのオブジェクトを生成する。

.. code-block:: python

   >>> import csv
   >>> with open("users.csv", "w", newline="", encoding="utf-8") as f:
   ...     writer = csv.writer(f)
   ...     writer.writerow(["name", "age"])
   ...     writer.writerow(["Alice", 30])
   ...     writer.writerow(["Bob", 25])
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

先頭行をヘッダとして扱い、各行を辞書として読み書きできる。列の対応関係を
インデックスではなくキー名で管理できるため、列の順序に依存しないコードが書ける。

.. code-block:: python

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
   ...     writer.writerow({"name": "Carol", "age": 40})
   ...

delimiter オプション
----------------------

区切り文字を変更することで、タブ区切り（TSV）やセミコロン区切りなど CSV 以外の形式にも対応できる。書き込み時にも同じ ``delimiter`` を ``csv.writer`` に渡す必要がある。

.. code-block:: python

   >>> with open("users.tsv", "w", newline="", encoding="utf-8") as f:
   ...     writer = csv.writer(f, delimiter="\t")
   ...     writer.writerow(["name", "age"])
   ...     writer.writerow(["Alice", 30])
   ...     writer.writerow(["Bob", 25])
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

   >>> # 誤り: newline を指定しないと Windows 環境で余分な空行が
   >>> # 挿入されることがある
   >>> f = open("users.csv", "w", encoding="utf-8")
   >>>
   >>> # 正しい書き方
   >>> f = open("users.csv", "w", newline="", encoding="utf-8")

.. note::

   この挙動は ``csv`` モジュール自身が改行の処理を行うために生じる。
   詳細は Python 公式ドキュメントの csv モジュールの説明を参照。
