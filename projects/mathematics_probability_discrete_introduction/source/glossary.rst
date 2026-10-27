用語集
======

本書の主な用語を五十音順にまとめる。括弧内は英語表記である。

.. glossary::

   握手補題
      （handshaking lemma）無向グラフの次数の総和が辺の本数の 2 倍に等しいという定理。第 5 章を参照。

   オイラー路
      （Eulerian path）グラフのすべての辺をちょうど 1 回ずつ通る歩道。連結グラフがオイラー路を持つための必要十分条件は、次数が奇数の頂点が 0 個または 2 個であることである。第 5 章を参照。

   確率質量関数
      （probability mass function）離散確率変数 :math:`X` の各値 :math:`x` に確率 :math:`P(X = x)` を対応させる関数。第 7 章を参照。

   確率変数
      （random variable）標本空間の各根元事象に実数を対応させる写像。第 7 章を参照。

   木
      （tree）連結で閉路を持たない無向グラフ。頂点数 :math:`n` の木の辺の本数は :math:`n - 1` である。第 5 章を参照。

   期待値
      （expected value）確率変数のとる値を確率で重み付けした平均 :math:`E[X] = \sum_i x_i P(X = x_i)`。第 7 章を参照。

   共分散
      （covariance）2 つの確率変数の関係の向きと強さを表す量 :math:`\mathrm{Cov}[X, Y] = E[XY] - E[X] E[Y]`。第 9 章を参照。

   組合せ
      （combination）異なる :math:`n` 個のものから、順序を考えずに :math:`r` 個を選んだもの。総数は :math:`\binom{n}{r}`。第 4 章を参照。

   グラフ
      （graph）頂点の集合と、頂点の組を結ぶ辺の集合の組。第 5 章を参照。

   根元事象
      （elementary event）標本空間の 1 つの要素、または 1 つの要素だけからなる事象。第 6 章を参照。

   事象
      （event）標本空間の部分集合。第 6 章を参照。

   指示確率変数
      （indicator random variable）事象 :math:`A` が起これば 1、起こらなければ 0 をとる確率変数 :math:`I_A`。:math:`E[I_A] = P(A)` が成り立つ。第 7 章を参照。

   写像
      （map）集合 :math:`A` の各要素に、集合 :math:`B` の要素をちょうど 1 つ対応させる規則。第 3 章を参照。

   順列
      （permutation）異なる :math:`n` 個のものから :math:`r` 個を選んで 1 列に並べたもの。総数は :math:`P(n, r) = n!/(n - r)!`。第 4 章を参照。

   条件付き確率
      （conditional probability）事象 :math:`B` が起こったという条件のもとでの事象 :math:`A` の確率 :math:`P(A \mid B) = P(A \cap B)/P(B)`。第 6 章を参照。

   遷移行列
      （transition matrix）マルコフ連鎖の遷移確率 :math:`p_{ij}` を並べた行列。各行の和は 1 である。第 11 章を参照。

   全射
      （surjection）値域が終域に一致する写像。第 3 章を参照。

   全単射
      （bijection）単射かつ全射である写像。有限集合の間に全単射があれば、要素数は等しい。第 3 章を参照。

   大数の法則
      （law of large numbers）独立で同じ分布に従う確率変数の標本平均が、試行回数を増やすと期待値に近づくという定理。第 10 章を参照。

   単射
      （injection）異なる要素を異なる要素に移す写像。第 3 章を参照。

   中心極限定理
      （central limit theorem）独立で同じ分布に従う確率変数の和を標準化したものの分布が、標準正規分布に近づくという定理。第 10 章を参照。

   定常分布
      （stationary distribution）マルコフ連鎖の遷移行列 :math:`P` について :math:`\pi P = \pi` を満たす確率分布 :math:`\pi`。第 11 章を参照。

   同値関係
      （equivalence relation）反射律・対称律・推移律を満たす関係。集合を互いに素な同値類に分割する。第 3 章を参照。

   独立
      （independence）事象 :math:`A, B` について :math:`P(A \cap B) = P(A) P(B)` が成り立つこと。確率変数 :math:`X, Y` については、すべての :math:`x, y` で :math:`P(X = x, Y = y) = P(X = x) P(Y = y)` が成り立つこと。第 6 章、第 9 章を参照。

   二項係数
      （binomial coefficient）組合せの総数 :math:`\binom{n}{r}`。二項定理の係数として現れる。第 4 章を参照。

   二部グラフ
      （bipartite graph）頂点集合を 2 つに分割し、すべての辺が異なる側の頂点を結ぶようにできるグラフ。第 5 章を参照。

   鳩の巣原理
      （pigeonhole principle） :math:`n + 1` 個のものを :math:`n` 個の箱に入れると、2 個以上入る箱が存在するという原理。第 4 章を参照。

   半順序
      （partial order）反射律・反対称律・推移律を満たす関係。第 3 章を参照。

   標本空間
      （sample space）試行の結果として起こりうるもの全体の集合 :math:`\Omega`。第 6 章を参照。

   分散
      （variance）確率変数の値のばらつきの大きさを表す量 :math:`V[X] = E[(X - E[X])^2]`。第 7 章を参照。

   包除原理
      （inclusion-exclusion principle）和集合の要素数を、各集合とその共通部分の要素数の符号付きの和で表す公式。第 4 章を参照。

   マルコフ連鎖
      （Markov chain）次の状態の分布が現在の状態だけで決まる確率過程。第 11 章を参照。

   命題
      （proposition）真か偽かが明確に定まる文。第 2 章を参照。

   累積分布関数
      （cumulative distribution function）確率変数 :math:`X` について :math:`F_X(x) = P(X \le x)` で定まる関数。第 7 章を参照。
