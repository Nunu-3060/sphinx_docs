付録 A 記号一覧
===============

本書で用いる主な記号をまとめる。

集合と論理
----------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`a \in A`、:math:`a \notin A`
     - :math:`a` は :math:`A` の要素である、要素でない
     - 第 2 章
   * - :math:`\emptyset`
     - 空集合
     - 第 2 章
   * - :math:`|A|`
     - 有限集合 :math:`A` の要素の個数
     - 第 2 章
   * - :math:`A \subseteq B`
     - :math:`A` は :math:`B` の部分集合である
     - 第 2 章
   * - :math:`A \cup B`、:math:`A \cap B`
     - 和集合、共通部分
     - 第 2 章
   * - :math:`A \setminus B`
     - 差集合
     - 第 2 章
   * - :math:`\overline{A}`
     - 補集合（確率では余事象）
     - 第 2 章
   * - :math:`A \times B`
     - 直積
     - 第 2 章
   * - :math:`2^A`
     - べき集合
     - 第 2 章
   * - :math:`\mathbb{N}`、:math:`\mathbb{R}`
     - 自然数全体（0 を含まない）、実数全体
     - 第 1 章
   * - :math:`\neg`、:math:`\land`、:math:`\lor`、:math:`\to`
     - 否定、論理積、論理和、含意
     - 第 2 章
   * - :math:`\forall`、:math:`\exists`
     - 全称量化子、存在量化子
     - 第 2 章

写像・関係・数え上げ
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`f\colon A \to B`
     - :math:`A` から :math:`B` への写像
     - 第 3 章
   * - :math:`g \circ f`
     - 合成写像
     - 第 3 章
   * - :math:`f^{-1}`
     - 逆写像
     - 第 3 章
   * - :math:`a \equiv b \pmod{m}`
     - :math:`a - b` は :math:`m` で割り切れる
     - 第 3 章
   * - :math:`a \mid b`
     - :math:`a` は :math:`b` を割り切る
     - 第 3 章
   * - :math:`n!`
     - :math:`n` の階乗
     - 第 4 章
   * - :math:`P(n, r)`
     - 順列の総数
     - 第 4 章
   * - :math:`\binom{n}{r}`、:math:`C(n, r)`
     - 組合せの総数（二項係数）
     - 第 4 章
   * - :math:`H(n, r)`
     - 重複組合せの総数
     - 第 4 章
   * - :math:`D(n)`
     - 攪乱順列の個数
     - 第 4 章
   * - :math:`\lceil x \rceil`
     - :math:`x` 以上の最小の整数
     - 第 4 章
   * - :math:`H_n`
     - 調和数 :math:`1 + 1/2 + \cdots + 1/n`
     - 第 12 章

グラフ
------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`G = (V, E)`
     - 頂点集合 :math:`V`、辺集合 :math:`E` のグラフ
     - 第 5 章
   * - :math:`\{u, v\}`
     - 無向グラフの辺
     - 第 5 章
   * - :math:`(u, v)`
     - 有向グラフの辺
     - 第 5 章
   * - :math:`\deg(v)`
     - 頂点 :math:`v` の次数
     - 第 5 章

確率
----

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`\Omega`
     - 標本空間
     - 第 6 章
   * - :math:`P(A)`
     - 事象 :math:`A` の確率
     - 第 6 章
   * - :math:`P(A \mid B)`
     - :math:`B` のもとでの :math:`A` の条件付き確率
     - 第 6 章
   * - :math:`I_A`
     - 事象 :math:`A` の指示確率変数
     - 第 7 章
   * - :math:`p_X(x)`
     - 確率質量関数 :math:`P(X = x)`
     - 第 7 章
   * - :math:`F_X(x)`
     - 累積分布関数 :math:`P(X \le x)`
     - 第 7 章
   * - :math:`E[X]`
     - 期待値
     - 第 7 章
   * - :math:`V[X]`
     - 分散
     - 第 7 章
   * - :math:`X \sim D`
     - 確率変数 :math:`X` が分布 :math:`D` に従う
     - 第 8 章
   * - :math:`\mathrm{Ber}(p)`、:math:`\mathrm{Bin}(n, p)`
     - ベルヌーイ分布、二項分布
     - 第 8 章
   * - :math:`\mathrm{Geo}(p)`、:math:`\mathrm{NB}(r, p)`
     - 幾何分布、負の二項分布
     - 第 8 章
   * - :math:`\mathrm{Po}(\lambda)`
     - ポアソン分布
     - 第 8 章
   * - :math:`\mathrm{Cov}[X, Y]`
     - 共分散
     - 第 9 章
   * - :math:`\rho[X, Y]`
     - 相関係数
     - 第 9 章
   * - :math:`\overline{X}_n`
     - 標本平均
     - 第 10 章
   * - :math:`N(\mu, \sigma^2)`
     - 期待値 :math:`\mu`、分散 :math:`\sigma^2` の正規分布
     - 第 10 章
   * - :math:`\Phi(z)`
     - 標準正規分布の累積分布関数
     - 第 10 章
   * - :math:`P = (p_{ij})`
     - マルコフ連鎖の遷移行列
     - 第 11 章
   * - :math:`\pi`
     - 定常分布（行ベクトル）
     - 第 11 章
