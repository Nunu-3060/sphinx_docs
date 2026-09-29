pandas とは
===========

pandas は、表形式のデータを扱うための Python ライブラリです。CSV や Excel のようなデータを読み込み、集計・加工・分析するための機能が豊富に用意されています。

公式サイト: `pandas <https://pandas.pydata.org/>`_

主なデータ構造
----------------

pandas には、主に 2 つのデータ構造があります。

- ``Series``: ラベル（インデックス）付きの 1 次元配列
- ``DataFrame``: 複数の ``Series`` を列として持つ、表形式の 2 次元データ

.. code-block:: python

   import pandas as pd

   s: pd.Series = pd.Series([10, 20, 30])
   print(s)
   # 0    10
   # 1    20
   # 2    30
   # dtype: int64

   df: pd.DataFrame = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})
   print(df)
   #     name  age
   # 0  Alice   30
   # 1    Bob   25

numpy との関係
----------------

``DataFrame`` や ``Series`` の内部データは numpy の ``ndarray`` で保持されています。そのため、numpy で学んだ配列操作や集約関数の考え方の多くがそのまま活かせます。

.. code-block:: python

   df["age"].to_numpy()
   # array([30, 25])

次のページから、``Series`` と ``DataFrame`` の基本的な使い方を見ていきます。
