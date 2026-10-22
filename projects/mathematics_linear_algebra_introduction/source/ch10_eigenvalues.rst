第 10 章 固有値と固有ベクトル
=============================

行列による変換では、ほとんどのベクトルの向きが変わる。しかし、特別な方向のベクトルだけは、向きを変えずに伸び縮みするだけである。この方向が固有ベクトル、伸び縮みの倍率が固有値である。この章では、固有値と固有ベクトルの意味と求め方、対角化を説明し、漸化式、マルコフ連鎖、振動の問題に応用する。

固有値と固有ベクトル
--------------------

:math:`n` 次の正方行列 :math:`A` について、

.. math::

   A\bm{v} = \lambda \bm{v} \qquad (\bm{v} \ne \bm{0})

を満たす数 :math:`\lambda` と 0 でないベクトル :math:`\bm{v}` があるとき、:math:`\lambda` を :math:`A` の\ :term:`固有値`\ 、:math:`\bm{v}` を固有値 :math:`\lambda` に対する\ :term:`固有ベクトル`\ という。

:math:`A\bm{v} = \lambda \bm{v}` は、「:math:`\bm{v}` を :math:`A` で変換しても、向きが変わらず（または真逆になり）、長さが :math:`\lambda` 倍になるだけ」という意味である。:numref:`fig-ch10-eigen-geometry` は、次の行列 :math:`A` で、単位円の上のベクトルを変換したものである。

.. math::

   A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}

.. _fig-ch10-eigen-geometry:

.. figure:: ../build/figures/ch10_eigen_geometry.svg
   :alt: いろいろな向きのベクトルとその像のうち、固有ベクトルの方向のものだけが同じ直線の上にある様子と、単位円が楕円に移る様子

   ベクトルとその像（左）、単位円とその像（右）

左の図で、青の矢印 :math:`\bm{v}` と橙の矢印 :math:`A\bm{v}` は、ほとんどが異なる向きを向いている。しかし、点線で示した 2 つの方向では、緑の矢印（:math:`\bm{v}`）と赤の矢印（:math:`A\bm{v}`）が同じ直線の上にある。これが固有ベクトルの方向であり、:math:`(1, 1)` 方向は 5 倍に、:math:`(1, -2)` 方向は 2 倍になる。

固有ベクトルを何倍しても固有ベクトルである（:math:`A(c\bm{v}) = \lambda (c\bm{v})`）。そのため、固有ベクトルは「方向」として決まり、長さや符号は任意である。NumPy などのライブラリは、通常、ノルムが 1 の固有ベクトルを返す。

固有値の求め方
--------------

:math:`A\bm{v} = \lambda \bm{v}` は :math:`(A - \lambda I)\bm{v} = \bm{0}` と書き直せる。これが :math:`\bm{0}` でない解 :math:`\bm{v}` を持つのは、:math:`A - \lambda I` が正則でないとき、つまり

.. math::

   \det(A - \lambda I) = 0

のときである（第 6 章）。これを :math:`A` の\ :term:`固有方程式`\ （特性方程式）という。左辺は :math:`\lambda` の :math:`n` 次の多項式なので、固有値は（重複や複素数を含めて）:math:`n` 個ある。

上の :math:`A` で計算してみる。

