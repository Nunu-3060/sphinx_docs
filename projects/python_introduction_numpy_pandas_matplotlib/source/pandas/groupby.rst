集計とグルーピング
====================

``groupby`` を使うと、ある列の値ごとにデータをグループ化し、グループごとに集計を行うことができます。

groupby の基本
----------------

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "city": ["Tokyo", "Osaka", "Tokyo", "Osaka"],
       "sales": [100, 200, 150, 250],
   })

   df.groupby("city")["sales"].sum()
   # city
   # Osaka    450
   # Tokyo    250
   # Name: sales, dtype: int64

集約関数
----------

``sum`` 以外にも、numpy と同様の集約関数が利用できます。

.. code-block:: python

   df.groupby("city")["sales"].mean()
   # 都市ごとの平均売上

   df.groupby("city")["sales"].count()
   # 都市ごとのデータ件数

複数の集計をまとめて行う
--------------------------

``agg`` を使うと、複数の集計を一度に計算できます。

.. code-block:: python

   df.groupby("city")["sales"].agg(["sum", "mean", "count"])
   #        sum   mean  count
   # city
   # Osaka  450  225.0      2
   # Tokyo  250  125.0      2

value_counts による件数のカウント
------------------------------------

「列の値ごとの件数を数えたい」だけであれば、``groupby`` を使わずに ``value_counts`` を使う方がシンプルです。

.. code-block:: python

   visits: pd.DataFrame = pd.DataFrame({
       "city": ["Tokyo", "Osaka", "Tokyo", "Osaka", "Tokyo"],
   })

   visits["city"].value_counts()
   # city
   # Tokyo    3
   # Osaka    2
   # Name: count, dtype: int64

件数の多い順に自動的に並び替えられた ``Series`` が返ります。同じ内容は ``visits.groupby("city").size().sort_values(ascending=False)`` でも書けますが、単純な件数カウントであれば ``value_counts`` の方が簡潔です。

複数の列でグルーピングする
----------------------------

グルーピングに使う列は複数指定することもできます。

.. code-block:: python

   df2: pd.DataFrame = pd.DataFrame({
       "city": ["Tokyo", "Tokyo", "Osaka", "Osaka"],
       "category": ["Food", "Book", "Food", "Book"],
       "sales": [100, 50, 200, 80],
   })

   result: pd.Series = df2.groupby(["city", "category"])["sales"].sum()
   print(result)
   # city   category
   # Osaka  Book        80
   #        Food       200
   # Tokyo  Book        50
   #        Food       100
   # Name: sales, dtype: int64

複数の列でグルーピングした結果のインデックスは、``city`` と ``category`` の 2 つの階層を持つ ``MultiIndex`` になります。``loc`` に最初の階層のラベルだけを渡すと、そのグループに属する行を ``Series`` として取得でき、タプルで両方の階層を指定すると値を 1 つだけ取り出せます。

.. code-block:: python

   result.loc["Tokyo"]
   # category
   # Book     50
   # Food    100
   # Name: sales, dtype: int64

   result.loc[("Tokyo", "Food")]
   # 100

unstack / stack による整形
-------------------------------

``MultiIndex`` の内側の階層（この例では ``category``）を列に展開して「横持ち」の表にしたい場合は、``unstack`` を使います。

.. code-block:: python

   result.unstack()
   # category  Book  Food
   # city
   # Osaka       80   200
   # Tokyo       50   100

これは次に紹介する ``pivot_table`` と同じ形の表になります。反対に、列を階層に戻して「縦持ち」に戻したい場合は ``stack`` を使います。

.. code-block:: python

   result.unstack().stack()
   # city   category
   # Osaka  Book        80
   #        Food       200
   # Tokyo  Book        50
   #        Food       100
   # dtype: int64
   # unstack する前の result と同じ形に戻る

pivot_table によるクロス集計
------------------------------

``groupby`` で複数の列を集計すると、結果は ``city`` と ``category`` の組み合わせごとに 1 行が並ぶ「縦持ち」の形になります。これを「行に ``city``、列に ``category``」のような表（クロス集計表）に整形したい場合は、上で紹介した ``unstack`` のほかに、``pivot_table`` を使う方法もあります。

.. code-block:: python

   df2.pivot_table(
       index="city", columns="category", values="sales", aggfunc="sum"
   )
   # category  Book  Food
   # city
   # Osaka       80   200
   # Tokyo       50   100

Excel のピボットテーブルを使ったことがあれば、考え方はほぼ同じです。``index`` が行フィールド、``columns`` が列フィールド、``values`` が値フィールド、``aggfunc`` が集計方法に対応します。

- ``index``: 表の行に使う列
- ``columns``: 表の列に使う列
- ``values``: 集計対象の値
- ``aggfunc``: 集計方法（既定は ``"mean"``。``"sum"`` や ``"count"`` なども指定可能）

同じ ``city`` と ``category`` の組み合わせが複数行に存在する場合でも、``aggfunc`` で指定した方法（上の例では合計）でまとめて集計してくれます。

.. note::

   似たメソッドに ``pivot`` もありますが、こちらは集計を行わず、単純に表の形を変えるだけです。そのため ``index`` と ``columns`` の組み合わせが重複しているとエラーになります。集計を伴う実務のデータでは、より頑健な ``pivot_table`` を使う方が安全です。
