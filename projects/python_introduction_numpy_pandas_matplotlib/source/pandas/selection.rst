行・列の選択
==============

列の選択
----------

列名を指定すると、その列を ``Series`` として取得できます。

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, 25, 35],
       "city": ["Tokyo", "Osaka", "Nagoya"],
   })

   df["name"]
   # 0    Alice
   # 1      Bob
   # 2    Carol
   # Name: name, dtype: str

複数列を選択する場合は、列名の list を渡します（結果は ``DataFrame``）。

.. code-block:: python

   df[["name", "age"]]
   #     name  age
   # 0  Alice   30
   # 1    Bob   25
   # 2  Carol   35

loc（ラベルによる選択）
--------------------------

``loc`` は、行・列をラベル（インデックス名・列名）で指定します。

.. code-block:: python

   df.loc[0, "name"]
   # 'Alice'

   df.loc[0:1, ["name", "age"]]
   #     name  age
   # 0  Alice   30
   # 1    Bob   25

iloc（位置による選択）
-------------------------

``iloc`` は、行・列を 0 始まりの位置で指定します。list のスライスと同様、終了位置は含まれません。

.. code-block:: python

   df.iloc[0, 0]
   # 'Alice'

   df.iloc[0:2, 0:2]
   #     name  age
   # 0  Alice   30
   # 1    Bob   25

.. note::

   ``loc`` はラベルの範囲指定で終了位置を含み、``iloc`` は位置の範囲指定で終了位置を含まないという違いがあるので注意してください。

at / iat（スカラー値への高速アクセス）
----------------------------------------

単一の値だけを読み書きしたい場合は、``loc`` / ``iloc`` の代わりに ``at`` / ``iat`` を使うと、より高速かつ意図が明確になります。

.. code-block:: python

   df.at[0, "name"]
   # 'Alice'（loc[0, "name"] と同じ結果）

   df.iat[0, 0]
   # 'Alice'（iloc[0, 0] と同じ結果）

   df.at[0, "age"] = 31
   # 値の書き換えにも使える（以降の例では Alice の age は 31 になる）

``at`` はラベル、``iat`` は位置で指定する点は ``loc`` / ``iloc`` と同じです。複数行・複数列の範囲選択はできず、あくまで単一要素の取得・設定に限られます。

set_index / reset_index（インデックスの設定と解除）
------------------------------------------------------

既定では 0 始まりの連番がインデックスになりますが、``set_index`` を使うと任意の列をインデックスに設定できます。

.. code-block:: python

   df2: pd.DataFrame = df.set_index("name")
   print(df2)
   #        age    city
   # name
   # Alice   31   Tokyo
   # Bob     25   Osaka
   # Carol   35  Nagoya

   df2.loc["Bob"]
   # インデックスに設定した値でラベル選択できる

インデックスを元の連番に戻したい場合は ``reset_index`` を使います。

.. code-block:: python

   df2.reset_index()
   #     name  age    city
   # 0  Alice   31   Tokyo
   # 1    Bob   25   Osaka
   # 2  Carol   35  Nagoya
   # インデックスだった列が通常の列に戻り、新しく連番のインデックスが振られる

.. note::

   ``groupby`` や ``sort_values`` を行った後は、インデックスが連番でなくなっていることがあります。次の処理でインデックスを前提にした操作を行う場合は、``reset_index(drop=True)``\ （インデックスを列として残さず破棄する）で連番に振り直しておくと安全です。
