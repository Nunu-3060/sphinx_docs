.. _appendix-a:

付録 A 双曲線関数
=================

本書で使う双曲線関数の定義と公式をまとめる。

定義
----

双曲線関数は、指数関数を使って次のように定義する。

.. math::

   \cosh x = \frac{e^x + e^{-x}}{2}, \qquad \sinh x = \frac{e^x - e^{-x}}{2}, \qquad \tanh x = \frac{\sinh x}{\cosh x} = \frac{e^x - e^{-x}}{e^x + e^{-x}}

それぞれハイパボリックコサイン、ハイパボリックサイン、ハイパボリックタンジェントと読む。:math:`\cosh x \ge 1`、:math:`-1 < \tanh x < 1` である。

三角関数の :math:`(\cos t, \sin t)` が単位円 :math:`x^2 + y^2 = 1` の上の点を表すのと同じく、:math:`(\cosh t, \sinh t)` は双曲線 :math:`x^2 - y^2 = 1` の右側の枝の上の点を表す。「双曲線関数」の名はこれに由来する。双曲面モデル（\ :ref:`第 3 章 <ch03>`\ ）の点を :math:`(\cosh t, \sinh t \cos\theta, \sinh t \sin\theta)` と表せるのも、この性質による。

基本的な公式
------------

.. list-table:: 双曲線関数の公式
   :header-rows: 1
   :widths: 40 60

   * - 公式
     - 備考
   * - :math:`\cosh^2 x - \sinh^2 x = 1`
     - 三角関数の :math:`\cos^2 x + \sin^2 x = 1` に対応する。
   * - :math:`(\cosh x)' = \sinh x`、:math:`(\sinh x)' = \cosh x`
     - 三角関数と異なり、符号が変わらない。
   * - :math:`\cosh(x + y) = \cosh x \cosh y + \sinh x \sinh y`
     - 加法定理
   * - :math:`\sinh(x + y) = \sinh x \cosh y + \cosh x \sinh y`
     - 加法定理
   * - :math:`\tanh(x + y) = \dfrac{\tanh x + \tanh y}{1 + \tanh x \tanh y}`
     - 相対論的な速度の合成（\ :ref:`第 9 章 <ch09>`\ ）
   * - :math:`\cosh 2x = 1 + 2 \sinh^2 x`、:math:`\sinh 2x = 2 \sinh x \cosh x`
     - 倍角の公式
   * - :math:`\cosh x = \dfrac{1 + t^2}{1 - t^2}`、:math:`\sinh x = \dfrac{2t}{1 - t^2}` （:math:`t = \tanh(x/2)`）
     - 円板モデルの計算（\ :ref:`第 4 章 <ch04>`\ 、\ :ref:`第 7 章 <ch07>`\ ）で使う。
   * - :math:`\cosh x = \cos(ix)`、:math:`\sinh x = -i \sin(ix)`
     - 球面と双曲平面の公式の対応（\ :ref:`第 2 章 <ch02>`\ ）

逆関数
------

:math:`\cosh`、:math:`\sinh`、:math:`\tanh` の逆関数を :math:`\arcosh`、:math:`\arsinh`、:math:`\artanh` と書く（:math:`\cosh^{-1}` などとも書く）。対数で表すと次のようになる。

.. math::

   \arcosh x = \ln \left( x + \sqrt{x^2 - 1} \right) \ (x \ge 1), \qquad
   \arsinh x = \ln \left( x + \sqrt{x^2 + 1} \right), \qquad
   \artanh x = \frac{1}{2} \ln \frac{1 + x}{1 - x} \ (|x| < 1)

:math:`\arcosh` は :math:`x \ge 1` で定義され、値が 0 以上のものをとる。Python では ``math.acosh()``、``math.asinh()``、``math.atanh()``、NumPy では ``np.arccosh()``、``np.arcsinh()``、``np.arctanh()`` で計算できる。

円板モデルの距離の公式で、:math:`\cosh` を使う形と :math:`\artanh` を使う形が同じ値になることは、上の表の :math:`\cosh x = (1 + t^2) / (1 - t^2)` （:math:`t = \tanh(x/2)`）から確かめられる。

近似式
------

.. list-table:: 双曲線関数の近似
   :header-rows: 1
   :widths: 50 50

   * - :math:`x` が小さいとき
     - :math:`x` が大きいとき
   * - :math:`\cosh x \approx 1 + x^2/2`
     - :math:`\cosh x \approx e^x / 2`
   * - :math:`\sinh x \approx x`
     - :math:`\sinh x \approx e^x / 2`
   * - :math:`\tanh x \approx x`
     - :math:`\tanh x \approx 1 - 2e^{-2x}`

小さな :math:`x` の近似は、双曲平面の公式が小さな図形でユークリッドの公式に近づくこと（\ :ref:`第 6 章 <ch06>`\ ）の説明に使う。大きな :math:`x` の近似は、双曲平面の指数的な広がり（\ :ref:`第 7 章 <ch07>`\ ）の説明に使う。
