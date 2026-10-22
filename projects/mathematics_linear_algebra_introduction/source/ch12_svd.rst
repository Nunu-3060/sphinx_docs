第 12 章 特異値分解
===================

固有値分解は正方行列にしか使えず、対角化できない行列もある。特異値分解は、長方形の行列を含むすべての行列に使える分解であり、「線形代数の到達点」と呼ばれることもある。この章では、特異値分解の意味と性質を説明し、低ランク近似による画像の圧縮と、擬似逆行列による最小ノルム解に応用する。

特異値分解
----------

任意の :math:`m \times n` 行列 :math:`A` は、

.. math::

   A = U \Sigma V^\top

と分解できる。ここで、

* :math:`U` は :math:`m` 次の直交行列で、その列 :math:`\bm{u}_1, \ldots, \bm{u}_m` を\ :term:`左特異ベクトル`\ という。
* :math:`V` は :math:`n` 次の直交行列で、その列 :math:`\bm{v}_1, \ldots, \bm{v}_n` を\ :term:`右特異ベクトル`\ という。
* :math:`\Sigma` は :math:`m \times n` の「対角」行列で、対角成分 :math:`\sigma_1 \ge \sigma_2 \ge \cdots \ge 0` を\ :term:`特異値`\ という。対角成分以外はすべて 0 である。

これを\ :term:`特異値分解`\ （singular value decomposition、SVD）という。0 でない特異値の個数は、:math:`A` のランクに等しい。

:math:`A = U\Sigma V^\top` の右から :math:`V` を掛けると :math:`AV = U\Sigma`、つまり列ごとに

.. math::

   A\bm{v}_i = \sigma_i \bm{u}_i

である。固有ベクトルの式 :math:`A\bm{v} = \lambda \bm{v}` と似ているが、入力の方向 :math:`\bm{v}_i` と出力の方向 :math:`\bm{u}_i` が異なってよい。特異値分解は「定義域の正規直交基底 :math:`\bm{v}_i` を、値域の正規直交基底 :math:`\bm{u}_i` の :math:`\sigma_i` 倍に移す」という形で、行列を表している。

幾何学的な意味
--------------

:math:`A\bm{x} = U(\Sigma(V^\top \bm{x}))` と見ると、どんな線形写像も、次の 3 つの変換の合成であることが分かる。

1. :math:`V^\top`：回転（と反射）。右特異ベクトル :math:`\bm{v}_i` を座標軸の方向 :math:`\bm{e}_i` に回す。
2. :math:`\Sigma`：座標軸の方向に、特異値の倍率で拡大縮小する。
3. :math:`U`：回転（と反射）。座標軸の方向を左特異ベクトル :math:`\bm{u}_i` の方向に回す。

:numref:`fig-ch12-svd-geometry` は、次の行列で単位円を変換する過程を 3 段階に分けて描いたものである。緑と赤の矢印は、:math:`\bm{v}_1, \bm{v}_2` とその行き先である。

.. math::

   A = \begin{pmatrix} 3 & 0 \\ 4 & 5 \end{pmatrix}

.. _fig-ch12-svd-geometry:

.. figure:: ../build/figures/ch12_svd_geometry.svg
   :alt: 単位円が、回転、拡大縮小、回転の 3 段階で楕円に変換される様子

   特異値分解による変換の分解。:math:`\sigma_1 = 3\sqrt{5} \approx 6.71`、:math:`\sigma_2 = \sqrt{5} \approx 2.24`

単位円は、最終的に楕円に移る。楕円の長軸の半径が最大の特異値 :math:`\sigma_1`、短軸の半径が最小の特異値 :math:`\sigma_2` であり、軸の方向が左特異ベクトルである。つまり、:math:`\sigma_1` は「:math:`A` がベクトルを最も大きく伸ばす倍率」であり、:math:`\|A\bm{x}\| \le \sigma_1 \|\bm{x}\|` が成り立つ。

サンプルの全体：:download:`ch12_svd_geometry.py <../examples/ch12_svd_geometry.py>`

固有値分解との関係
------------------

:math:`A^\top A` を計算すると、:math:`U^\top U = I` から

