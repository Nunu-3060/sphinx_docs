データの読み込みと書き出し
============================

実務では、ゼロから ``DataFrame`` を作るよりも、既存のファイルからデータを読み込むことがほとんどです。

CSV ファイル
--------------

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.read_csv("data.csv")

   df.to_csv("output.csv", index=False)
   # index=False を指定すると、行インデックスを列として書き出さない

``read_csv`` にはエンコーディングや区切り文字を指定するオプションもあります。

.. code-block:: python

   df: pd.DataFrame = pd.read_csv("data.csv", encoding="utf-8", sep=",")

Windows の Excel で保存した日本語を含む CSV ファイルは、Shift_JIS 系の文字コードになっていることがあります。その場合は ``encoding="cp932"`` を指定すると、文字化けせずに読み込めます。

Excel ファイル
----------------

Excel ファイルの読み書きには、``openpyxl`` パッケージが別途必要です。

.. code-block:: console

   > py -m pip install openpyxl

.. code-block:: python

   df: pd.DataFrame = pd.read_excel("data.xlsx", sheet_name="Sheet1")

   df.to_excel("output.xlsx", sheet_name="Sheet1", index=False)

.. note::

   このほかにも ``read_json`` や ``read_sql`` など、さまざまな形式に対応した読み込み関数が用意されています。用途に応じて公式ドキュメントを参照してください。
