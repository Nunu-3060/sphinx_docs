付録 A　数学メモ
============================================================

本書で使う数学の道具を、式と使いどころに絞ってまとめる。証明や厳密な定義は省く。

ベクトル
------------------------------------------------------------

本書では、位置・方向・速度・色などを、成分を並べた\ **ベクトル**\ で表す。太字の :math:`\boldsymbol{a} = (a_x, a_y, a_z)` はベクトル、細字の :math:`s` はスカラー（1 個の数）を表す。

.. list-table:: ベクトルの基本演算
   :header-rows: 1
   :widths: 22 38 40

   * - 演算
     - 式
     - 使いどころ
   * - 和・差
     - :math:`\boldsymbol{a} \pm \boldsymbol{b} = (a_x \pm b_x, a_y \pm b_y, a_z \pm b_z)`
     - 移動、2 点間の変位 :math:`\boldsymbol{b} - \boldsymbol{a}`
   * - スカラー倍
     - :math:`s \boldsymbol{a} = (s a_x, s a_y, s a_z)`
     - 拡大・縮小、速度 × 時間
   * - 長さ
     - :math:`|\boldsymbol{a}| = \sqrt{a_x^2 + a_y^2 + a_z^2}`
     - 距離、距離関数（第 9 章）
   * - 正規化
     - :math:`\hat{\boldsymbol{a}} = \boldsymbol{a} / |\boldsymbol{a}|`
     - 向きだけを取り出す（長さ 1 の\ **単位ベクトル**\ にする）

内積
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   \boldsymbol{a} \cdot \boldsymbol{b} = a_x b_x + a_y b_y + a_z b_z = |\boldsymbol{a}| |\boldsymbol{b}| \cos \theta

:math:`\theta` は 2 つのベクトルのなす角である。内積は、2 つの向きがどれだけそろっているかを表す。向きが同じなら正、直交していれば 0、逆向きなら負になる。本書では次の場面で使う。

* パーリンノイズで、格子点の勾配ベクトルと格子点からの変位の内積を取る（第 3 章）。
* 法線と光の向きの内積で、面の明るさを決める（ランバート反射。第 6 章、第 9 章）。
* :math:`\boldsymbol{a} \cdot \boldsymbol{a} = |\boldsymbol{a}|^2` なので、平方根を避けて距離を比べる。

外積
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. math::

   \boldsymbol{a} \times \boldsymbol{b} = (a_y b_z - a_z b_y,\ a_z b_x - a_x b_z,\ a_x b_y - a_y b_x)

外積は 3 次元のベクトルどうしに定義され、両方に垂直なベクトルを返す。その長さは、:math:`\boldsymbol{a}` と :math:`\boldsymbol{b}` が作る平行四辺形の面積に等しい。三角形の頂点を :math:`\boldsymbol{p}_0, \boldsymbol{p}_1, \boldsymbol{p}_2` とすると、:math:`(\boldsymbol{p}_1 - \boldsymbol{p}_0) \times (\boldsymbol{p}_2 - \boldsymbol{p}_0)` の向きが面の法線になる（第 6 章）。頂点の並び順を逆にすると法線も逆を向く。

2 次元では、:math:`a_x b_y - a_y b_x` をスカラーの外積として使う。符号で、:math:`\boldsymbol{b}` が :math:`\boldsymbol{a}` の左右どちらにあるかが分かる。

回転
------------------------------------------------------------

2 次元の点を原点の周りに角 :math:`\theta` だけ反時計回りに回転するには、次の行列を掛ける。

.. math::

   \begin{pmatrix} x' \\ y' \end{pmatrix} =
   \begin{pmatrix} \cos \theta & -\sin \theta \\ \sin \theta & \cos \theta \end{pmatrix}
   \begin{pmatrix} x \\ y \end{pmatrix}

3 次元では、どの軸の周りに回すかを決める必要がある。たとえば :math:`z` 軸の周りの回転は、上の 2 × 2 の行列を :math:`x, y` 成分に適用し、:math:`z` 成分は変えない。任意の単位ベクトル :math:`\hat{\boldsymbol{k}}` の周りの回転は、次のロドリゲスの回転公式で計算できる。

.. math::

   \boldsymbol{v}' = \boldsymbol{v} \cos \theta + (\hat{\boldsymbol{k}} \times \boldsymbol{v}) \sin \theta + \hat{\boldsymbol{k}} (\hat{\boldsymbol{k}} \cdot \boldsymbol{v}) (1 - \cos \theta)

L-system のタートル（第 8 章）や、インスタンスごとの回転のばらつき（第 10 章）で使う。

極座標
------------------------------------------------------------

平面上の点を、原点からの距離 :math:`r` と角度 :math:`\theta` で表す方法を\ **極座標**\ と呼ぶ。

.. math::

   x = r \cos \theta, \quad y = r \sin \theta, \qquad r = \sqrt{x^2 + y^2}, \quad \theta = \operatorname{atan2}(y, x)

円柱・球・回転体のメッシュ（第 6 章）、円周上でノイズを取る完全なループ（第 14 章）で使う。

繰り返しと分割
------------------------------------------------------------

座標 :math:`x` を、整数部と小数部に分ける操作は、パターンやノイズの基本である。

.. math::

   \lfloor x \rfloor = (x \text{ 以下の最大の整数}), \qquad \mathrm{fract}(x) = x - \lfloor x \rfloor

