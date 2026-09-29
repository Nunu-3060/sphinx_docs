代表的なグラフの種類
======================

折れ線グラフ以外にも、目的に応じてさまざまな種類のグラフを描画できます。

散布図
--------

2 つの変数の関係を見るには散布図 ``scatter`` を使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   rng: np.random.Generator = np.random.default_rng(seed=0)
   x: np.ndarray = rng.random(50)
   y: np.ndarray = rng.random(50)

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.scatter(x, y)

散布図に相関係数や回帰直線を組み合わせて 2 つの変数の関係を調べる例は、「:doc:`../practice/correlation`」で紹介します。

棒グラフ
----------

カテゴリごとの値を比較するには棒グラフ ``bar`` を使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   categories: list[str] = ["Tokyo", "Osaka", "Nagoya"]
   values: list[int] = [450, 300, 200]

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.bar(categories, values)

ヒストグラム
--------------

データの分布を確認するにはヒストグラム ``hist`` を使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   rng: np.random.Generator = np.random.default_rng(seed=0)
   data: np.ndarray = rng.normal(loc=50, scale=10, size=1000)

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.hist(data, bins=30)

``bins`` で階級（棒）の数を指定します。データの分布に応じて調整してください。

``range`` 引数を指定すると、ヒストグラムの階級の範囲（最小値・最大値）を明示的に指定できます。指定しない場合は、データの最小値から最大値までが自動的に範囲として使われます。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   rng: np.random.Generator = np.random.default_rng(seed=0)
   data: np.ndarray = rng.normal(loc=50, scale=10, size=1000)

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.hist(data, bins=30, range=(20, 80))

``range=(20, 80)`` のように最小値と最大値をタプルで指定すると、外れ値の影響を受けずに階級の範囲を固定できます。複数のグラフを並べて表示範囲を揃えたい場合にも便利です。

円グラフ
----------

全体に対する各要素の割合を示すには円グラフ ``pie`` を使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   labels: list[str] = ["Tokyo", "Osaka", "Nagoya"]
   sizes: list[int] = [450, 300, 200]

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.pie(sizes, labels=labels, autopct="%1.1f%%")

``autopct`` 引数に書式文字列を指定すると、各要素の割合をパーセント表示できます。

箱ひげ図
----------

複数のグループのデータ分布（最小値・最大値・四分位数など）を比較するには箱ひげ図 ``boxplot`` を使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   rng: np.random.Generator = np.random.default_rng(seed=0)
   data: list[np.ndarray] = [rng.normal(size=100), rng.normal(loc=1, size=100)]

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.boxplot(data, tick_labels=["A", "B"])

箱の中央の線が中央値、箱の上下端がそれぞれ第 3 四分位数・第 1 四分位数、ひげの端が、箱の端から箱の長さの 1.5 倍以内にあるデータの最小値・最大値を表します。その範囲の外にあるデータは、外れ値として点で表示されます。グループ間でデータの散らばり方を比較する際に便利です。

matplotlib には、ここで紹介した散布図・棒グラフ・ヒストグラム・円グラフ・箱ひげ図以外にも、ヒートマップ（``imshow``）など、非常に多くの種類のグラフが用意されています。どのようなグラフを描けるかは、公式サイトの `Examples <https://matplotlib.org/stable/gallery/index.html>`_\ （サンプルギャラリー）で確認できます。
