.. _appendix-a:

付録 A 公式集
=============

本書で扱った公式と、関連する公式をまとめる。記号は\ :ref:`第 1 章 <ch01>`\ の記法に従う。:math:`f`, :math:`g` はスカラー場、:math:`\bm{F}`, :math:`\bm{G}` はベクトル場で、いずれも必要なだけ滑らかであるとする。

ベクトルの代数
--------------

.. list-table:: ベクトルの演算
   :header-rows: 1
   :widths: 30 70

   * - 名前
     - 公式
   * - 内積
     - :math:`\bm{a} \cdot \bm{b} = a_x b_x + a_y b_y + a_z b_z = |\bm{a}| |\bm{b}| \cos\theta`
   * - 外積
     - :math:`\bm{a} \times \bm{b} = (a_y b_z - a_z b_y, \ a_z b_x - a_x b_z, \ a_x b_y - a_y b_x)`
   * - スカラー三重積
     - :math:`\bm{a} \cdot (\bm{b} \times \bm{c}) = \bm{b} \cdot (\bm{c} \times \bm{a}) = \bm{c} \cdot (\bm{a} \times \bm{b})`
   * - ベクトル三重積
     - :math:`\bm{a} \times (\bm{b} \times \bm{c}) = \bm{b} (\bm{a} \cdot \bm{c}) - \bm{c} (\bm{a} \cdot \bm{b})`
   * - ラグランジュの恒等式
     - :math:`(\bm{a} \times \bm{b}) \cdot (\bm{c} \times \bm{d}) = (\bm{a} \cdot \bm{c})(\bm{b} \cdot \bm{d}) - (\bm{a} \cdot \bm{d})(\bm{b} \cdot \bm{c})`

勾配・発散・回転・ラプラシアン（直交座標）
------------------------------------------

.. math::

   \nabla f &= \frac{\partial f}{\partial x} \bm{e}_x + \frac{\partial f}{\partial y} \bm{e}_y + \frac{\partial f}{\partial z} \bm{e}_z \\
   \nabla \cdot \bm{F} &= \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z} \\
   \nabla \times \bm{F} &= \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) \bm{e}_x + \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) \bm{e}_y + \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) \bm{e}_z \\
   \nabla^2 f &= \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}

方向微分（:math:`\bm{u}` は単位ベクトル）は :math:`D_{\bm{u}} f = \nabla f \cdot \bm{u}` である。

ナブラを含む公式
----------------

積の微分公式
~~~~~~~~~~~~

.. math::

   \nabla (fg) &= f \nabla g + g \nabla f \\
   \nabla \cdot (f \bm{F}) &= f \, \nabla \cdot \bm{F} + \bm{F} \cdot \nabla f \\
   \nabla \times (f \bm{F}) &= f \, \nabla \times \bm{F} + \nabla f \times \bm{F} \\
   \nabla \cdot (\bm{F} \times \bm{G}) &= \bm{G} \cdot (\nabla \times \bm{F}) - \bm{F} \cdot (\nabla \times \bm{G}) \\
   \nabla \times (\bm{F} \times \bm{G}) &= \bm{F} (\nabla \cdot \bm{G}) - \bm{G} (\nabla \cdot \bm{F}) + (\bm{G} \cdot \nabla) \bm{F} - (\bm{F} \cdot \nabla) \bm{G} \\
   \nabla (\bm{F} \cdot \bm{G}) &= (\bm{F} \cdot \nabla) \bm{G} + (\bm{G} \cdot \nabla) \bm{F} + \bm{F} \times (\nabla \times \bm{G}) + \bm{G} \times (\nabla \times \bm{F}) \\
   \nabla^2 (fg) &= f \nabla^2 g + 2 \nabla f \cdot \nabla g + g \nabla^2 f

ここで :math:`(\bm{F} \cdot \nabla)` は :math:`F_x \, \partial / \partial x + F_y \, \partial / \partial y + F_z \, \partial / \partial z` を表す演算子で、ベクトル場の各成分に作用する。

