付録 A 記号一覧
===============

本書で使う主な記号を示す。

.. list-table:: 記号一覧
   :header-rows: 1
   :widths: 25 50 25

   * - 記号
     - 意味
     - 初出
   * - :math:`a, b, c, \lambda`
     - スカラー（数）
     - 第 1 章
   * - :math:`\bm{u}, \bm{v}, \bm{x}`
     - ベクトル（列ベクトル）
     - 第 1 章
   * - :math:`A, B, P`
     - 行列
     - 第 1 章
   * - :math:`a_{ij}`
     - 行列 :math:`A` の :math:`i` 行 :math:`j` 列の成分
     - 第 1 章
   * - :math:`\mathbb{R}^n`
     - :math:`n` 個の実数を成分とするベクトル全体の集合
     - 第 1 章
   * - :math:`A^\top`
     - 行列 :math:`A` の転置
     - 第 1 章
   * - :math:`\bm{u} \cdot \bm{v}`
     - 内積
     - 第 2 章
   * - :math:`\|\bm{v}\|`
     - ベクトルのノルム（長さ）
     - 第 2 章
   * - :math:`\bm{a} \times \bm{b}`
     - 外積（3 次元のベクトルのみ）
     - 第 2 章
   * - :math:`\bm{a}_j`
     - 行列 :math:`A` の :math:`j` 番目の列ベクトル
     - 第 3 章
   * - :math:`\bm{e}_j`
     - 基本ベクトル（:math:`j` 番目の成分だけが 1 で、他が 0）
     - 第 3 章
   * - :math:`I`、:math:`I_n`
     - 単位行列
     - 第 3 章
   * - :math:`O`
     - 零行列
     - 第 3 章
   * - :math:`\bm{0}`
     - 零ベクトル（すべての成分が 0 のベクトル）
     - 第 4 章
   * - :math:`(A \mid \bm{b})`
     - 拡大係数行列
     - 第 5 章
   * - :math:`L`、:math:`U`
     - LU 分解の下三角行列と上三角行列
     - 第 5 章
   * - :math:`A^{-1}`
     - 逆行列
     - 第 6 章
   * - :math:`\det A`
     - 行列式
     - 第 6 章
   * - :math:`\mathrm{span}\{\bm{v}_1, \ldots, \bm{v}_k\}`
     - ベクトルが張る空間
     - 第 7 章
   * - :math:`\dim V`
     - 部分空間 :math:`V` の次元
     - 第 7 章
   * - :math:`\mathrm{rank}\,A`
     - 行列のランク
     - 第 8 章
   * - :math:`Q`
     - 直交行列（列が正規直交）
     - 第 9 章
   * - :math:`P`
     - 射影行列（第 9 章）、固有ベクトルを並べた行列（第 10 章）、推移行列（第 10 章）。章ごとに意味を示す
     - 第 9 章
   * - :math:`\lambda`
     - 固有値
     - 第 10 章
   * - :math:`D`、:math:`\Lambda`
     - 固有値を対角成分に並べた対角行列
     - 第 10 章
   * - :math:`\mathrm{tr}\,A`
     - トレース（対角成分の和）
     - 第 10 章
   * - :math:`\sigma_i`
     - 特異値
     - 第 12 章
   * - :math:`U, \Sigma, V`
     - 特異値分解 :math:`A = U\Sigma V^\top` の行列
     - 第 12 章
   * - :math:`A^{+}`
     - 擬似逆行列
     - 第 12 章
   * - :math:`\kappa(A)`
     - 条件数
     - 第 13 章

NumPy の関数との対応
--------------------

数式と NumPy のコードの対応を示す。``a``、``b`` は行列、``u``、``v`` はベクトル（1 次元の配列）である。

.. list-table:: 数式と NumPy のコードの対応
   :header-rows: 1
   :widths: 35 65

   * - 数式
     - NumPy のコード
   * - :math:`AB`、:math:`A\bm{v}`
     - ``a @ b``、``a @ v``
   * - :math:`\bm{u} \cdot \bm{v}`
     - ``u @ v``、``np.dot(u, v)``
   * - :math:`\|\bm{v}\|`
     - ``np.linalg.norm(v)``
   * - :math:`\bm{u} \times \bm{v}`
     - ``np.cross(u, v)``
   * - :math:`A^\top`
     - ``a.T``
   * - :math:`I_n`
     - ``np.eye(n)``
   * - :math:`A^{-1}`
     - ``np.linalg.inv(a)``
   * - :math:`A^{-1}\bm{b}`\ （:math:`A\bm{x} = \bm{b}` の解）
     - ``np.linalg.solve(a, b)``
   * - :math:`\det A`
     - ``np.linalg.det(a)``
   * - :math:`\mathrm{rank}\,A`
     - ``np.linalg.matrix_rank(a)``
   * - :math:`A^k`
     - ``np.linalg.matrix_power(a, k)``
   * - 固有値と固有ベクトル
     - ``np.linalg.eig(a)``、対称行列なら ``np.linalg.eigh(a)``
   * - :math:`A = QR`
     - ``np.linalg.qr(a)``
   * - :math:`A = LL^\top`
     - ``np.linalg.cholesky(a)``
   * - :math:`A = U\Sigma V^\top`
     - ``np.linalg.svd(a)``\ （:math:`U`、特異値の配列、:math:`V^\top` を返す）
   * - :math:`A^{+}`
     - ``np.linalg.pinv(a)``
   * - 最小二乗解
     - ``np.linalg.lstsq(a, b)``
   * - :math:`\kappa(A)`
     - ``np.linalg.cond(a)``
