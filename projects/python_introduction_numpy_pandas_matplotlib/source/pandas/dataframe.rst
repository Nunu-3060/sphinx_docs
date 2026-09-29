DataFrame の基本
=================

``DataFrame`` は、複数の列（``Series``）から構成される表形式のデータです。

DataFrame の作成
------------------

辞書（列名 → 値の list）から作成するのが最も一般的です。

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, 25, 35],
       "city": ["Tokyo", "Osaka", "Nagoya"],
   })
   print(df)
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 1    Bob   25   Osaka
   # 2  Carol   35  Nagoya

基本的な属性
--------------

.. code-block:: python

   df.shape
   # (3, 3)  行数と列数

   df.columns
   # Index(['name', 'age', 'city'], dtype='str')

   df.index
   # RangeIndex(start=0, stop=3, step=1)

   df.dtypes
   # name      str
   # age     int64
   # city      str
   # dtype: object

列の追加・削除・リネーム
--------------------------

既存の列を使った計算結果を新しい列として追加するには、``[]`` に新しい列名を指定して代入します。

.. code-block:: python

   df["is_adult"] = df["age"] >= 30
   print(df)
   #     name  age    city  is_adult
   # 0  Alice   30   Tokyo      True
   # 1    Bob   25   Osaka     False
   # 2  Carol   35  Nagoya      True

列を削除するには ``drop`` を使い、``columns`` 引数に削除したい列名（または列名の list）を指定します。

.. code-block:: python

   df2: pd.DataFrame = df.drop(columns=["is_adult"])
   print(df2)
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 1    Bob   25   Osaka
   # 2  Carol   35  Nagoya

列名を変更するには ``rename`` を使い、``columns`` 引数に「元の列名 → 新しい列名」の辞書を指定します。

.. code-block:: python

   df3: pd.DataFrame = df2.rename(columns={"name": "full_name"})
   print(df3)
   #   full_name  age    city
   # 0     Alice   30   Tokyo
   # 1       Bob   25   Osaka
   # 2     Carol   35  Nagoya

.. note::

   ``drop`` や ``rename`` は、既定では元の ``DataFrame`` を変更せず、結果を新しい ``DataFrame`` として返します。元のデータを直接書き換えたい場合は、戻り値を変数に代入し直すか、``inplace=True`` を指定します。

型変換（astype）
------------------

CSV から読み込んだデータで数値のはずの列が文字列型になっている場合など、列の型を変換したいことがあります。そのような場合は ``astype`` を使います。

.. code-block:: python

   df["age"] = df["age"].astype(float)
   df.dtypes
   # name        str
   # age     float64
   # city        str
   # dtype: object

``astype`` には ``float`` や ``int`` のような Python の組み込み型のほか、``"float64"`` のような dtype を表す文字列も指定できます。

カテゴリ型（category dtype）
--------------------------------

列に含まれる値の種類が少なく、同じ値が繰り返し登場する場合（都市名や商品カテゴリなど）は、``astype("category")`` でカテゴリ型に変換すると、メモリ使用量を大きく削減できます。

.. code-block:: python

   df["city"] = df["city"].astype("category")
   df["city"].dtype
   # category

   df["city"].cat.categories
   # Index(['Nagoya', 'Osaka', 'Tokyo'], dtype='str')

内部的には、値そのものではなく整数のコードとカテゴリの対応表として保持されるため、行数が多く同じ値が繰り返されるデータほど効果が大きくなります。

.. code-block:: python

   # 1 万行のうち、値の種類が 5 種類だけの場合の比較（memory_usage(deep=True)）
   # str 型      : 550129 バイト
   # category 型 :  10407 バイト

``pd.Categorical`` を使うと、``ordered=True`` を指定して順序を持つカテゴリ（「小 < 中 < 大」のような大小関係のある区分）を作ることもできます。順序付きカテゴリでは、比較演算子（``<`` など）による比較も可能です。

.. code-block:: python

   sizes: pd.Categorical = pd.Categorical(
       ["S", "M", "L"], categories=["S", "M", "L"], ordered=True
   )

   pd.Series(sizes) < "L"
   # 0     True
   # 1     True
   # 2    False
   # dtype: bool

データの概要を確認する
------------------------

データの中身をざっと確認するために、よく使われるメソッドです。

.. code-block:: python

   df.head(2)
   # 先頭 2 行を表示

   df.tail(2)
   # 末尾 2 行を表示

   df.info()
   # 列ごとのデータ型・欠損値の有無などを表示

   df.describe()
   # 数値列の統計量（平均・標準偏差・最小値など）を表示