.. math::

   \det(A - \lambda I) = \det \begin{pmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{pmatrix}
   = (4 - \lambda)(3 - \lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2)

なので、固有値は :math:`\lambda = 5, 2` である。固有ベクトルは、それぞれの :math:`\lambda` について :math:`(A - \lambda I)\bm{v} = \bm{0}` を解いて求める。

* :math:`\lambda = 5`：:math:`\begin{pmatrix} -1 & 1 \\ 2 & -2 \end{pmatrix} \bm{v} = \bm{0}` から :math:`\bm{v} = (1, 1)`
* :math:`\lambda = 2`：:math:`\begin{pmatrix} 2 & 1 \\ 2 & 1 \end{pmatrix} \bm{v} = \bm{0}` から :math:`\bm{v} = (1, -2)`

固有値には、次の便利な性質がある（:math:`\lambda_1, \ldots, \lambda_n` は重複を含めた固有値）。

* 固有値の和は、対角成分の和（\ :term:`トレース`\ 、:math:`\mathrm{tr}\,A`）に等しい。例では :math:`5 + 2 = 4 + 3`。
* 固有値の積は、行列式に等しい。例では :math:`5 \times 2 = 4 \cdot 3 - 1 \cdot 2`。
* したがって、固有値に 0 があることと、:math:`A` が正則でないことは同値である。
* 三角行列の固有値は、対角成分である。

固有方程式を解く方法は、2 次や 3 次の手計算では使えるが、5 次以上の多項式には解の公式がないので、一般の行列には使えない。数値計算では、QR 法などの反復法で固有値を求める。NumPy の ``np.linalg.eig()`` は、LAPACK のこのような方法を使っている。

.. literalinclude:: ../examples/ch10_eigen.py
   :pyobject: report
   :lineno-match:
   :caption: ch10_eigen.py の report()
   :name: list-ch10-eigen

.. literalinclude:: ../build/outputs/ch10_eigen.txt
   :language: text
   :caption: ch10_eigen.py の実行結果

``np.linalg.eig()`` は、固有値の配列と、固有ベクトルを列に並べた行列を返す。固有ベクトルは正規化されているので、:math:`(1, 1)` は :math:`(0.7071, 0.7071)` に、:math:`(1, -2)` は符号が反転して :math:`(-0.4472, 0.8944)` になっている。どちらも同じ方向を表す。また、``np.linalg.eig()`` は結果を複素数の配列で返すことがあるので、サンプルでは ``np.real_if_close()`` で、虚部が 0 なら実数の配列に変換している。

サンプルの全体：:download:`ch10_eigen.py <../examples/ch10_eigen.py>`、:download:`ch10_eigen_geometry.py <../examples/ch10_eigen_geometry.py>`

対角化
------

:math:`n` 次の正方行列 :math:`A` が線形独立な :math:`n` 本の固有ベクトル :math:`\bm{v}_1, \ldots, \bm{v}_n` を持つとき、それらを列に並べた行列 :math:`P` と、固有値を対角成分に並べた対角行列 :math:`D` を使って

.. math::

   AP = PD, \qquad \text{つまり} \qquad A = PDP^{-1}, \quad P^{-1}AP = D

と書ける。:math:`AP` の :math:`j` 列目は :math:`A\bm{v}_j = \lambda_j \bm{v}_j` であり、:math:`PD` の :math:`j` 列目も :math:`\lambda_j \bm{v}_j` だからである。これを :math:`A` の\ :term:`対角化`\ という。

第 7 章の言葉では、:math:`P^{-1}AP` は「固有ベクトルを基底とする座標で見た :math:`A`」である。固有ベクトルの座標系では、変換は「各軸の方向に固有値倍するだけ」という最も簡単な形になる。

対角化の効果が最もよく分かるのは、行列のべき乗である。

.. math::

   A^k = (PDP^{-1})(PDP^{-1}) \cdots (PDP^{-1}) = PD^kP^{-1}, \qquad
   D^k = \begin{pmatrix} \lambda_1^k & & \\ & \ddots & \\ & & \lambda_n^k \end{pmatrix}

途中の :math:`P^{-1}P` が消えるので、:math:`A^k` は固有値を :math:`k` 乗するだけで計算できる。:numref:`list-ch10-eigen` の実行結果では、:math:`PD^{10}P^{-1}` と ``np.linalg.matrix_power(a, 10)`` が一致している。また、:math:`k` が大きくなると、:math:`A^k` は絶対値が最大の固有値の項が支配的になる。この性質は、マルコフ連鎖や PageRank（第 14 章）で使う。

すべての行列が対角化できるわけではない。例えば :math:`\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}` は、固有値が 1（重複）で、固有ベクトルは :math:`(1, 0)` 方向しかないので、:math:`P` を作れない。ただし、固有値がすべて異なる行列は必ず対角化でき、第 11 章で扱う対称行列も必ず対角化できる。工学で現れる行列の多くは、どちらかに当てはまる。

固有値が複素数になる場合
------------------------

90 度の回転 :math:`R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}` は、すべてのベクトルの向きを変えるので、実数の固有ベクトルを持たない。固有方程式は :math:`\lambda^2 + 1 = 0` であり、固有値は :math:`\pm i`\ （虚数単位）になる（:numref:`list-ch10-eigen` の実行結果の最後の行）。一般に、固有値が複素数になることは、変換に回転の成分が含まれることを表す。本書では、複素数の固有値はこの例で触れるだけにする。

例：フィボナッチ数列
--------------------

フィボナッチ数列 :math:`F_0 = 0, F_1 = 1, F_{n+1} = F_n + F_{n-1}` は、ベクトルと行列で次のように書ける。

.. math::

   \begin{pmatrix} F_{n+1} \\ F_n \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} F_n \\ F_{n-1} \end{pmatrix}