.. math::

   A^\top A = V \Sigma^\top U^\top U \Sigma V^\top = V (\Sigma^\top \Sigma) V^\top

となる。これは対称行列 :math:`A^\top A` のスペクトル分解（第 11 章）である。つまり、右特異ベクトルは :math:`A^\top A` の固有ベクトルであり、特異値の 2 乗は :math:`A^\top A` の固有値である。同様に、左特異ベクトルは :math:`AA^\top` の固有ベクトルである。

固有値分解との違いをまとめる。

.. list-table:: 固有値分解と特異値分解
   :header-rows: 1
   :widths: 24 38 38

   * - 項目
     - 固有値分解 :math:`A = PDP^{-1}`
     - 特異値分解 :math:`A = U\Sigma V^\top`
   * - 使える行列
     - 対角化できる正方行列だけ
     - すべての行列（長方形でもよい）
   * - 基底
     - 1 組（:math:`P` の列）。直交するとは限らない
     - 2 組（:math:`U` と :math:`V` の列）。どちらも正規直交
   * - 対角成分
     - 固有値。負や複素数のこともある
     - 特異値。必ず 0 以上の実数
   * - 対称行列の場合
     - :math:`A = Q\Lambda Q^\top`
     - 正定値なら固有値分解と一致する

:numref:`list-ch12-svd` で、2 行 3 列の行列の特異値分解を求める。

.. literalinclude:: ../examples/ch12_svd.py
   :pyobject: report
   :lineno-match:
   :caption: ch12_svd.py の report()
   :name: list-ch12-svd

.. literalinclude:: ../build/outputs/ch12_svd.txt
   :language: text
   :caption: ch12_svd.py の実行結果

``np.linalg.svd()`` は、:math:`U`、特異値の 1 次元の配列、:math:`V^\top` を返す（:math:`V` ではなく転置であることに注意する）。特異値は 5 と 3 で、:math:`A^\top A` の固有値 25、9、0 の平方根になっている。:math:`A` は 2 行 3 列なので、:math:`A^\top A` は 3 次の正方行列であり、ランク 2 なので固有値の 1 つが 0 になる。

サンプルの全体：:download:`ch12_svd.py <../examples/ch12_svd.py>`

低ランク近似
------------

特異値分解を列ごとに書くと、:math:`A` はランク 1 の行列の和で表せる（:math:`r` はランク）。

.. math::

   A = \sigma_1 \bm{u}_1 \bm{v}_1^\top + \sigma_2 \bm{u}_2 \bm{v}_2^\top + \cdots + \sigma_r \bm{u}_r \bm{v}_r^\top

特異値は大きい順に並んでいるので、前のほうの項ほど :math:`A` への寄与が大きい。最初の :math:`k` 項だけを残した

.. math::

   A_k = \sigma_1 \bm{u}_1 \bm{v}_1^\top + \cdots + \sigma_k \bm{u}_k \bm{v}_k^\top

は、ランクが :math:`k` 以下のすべての行列の中で、:math:`A` に最も近い行列である（誤差を、成分の差の 2 乗の和の平方根で測った場合）。これを\ :term:`エッカート・ヤングの定理`\ といい [Eckart1936]_、:math:`A_k` を :math:`A` の\ :term:`低ランク近似`\ という。

低ランク近似の応用として、画像の圧縮を試す。グレースケールの画像は、画素値を成分とする行列とみなせる。:numref:`fig-ch12-image-compression` は、Pillow で図形を描いた 128 × 128 画素の画像を、ランク :math:`k` の行列で近似したものである。

.. _fig-ch12-image-compression:

.. figure:: ../build/figures/ch12_image_compression.svg
   :alt: 元の画像と、ランク 1、5、10、20、40 で近似した画像、特異値のグラフ

   特異値分解による画像の低ランク近似

.. literalinclude:: ../examples/ch12_image_compression.py
   :pyobject: low_rank
   :lineno-match:
   :caption: ch12_image_compression.py の low_rank()

``full_matrices=False`` を指定すると、:math:`U` と :math:`V` の、特異値に対応しない余分な列を省いて計算する。``u[:, :k] * s[:k]`` は、:math:`U` の最初の :math:`k` 列に、それぞれの特異値を掛けたものである（NumPy のブロードキャスト）。

