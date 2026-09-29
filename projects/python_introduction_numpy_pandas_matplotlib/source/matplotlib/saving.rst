グラフの保存
============

作成したグラフをファイルとして保存するには、``fig.savefig()`` を使います。

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   x: np.ndarray = np.linspace(0, 2 * np.pi, 100)

   fig: Figure
   ax: Axes
   fig, ax = plt.subplots()
   ax.plot(x, np.sin(x))

   fig.savefig("sin_curve.png")

拡張子から出力形式（PNG、PDF、SVG など）が自動的に判別されます。

.. code-block:: python

   fig.savefig("sin_curve.pdf")
   fig.savefig("sin_curve.svg")

解像度の指定
--------------

``dpi``\ （1 インチあたりのドット数）を指定すると、画質を調整できます。資料に貼り付ける画像は、``dpi`` を高めに設定するときれいに表示されます。

.. code-block:: python

   fig.savefig("sin_curve.png", dpi=200)

余白の調整
------------

保存時にグラフの周囲の余白が気になる場合は、``bbox_inches="tight"`` を指定すると余分な余白を自動的に切り詰められます。

.. code-block:: python

   fig.savefig("sin_curve.png", dpi=200, bbox_inches="tight")

.. note::

   ``plt.show()`` でグラフを表示した後は、``Figure`` の内容が破棄される環境があります。表示と保存の両方を行いたい場合は、``fig.savefig()`` を ``plt.show()`` より前に呼び出してください。

グラフを閉じる（メモリの解放）
------------------------------

``for`` ループで大量のグラフを作成して保存するような場合、``fig.savefig()`` を呼び出した後も ``Figure`` はメモリ上に残り続けます。件数が多いとメモリ使用量が増え続けてしまうため、保存が終わった ``Figure`` は ``plt.close()`` で明示的に閉じておくと安全です。

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   from matplotlib.axes import Axes
   from matplotlib.figure import Figure

   for i in range(3):
       x: np.ndarray = np.linspace(0, 2 * np.pi, 100)

       fig: Figure
       ax: Axes
       fig, ax = plt.subplots()
       ax.plot(x, np.sin(x + i))
       fig.savefig(f"sin_curve_{i}.png")

       plt.close(fig)
       # 保存済みの Figure をメモリから解放する

``plt.close(fig)`` のように ``Figure`` を指定すると、そのグラフだけを閉じます。引数を省略した ``plt.close()`` は現在の ``Figure`` を、``plt.close("all")`` はすべての ``Figure`` を閉じます。

.. note::

   ``plt.show()`` で画面表示だけを行うような対話的な用途では、グラフの数も少なく問題になりにくいため、``plt.close()`` を意識する必要はあまりありません。「:doc:`../practice/index`」の章のように大量のデータから多数のグラフを自動生成・保存するスクリプトを書く場合に、特に効果を発揮します。