したがって :math:`(F_{n+1}, F_n) = A^n (F_1, F_0)` であり、:math:`A^n` の (1, 2) 成分が :math:`F_n` である。:math:`A` の固有値は :math:`\phi = (1 + \sqrt{5})/2 \approx 1.618`\ （黄金比）と :math:`\psi = (1 - \sqrt{5})/2 \approx -0.618` で、対角化すると一般項

.. math::

   F_n = \frac{\phi^n - \psi^n}{\sqrt{5}}

が得られる（ビネの公式）。:math:`|\psi| < 1` なので、:math:`n` が大きいと :math:`F_n \approx \phi^n / \sqrt{5}` であり、フィボナッチ数列は公比 :math:`\phi` の等比数列のように増える。

.. literalinclude:: ../examples/ch10_fibonacci.py
   :pyobject: report
   :lineno-match:
   :caption: ch10_fibonacci.py の report()

.. literalinclude:: ../build/outputs/ch10_fibonacci.txt
   :language: text
   :caption: ch10_fibonacci.py の実行結果

:math:`F_{80}` では、ビネの公式の結果が正しい値とずれている。浮動小数点数の有効数字は約 16 桁なので、17 桁の整数は正確に表せないからである。整数の行列でべき乗を計算した結果は正確である（ただし、64 ビット整数で表せる :math:`F_{92}` まで）。

サンプルの全体：:download:`ch10_fibonacci.py <../examples/ch10_fibonacci.py>`

例：マルコフ連鎖
----------------

天気が「晴れ」「曇り」「雨」の 3 つの状態を、次の確率で移り変わるとする。行列 :math:`P` の :math:`j` 列目は、今日の天気が :math:`j` 番目の状態のときの、明日の天気の確率である。各列の和は 1 である。

.. math::

   P = \begin{pmatrix} 0.7 & 0.3 & 0.2 \\ 0.2 & 0.4 & 0.3 \\ 0.1 & 0.3 & 0.5 \end{pmatrix}
   \quad
   \begin{matrix} \leftarrow \text{明日が晴れ} \\ \leftarrow \text{明日が曇り} \\ \leftarrow \text{明日が雨} \end{matrix}

今日の天気の確率分布を :math:`\bm{x}_0` とすると、:math:`k` 日後の分布は :math:`\bm{x}_k = P^k \bm{x}_0` である。このように、次の状態の確率が現在の状態だけで決まる過程を\ :term:`マルコフ連鎖`\ 、:math:`P` を\ :term:`推移行列`\ という。

:numref:`fig-ch10-markov` のように、分布は日数とともに一定の分布に近づく。今日が晴れでも雨でも、行き着く先は同じである。

.. _fig-ch10-markov:

.. figure:: ../build/figures/ch10_markov.svg
   :alt: 晴れから始めた場合と雨から始めた場合の、各天気の確率の変化。どちらも同じ値に近づく

   天気の確率分布の変化。点線は定常分布

行き着く先の分布 :math:`\bm{\pi}` は、:math:`P\bm{\pi} = \bm{\pi}` を満たす。つまり、固有値 1 の固有ベクトルである。これを\ :term:`定常分布`\ という。各列の和が 1 で、成分が正の推移行列は、必ず固有値 1 を持ち、他の固有値の絶対値は 1 より小さい。そのため、:math:`P^k \bm{x}_0` を固有ベクトルで展開すると、固有値 1 の成分だけが残り、他の成分は :math:`k` とともに 0 に近づく。

.. literalinclude:: ../examples/ch10_markov.py
   :pyobject: steady_state
   :lineno-match:
   :caption: ch10_markov.py の steady_state()

.. literalinclude:: ../build/outputs/ch10_markov.txt
   :language: text
   :caption: ch10_markov.py の実行結果

