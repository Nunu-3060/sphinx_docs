記号一覧
========

本書の数式で使う主な記号を次に示す。

.. list-table:: 記号一覧
   :header-rows: 1
   :widths: 25 75

   * - 記号
     - 意味
   * - :math:`x`、:math:`w`
     - スカラー（1 つの数値）。細字の小文字で表す。
   * - :math:`\boldsymbol{x}`、:math:`\boldsymbol{w}`
     - ベクトル。太字の小文字で表す。特に断らない限り縦ベクトルとする。
   * - :math:`X`、:math:`W`
     - 行列。大文字で表す。
   * - :math:`x_i`
     - ベクトル :math:`\boldsymbol{x}` の :math:`i` 番目の要素。
   * - :math:`\boldsymbol{x}_i`
     - :math:`i` 番目のサンプルの特徴量ベクトル。
   * - :math:`n`
     - サンプル数。
   * - :math:`d`
     - 特徴量の数（ベクトルの次元）。
   * - :math:`K`
     - 分類のクラス数。第 12 章ではキーを並べた行列を表す（:math:`Q`、:math:`V` はクエリとバリューを並べた行列）。
   * - :math:`y`、:math:`\boldsymbol{y}`
     - 正解のラベル。
   * - :math:`\hat{y}`
     - モデルによる予測値。
   * - :math:`p`
     - モデルが予測した確率。
   * - :math:`b`
     - バイアス（切片）。
   * - :math:`L`
     - 損失関数。
   * - :math:`\eta`
     - 学習率。
   * - :math:`\alpha`
     - 正則化の強さ。
   * - :math:`\boldsymbol{x}^\top`、:math:`X^\top`
     - ベクトルや行列の転置。
   * - :math:`\boldsymbol{w}^\top \boldsymbol{x}`
     - ベクトルの内積 :math:`\sum_i w_i x_i`。
   * - :math:`\| \boldsymbol{v} \|^2`
     - ベクトルの各要素の 2 乗の和。
   * - :math:`\sum_{i=1}^{n}`
     - :math:`i = 1` から :math:`n` までの和。
   * - :math:`f'(x)`、:math:`\dfrac{df}{dx}`
     - 関数 :math:`f` の微分（導関数）。
   * - :math:`\dfrac{\partial f}{\partial x}`
     - 関数 :math:`f` の :math:`x` についての偏微分。
   * - :math:`\nabla f`
     - 関数 :math:`f` の勾配。
   * - :math:`\log x`
     - 自然対数（底が :math:`e` の対数）。
   * - :math:`e^x`、:math:`\exp(x)`
     - 指数関数。
   * - :math:`\sigma(z)`
     - シグモイド関数（第 5 章）。第 2 章などでは標準偏差を表す場合もあり、文脈で区別する。
   * - :math:`\mu`
     - 平均。
   * - :math:`P(y \mid \boldsymbol{x})`
     - :math:`\boldsymbol{x}` が与えられたときの :math:`y` の条件付き確率。
   * - :math:`\lfloor a \rfloor`
     - :math:`a` 以下の最大の整数（小数点以下の切り捨て）。
