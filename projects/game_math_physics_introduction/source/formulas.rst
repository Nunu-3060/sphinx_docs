付録 A 数式・記号の早見表
=========================

本書で使った記号と、よく使う公式をまとめる。

記号
----

.. list-table:: 本書で使う記号
   :header-rows: 1
   :widths: 25 75

   * - 記号
     - 意味
   * - :math:`\mathbf{a}`、:math:`\mathbf{v}`\ （太字）
     - ベクトル
   * - :math:`a_x`、:math:`a_y`
     - ベクトル :math:`\mathbf{a}` の x 成分、y 成分
   * - :math:`|\mathbf{a}|`
     - ベクトルの長さ
   * - :math:`\hat{\mathbf{a}}`
     - :math:`\mathbf{a}` を正規化した単位ベクトル
   * - :math:`\mathbf{a} \cdot \mathbf{b}`
     - 内積
   * - :math:`\mathbf{a} \times \mathbf{b}`
     - 外積（2D では数、3D ではベクトル）
   * - :math:`\mathbf{n}`
     - 法線（面に垂直な単位ベクトル）
   * - :math:`\Delta t`、dt
     - デルタタイム（1 回の更新で進める時間）
   * - :math:`h`
     - 固定タイムステップの 1 ステップの時間
   * - :math:`\theta`、:math:`\phi`
     - 角度（ラジアン）
   * - :math:`\omega`
     - 角速度、または角振動数
   * - :math:`m`、:math:`I`
     - 質量、慣性モーメント
   * - :math:`g`
     - 重力加速度の大きさ
   * - :math:`e`
     - 反発係数（指数関数の底 :math:`e^x` と区別すること）
   * - :math:`\mu`
     - 摩擦係数
   * - :math:`k`、:math:`c`
     - ばね定数、減衰係数
   * - :math:`\zeta`
     - 減衰比

ベクトル
--------

.. list-table:: ベクトルの公式
   :header-rows: 1
   :widths: 30 70

   * - 演算
     - 式
   * - 長さ
     - :math:`|\mathbf{a}| = \sqrt{a_x^2 + a_y^2}`
   * - 正規化
     - :math:`\hat{\mathbf{a}} = \mathbf{a} / |\mathbf{a}|`
   * - 内積
     - :math:`\mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y = |\mathbf{a}|\,|\mathbf{b}|\cos\theta`
   * - 2D の外積
     - :math:`\mathbf{a} \times \mathbf{b} = a_x b_y - a_y b_x = |\mathbf{a}|\,|\mathbf{b}|\sin\theta`
   * - 3D の外積
     - :math:`(a_y b_z - a_z b_y,\ a_z b_x - a_x b_z,\ a_x b_y - a_y b_x)`
   * - 射影
     - :math:`\mathrm{proj}_{\mathbf{b}}\mathbf{a} = \dfrac{\mathbf{a} \cdot \mathbf{b}}{\mathbf{b} \cdot \mathbf{b}}\,\mathbf{b}`
   * - 反射
     - :math:`\mathbf{r} = \mathbf{v} - 2(\mathbf{v} \cdot \mathbf{n})\,\mathbf{n}`

角度と回転
----------

.. list-table:: 角度と回転の公式
   :header-rows: 1
   :widths: 30 70

   * - 内容
     - 式
   * - 度とラジアン
     - :math:`\theta_{\text{rad}} = \theta_{\text{度}} \times \pi / 180`
   * - 極座標から直交座標
     - :math:`(r\cos\theta,\ r\sin\theta)`
   * - ベクトルの向き
     - :math:`\theta = \mathrm{atan2}(y, x)`
   * - 2D の回転
     - :math:`x' = x\cos\theta - y\sin\theta,\quad y' = x\sin\theta + y\cos\theta`
   * - 角度の正規化
     - :math:`((\theta + \pi) \bmod 2\pi) - \pi`

行列
----

.. list-table:: 2D のアフィン変換の行列
   :header-rows: 1
   :widths: 30 70

   * - 変換
     - 行列
   * - 平行移動
     - :math:`\begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix}`
   * - 回転
     - :math:`\begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}`
   * - 拡大縮小
     - :math:`\begin{pmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{pmatrix}`
   * - 合成の逆
     - :math:`(AB)^{-1} = B^{-1}A^{-1}`

補間
----

.. list-table:: 補間の公式
   :header-rows: 1
   :widths: 30 70

   * - 内容
     - 式
   * - 線形補間
     - :math:`\mathrm{lerp}(a, b, t) = a + (b - a)\,t`
   * - 逆補間
     - :math:`(v - a) / (b - a)`
   * - 指数関数的減衰
     - :math:`x \leftarrow \mathrm{lerp}(x,\ x_{\text{目標}},\ 1 - e^{-k\,\Delta t})`
   * - smoothstep
     - :math:`3t^2 - 2t^3`
   * - 3 次ベジェ曲線
     - :math:`(1 - t)^3 P_0 + 3(1 - t)^2 t\,P_1 + 3(1 - t)t^2 P_2 + t^3 P_3`
   * - 球面線形補間
     - :math:`\dfrac{\sin((1 - t)\Omega)}{\sin\Omega}\,a + \dfrac{\sin(t\Omega)}{\sin\Omega}\,b`

確率
----

.. list-table:: 確率の公式
   :header-rows: 1
   :widths: 30 70

   * - 内容
     - 式
   * - 初めて当たるまでの回数の期待値
     - :math:`1/p`
   * - n 回で少なくとも 1 回当たる確率
     - :math:`1 - (1 - p)^n`
   * - その確率が P 以上になる回数
     - :math:`\lceil \log(1 - P) / \log(1 - p) \rceil`

運動と衝突
----------

.. list-table:: 運動と衝突の公式
   :header-rows: 1
   :widths: 30 70

   * - 内容
     - 式
   * - 運動方程式
     - :math:`\mathbf{F} = m\,\mathbf{a}`
   * - 半陰的オイラー法
     - :math:`\mathbf{v} \leftarrow \mathbf{v} + \mathbf{a}\,\Delta t,\quad \mathbf{x} \leftarrow \mathbf{x} + \mathbf{v}\,\Delta t`
   * - ジャンプの重力と初速
     - :math:`g = 2h / T^2,\quad v_0 = 2h / T`
   * - 反発
     - :math:`v_n' = -e\,v_n`
   * - 衝突の力積
     - :math:`j = \dfrac{-(1 + e)\,v_n}{1/m_A + 1/m_B}`
   * - ばねとダンパー
     - :math:`a = -k(x - x_0) - c\,v,\quad k = \omega^2,\quad c = 2\zeta\omega`
   * - 位置ベルレ法
     - :math:`\mathbf{x}_{\text{次}} = 2\mathbf{x}_{\text{今}} - \mathbf{x}_{\text{前}} + \mathbf{a}\,\Delta t^2`
   * - 慣性モーメント（円板）
     - :math:`\frac{1}{2} m r^2`
   * - 慣性モーメント（長方形の板）
     - :math:`\frac{1}{12} m (w^2 + h^2)`