2 回の微分
~~~~~~~~~~

.. math::

   \nabla \times (\nabla f) &= \bm{0} \\
   \nabla \cdot (\nabla \times \bm{F}) &= 0 \\
   \nabla \cdot (\nabla f) &= \nabla^2 f \\
   \nabla \times (\nabla \times \bm{F}) &= \nabla (\nabla \cdot \bm{F}) - \nabla^2 \bm{F}

:math:`\nabla^2 \bm{F}` は、直交座標では各成分のラプラシアンを並べたベクトル :math:`(\nabla^2 F_x, \nabla^2 F_y, \nabla^2 F_z)` である。

位置ベクトルに関する公式
~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\bm{r} = (x, y, z)`、:math:`r = |\bm{r}|` とする。:math:`r` を含む式は原点を除いて成り立つ。

.. math::

   \nabla r &= \frac{\bm{r}}{r}, \qquad \nabla \cdot \bm{r} = 3, \qquad \nabla \times \bm{r} = \bm{0} \\
   \nabla \frac{1}{r} &= -\frac{\bm{r}}{r^3}, \qquad \nabla \cdot \frac{\bm{r}}{r^3} = 0, \qquad \nabla^2 \frac{1}{r} = 0

曲線座標系
----------

座標とスケール因子
~~~~~~~~~~~~~~~~~~

.. list-table:: 曲線座標系の定義と体積素
   :header-rows: 1
   :widths: 16 40 20 24

   * - 座標系
     - 直交座標との関係
     - スケール因子
     - 体積素（面素）
   * - 極座標 :math:`(r, \theta)`
     - :math:`x = r \cos\theta, \ y = r \sin\theta`
     - :math:`1, \ r`
     - :math:`dA = r \, dr \, d\theta`
   * - 円柱座標 :math:`(\rho, \phi, z)`
     - :math:`x = \rho \cos\phi, \ y = \rho \sin\phi, \ z = z`
     - :math:`1, \ \rho, \ 1`
     - :math:`dV = \rho \, d\rho \, d\phi \, dz`
   * - 球座標 :math:`(r, \theta, \phi)`
     - :math:`x = r \sin\theta \cos\phi, \ y = r \sin\theta \sin\phi, \ z = r \cos\theta`
     - :math:`1, \ r, \ r \sin\theta`
     - :math:`dV = r^2 \sin\theta \, dr \, d\theta \, d\phi`

半径 :math:`R` の球面の面素は :math:`dS = R^2 \sin\theta \, d\theta \, d\phi` である。

一般の直交曲線座標系
~~~~~~~~~~~~~~~~~~~~

座標 :math:`(u_1, u_2, u_3)`、スケール因子 :math:`h_1, h_2, h_3`、単位ベクトル :math:`\bm{e}_1, \bm{e}_2, \bm{e}_3`\ （右手系）とする。

.. math::

   \nabla f &= \frac{1}{h_1} \frac{\partial f}{\partial u_1} \bm{e}_1 + \frac{1}{h_2} \frac{\partial f}{\partial u_2} \bm{e}_2 + \frac{1}{h_3} \frac{\partial f}{\partial u_3} \bm{e}_3 \\
   \nabla \cdot \bm{F} &= \frac{1}{h_1 h_2 h_3} \left[ \frac{\partial (h_2 h_3 F_1)}{\partial u_1} + \frac{\partial (h_3 h_1 F_2)}{\partial u_2} + \frac{\partial (h_1 h_2 F_3)}{\partial u_3} \right] \\
   \nabla \times \bm{F} &= \frac{1}{h_1 h_2 h_3} \begin{vmatrix} h_1 \bm{e}_1 & h_2 \bm{e}_2 & h_3 \bm{e}_3 \\ \dfrac{\partial}{\partial u_1} & \dfrac{\partial}{\partial u_2} & \dfrac{\partial}{\partial u_3} \\ h_1 F_1 & h_2 F_2 & h_3 F_3 \end{vmatrix} \\
   \nabla^2 f &= \frac{1}{h_1 h_2 h_3} \left[ \frac{\partial}{\partial u_1} \left( \frac{h_2 h_3}{h_1} \frac{\partial f}{\partial u_1} \right) + \frac{\partial}{\partial u_2} \left( \frac{h_3 h_1}{h_2} \frac{\partial f}{\partial u_2} \right) + \frac{\partial}{\partial u_3} \left( \frac{h_1 h_2}{h_3} \frac{\partial f}{\partial u_3} \right) \right]

円柱座標
~~~~~~~~

.. math::

   \nabla f &= \frac{\partial f}{\partial \rho} \bm{e}_\rho + \frac{1}{\rho} \frac{\partial f}{\partial \phi} \bm{e}_\phi + \frac{\partial f}{\partial z} \bm{e}_z \\
   \nabla \cdot \bm{F} &= \frac{1}{\rho} \frac{\partial (\rho F_\rho)}{\partial \rho} + \frac{1}{\rho} \frac{\partial F_\phi}{\partial \phi} + \frac{\partial F_z}{\partial z} \\
   \nabla \times \bm{F} &= \left( \frac{1}{\rho} \frac{\partial F_z}{\partial \phi} - \frac{\partial F_\phi}{\partial z} \right) \bm{e}_\rho + \left( \frac{\partial F_\rho}{\partial z} - \frac{\partial F_z}{\partial \rho} \right) \bm{e}_\phi + \frac{1}{\rho} \left( \frac{\partial (\rho F_\phi)}{\partial \rho} - \frac{\partial F_\rho}{\partial \phi} \right) \bm{e}_z \\
   \nabla^2 f &= \frac{1}{\rho} \frac{\partial}{\partial \rho} \left( \rho \frac{\partial f}{\partial \rho} \right) + \frac{1}{\rho^2} \frac{\partial^2 f}{\partial \phi^2} + \frac{\partial^2 f}{\partial z^2}

2 次元の極座標 :math:`(r, \theta)` の公式は、円柱座標の公式で :math:`\rho` を :math:`r`、:math:`\phi` を :math:`\theta` に置き換え、:math:`z` を含む項を除いたものである。

球座標
~~~~~~

.. math::

   \nabla f &= \frac{\partial f}{\partial r} \bm{e}_r + \frac{1}{r} \frac{\partial f}{\partial \theta} \bm{e}_\theta + \frac{1}{r \sin\theta} \frac{\partial f}{\partial \phi} \bm{e}_\phi \\
   \nabla \cdot \bm{F} &= \frac{1}{r^2} \frac{\partial (r^2 F_r)}{\partial r} + \frac{1}{r \sin\theta} \frac{\partial (\sin\theta \, F_\theta)}{\partial \theta} + \frac{1}{r \sin\theta} \frac{\partial F_\phi}{\partial \phi} \\
   \nabla \times \bm{F} &= \frac{1}{r \sin\theta} \left( \frac{\partial (\sin\theta \, F_\phi)}{\partial \theta} - \frac{\partial F_\theta}{\partial \phi} \right) \bm{e}_r + \frac{1}{r} \left( \frac{1}{\sin\theta} \frac{\partial F_r}{\partial \phi} - \frac{\partial (r F_\phi)}{\partial r} \right) \bm{e}_\theta + \frac{1}{r} \left( \frac{\partial (r F_\theta)}{\partial r} - \frac{\partial F_r}{\partial \theta} \right) \bm{e}_\phi \\
   \nabla^2 f &= \frac{1}{r^2} \frac{\partial}{\partial r} \left( r^2 \frac{\partial f}{\partial r} \right) + \frac{1}{r^2 \sin\theta} \frac{\partial}{\partial \theta} \left( \sin\theta \frac{\partial f}{\partial \theta} \right) + \frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}

積分の公式
----------

重積分の変数変換
~~~~~~~~~~~~~~~~

.. math::

   \iint_D f(x, y) \, dx \, dy = \iint_{D'} f(x(u, v), y(u, v)) \left| \frac{\partial(x, y)}{\partial(u, v)} \right| du \, dv, \qquad \frac{\partial(x, y)}{\partial(u, v)} = \begin{vmatrix} \dfrac{\partial x}{\partial u} & \dfrac{\partial x}{\partial v} \\ \dfrac{\partial y}{\partial u} & \dfrac{\partial y}{\partial v} \end{vmatrix}

線積分と面積分
~~~~~~~~~~~~~~

曲線 :math:`C` を :math:`\bm{r}(t)`\ （:math:`a \le t \le b`）、曲面 :math:`S` を :math:`\bm{r}(u, v)`\ （:math:`(u, v) \in D`）で表すとき、次のようになる。

.. math::

   \int_C f \, ds &= \int_a^b f(\bm{r}(t)) \left| \frac{d\bm{r}}{dt} \right| dt, \qquad \int_C \bm{F} \cdot d\bm{r} = \int_a^b \bm{F}(\bm{r}(t)) \cdot \frac{d\bm{r}}{dt} \, dt \\
   \iint_S f \, dS &= \iint_D f(\bm{r}(u, v)) \, |\bm{r}_u \times \bm{r}_v| \, du \, dv, \qquad \iint_S \bm{F} \cdot d\bm{S} = \iint_D \bm{F}(\bm{r}(u, v)) \cdot (\bm{r}_u \times \bm{r}_v) \, du \, dv

面積分の第 2 式は、:math:`\bm{r}_u \times \bm{r}_v` の向きが曲面の向き（単位法線ベクトル :math:`\bm{n}` の向き）と一致する場合の式である。逆向きの場合は符号が変わる。

積分定理
~~~~~~~~

.. list-table:: ベクトル解析の積分定理
   :header-rows: 1
   :widths: 24 76

   * - 名前
     - 公式
   * - 勾配定理
     - :math:`\displaystyle \int_C \nabla f \cdot d\bm{r} = f(\mathrm{B}) - f(\mathrm{A})`\ （:math:`C` は点 A から点 B への曲線）
   * - グリーンの定理（循環形）
     - :math:`\displaystyle \oint_{\partial D} (P \, dx + Q \, dy) = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dx \, dy`
   * - グリーンの定理（流束形）
     - :math:`\displaystyle \oint_{\partial D} \bm{F} \cdot \bm{n} \, ds = \iint_D \left( \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} \right) dx \, dy`\ （:math:`\bm{F} = (P, Q)`、:math:`\bm{n}` は外向きの単位法線ベクトル）
   * - ガウスの発散定理
     - :math:`\displaystyle \iint_{\partial V} \bm{F} \cdot d\bm{S} = \iiint_V \nabla \cdot \bm{F} \, dV`\ （:math:`\partial V` は外向き）
   * - ストークスの定理
     - :math:`\displaystyle \oint_{\partial S} \bm{F} \cdot d\bm{r} = \iint_S (\nabla \times \bm{F}) \cdot d\bm{S}`\ （:math:`\partial S` の向きと :math:`S` の向きは右ねじの関係）

グリーンの定理の :math:`\partial D` は、領域 :math:`D` を左手に見て進む向き（外側の境界では反時計回り）とする。

ガウスの発散定理から導かれる公式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

   \iiint_V \nabla f \, dV &= \iint_{\partial V} f \, \bm{n} \, dS \\
   \iiint_V \nabla \times \bm{F} \, dV &= \iint_{\partial V} \bm{n} \times \bm{F} \, dS \\
   \iiint_V (f \nabla^2 g + \nabla f \cdot \nabla g) \, dV &= \iint_{\partial V} f \nabla g \cdot d\bm{S} \\
   \iiint_V (f \nabla^2 g - g \nabla^2 f) \, dV &= \iint_{\partial V} (f \nabla g - g \nabla f) \cdot d\bm{S}

最後の 2 つの式を、それぞれグリーンの第 1 恒等式、第 2 恒等式という。
