ソートとデータの結合
======================

ソート
--------

``sort_values`` を使うと、指定した列の値に基づいて行を並び替えられます。

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, 25, 35],
   })

   df.sort_values("age")
   #     name  age
   # 1    Bob   25
   # 0  Alice   30
   # 2  Carol   35

   df.sort_values("age", ascending=False)
   # 降順に並び替え

複数列を基準にソートしたい場合は、列名の list を渡します。list の先頭の列ほど優先して並び替えられます。

.. code-block:: python

   df.sort_values(["age", "name"])
   # age の昇順に並べ、age が同じ行は name の昇順に並べる

``sort_values`` が値によるソートであるのに対し、``sort_index`` はインデックスの値そのものでソートします。

.. code-block:: python

   df3: pd.DataFrame = df.sort_values("age")
   print(df3)
   #     name  age
   # 1    Bob   25
   # 0  Alice   30
   # 2  Carol   35

   df3.sort_index()
   #     name  age
   # 0  Alice   30
   # 1    Bob   25
   # 2  Carol   35
   # 元の（sort_values 前の）行の並びに戻る

上の例のように、インデックスがまだ連番のままであれば、``sort_index()`` で ``sort_values`` によって崩れた行の並びを元の順序に戻せます。一方、``groupby`` の後のようにインデックスの値自体を振り直したい場合は、``sort_index()`` ではなく ``reset_index()`` を使います。

concat によるデータの連結
----------------------------

``concat`` は、複数の ``DataFrame`` を縦や横に連結します。

.. code-block:: python

   df1: pd.DataFrame = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
   df2: pd.DataFrame = pd.DataFrame({"name": ["Carol"], "age": [35]})

   pd.concat([df1, df2], ignore_index=True)
   #     name  age
   # 0  Alice   30
   # 1    Bob   25
   # 2  Carol   35

``ignore_index=True`` を指定すると、連結後にインデックスを振り直します。

``axis=1`` を指定すると、行数が揃った ``DataFrame`` 同士を横に連結できます。

.. code-block:: python

   df4: pd.DataFrame = pd.DataFrame({"city": ["Tokyo", "Osaka"], "score": [80, 90]})

   pd.concat([df1, df4], axis=1)
   #     name  age   city  score
   # 0  Alice   30  Tokyo     80
   # 1    Bob   25  Osaka     90

縦連結（既定の ``axis=0``）は行を追加し、横連結（``axis=1``）は列を追加するというイメージです。横連結ではインデックスを基準に位置が揃えられるため、行数や行の順序が異なる ``DataFrame`` を結合すると、意図しない ``NaN`` が発生することがあります。

merge によるデータの結合
---------------------------

``merge`` は、共通の列（キー）を基準に、SQL の JOIN のように複数の ``DataFrame`` を結合します。

.. code-block:: python

   users: pd.DataFrame = pd.DataFrame({
       "user_id": [1, 2, 3],
       "name": ["Alice", "Bob", "Carol"],
   })
   orders: pd.DataFrame = pd.DataFrame({
       "user_id": [1, 2],
       "amount": [1000, 2000],
   })

   pd.merge(users, orders, on="user_id")
   #    user_id   name  amount
   # 0        1  Alice    1000
   # 1        2    Bob    2000

   pd.merge(users, orders, on="user_id", how="left")
   #    user_id   name  amount
   # 0        1  Alice  1000.0
   # 1        2    Bob  2000.0
   # 2        3  Carol     NaN
   # how="left" を指定すると、左側（users）の行をすべて残す

``how`` には ``"inner"``\ （既定、両方に存在するキーのみ）、``"left"``、``"right"``、``"outer"`` を指定できます。

キー以外の列名が重複する場合（suffixes）
--------------------------------------------

結合する ``DataFrame`` 同士で、キー以外にも同じ名前の列がある場合、既定では列名の末尾に ``_x`` / ``_y`` が付与されて区別されます。

.. code-block:: python

   left: pd.DataFrame = pd.DataFrame({"user_id": [1, 2], "score": [80, 90]})
   right: pd.DataFrame = pd.DataFrame({"user_id": [1, 2], "score": [100, 200]})

   pd.merge(left, right, on="user_id")
   #    user_id  score_x  score_y
   # 0        1       80      100
   # 1        2       90      200
   # 左側（left）の score には _x、右側（right）の score には _y が付与される

``suffixes`` 引数を指定すると、付与される文字列を変更できます。

.. code-block:: python

   pd.merge(left, right, on="user_id", suffixes=("_before", "_after"))
   #    user_id  score_before  score_after
   # 0        1            80          100
   # 1        2            90          200
