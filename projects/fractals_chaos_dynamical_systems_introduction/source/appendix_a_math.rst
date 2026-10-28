.. _appendix-a:

付録 A 数学の補足
=================

本文で使った数学のうち、高校数学の範囲を少し超えるものを簡単にまとめる。

複素数
------

複素数 :math:`z = x + iy`\ （:math:`i^2 = -1`）は、平面上の点 :math:`(x, y)` と同一視できる。この平面を\ **複素平面**\ といい、:math:`x` を実部（:math:`\mathrm{Re}\,z`）、:math:`y` を虚部（:math:`\mathrm{Im}\,z`）という。

極形式
^^^^^^

原点からの距離 :math:`|z| = \sqrt{x^2 + y^2}` を\ **絶対値**\ 、正の実軸から反時計回りに測った角度 :math:`\theta = \arg z` を\ **偏角**\ という。オイラーの公式 :math:`e^{i\theta} = \cos\theta + i\sin\theta` を使うと、

.. math::

   z = |z|\,(\cos\theta + i\sin\theta) = |z|\,e^{i\theta}

と書ける。これを\ **極形式**\ という。

積と回転
^^^^^^^^

2 つの複素数 :math:`z_1 = r_1 e^{i\theta_1}`、:math:`z_2 = r_2 e^{i\theta_2}` の積は

.. math::

   z_1 z_2 = r_1 r_2\,e^{i(\theta_1 + \theta_2)}

である。つまり、積は「絶対値を掛け、偏角を足す」操作である。特に、絶対値 1 の複素数 :math:`e^{i\alpha}` を掛けると、原点の周りに角度 :math:`\alpha` だけ回転する。第 7 章のコッホ曲線では、:math:`e^{i\pi/3}` を掛けて 60 度回転させた。また、:math:`z^2 = r^2 e^{2i\theta}` なので、2 乗は絶対値を 2 乗し、偏角を 2 倍する（第 9 章）。

共役複素数
^^^^^^^^^^

:math:`z = x + iy` に対して :math:`\bar{z} = x - iy` を\ **共役複素数**\ という。複素平面では、実軸に関して折り返した点である。:math:`z\bar{z} = |z|^2` が成り立つ。

Python では、``1 + 2j`` のように ``j`` を付けて複素数を書く。``abs(z)`` で絶対値、``cmath.phase(z)``\ （NumPy では ``np.angle(z)``）で偏角、``z.conjugate()``\ （NumPy では ``np.conj(z)``）で共役複素数が求められる。

2 次の行列の固有値
------------------

正方行列 :math:`A` とゼロでないベクトル :math:`\boldsymbol{v}` が :math:`A\boldsymbol{v} = \lambda\boldsymbol{v}` を満たすとき、数 :math:`\lambda` を :math:`A` の\ **固有値**\ 、:math:`\boldsymbol{v}` を\ **固有ベクトル**\ という。固有ベクトルの方向では、:math:`A` を掛ける操作は、:math:`\lambda` 倍に伸び縮みさせるだけになる。

2 次の行列 :math:`A = \begin{pmatrix} a & b \\ c & d \end{pmatrix}` の固有値は、2 次方程式

.. math::

   \lambda^2 - (a + d)\,\lambda + (ad - bc) = 0

の解である。:math:`\tau = a + d` を\ **トレース**\ 、:math:`\Delta = ad - bc` を\ **行列式**\ という。解の公式から、固有値は

.. math::

   \lambda = \frac{\tau \pm \sqrt{\tau^2 - 4\Delta}}{2}

となる。:math:`\tau^2 - 4\Delta < 0` のとき、固有値は互いに共役な複素数になる。2 つの固有値の和は :math:`\tau`、積は :math:`\Delta` に等しい。

第 3 章の平衡点の分類は、トレースと行列式で次のように言い換えられる。

.. list-table:: トレースと行列式による平衡点の分類
   :header-rows: 1
   :widths: 40 60

   * - 条件
     - 平衡点の種類
   * - :math:`\Delta < 0`
     - 鞍点
   * - :math:`\Delta > 0`、:math:`\tau^2 \ge 4\Delta`
     - 結節点（:math:`\tau < 0` なら安定、:math:`\tau > 0` なら不安定）
   * - :math:`\Delta > 0`、:math:`\tau^2 < 4\Delta`、:math:`\tau \ne 0`
     - 渦状点（:math:`\tau < 0` なら安定、:math:`\tau > 0` なら不安定）
   * - :math:`\Delta > 0`、:math:`\tau = 0`
     - 中心

NumPy では、``np.linalg.eigvals(A)`` で固有値を、``np.linalg.eig(A)`` で固有値と固有ベクトルを求められる。

テイラー展開と線形化
--------------------

関数 :math:`f` が点 :math:`a` の近くで滑らかなら、

.. math::

   f(x) = f(a) + f'(a)(x - a) + \frac{f''(a)}{2}(x - a)^2 + \cdots

と、:math:`x - a` のべき乗の和で表せる。これを\ **テイラー展開**\ という。:math:`x` が :math:`a` に十分近ければ、:math:`(x - a)^2` 以降の項は :math:`(x - a)` の項に比べて非常に小さいので、

.. math::

   f(x) \approx f(a) + f'(a)(x - a)

と 1 次式で近似できる。これが第 2 章の線形化である。

多変数の関数 :math:`F(\boldsymbol{x}) = (F_1(\boldsymbol{x}), \ldots, F_n(\boldsymbol{x}))` では、微分 :math:`f'(a)` の代わりに、偏微分を並べたヤコビ行列 :math:`J_{ij} = \partial F_i / \partial x_j` を使う。

.. math::

   F(\boldsymbol{x}) \approx F(\boldsymbol{a}) + J(\boldsymbol{a})(\boldsymbol{x} - \boldsymbol{a})

第 3 章では、この近似を使って、非線形の系の平衡点を線形の系として調べた。また、ヤコビ行列の行列式の絶対値は、写像によって小さな領域の面積（体積）が何倍になるかを表す（第 6 章）。

べき乗則と両対数グラフ
----------------------

2 つの量の間に :math:`y = C x^{a}` の関係（\ **べき乗則**\ 、power law）があるとき、両辺の対数をとると

.. math::

   \log y = a \log x + \log C

となり、:math:`\log x` と :math:`\log y` は直線の関係になる。したがって、両対数グラフに点を描いて直線になれば、べき乗則が成り立っていると判断でき、直線の傾きが指数 :math:`a` を表す。第 3 章の数値解法の誤差、第 7 章のボックスカウント次元、第 10 章の相関次元は、いずれもこの方法で指数を求めた。

一方、:math:`y = C e^{a x}` の関係（指数関数的な変化）は、縦軸だけを対数目盛りにした片対数グラフで直線になる。第 5 章の初期値鋭敏性では、差の時間変化が片対数グラフで直線になることから、差が指数関数的に増えることを確かめた。

直線の傾きは、最小二乗法で求められる。NumPy では、``np.polyfit(np.log(x), np.log(y), 1)`` で、傾きと切片が得られる。
