matplotlib とは
================

matplotlib は、Python でグラフや図を描画するためのライブラリです。numpy の配列や pandas の ``DataFrame`` / ``Series`` をそのまま渡して、折れ線グラフ、散布図、棒グラフなどさまざまな図を作成できます。

公式サイト: `matplotlib <https://matplotlib.org/>`_

Figure と Axes
----------------

matplotlib では、図全体を ``Figure``、その中に配置される個々のグラフ領域を ``Axes`` と呼びます。1 つの ``Figure`` に複数の ``Axes`` を配置することもできます。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   fig: Figure  # 図全体
   ax: Axes  # グラフを描画する領域
   fig, ax = plt.subplots()

このドキュメントでは、``fig, ax = plt.subplots()`` で ``Figure`` と ``Axes`` を作成し、``ax`` に対してメソッドを呼び出してグラフを描画する書き方で統一します。この書き方はグラフが 1 つの場合でも複数の場合でも共通して使えます。
