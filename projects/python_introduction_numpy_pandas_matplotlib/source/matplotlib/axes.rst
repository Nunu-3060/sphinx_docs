軸の設定
==========

目盛りの調整
--------------

x 軸の目盛りの位置や表示ラベルを自分で指定したい場合は、``set_xticks()`` と ``set_xticklabels()`` を組み合わせて使います。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   x: np.ndarray = np.arange(4)
   sales: list[int] = [120, 150, 90, 200]

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.bar(x, sales)
   ax.set_xticks(x)
   ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"])

- ``set_xticks()``: 目盛りを表示する位置（x 座標）を指定します。
- ``set_xticklabels()``: ``set_xticks()`` で指定した位置に表示するラベルの文字列を指定します。位置とラベルの数は一致させる必要があります。

ラベルが長くて重なってしまう場合は、``rotation`` 引数でラベルを回転させると見やすくなります。

.. code-block:: python

   ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"], rotation=45)

.. note::

   ``bar()`` に文字列の list（例: ``ax.bar(["Tokyo", "Osaka"], [10, 20])``）を直接渡す場合は、目盛りラベルは自動的に設定されるため、``set_xticks()`` / ``set_xticklabels()`` は不要です。数値の x 座標に対して独自のラベルを割り当てたい場合に、これらのメソッドを使います。

表示範囲の指定
----------------

軸の表示範囲は、既定ではデータに合わせて自動的に決まりますが、``set_xlim()`` / ``set_ylim()`` を使うと明示的に指定できます。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   x: np.ndarray = np.linspace(0, 2 * np.pi, 100)
   y: np.ndarray = np.sin(x)

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.plot(x, y)
   ax.set_xlim(0, np.pi)
   ax.set_ylim(-1.2, 1.2)

グラフの一部分を拡大して確認したい場合や、複数のグラフを並べて比較する際に軸の範囲を揃えたい場合によく使います。``ax.hist()`` の ``range`` 引数で階級の範囲を揃えるのと同様に、軸の見た目を統一することで比較しやすいグラフになります。

対数スケール
--------------

指数的に増加するデータのように、値の桁が大きく変化するデータをそのまま線形スケール（既定）でプロットすると、値が小さい部分がグラフ上でつぶれて見えなくなってしまうことがあります。このような場合は ``set_yscale()`` / ``set_xscale()`` で軸を対数スケールに変更すると、桁の異なるデータでも変化の様子を見やすく表示できます。

.. plot::
   :include-source:

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   x: np.ndarray = np.arange(1, 11)
   y: np.ndarray = 2.0**x  # 指数的に増加するデータ

   fig: Figure
   axes: np.ndarray
   fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9, 3.5))

   axes[0].plot(x, y, marker="o")
   axes[0].set_title("linear scale")

   axes[1].plot(x, y, marker="o")
   axes[1].set_yscale("log")
   axes[1].set_title("log scale")

   fig.tight_layout()

左側の線形スケールでは、x が大きくなるほど値の変化がグラフの上端に偏ってしまいますが、右側のように y 軸を対数スケールにすると、桁が変わっても変化の傾向を等しく比較できます。``set_yscale()`` / ``set_xscale()`` には、既定の ``"linear"`` のほか ``"log"`` を指定できます。
