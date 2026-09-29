グラフの装飾
==============

タイトルと軸ラベル
--------------------

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
   ax.set_title("sin curve")
   ax.set_xlabel("x")
   ax.set_ylabel("sin(x)")

凡例
------

``label`` 引数と ``legend()`` を組み合わせることで、グラフに凡例を表示できます。

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
   ax.plot(x, y, label="sin")
   ax.legend()

``loc`` 引数を指定すると、凡例を表示する位置を指定できます。指定しない場合は ``"best"``\ （グラフと重なりにくい位置を自動で選ぶ）になります。

.. code-block:: python

   ax.legend(loc="upper left")

``loc`` には ``"upper right"``、``"lower left"``、``"center"`` のように、上下（upper/lower/center）と左右（left/right/center）を組み合わせた文字列を指定します。

複数の系列を重ねて描画する場合の凡例の詳しい扱い方（``twinx()`` を使う場合の凡例の結合など）については、「:doc:`multiple_series`」で説明します。

グリッド
----------

``grid()`` を呼び出すと、背景にグリッド線を表示できます。

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
   ax.grid(True)

注釈（annotate）
------------------

``annotate()`` を使うと、グラフ上の特定の点に矢印付きのテキストで注釈を付けることができます。

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
   ax.annotate(
       "peak",
       xy=(np.pi / 2, 1.0),
       xytext=(np.pi, 0.5),
       arrowprops={"arrowstyle": "->"},
   )

``xy`` 引数で注釈を付けたい点の座標、``xytext`` 引数でテキストを表示する座標を指定します。``arrowprops`` に矢印の見た目を指定すると、``xytext`` から ``xy`` へ矢印が描画されます。