固有値は 1、0.4732、0.1268 である。2 番目に大きい固有値の絶対値 0.4732 が、定常分布に近づく速さを決める（1 日ごとに、定常分布とのずれがおよそ 0.47 倍になる）。

サンプルの全体：:download:`ch10_markov.py <../examples/ch10_markov.py>`

例：ばねと質点の振動
--------------------

2 つの質点（質量 :math:`m`）を 3 本のばね（ばね定数 :math:`k`）で「壁 - ばね - 質点 1 - ばね - 質点 2 - ばね - 壁」とつないだ系を考える。質点の変位を :math:`x_1, x_2` とすると、運動方程式は次のようになる。

.. math::

   m \ddot{x}_1 = -k x_1 + k (x_2 - x_1), \qquad m \ddot{x}_2 = -k (x_2 - x_1) - k x_2

:math:`m = k = 1` とし、ベクトルで書くと次のようになる。:math:`\ddot{\bm{x}}` は時間による 2 階微分（加速度）である。

.. math::

   \ddot{\bm{x}} = -K\bm{x}, \qquad K = \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}

2 つの質点の運動は、ばねを通じて互いに影響し合う（連成している）ので、このままでは解きにくい。そこで、:math:`K` の固有ベクトル :math:`\bm{v}` の方向の運動 :math:`\bm{x}(t) = q(t)\,\bm{v}` を考えると、:math:`\ddot{q}\,\bm{v} = -q K\bm{v} = -\lambda q\,\bm{v}` なので、:math:`\ddot{q} = -\lambda q` という 1 つの単振動の方程式になる。角振動数は :math:`\omega = \sqrt{\lambda}` である。

.. literalinclude:: ../build/outputs/ch10_vibration.txt
   :language: text
   :caption: ch10_vibration.py の実行結果

固有値は 1 と 3 で、次の 2 つの振動の仕方（\ :term:`固有モード`\ ）がある。

* モード 1：固有ベクトル :math:`(1, 1)` 方向。2 つの質点が同じ向きに動き、角振動数は :math:`\omega_1 = 1` である。
* モード 2：固有ベクトル :math:`(1, -1)` 方向。2 つの質点が逆向きに動き、中央のばねが大きく伸び縮みするので、角振動数は :math:`\omega_2 = \sqrt{3}` と高い。

任意の運動は、2 つの固有モードの重ね合わせで表せる。:numref:`fig-ch10-vibration` は、質点 1 だけを 1 だけずらして静かに離した場合の運動である。各質点の変位は複雑に見えるが、固有モードの座標（:math:`q_1, q_2`）に分けると、それぞれ単純な単振動である。

.. _fig-ch10-vibration:

.. figure:: ../build/figures/ch10_vibration.svg
   :alt: 2 つの質点の変位の時間変化と、2 つの固有モードの座標の時間変化

   ばねと質点の振動。各質点の変位（上）と固有モードの座標（下）

.. literalinclude:: ../examples/ch10_vibration.py
   :pyobject: displacement
   :lineno-match:
   :caption: ch10_vibration.py の displacement()

``K`` は対称行列なので、固有ベクトルを求めるのに ``np.linalg.eigh()`` を使っている（第 11 章）。固有ベクトルを列に並べた行列は直交行列になるので、初期変位の固有モードの座標は、転置を掛けるだけで求められる（第 9 章）。

この考え方は、建物や橋、機械の振動解析の基本である。自由度が数万の構造物でも、剛性行列と質量行列の固有値問題を解いて固有振動数と固有モードを求め、外から加わる振動の周波数が固有振動数と一致しないか（共振しないか）を調べる。

サンプルの全体：:download:`ch10_vibration.py <../examples/ch10_vibration.py>`

この章のまとめ
--------------

* 固有ベクトルは、行列で変換しても向きが変わらないベクトルであり、固有値はその伸び縮みの倍率である。
* 固有値は、固有方程式 :math:`\det(A - \lambda I) = 0` の解である。固有値の和はトレース、積は行列式に等しい。
* 線形独立な固有ベクトルが :math:`n` 本あれば、:math:`A = PDP^{-1}` と対角化でき、:math:`A^k = PD^kP^{-1}` と計算できる。
* 固有値と固有ベクトルは、漸化式の一般項、マルコフ連鎖の定常分布、振動の固有モードの計算に使われる。
