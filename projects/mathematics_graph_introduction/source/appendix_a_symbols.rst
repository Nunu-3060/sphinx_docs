付録 A 記号一覧
===============

本書で用いる主な記号を示す。慣例に従い、同じ文字を章によって異なる意味で用いている場合がある。たとえば :math:`\alpha` は独立数 :math:`\alpha(G)`、アッカーマン関数の逆関数 :math:`\alpha(n)`、PageRank の減衰率を、:math:`f` は平面グラフの面数とフローの流量を表す。:math:`\delta` は最小次数のほかに第 13 章で増加量を、:math:`m` は辺数のほかに第 15 章で BA モデルのパラメータを表す。意味は各章の文脈で判断してほしい。

グラフと頂点・辺
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`G = (V, E)`
     - 頂点集合 :math:`V`、辺集合 :math:`E` のグラフ
     - 第 2 章
   * - :math:`V(G)`, :math:`E(G)`
     - グラフ :math:`G` の頂点集合、辺集合
     - 第 2 章
   * - :math:`n`, :math:`m`
     - 頂点数 :math:`|V|`、辺数 :math:`|E|`
     - 第 2 章
   * - :math:`uv`, :math:`\{u, v\}`
     - 頂点 :math:`u` と :math:`v` を結ぶ無向辺
     - 第 2 章
   * - :math:`(u, v)`
     - :math:`u` から :math:`v` への有向辺
     - 第 2 章
   * - :math:`w(e)`, :math:`w(u, v)`
     - 辺の重み
     - 第 2 章
   * - :math:`N(v)`
     - 頂点 :math:`v` の近傍（隣接する頂点の集合）
     - 第 2 章
   * - :math:`N(S)`
     - 頂点集合 :math:`S` のいずれかの頂点に隣接する頂点の集合
     - 第 10 章
   * - :math:`\deg(v)`
     - 頂点 :math:`v` の次数
     - 第 2 章
   * - :math:`\deg^+(v)`, :math:`\deg^-(v)`
     - 有向グラフの出次数、入次数
     - 第 2 章
   * - :math:`\delta(G)`, :math:`\Delta(G)`
     - 最小次数、最大次数
     - 第 2 章
   * - :math:`G[S]`
     - 頂点集合 :math:`S` による誘導部分グラフ
     - 第 2 章
   * - :math:`G - v`, :math:`G - e`
     - 頂点 :math:`v`、辺 :math:`e` を取り除いたグラフ
     - 第 2 章
   * - :math:`G / e`
     - 辺 :math:`e` を縮約したグラフ
     - 第 9 章
   * - :math:`G \cong H`
     - :math:`G` と :math:`H` は同型
     - 第 2 章
   * - :math:`\overline{G}`
     - :math:`G` の補グラフ
     - 第 5 章
   * - :math:`L(G)`
     - :math:`G` の線グラフ
     - 第 5 章
   * - :math:`G^*`
     - 平面グラフ :math:`G` の双対グラフ
     - 第 8 章

代表的なグラフ
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`K_n`
     - :math:`n` 頂点の完全グラフ
     - 第 5 章
   * - :math:`K_{p,q}`
     - 完全二部グラフ
     - 第 5 章
   * - :math:`P_n`
     - :math:`n` 頂点の道グラフ
     - 第 5 章
   * - :math:`C_n`
     - :math:`n` 頂点の閉路グラフ
     - 第 5 章
   * - :math:`Q_d`
     - :math:`d` 次元の超立方体グラフ
     - 第 5 章

グラフの量
----------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`d(u, v)`
     - 頂点 :math:`u` と :math:`v` の距離
     - 第 4 章
   * - :math:`e(v)`
     - 頂点 :math:`v` の離心数
     - 第 4 章
   * - :math:`\kappa(G)`, :math:`\kappa'(G)`
     - 点連結度、辺連結度
     - 第 4 章
   * - :math:`\chi(G)`
     - 彩色数
     - 第 9 章
   * - :math:`\chi'(G)`
     - 辺彩色数
     - 第 9 章
   * - :math:`\omega(G)`
     - クリーク数
     - 第 9 章
   * - :math:`\alpha(G)`
     - 独立数
     - 第 9 章
   * - :math:`P(G, k)`
     - 彩色多項式
     - 第 9 章
   * - :math:`f`
     - 平面グラフの面数
     - 第 8 章
   * - :math:`c(u, v)`, :math:`f(u, v)`
     - フローネットワークの辺の容量、流量
     - 第 13 章
   * - :math:`C_v`
     - 頂点 :math:`v` の局所クラスタ係数
     - 第 15 章
   * - :math:`P(k)`
     - 次数分布（次数が :math:`k` の頂点の割合）
     - 第 15 章

行列
----

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`A`
     - 隣接行列
     - 第 3 章
   * - :math:`B`
     - 接続行列
     - 第 3 章
   * - :math:`D`
     - 次数行列（次数を対角に並べた行列）
     - 第 3 章
   * - :math:`L = D - A`
     - ラプラシアン行列
     - 第 14 章
   * - :math:`\mu_1 \le \cdots \le \mu_n`
     - ラプラシアン行列の固有値
     - 第 14 章
   * - :math:`\mathbf{1}`
     - すべての成分が 1 のベクトル
     - 第 14 章
   * - :math:`J`
     - すべての成分が 1 の行列
     - 第 14 章

計算量
------

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - 記号
     - 意味
     - 初出
   * - :math:`O(f(n))`
     - 定数倍を除いて :math:`f(n)` 以下で抑えられる量
     - 第 1 章
   * - :math:`\alpha(n)`
     - アッカーマン関数の逆関数（Union-Find の計算量に現れる）
     - 第 6 章
