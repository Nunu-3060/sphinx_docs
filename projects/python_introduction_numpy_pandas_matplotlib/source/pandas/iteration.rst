行・列に対する反復処理
========================

``DataFrame`` の行や列を 1 つずつ取り出して処理したくなることがあります。pandas にはそのためのメソッドが用意されていますが、いずれも ``groupby`` やベクトル化された演算（列全体に対する四則演算やブールインデックスなど）に比べて低速です。まずはベクトル化や ``groupby``、``apply`` で実現できないかを検討し、それでも難しい場合の最終手段としてここで紹介するメソッドを使うようにしてください。

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, 25, 35],
       "city": ["Tokyo", "Osaka", "Nagoya"],
   })

items（列ごとの反復）
-----------------------

``items()`` は、列ごとに ``(列名, Series)`` のペアを返します。

.. code-block:: python

   for name, col in df.items():
       print(name, col.dtype)
   # name str
   # age int64
   # city str

iterrows（行ごとの反復）
--------------------------

``iterrows()`` は、行ごとに ``(index, Series)`` のペアを返します。

.. code-block:: python

   for index, row in df.iterrows():
       print(index, row["name"], row["age"])
   # 0 Alice 30
   # 1 Bob 25
   # 2 Carol 35

.. note::

   1 行分のデータは列ごとに型が異なることが多いため、``row`` は ``Series`` として 1 つの ``dtype`` にまとめられます。上の例では文字列の列と数値の列が混在しているため、``row`` 全体の ``dtype`` は ``object`` になり、``age`` 列の値も ``int64`` としての情報を失います（数値の列だけで構成されている場合は、``int64`` と ``float64`` が混在していると ``float64`` にまとめられる、といったことも起こります）。列ごとの型をそのまま扱いたい場合は、次に紹介する ``itertuples()`` を使ってください。

itertuples（高速な行の反復）
-------------------------------

``itertuples()`` は、行ごとに名前付きタプルを返します。``iterrows()`` のような型変換が起きないため、より高速に動作します。

.. code-block:: python

   for row in df.itertuples():
       print(row.Index, row.name, row.age)
   # 0 Alice 30
   # 1 Bob 25
   # 2 Carol 35

既定では先頭にインデックスが ``Index`` フィールドとして追加されます。インデックス不要な場合は ``index=False`` を指定します。

.. code-block:: python

   for row in df.itertuples(index=False):
       print(row.name, row.age)

.. note::

   列名が Python の識別子として使えない文字（空白や記号など）を含む場合、対応するフィールド名は ``_1``、``_2`` のような連番に置き換わります。そのような列が多い場合は、``name=None`` を指定すると通常のタプルとして扱えます。

apply によるループの代替
--------------------------

行や列に対して関数を適用したいだけであれば、明示的にループを書かずに ``apply()`` を使う方法もあります。``axis=1`` を指定すると行ごとに、指定しない場合は列ごとに関数が呼び出されます。

.. code-block:: python

   df["greeting"] = df.apply(
       lambda row: f"{row['name']} ({row['city']})", axis=1
   )
   print(df["greeting"])
   # 0      Alice (Tokyo)
   # 1        Bob (Osaka)
   # 2    Carol (Nagoya)
   # Name: greeting, dtype: str

内部的にはループと同様の処理が行われるため速度面での劇的な改善は期待できませんが、``for`` 文を書かずに簡潔に表現できます。

map による要素ごとの変換
--------------------------

``Series`` の要素を 1 つずつ別の値に変換したいだけであれば、``apply`` よりも ``Series.map()`` の方が用途が明確です。関数だけでなく、辞書や別の ``Series`` を渡して値を対応させることもできます。

.. code-block:: python

   city_ja: dict[str, str] = {"Tokyo": "東京", "Osaka": "大阪", "Nagoya": "名古屋"}

   df["city"].map(city_ja)
   # 0     東京
   # 1     大阪
   # 2    名古屋
   # Name: city, dtype: str

辞書に対応する値が見つからない場合は ``NaN`` になります。関数を渡す使い方は ``apply`` とほとんど同じですが、慣習として、``Series`` の要素ごとの値変換には ``map``、行・列単位で複数の値を組み合わせた処理には ``apply`` を使うと、コードを読む人に意図が伝わりやすくなります。

.. note::

   速度が気になる場合の検討順序としては、まず列全体に対するベクトル化演算や ``groupby`` を検討し、それでも難しければ ``map`` / ``apply``、さらに細かい制御が必要な場合に ``itertuples()``、``iterrows()`` の順に検討するとよいでしょう。
