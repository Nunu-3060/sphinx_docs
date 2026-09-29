日付・時刻データの扱い
========================

実務のデータには日付・時刻の列がよく登場します。pandas には日付・時刻を専用に扱うための仕組みが用意されています。

pd.to_datetime による変換
----------------------------

CSV などから読み込んだ日付は、多くの場合ただの文字列になっています。``pd.to_datetime`` を使うと、日付・時刻専用の型（``datetime64``）に変換できます。

.. code-block:: python

   import pandas as pd

   dates: pd.DatetimeIndex = pd.to_datetime(
       ["2024-01-05", "2024-02-10", "2024-03-01"]
   )
   print(dates)
   # DatetimeIndex(['2024-01-05', '2024-02-10', '2024-03-01'],
   #               dtype='datetime64[us]', freq=None)

上の例のように list を渡した場合は、日付の並びを表す ``DatetimeIndex`` が返されます。``DataFrame`` の列を作る場合も同様に変換できます。

.. code-block:: python

   df: pd.DataFrame = pd.DataFrame({
       "date": pd.to_datetime(["2024-01-05", "2024-02-10", "2024-03-01"]),
       "sales": [1200, 1500, 900],
   })
   df.dtypes
   # date     datetime64[us]
   # sales             int64
   # dtype: object

dt アクセサ
-------------

日付・時刻型の列には、``.dt`` を経由して年・月・日などの情報を取り出す専用のアクセサが用意されています。

.. code-block:: python

   df["date"].dt.year
   # 0    2024
   # 1    2024
   # 2    2024
   # Name: date, dtype: int32

   df["date"].dt.month
   # 0    1
   # 1    2
   # 2    3
   # Name: date, dtype: int32

   df["date"].dt.to_period("M").astype(str)
   # 0    2024-01
   # 1    2024-02
   # 2    2024-03
   # Name: date, dtype: str
   # to_period("M") で日付を「年月」の単位に変換する

「年月ごとの合計」のように月単位で集計したい場合は、``dt.to_period("M")`` で年月の列を作ってから ``groupby`` するのが定番のパターンです。

.. note::

   ``to_period("M")`` の ``"M"`` は「月」を表す期間エイリアスです。これは次に紹介する ``pd.date_range`` や ``resample`` で頻度を指定する際に使う頻度エイリアスとは別物で、そちらでは月末を表すのに ``"ME"`` を使います（pandas 3.0 以降では、頻度として ``"M"`` を指定するとエラーになります）。どちらも「月」を意味しますが、用途に応じて別のエイリアスが使われる点に注意してください。

pd.date_range による日付の生成
---------------------------------

サンプルデータの作成などで、連続した日付を生成したい場合は ``pd.date_range`` が便利です。

.. code-block:: python

   dates: pd.DatetimeIndex = pd.date_range("2024-01-01", periods=5, freq="D")
   print(dates)
   # DatetimeIndex(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04',
   #                '2024-01-05'],
   #               dtype='datetime64[us]', freq='D')

``freq="D"`` は 1 日ごと、``freq="ME"`` は月末ごとのように、間隔を指定できます。

Timedelta（日付・時刻の差分）
--------------------------------

日付や時刻同士を引き算すると、その差分を表す ``Timedelta`` が得られます。

.. code-block:: python

   pd.Timestamp("2024-01-10") - pd.Timestamp("2024-01-01")
   # Timedelta('9 days 00:00:00')

``.days`` を使うと、日数部分だけを整数として取り出せます。

.. code-block:: python

   delta: pd.Timedelta = pd.Timestamp("2024-01-10") - pd.Timestamp("2024-01-01")
   delta.days
   # 9

``DataFrame`` の日付の列に対して引き算を行えば、行ごとの経過日数を一度に計算できます。列（``Series``）から日数を取り出す場合は、``.dt`` アクセサを経由して ``.dt.days`` と書きます。

.. code-block:: python

   (df["date"] - pd.Timestamp("2024-01-01")).dt.days
   # 0     4
   # 1    40
   # 2    60
   # Name: date, dtype: int64

日付をインデックスに設定する
------------------------------

日付の列を ``set_index`` でインデックスに設定すると、時系列データとして扱いやすくなります。

.. code-block:: python

   df2: pd.DataFrame = df.set_index("date")
   print(df2)
   #             sales
   # date
   # 2024-01-05   1200
   # 2024-02-10   1500
   # 2024-03-01    900

移動平均（rolling）
----------------------

日付をインデックスにした時系列データでは、``rolling`` を使って移動平均（直近 N 件の平均）を計算できます。

.. code-block:: python

   df2["sales"].rolling(2).mean()
   # date
   # 2024-01-05       NaN
   # 2024-02-10    1350.0
   # 2024-03-01    1200.0
   # Name: sales, dtype: float64
   # rolling(2) は自分を含む直近 2 件の平均を計算する
   # 先頭 1 件は直近 2 件分のデータが揃わないため NaN になる

日々の値のばらつきが大きいデータでも、移動平均を合わせて見ることで大まかな傾向をつかみやすくなります。
