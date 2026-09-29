Series の基本
==============

``Series`` は、ラベル（インデックス）付きの 1 次元データです。

Series の作成
----------------

.. code-block:: python

   import pandas as pd

   s: pd.Series = pd.Series([10, 20, 30])
   print(s)
   # 0    10
   # 1    20
   # 2    30
   # dtype: int64

インデックスを指定しない場合は 0 始まりの連番が自動的に振られます。明示的にラベルを指定することもできます。

.. code-block:: python

   s: pd.Series = pd.Series([10, 20, 30], index=["a", "b", "c"])
   print(s)
   # a    10
   # b    20
   # c    30
   # dtype: int64

要素へのアクセス
------------------

ラベルまたは位置のどちらでもアクセスできます。

.. code-block:: python

   s["b"]
   # 20

   s.iloc[1]
   # 20（位置指定）

基本的な演算
--------------

``Series`` は ``ndarray`` をベースにしているため、numpy と同様に要素ごとの演算や集約関数が利用できます。

.. code-block:: python

   s * 2
   # a    20
   # b    40
   # c    60
   # dtype: int64

   s.sum()
   # 60

   s.mean()
   # 20.0

items（ラベルと値の反復）
--------------------------

``items()`` を使うと、``(ラベル, 値)`` のペアを 1 つずつ取り出せます。

.. code-block:: python

   s: pd.Series = pd.Series([10, 20, 30], index=["a", "b", "c"])

   for label, value in s.items():
       print(label, value)
   # a 10
   # b 20
   # c 30

.. note::

   ``items()`` は Python 標準の辞書の ``items()`` と同じ感覚で使えますが、``Series`` 全体に対する演算（``s * 2`` など）で済む場合はそちらの方が高速です。``DataFrame`` の行・列に対する反復処理（``iterrows()`` / ``itertuples()`` など）については「:doc:`iteration`」を参照してください。

文字列を扱う（str アクセサ）
------------------------------

文字列を要素に持つ ``Series`` には、``.str`` を経由して文字列操作用のメソッドを呼び出せる専用のアクセサが用意されています。Python 標準の文字列メソッドと同じ名前のものが多く、各要素に対して一括で適用されます。

.. code-block:: python

   cities: pd.Series = pd.Series(["Tokyo", "Osaka", "Nagoya"])

   cities.str.contains("o")
   # 0     True
   # 1    False
   # 2     True
   # dtype: bool

   cities.str.lower()
   # 0     tokyo
   # 1     osaka
   # 2    nagoya
   # dtype: str

``str.split`` を使うと、区切り文字で文字列を分割できます。``expand=True`` を指定すると、分割結果を複数の列を持つ ``DataFrame`` として展開できます。

.. code-block:: python

   full_names: pd.Series = pd.Series(["Alice Smith", "Bob Jones", "Carol Lee"])

   full_names.str.split(" ")
   # 0    [Alice, Smith]
   # 1      [Bob, Jones]
   # 2      [Carol, Lee]
   # dtype: object

   full_names.str.split(" ", expand=True)
   #        0      1
   # 0  Alice  Smith
   # 1    Bob  Jones
   # 2  Carol    Lee

.. note::

   ``str.contains`` は、「:doc:`filtering`」で紹介するブール条件による抽出の条件としてもよく使われます。日付・時刻データに対する同様のアクセサとして ``.dt`` もあり、こちらは「:doc:`datetime`」で紹介します。