:math:`\lfloor x \rfloor` は「何番目のマスか」、:math:`\mathrm{fract}(x)` は「マスの中のどこか」を表す。座標を :math:`n` 倍してから :math:`\mathrm{fract}` を取れば、同じ模様を 1 辺に :math:`n` 個繰り返せる（第 4 章）。マスの番号をハッシュ関数に入れれば、マスごとに異なる乱数が得られる（第 2 章）。

GLSL の ``mod(x, y)`` は :math:`x - y \lfloor x / y \rfloor` で、負の数でも 0 以上 :math:`y` 未満の値を返す。C 言語の整数の ``%`` は負の数に対して負の値を返し、GLSL の整数の ``%`` は負の数に対する結果が規格で定められていないので注意する。Python の ``%`` と NumPy の ``np.mod`` は ``mod`` と同じく 0 以上を返す。

補間
------------------------------------------------------------

**線形補間**\ と、その重みを滑らかにする曲線は\ :ref:`basics-interpolation`\ で扱った。

.. math::

   \mathrm{lerp}(a, b, t) = a + (b - a) t

2 次元の格子では、4 隅の値 :math:`v_{00}, v_{10}, v_{01}, v_{11}` を、まず :math:`x` 方向に、次に :math:`y` 方向に線形補間する（\ **双線形補間**\ ）。

.. math::

   v(t_x, t_y) = \mathrm{lerp} \bigl( \mathrm{lerp}(v_{00}, v_{10}, t_x),\ \mathrm{lerp}(v_{01}, v_{11}, t_x),\ t_y \bigr)

3 次元では、8 隅の値を :math:`x, y, z` の順に補間する（\ **3 線形補間**\ ）。バリューノイズとパーリンノイズは、:math:`t_x, t_y` に smootherstep を適用してからこの補間を行う（第 3 章）。

勾配と数値微分
------------------------------------------------------------

2 変数の関数 :math:`f(x, y)` の\ **勾配**\ は、各方向の偏微分を並べたベクトルである。

.. math::

   \nabla f = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y} \right)

勾配は、値が最も急に増える向きを指し、その長さは増え方の大きさを表す。ハイトマップでは、勾配が斜面の傾きと向きを表す。式で微分できない場合は、近くの 2 点の差で近似する（\ **中心差分**\ ）。

.. math::

   \frac{\partial f}{\partial x} \approx \frac{f(x + h, y) - f(x - h, y)}{2h}

本書では次の場面で使う。

* ハイトマップ :math:`h(x, y)` の面の法線は :math:`(-\partial h / \partial x,\ -\partial h / \partial y,\ 1)` を正規化して求める（法線マップ・第 4 章、地形・第 7 章）。
* 距離関数 :math:`d(\boldsymbol{p})` の勾配は、表面の法線の向きになる（第 9 章）。
* 2 次元のスカラー場 :math:`\psi` から :math:`(\partial \psi / \partial y,\ -\partial \psi / \partial x)` を作ると、発散が 0 の流れ場になる（カールノイズ・第 13 章）。

数値積分
------------------------------------------------------------

シミュレーションでは、速度 :math:`\boldsymbol{v}` と加速度 :math:`\boldsymbol{a}` から、時間刻み :math:`\Delta t` ごとに位置 :math:`\boldsymbol{x}` を更新する。

.. list-table:: 本書で使う数値積分
   :header-rows: 1
   :widths: 24 46 30

   * - 方法
     - 更新式
     - 使いどころ
   * - 前進オイラー法
     - :math:`\boldsymbol{x} \leftarrow \boldsymbol{x} + \boldsymbol{v} \Delta t,\ \boldsymbol{v} \leftarrow \boldsymbol{v} + \boldsymbol{a} \Delta t`
     - 最も単純。ばねなどでは誤差がたまって発散しやすい
   * - 半陰的オイラー法
     - :math:`\boldsymbol{v} \leftarrow \boldsymbol{v} + \boldsymbol{a} \Delta t,\ \boldsymbol{x} \leftarrow \boldsymbol{x} + \boldsymbol{v} \Delta t`
     - 速度を先に更新するだけで安定性が大きく上がる。粒子・ばね（第 12〜13 章）
   * - ベルレ法
     - :math:`\boldsymbol{x}_{n+1} = 2 \boldsymbol{x}_n - \boldsymbol{x}_{n-1} + \boldsymbol{a} \Delta t^2`
     - 速度を持たず、前回の位置から動きを推定する。距離の制約と組み合わせやすい。紐・布（第 13 章）

時間刻み :math:`\Delta t` が大きいほど誤差が大きく、不安定になりやすい。描画のフレームレートが変わっても結果を変えたくない場合は、:math:`\Delta t` を固定して、1 フレームに必要な回数だけ更新する。

確率と統計
------------------------------------------------------------

.. list-table:: 本書で使う確率・統計の用語
   :header-rows: 1
   :widths: 22 78

   * - 用語
     - 意味
   * - 一様分布
     - 範囲内のどの値も同じ確率で出る分布。ハッシュ関数や擬似乱数が直接返す
   * - 正規分布
     - 平均の周りに集まり、離れるほど出にくくなる釣り鐘形の分布。平均 :math:`\mu` と標準偏差 :math:`\sigma` で決まる
   * - 中心極限定理
     - 独立な乱数を多数足し合わせると、元の分布によらず正規分布に近づくという定理
   * - パワースペクトル
     - 信号や画像を、周波数ごとの成分の強さに分解したもの。ノイズの性質（第 3 章）や点の配置の性質（第 10 章）を比べるのに使う
