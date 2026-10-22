付録 A 記号一覧
===============

本書で使う主な記号をまとめる。初出の欄は、その記号が本文に最初に現れる章を示す（行に複数の記号がある場合は、最も早く現れるものの章）。

集合と論理
----------

.. list-table:: 集合と論理の記号
   :name: appA-tab-sets
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`\mathbb{N}`
     - 自然数全体 :math:`\{1, 2, 3, \ldots\}`\ （:math:`0` を含まない）
     - 第 1 章
   * - :math:`\mathbb{Z}`
     - 整数全体
     - 第 1 章
   * - :math:`\mathbb{Q}`
     - 有理数全体
     - 第 1 章
   * - :math:`\mathbb{R}`
     - 実数全体
     - 第 1 章
   * - :math:`\mathbb{R}^n`
     - :math:`n` 個の実数の組 :math:`(x_1, \ldots, x_n)` 全体
     - 第 9 章
   * - :math:`a \in A`
     - :math:`a` は集合 :math:`A` の要素である
     - 第 1 章
   * - :math:`a \notin A`
     - :math:`a` は集合 :math:`A` の要素でない
     - 第 1 章
   * - :math:`A \subset B`
     - :math:`A` は :math:`B` の部分集合である（:math:`A = B` の場合を含む）
     - 第 1 章
   * - :math:`A \cup B`、:math:`A \cap B`
     - 和集合、共通部分
     - 第 7 章
   * - :math:`A \setminus B`
     - 差集合（:math:`A` の要素のうち :math:`B` に属さないもの全体）
     - 第 9 章
   * - :math:`\{x \mid P(x)\}`
     - 条件 :math:`P(x)` を満たす :math:`x` 全体の集合
     - 第 1 章
   * - :math:`\forall`
     - 「任意の」「すべての」
     - 第 2 章
   * - :math:`\exists`
     - 「ある〜が存在する」
     - 第 2 章
   * - :math:`P \Rightarrow Q`
     - :math:`P` ならば :math:`Q`
     - 付録 B
   * - :math:`P \Leftrightarrow Q`
     - :math:`P` と :math:`Q` は同値である
     - 付録 B
   * - :math:`\neg P`
     - :math:`P` の否定
     - 付録 B

実数と区間
----------

.. list-table:: 実数と区間に関する記号
   :name: appA-tab-reals
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`[a, b]`
     - 閉区間 :math:`\{x \mid a \leq x \leq b\}`
     - 第 2 章
   * - :math:`(a, b)`
     - 開区間 :math:`\{x \mid a < x < b\}`。文脈によっては :math:`\mathbb{R}^2` の点を表す
     - 第 1 章
   * - :math:`[a, b)`、:math:`(a, b]`
     - 半開区間
     - 第 1 章
   * - :math:`|x|`
     - 絶対値
     - 第 1 章
   * - :math:`\sup A`、:math:`\inf A`
     - 集合 :math:`A` の上限、下限
     - 第 1 章
   * - :math:`\max A`、:math:`\min A`
     - 集合 :math:`A` の最大値、最小値
     - 第 1 章
   * - :math:`\varepsilon_{\mathrm{mach}}`
     - 機械イプシロン（倍精度では :math:`2^{-52}`）
     - 第 1 章
   * - :math:`\mathrm{fl}(x)`
     - 実数 :math:`x` を最も近い浮動小数点数に丸めた値
     - 第 1 章
   * - :math:`n!`
     - :math:`n` の階乗 :math:`1 \cdot 2 \cdots n`\ （:math:`0! = 1`）
     - 第 2 章
   * - :math:`\binom{n}{k}`
     - 二項係数 :math:`\dfrac{n!}{k!(n - k)!}`
     - 第 2 章
   * - :math:`e`
     - ネイピア数 :math:`\lim (1 + 1/n)^n = 2.71828\ldots`
     - 第 2 章
   * - :math:`\log x`
     - 自然対数（底は :math:`e`）
     - 第 3 章

数列・級数・関数
----------------