.. literalinclude:: ../build/outputs/ch12_image_compression.txt
   :language: text
   :caption: ch12_image_compression.py の実行結果

ランク :math:`k` の近似を保存するには、:math:`\bm{u}_i`\ （128 個の数）、:math:`\bm{v}_i`\ （128 個の数）、:math:`\sigma_i` を :math:`k` 組保存すればよいので、データ量は :math:`k(m + n + 1)` である。元の画像の :math:`mn` 個に比べると、:math:`k = 20` で約 3 割に減るが、図形の形はほぼ再現できている。特異値のグラフを見ると、最初のいくつかの特異値が大きく、後ろほど小さい。画像の情報の多くが、大きな特異値の成分に集まっていることが分かる。

実際の画像の圧縮（JPEG など）には、特異値分解ではなく、離散コサイン変換などの別の方法が使われる。しかし、低ランク近似の考え方は、データの雑音除去、推薦システム（利用者と商品の評価の行列の近似）、大規模な機械学習のモデルの圧縮などで広く使われている。第 14 章の主成分分析も、低ランク近似の一種である。

サンプルの全体：:download:`ch12_image_compression.py <../examples/ch12_image_compression.py>`

擬似逆行列
----------

長方形の行列や正則でない行列には、逆行列がない。しかし、特異値分解を使うと、逆行列に代わるものを定義できる。

.. math::

   A^{+} = V \Sigma^{+} U^\top

ここで :math:`\Sigma^{+}` は、:math:`\Sigma` を転置し、0 でない特異値をその逆数 :math:`1/\sigma_i` に置き換えた :math:`n \times m` 行列である。:math:`A^{+}` を :math:`A` の\ :term:`擬似逆行列`\ （ムーア・ペンローズの一般逆行列）という。:math:`A` が正則なら :math:`A^{+} = A^{-1}` である。

:math:`\bm{x} = A^{+}\bm{b}` には、次の性質がある。

* 解が存在しない場合（方程式が多すぎる場合）：:math:`\|A\bm{x} - \bm{b}\|` を最小にする最小二乗解になる。
* 解が無数にある場合（未知数が多すぎる場合）：解のうち、ノルム :math:`\|\bm{x}\|` が最小のものになる。

つまり、擬似逆行列は、どのような連立一次方程式に対しても「最も合理的な答え」を 1 つ返す。:numref:`list-ch12-svd` の後半では、2 本の方程式に未知数が 3 つある :math:`A\bm{x} = (5, 5)` を擬似逆行列で解いている。得られた解 :math:`(1, 1, 0)` のノルムは :math:`\sqrt{2} \approx 1.414` である。零空間の基底ベクトル :math:`\bm{v}_3`\ （特異値 0 に対応する右特異ベクトル）を加えた :math:`(1, 1, 0) + \bm{v}_3` も解であるが、ノルムは 1.732 と大きい。第 8 章の :numref:`fig-ch08-solution-structure` のノルム最小の解も、``np.linalg.pinv()`` で求めたものである。

NumPy の ``np.linalg.lstsq()`` も、特異値分解を使って最小二乗解（解が無数にあればノルム最小の解）を求める。小さな特異値の逆数は非常に大きくなり、誤差を拡大するので、どちらの関数も、十分に小さい特異値を 0 とみなして計算する（引数 ``rcond`` で、その基準を指定できる）。

この章のまとめ
--------------

* すべての行列は :math:`A = U\Sigma V^\top` と特異値分解できる。:math:`U` と :math:`V` は直交行列、:math:`\Sigma` の対角成分は 0 以上の特異値である。
* 線形写像は「回転 → 座標軸の方向の拡大縮小 → 回転」に分解できる。単位円は、特異値を半径とする楕円に移る。
* 特異値の 2 乗は :math:`A^\top A` の固有値であり、右特異ベクトルはその固有ベクトルである。
* 大きい方から :math:`k` 個の特異値を残すと、ランク :math:`k` の最良の近似が得られる（エッカート・ヤングの定理）。
* 擬似逆行列 :math:`A^{+} = V\Sigma^{+}U^\top` は、最小二乗解やノルム最小の解を与える。
