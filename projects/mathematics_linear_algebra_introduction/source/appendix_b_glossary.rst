付録 B 用語集
=============

本書で使う主な用語を、英数字、五十音の順に並べる。括弧内は英語の表記である。

.. glossary::

   BLAS
      Basic Linear Algebra Subprograms。ベクトルと行列の基本的な演算（内積、行列とベクトルの積、行列の積など）を行う関数の標準的な仕様と、その実装。NumPy の行列の積はこれを呼び出す。

   LAPACK
      Linear Algebra PACKage。連立一次方程式、固有値問題、特異値分解などを解く数値計算ライブラリ。BLAS の上に作られている。

   LU 分解
      （LU decomposition）正方行列を、下三角行列 :math:`L` と上三角行列 :math:`U` の積 :math:`A = LU` に分解すること。ガウスの消去法の前進消去を記録したものにあたる。

   PageRank
      リンクの構造から、Web ページの重要度を求める方法。ランダムにリンクをたどる過程の定常分布として、推移行列の固有値 1 の固有ベクトルを求める。

   QR 分解
      （QR decomposition）行列を、列が正規直交な行列 :math:`Q` と上三角行列 :math:`R` の積 :math:`A = QR` に分解すること。

   悪条件
      （ill-conditioned）条件数が大きく、入力のわずかな誤差が、解の大きな誤差になる問題や行列の性質。

   アフィン変換
      （affine transformation）線形写像と平行移動を組み合わせた変換 :math:`\bm{x} \mapsto A\bm{x} + \bm{t}`。同次座標を使うと、行列の積で表せる。

   一般解
      （general solution）連立一次方程式のすべての解を表す式。特殊解に、同次方程式の解（零空間のベクトル）を加えた形で表される。

   エッカート・ヤングの定理
      （Eckart–Young theorem）特異値分解で大きい方から :math:`k` 個の特異値を残した行列が、ランク :math:`k` 以下の行列の中で元の行列に最も近いという定理。

   外積
      （cross product）3 次元のベクトル :math:`\bm{a}, \bm{b}` から作られる、両方に直交し、長さが平行四辺形の面積に等しいベクトル :math:`\bm{a} \times \bm{b}`。ベクトル積とも呼ぶ。

   ガウスの消去法
      （Gaussian elimination）行基本変形で係数行列を上三角行列にし（前進消去）、下の行から順に未知数を求める（後退代入）、連立一次方程式の解法。

   拡大係数行列
      （augmented matrix）連立一次方程式の係数行列 :math:`A` の右に、右辺のベクトル :math:`\bm{b}` を並べた行列 :math:`(A \mid \bm{b})`。

   重ね合わせの原理
      （superposition principle）入力の和に対する出力が出力の和になり、入力の定数倍に対する出力が出力の定数倍になるという性質。線形性と同じ意味である。

   擬似逆行列
      （pseudoinverse）特異値分解を使って :math:`A^{+} = V\Sigma^{+}U^\top` と定義される、逆行列を一般化した行列。:math:`A^{+}\bm{b}` は、最小二乗解のうちノルムが最小のものを与える。ムーア・ペンローズの一般逆行列とも呼ぶ。

   基底
      （basis）ベクトル空間を張る、線形独立なベクトルの組。

   共分散行列
      （covariance matrix）多変数のデータについて、各変数の分散を対角成分に、2 つの変数の共分散を非対角成分に並べた対称行列。半正定値である。

   寄与率
      （explained variance ratio）主成分分析で、全体の分散に対する、ある主成分の分散（固有値）の割合。

   逆行列
      （inverse matrix）正方行列 :math:`A` に対して :math:`AA^{-1} = A^{-1}A = I` を満たす行列 :math:`A^{-1}`。:math:`A` による変換を元に戻す変換を表す。

   行
      （row）行列の横の並び。

   行基本変形
      （elementary row operations）行列の行に対する 3 つの操作（ある行に別の行の定数倍を加える、2 つの行を入れ替える、ある行に 0 でない数を掛ける）。連立一次方程式の解を変えない。

   行ベクトル
      （row vector）成分を横に並べたベクトル。:math:`1 \times n` 行列とみなせる。

   行列
      （matrix）数を縦と横の長方形に並べたもの。線形写像を表す。

   行列式
      （determinant）正方行列から決まる数 :math:`\det A`。線形写像による面積や体積の符号付きの拡大率を表し、0 でないことと正則であることが同値である。

   クラメールの公式
      （Cramer's rule）連立一次方程式の解を、行列式の比で表す公式。理論的には重要だが、計算量が大きいので数値計算には使わない。

   グラム・シュミットの直交化
      （Gram–Schmidt process）線形独立なベクトルの組から、各ベクトルからそれまでに作った方向の成分を引いて正規化することで、同じ空間を張る正規直交系を作る方法。

   計算機イプシロン
      （machine epsilon）1 に加えたときに 1 と区別できる最小の正の浮動小数点数。倍精度では約 :math:`2.2 \times 10^{-16}`。

   係数行列
      （coefficient matrix）連立一次方程式 :math:`A\bm{x} = \bm{b}` の、未知数の係数を並べた行列 :math:`A`。

   桁落ち
      （loss of significance）近い値どうしの引き算で、有効数字の多くが失われること。

   コーシー・シュワルツの不等式
      （Cauchy–Schwarz inequality）任意のベクトル :math:`\bm{u}, \bm{v}` について :math:`|\bm{u} \cdot \bm{v}| \le \|\bm{u}\|\,\|\bm{v}\|` が成り立つという不等式。

   コサイン類似度
      （cosine similarity）2 つのベクトルのなす角の余弦 :math:`\bm{u} \cdot \bm{v} / (\|\bm{u}\|\,\|\bm{v}\|)`。向きの近さを -1 から 1 の値で表す。

   固有値
      （eigenvalue）正方行列 :math:`A` について :math:`A\bm{v} = \lambda \bm{v}` を満たす 0 でないベクトル :math:`\bm{v}` があるときの数 :math:`\lambda`。固有ベクトルの伸び縮みの倍率である。

   固有ベクトル
      （eigenvector）正方行列 :math:`A` について :math:`A\bm{v} = \lambda \bm{v}` を満たす 0 でないベクトル :math:`\bm{v}`。変換しても向きが変わらない（または真逆になる）ベクトルである。

   固有方程式
      （characteristic equation）固有値を求めるための方程式 :math:`\det(A - \lambda I) = 0`。特性方程式とも呼ぶ。

   固有モード
      （normal mode）振動系の、すべての部分が同じ振動数で振動する振動の仕方。固有値問題の固有ベクトルとして求められる。

   コレスキー分解
      （Cholesky decomposition）正定値の対称行列を、下三角行列 :math:`L` を使って :math:`A = LL^\top` と分解すること。

   最小二乗法
      （least squares method）残差の 2 乗の和を最小にする解を求める方法。正規方程式、QR 分解、特異値分解で解く。

   左特異ベクトル
      （left singular vector）特異値分解 :math:`A = U\Sigma V^\top` の :math:`U` の列ベクトル。:math:`AA^\top` の固有ベクトルである。

   座標
      （coordinates）基底を決めたときに、ベクトルを基底ベクトルの線形結合で表す係数を並べたもの。

   次元
      （dimension）ベクトル空間の基底を構成するベクトルの本数。

   次元定理
      （rank–nullity theorem）:math:`m \times n` 行列について、ランクと零空間の次元の和が :math:`n` に等しいという定理。ランク・退化次数の定理とも呼ぶ。

   射影行列
      （projection matrix）ベクトルを部分空間に正射影する行列 :math:`P`。:math:`P^2 = P`、:math:`P^\top = P` を満たす。

   写像
      （map）ある集合の要素を、別の（または同じ）集合の要素に対応させる規則。本書では、ベクトルをベクトルに移す関数を指す。

   自由変数
      （free variable）被約階段行列でピボットのない列に対応する変数。任意の値を取れる。

   主軸
      （principal axes）二次形式の対称行列の固有ベクトルの方向。主軸の座標では、二次形式は 2 乗の和になる。

   主成分分析
      （principal component analysis、PCA）共分散行列の固有ベクトル（データ行列の特異ベクトル）でデータの分散が大きい方向を求め、少ない方向でデータを要約する方法。

   条件数
      （condition number）行列の最大の特異値と最小の特異値の比 :math:`\kappa(A)`。入力の相対誤差が解で何倍に拡大されうるかを表す。

   推移行列
      （transition matrix）マルコフ連鎖で、ある状態から別の状態に移る確率を並べた行列。本書では、各列の和が 1 になるように並べる。

   スカラー
      （scalar）ベクトルや行列と区別して、ただの数を指す言葉。

   スペクトル分解
      （spectral decomposition）対称行列を、直交行列 :math:`Q` と対角行列 :math:`\Lambda` で :math:`A = Q\Lambda Q^\top` と表すこと。各固有ベクトルの方向への射影行列の、固有値による重み付きの和とも見られる。

   正規化
      （normalization）0 でないベクトルを、そのノルムで割って単位ベクトルにすること。

   正規直交基底
      （orthonormal basis）正規直交系である基底。座標が内積で求められる。

   正規直交系
      （orthonormal set）どの 2 つも互いに直交し、それぞれのノルムが 1 であるベクトルの組。

   正規方程式
      （normal equations）最小二乗法の解が満たす方程式 :math:`A^\top A \hat{\bm{x}} = A^\top \bm{b}`。

   正射影
      （orthogonal projection）ベクトルから、直線や部分空間に垂線を下ろしたときの足。部分空間の上で、元のベクトルに最も近い点である。

   正則行列
      （regular matrix、invertible matrix）逆行列を持つ正方行列。行列式が 0 でない行列である。

   正定値
      （positive definite）0 でないすべての :math:`\bm{x}` について :math:`\bm{x}^\top A \bm{x} > 0` となる対称行列 :math:`A` の性質。固有値がすべて正であることと同値である。

   成分
      （component、entry）ベクトルや行列を構成する個々の数。

   正方行列
      （square matrix）行と列の数が等しい行列。

   線形
      （linear）重ね合わせの原理が成り立つこと。

   線形結合
      （linear combination）ベクトルのスカラー倍の和 :math:`c_1 \bm{v}_1 + \cdots + c_k \bm{v}_k`。一次結合とも呼ぶ。

   線形写像
      （linear map）重ね合わせの原理を満たす写像。行列の積で表せる。入力と出力の空間が同じものを線形変換とも呼ぶ。

   線形従属
      （linearly dependent）ベクトルの組のうち、どれかが他のベクトルの線形結合で表せること。一次従属とも呼ぶ。

   線形独立
      （linearly independent）ベクトルの組のうち、どれも他のベクトルの線形結合で表せないこと。:math:`c_1 \bm{v}_1 + \cdots + c_k \bm{v}_k = \bm{0}` となる係数がすべて 0 の場合に限ることと同値である。一次独立とも呼ぶ。

   像
      （image）線形写像の行き先全体の集合。行列の列空間に等しい。

   疎行列
      （sparse matrix）成分のほとんどが 0 である行列。0 でない成分だけを保存して扱う。

   第 1 主成分
      （first principal component）主成分分析で、データの分散が最大になる方向。共分散行列の最大の固有値の固有ベクトルである。

   対角化
      （diagonalization）正方行列 :math:`A` を、固有ベクトルを並べた行列 :math:`P` と固有値を並べた対角行列 :math:`D` で :math:`A = PDP^{-1}` と表すこと。

   対角行列
      （diagonal matrix）対角成分以外がすべて 0 の正方行列。

   対称行列
      （symmetric matrix）:math:`A^\top = A` を満たす正方行列。

   単位行列
      （identity matrix）対角成分がすべて 1 で、他の成分が 0 の正方行列 :math:`I`。

   単位ベクトル
      （unit vector）ノルムが 1 のベクトル。

   ダンピング係数
      （damping factor）PageRank で、リンクをたどる確率 :math:`d`。残りの確率 :math:`1 - d` で、すべてのページから等確率でページを選ぶ。

   置換行列
      （permutation matrix）単位行列の行（または列）を並べ替えた行列。掛けると行や列が並べ替わる。

   中心化
      （centering）データの各変数から、その平均を引くこと。

   直交
      （orthogonal）2 つのベクトルの内積が 0 であること。なす角が直角であることを意味する。

   直交行列
      （orthogonal matrix）列ベクトルが正規直交基底をなす正方行列 :math:`Q`。:math:`Q^\top Q = I` を満たし、長さと角度を変えない（回転と反射）。

   定常分布
      （stationary distribution）マルコフ連鎖で、推移しても変わらない確率分布。推移行列の固有値 1 の固有ベクトルである。

   低ランク近似
      （low-rank approximation）行列を、ランクの小さい行列で近似すること。特異値分解で大きい特異値の成分だけを残すと、最良の近似が得られる。

   転置行列
      （transpose）行列の行と列を入れ替えた行列 :math:`A^\top`。

   透視投影
      （perspective projection）3 次元の点を、カメラからの距離で割って画面に投影する方法。遠くのものほど小さく描かれる。

   同次座標
      （homogeneous coordinates）:math:`n` 次元の点に 1 つ成分を加えて :math:`n + 1` 次元のベクトルで表す方法。平行移動や透視投影を行列の積で表せる。

   特異値
      （singular value）特異値分解 :math:`A = U\Sigma V^\top` の :math:`\Sigma` の対角成分。0 以上の実数で、:math:`A^\top A` の固有値の平方根である。

   特異値分解
      （singular value decomposition、SVD）任意の行列を、直交行列 :math:`U, V` と対角成分が特異値の行列 :math:`\Sigma` で :math:`A = U\Sigma V^\top` と分解すること。

   特殊解
      （particular solution）連立一次方程式の解のうちの 1 つ。

   トレース
      （trace）正方行列の対角成分の和 :math:`\mathrm{tr}\,A`。固有値の和に等しい。

   内積
      （inner product、dot product）2 つのベクトルの成分の積の和 :math:`\bm{u} \cdot \bm{v}`。:math:`\|\bm{u}\|\,\|\bm{v}\|\cos\theta` に等しい。

   二次形式
      （quadratic form）対称行列 :math:`A` とベクトル :math:`\bm{x}` から作られる数 :math:`\bm{x}^\top A \bm{x}`。すべての項が 2 次の多項式である。

   ノルム
      （norm）ベクトルの長さ :math:`\|\bm{v}\| = \sqrt{\bm{v} \cdot \bm{v}}`。

   張る空間
      （span）ベクトルの組の線形結合全体の集合。部分空間になる。

   反復法
      （iterative method）近似解を繰り返し改良して、連立一次方程式などを解く方法。共役勾配法など。大規模な疎行列に使われる。

   ピボット
      （pivot）ガウスの消去法で、下の行の成分を消去するのに使う対角成分。被約階段行列では、各行の最初の 0 でない成分を指す。

   被約階段行列
      （reduced row echelon form、RREF）行基本変形で得られる、ピボットが 1 で、ピボットのある列の他の成分がすべて 0 の階段状の行列。

   標準基底
      （standard basis）基本ベクトル :math:`\bm{e}_1, \ldots, \bm{e}_n` からなる :math:`\mathbb{R}^n` の基底。

   ヒルベルト行列
      （Hilbert matrix）:math:`(i, j)` 成分が :math:`1/(i + j - 1)` の行列。悪条件の行列の代表例である。

   浮動小数点数
      （floating-point number）有限の桁数の仮数と指数で実数を近似して表す、コンピューターの数の表現。

   部分空間
      （subspace）ベクトル空間の部分集合で、和とスカラー倍について閉じているもの。必ず原点を含む。

   部分ピボット選択
      （partial pivoting）ガウスの消去法で、各列の消去の前に、その列で絶対値が最大の成分を持つ行をピボットの行に選ぶこと。

   ヘッセ行列
      （Hessian matrix）多変数関数の 2 階の偏導関数を並べた対称行列。極値の判定に使う。

   べき乗法
      （power iteration）ベクトルに行列を繰り返し掛けて、絶対値が最大の固有値の固有ベクトルを求める方法。

   ベクトル
      （vector）大きさと向きを持つ量。数の組として表す。

   ベクトル空間
      （vector space）和とスカラー倍が定義され、通常の計算の規則を満たす集合。本書では :math:`\mathbb{R}^n` とその部分空間を扱う。

   マルコフ連鎖
      （Markov chain）次の状態の確率が、現在の状態だけで決まる確率的な過程。

   丸め誤差
      （rounding error）実数を有限の桁数の浮動小数点数で表すときに生じる誤差。

   右特異ベクトル
      （right singular vector）特異値分解 :math:`A = U\Sigma V^\top` の :math:`V` の列ベクトル。:math:`A^\top A` の固有ベクトルである。

   余因子展開
      （cofactor expansion）行列式を、1 つの行（または列）の成分と、1 つ小さい行列式の積の和で表す方法。

   ランク
      （rank）行列の線形独立な列ベクトル（行ベクトル）の最大の本数。列空間の次元に等しい。階数とも呼ぶ。

   零空間
      （null space）:math:`A\bm{x} = \bm{0}` を満たす :math:`\bm{x}` 全体の集合。核とも呼ぶ。

   列
      （column）行列の縦の並び。

   列空間
      （column space）行列の列ベクトルが張る空間。:math:`A\bm{x}` の形で表せるベクトル全体である。

   列ベクトル
      （column vector）成分を縦に並べたベクトル。:math:`n \times 1` 行列とみなせる。本書では、ベクトルは列ベクトルとする。