.. list-table:: 数列・級数・関数に関する記号
   :name: appA-tab-functions
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`(a_n)`
     - 数列 :math:`a_1, a_2, a_3, \ldots`
     - 第 2 章
   * - :math:`\displaystyle\lim_{n \to \infty} a_n`
     - 数列の極限
     - 第 2 章
   * - :math:`a_n \to \alpha`
     - :math:`a_n` は :math:`\alpha` に収束する
     - 第 2 章
   * - :math:`\displaystyle\sum_{n=1}^{\infty} a_n`
     - 級数（部分和の極限）
     - 第 3 章
   * - :math:`f \colon A \to B`
     - :math:`A` を定義域とし、値を :math:`B` にとる関数（写像）
     - 第 3 章
   * - :math:`g \circ f`
     - 合成関数 :math:`(g \circ f)(x) = g(f(x))`
     - 第 4 章
   * - :math:`f^{-1}`
     - 逆関数
     - 第 5 章
   * - :math:`\displaystyle\lim_{x \to a} f(x)`
     - 関数の極限
     - 第 4 章
   * - :math:`f'(x)`
     - 導関数
     - 第 4 章
   * - :math:`f^{(n)}(x)`
     - :math:`n` 階導関数
     - 第 5 章
   * - :math:`\dfrac{d}{dx}`
     - 変数 :math:`x` について微分する演算（:math:`\dfrac{d}{dx} g(x) = g'(x)`）
     - 第 6 章
   * - :math:`C^n` 級、:math:`C^\infty` 級
     - :math:`n` 回微分可能で :math:`n` 階導関数が連続、何回でも微分可能
     - 第 5 章
   * - :math:`O(\cdot)`、:math:`o(\cdot)`
     - ランダウの記号
     - 第 3 章
   * - :math:`\displaystyle\int_a^b f(x)\,dx`
     - 定積分
     - 第 3 章
   * - :math:`\|g\|_\infty`
     - 一様ノルム :math:`\sup_{x \in I} |g(x)|`
     - 第 8 章

多変数
------

.. list-table:: 多変数関数に関する記号
   :name: appA-tab-multivariable
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`\boldsymbol{x}`
     - :math:`\mathbb{R}^n` の点（ベクトル）
     - 第 9 章
   * - :math:`\|\boldsymbol{x}\|`
     - ユークリッドノルム :math:`\sqrt{x_1^2 + \cdots + x_n^2}`
     - 第 9 章
   * - :math:`\langle \boldsymbol{x}, \boldsymbol{y} \rangle`
     - 内積 :math:`x_1 y_1 + \cdots + x_n y_n`
     - 第 9 章
   * - :math:`\dfrac{\partial f}{\partial x_i}`
     - 偏導関数
     - 第 9 章
   * - :math:`\nabla f`
     - 勾配
     - 第 9 章
   * - :math:`J_{\boldsymbol{f}}`
     - ベクトル値関数 :math:`\boldsymbol{f}` のヤコビ行列
     - 第 9 章
   * - :math:`H_f`
     - ヘッセ行列
     - 第 9 章
   * - :math:`\det A`
     - 行列 :math:`A` の行列式
     - 第 9 章
   * - :math:`\displaystyle\iint_D f(x, y)\,dx\,dy`
     - 重積分
     - 第 10 章

ギリシャ文字
------------

本書で使う主なギリシャ文字とその読みを示す。

.. list-table:: ギリシャ文字
   :name: appA-tab-greek
   :header-rows: 1
   :widths: 20 30 50

   * - 文字
     - 読み
     - 本書での主な用途
   * - :math:`\alpha`、:math:`\beta`
     - アルファ、ベータ
     - 極限値
   * - :math:`\delta`
     - デルタ
     - ε-δ 論法の許容幅
   * - :math:`\varepsilon`
     - イプシロン
     - 任意の正の数（許容誤差）
   * - :math:`\theta`
     - シータ
     - 平均値の定理などに現れる :math:`0 < \theta < 1` の数、角度
   * - :math:`\xi`
     - クシー（グザイ）
     - 平均値の定理などに現れる中間点
   * - :math:`\Delta`
     - デルタ（大文字）
     - 分割、増分
   * - :math:`\sum`、:math:`\prod`
     - シグマ、パイ（大文字）
     - 和、積
