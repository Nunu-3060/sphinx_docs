欠損値の処理と重複の除去
==========================

実際のデータには、値が存在しない「欠損値」が含まれていることがよくあります。pandas では欠損値を ``NaN`` として表現します。

欠損値の確認
--------------

.. code-block:: python

   import numpy as np
   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, np.nan, 35],
   })

   df.isna()
   #     name    age
   # 0  False  False
   # 1  False   True
   # 2  False  False

   df.isna().sum()
   # name    0
   # age     1
   # dtype: int64
   # 列ごとの欠損値の個数

any / all による判定
-----------------------

``any()`` は「1 つでも ``True`` があるか」、``all()`` は「すべて ``True`` か」を判定します。``notna()`` は ``isna()`` とちょうど逆の結果を返すメソッドで、欠損値でない要素を ``True`` と判定します。これらを組み合わせると、欠損値の有無を列ごと・``DataFrame`` 全体のどちらでも手早く確認できます。

.. code-block:: python

   df.isna().any()
   # name    False
   # age      True
   # dtype: bool
   # 列ごとに、欠損値が 1 つでもあるかどうか

   df.isna().any().any()
   # True
   # DataFrame 全体で欠損値が 1 つでもあるかどうか

   df.notna().all()
   # name     True
   # age     False
   # dtype: bool
   # 列ごとに、欠損値が 1 つも無いかどうか（isna().any() の逆）

.. note::

   ``any()`` / ``all()`` は ``Series`` に対しては単一の真偽値を返しますが、``DataFrame`` に対しては既定で列ごとの結果（``Series``）を返します。``DataFrame`` 全体で 1 つの真偽値にまとめたい場合は、上の例のように ``.any()`` をもう一度呼び出します。

欠損値の除去
--------------

.. code-block:: python

   df.dropna()
   # 欠損値を含む行をすべて削除する
   #     name   age
   # 0  Alice  30.0
   # 2  Carol  35.0

欠損値の穴埋め
----------------

.. code-block:: python

   df.fillna(0)
   # 欠損値を 0 で穴埋めする

   df["age"].fillna(df["age"].mean())
   # 欠損値をその列の平均値で穴埋めする

.. note::

   ``dropna`` や ``fillna`` も、「:doc:`dataframe`」で紹介した ``drop`` や ``rename`` と同様に、既定では元のデータを変更せず、結果を新しいオブジェクトとして返します。元のデータを直接書き換えたい場合は、戻り値を変数に代入し直すか、``inplace=True`` を指定します。

重複行の除去
--------------

欠損値の処理と並んで、重複行の除去もよく行うデータクレンジングです。

.. code-block:: python

   df2: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Alice"],
       "age": [30, 25, 30],
   })

   df2.duplicated()
   # 0    False
   # 1    False
   # 2     True
   # dtype: bool
   # 2 行目（Alice, 30）が、それより前の行と完全に一致している

   df2.drop_duplicates()
   #     name  age
   # 0  Alice   30
   # 1    Bob   25

既定ではすべての列が一致する行を重複とみなしますが、``subset`` 引数で判定に使う列を絞ることもできます。

.. code-block:: python

   df2.drop_duplicates(subset=["name"])
   # name 列だけで重複を判定する（先に出現した行が残る）

重複が複数見つかった場合にどちらを残すかは ``keep`` 引数（既定は ``"first"``）で指定できます。
