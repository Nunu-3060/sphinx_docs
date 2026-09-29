条件によるフィルタリング
==========================

ブール条件による抽出
-----------------------

条件式は、行ごとに真偽値を持つ ``Series`` を返します。これを ``DataFrame`` の ``[]`` に渡すことで、条件に合う行だけを抽出できます。

.. code-block:: python

   import pandas as pd

   df: pd.DataFrame = pd.DataFrame({
       "name": ["Alice", "Bob", "Carol"],
       "age": [30, 25, 35],
       "city": ["Tokyo", "Osaka", "Nagoya"],
   })

   df["age"] > 28
   # 0     True
   # 1    False
   # 2     True
   # Name: age, dtype: bool

   df[df["age"] > 28]
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 2  Carol   35  Nagoya

複数条件の組み合わせ
----------------------

複数の条件を組み合わせる場合は、Python の ``and`` / ``or`` ではなく ``&`` / ``|`` を使い、各条件を丸かっこで囲みます。

.. code-block:: python

   df[(df["age"] > 28) & (df["city"] == "Tokyo")]
   #     name  age   city
   # 0  Alice   30  Tokyo

~（否定）による条件の反転
----------------------------

条件を反転させたい場合は、Python の ``not`` ではなく ``~`` を使います。``&`` / ``|`` と同様、反転させたい条件は丸かっこで囲みます。

.. code-block:: python

   df[~(df["age"] < 30)]
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 2  Carol   35  Nagoya

``~(df["age"] < 30)`` は「``age`` が 30 未満ではない」、つまり「``age`` が 30 以上」という条件になります。

isin による複数値の一致判定
------------------------------

「複数の値のいずれかに一致する行」を抽出したい場合、``|`` で条件を並べる代わりに ``isin`` を使うと簡潔に書けます。

.. code-block:: python

   df[df["city"].isin(["Tokyo", "Nagoya"])]
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 2  Carol   35  Nagoya

上の例は ``df[(df["city"] == "Tokyo") | (df["city"] == "Nagoya")]`` と同じ結果になりますが、候補が増えるほど ``isin`` の方が読みやすくなります。

文字列条件によるフィルタリング（str.contains）
--------------------------------------------------

文字列の列に対しては、``.str`` アクセサ（「:doc:`series`」参照）の ``contains`` を条件として使うこともよくあります。

.. code-block:: python

   df[df["city"].str.contains("o")]
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 2  Carol   35  Nagoya

「都市名に "o" を含む行」のように、部分一致で行を絞り込みたい場合に便利です。``isin`` が値の完全一致による絞り込みであるのに対し、``str.contains`` は部分一致による絞り込みという違いがあります。

query による抽出
-------------------

``query`` メソッドを使うと、条件を文字列として記述できます。列名をそのまま変数のように書けるため、``&`` や ``()`` が減り、条件が読みやすくなる場合があります。

.. code-block:: python

   df.query("age > 28")
   #     name  age    city
   # 0  Alice   30   Tokyo
   # 2  Carol   35  Nagoya

   df.query("age > 28 and city == 'Tokyo'")
   #     name  age   city
   # 0  Alice   30  Tokyo

Python の変数を条件に使いたい場合は、変数名の前に ``@`` を付けます。

.. code-block:: python

   min_age: int = 28
   df.query("age > @min_age")

.. note::

   ``[]`` を使った書き方と ``query`` はどちらも同じ結果が得られます。条件がシンプルなら ``[]``、条件が複雑になってきたら ``query`` を使うとコードが読みやすくなることが多いです。好みや状況に応じて使い分けてください。
