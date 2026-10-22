.. _appendix-c:

付録 C 用語集
=============

本書で使った主な用語を、部ごとに本文に出てきた順に並べる。用語の後に英語の表記を示す。

はじめに・第 I 部 準備
----------------------

.. glossary::

   スカラー場
      空間の各点に 1 つの実数が決まっているもの。温度分布や電位などがその例である。英語：scalar field

   ベクトル場
      空間の各点に 1 つのベクトルが決まっているもの。流れの速度や電場などがその例である。英語：vector field

   場
      空間の各点に数やベクトルが決まっているもの。スカラー場とベクトル場の総称である。英語：field

   ベクトル
      大きさと向きを持つ量。矢印で表し、成分で表示できる。英語：vector

   位置ベクトル
      原点を始点とし、ある点を終点とするベクトル。本書では :math:`\bm{r} = (x, y, z)` と書く。英語：position vector

   右手系
      右手の親指、人差し指、中指が、それぞれ :math:`x` 軸、:math:`y` 軸、:math:`z` 軸の正の向きになる座標系。外積の向きはこれで決まる。英語：right-handed system

   ノルム
      ベクトルの大きさ（長さ）。:math:`|\bm{a}|` と書く。英語：norm

   単位ベクトル
      ノルムが 1 のベクトル。向きだけを表すのに使う。英語：unit vector

   内積
      :math:`\bm{a} \cdot \bm{b} = |\bm{a}| |\bm{b}| \cos\theta` で定義されるスカラー。成分では、対応する成分の積の和になる。英語：inner product, dot product

   コーシー・シュワルツの不等式
      :math:`|\bm{a} \cdot \bm{b}| \le |\bm{a}| |\bm{b}|` という不等式。等号は 2 つのベクトルが平行なときに成り立つ。英語：Cauchy–Schwarz inequality

   正射影
      あるベクトルから、ある方向の成分を取り出したベクトル。:math:`\bm{a}` の :math:`\bm{b}` 方向への正射影は :math:`(\bm{a} \cdot \bm{b} / \bm{b} \cdot \bm{b}) \, \bm{b}` である。英語：orthogonal projection

   外積
      2 つのベクトルの両方に垂直で、大きさがそれらの作る平行四辺形の面積に等しいベクトル。順序を入れ替えると符号が変わる。英語：cross product

   スカラー三重積
      :math:`\bm{a} \cdot (\bm{b} \times \bm{c})`。3 つのベクトルが作る平行六面体の符号付きの体積で、3 つのベクトルを並べた行列式に等しい。英語：scalar triple product

   ベクトル値関数
      実数に対してベクトルを 1 つ対応させる関数。曲線や運動を表すのに使う。英語：vector-valued function

   向き
      曲線については、曲線をたどる向き。曲面については、法線ベクトルの向きの選び方。ベクトル場の線積分と流束は、向きを逆にすると符号が変わる。英語：orientation

   接線ベクトル
      曲線のパラメーター表示を微分したベクトル :math:`\bm{r}'(t)`。曲線の接線の方向を向く。英語：tangent vector

   単位接線ベクトル
      接線ベクトルを大きさ 1 にしたもの。:math:`\bm{T}` と書く。英語：unit tangent vector

   弧長
      曲線の長さ。:math:`|\bm{r}'(t)|` を積分して求める。英語：arc length

   線素
      曲線に沿った微小な移動の長さ :math:`ds = |\bm{r}'(t)| \, dt`。微小な変位ベクトル :math:`d\bm{r}` を指すこともある。英語：line element

   曲率
      曲線の曲がり具合 :math:`\kappa = |d\bm{T} / ds|`。半径 :math:`R` の円では :math:`1/R` である。英語：curvature

   単位法線ベクトル
      大きさ 1 の法線ベクトル。曲線では :math:`d\bm{T} / ds` の向きの単位ベクトル :math:`\bm{N}`\ （主法線）を、曲面では曲面に垂直な単位ベクトル :math:`\bm{n}` を指す。英語：unit normal vector

   フレネ・セレの公式
      曲線に沿って動く正規直交基底 :math:`\bm{T}, \bm{N}, \bm{B}` の変化を、曲率とねじれ率で表す公式。英語：Frenet–Serret formulas

   定常
      時刻によって変わらないこと。英語：steady

   等高線
      2 変数のスカラー場の値が等しい点を結んだ曲線 :math:`f(x, y) = c`。英語：contour line

   等値面
      3 変数のスカラー場の値が等しい点の集まりである曲面 :math:`f(x, y, z) = c`。英語：level surface

   流線
      各点での接線がベクトル場の向きに一致する曲線。英語：streamline

   偏微分
      ほかの変数を定数とみなし、1 つの変数だけで微分すること。英語：partial differentiation

   偏導関数
      偏微分して得られる関数。:math:`\partial f / \partial x` や :math:`f_x` と書く。英語：partial derivative

   シュワルツの定理
      2 階の偏導関数 :math:`f_{xy}` と :math:`f_{yx}` が存在して連続なら、両者は等しいという定理。偏微分の順序を交換できる根拠になる。英語：Schwarz's theorem

   全微分
      :math:`df = f_x \, dx + f_y \, dy + f_z \, dz`。場の微小な変化を 1 次式で近似する。英語：total differential

   連鎖律
      合成関数の微分の規則。曲線に沿ったスカラー場の変化率は :math:`df/dt = f_x x' + f_y y' + f_z z'` になる。英語：chain rule

第 II 部 場の微分
-----------------

.. glossary::

   勾配
      スカラー場の偏導関数を成分とするベクトル場 :math:`\nabla f`。:math:`f` が最も急に増える向きを指し、大きさはその向きの変化率である。英語：gradient

   方向微分
      単位ベクトル :math:`\bm{u}` の向きに進んだときのスカラー場の変化率。:math:`\nabla f \cdot \bm{u}` で求まる。英語：directional derivative

   法線ベクトル
      曲線や曲面に垂直なベクトル。曲面 :math:`f = c` の法線ベクトルは :math:`\nabla f`、パラメーター表示された曲面 :math:`\bm{r}(u, v)` の法線ベクトルは :math:`\bm{r}_u \times \bm{r}_v` で求まる。英語：normal vector

   接平面
      曲面の 1 点で曲面に接する平面。曲面 :math:`f = c` の点 :math:`\bm{p}` での接平面は :math:`\nabla f(\bm{p}) \cdot (\bm{r} - \bm{p}) = 0` である。英語：tangent plane

   ナブラ
      偏微分を成分とするベクトルの形をした演算子 :math:`\nabla = (\partial / \partial x, \partial / \partial y, \partial / \partial z)`。勾配・発散・回転を統一的に表す。英語：nabla

   勾配降下法
      :math:`-\nabla f` の向きに少しずつ進むことを繰り返して、関数の最小点を数値的に探す方法。英語：gradient descent

   流束
      ベクトル場が面を通り抜ける量。小さな面では :math:`(\bm{F} \cdot \bm{n}) \Delta S`、曲面全体では面積分 :math:`\iint_S \bm{F} \cdot \bm{n} \, dS` で表す。英語：flux

   発散
      :math:`\nabla \cdot \bm{F} = \partial F_x / \partial x + \partial F_y / \partial y + \partial F_z / \partial z`。単位体積あたりの正味の流出量を表すスカラー場である。英語：divergence

   湧き出し
      ベクトル場が外へ流れ出る点や領域。発散が正の点にある。逆に、発散が負の点を吸い込みという。英語：source（吸い込みは sink）

   発散のない場
      至るところで発散が 0 のベクトル場。ソレノイダルな場ともいう。英語：divergence-free field, solenoidal field

   回転
      ベクトル場 :math:`\bm{F}` から作るベクトル場 :math:`\nabla \times \bm{F}`。各成分は、その軸に垂直な微小な面を一周する単位面積あたりの循環であり、渦の軸と強さを表す。英語：rotation, curl

   循環
      閉曲線に沿ったベクトル場の線積分 :math:`\oint_C \bm{F} \cdot d\bm{r}`。場が閉曲線に沿ってどれだけ回っているかを表す。英語：circulation

   剛体回転
      全体が一定の角速度で回る速度場 :math:`\bm{v} = \bm{\Omega} \times \bm{r}`。回転は :math:`2 \bm{\Omega}` である。英語：rigid-body rotation

   渦なしの場
      至るところで回転が 0 のベクトル場。英語：irrotational field

   渦度
      流れの速度の回転 :math:`\bm{\omega} = \nabla \times \bm{v}`。流体の微小な部分が回転する軸の向きと、角速度の 2 倍の大きさを持つ。英語：vorticity

   ラプラシアン
      勾配の発散 :math:`\nabla^2 f = \nabla \cdot \nabla f`。ある点の値と周囲の平均との差を表す。:math:`\Delta f` とも書く。英語：Laplacian

   ラプラス方程式
      :math:`\nabla^2 f = 0` の形の偏微分方程式。湧き出しのない領域でのポテンシャルや定常状態の温度が満たす。湧き出しがある場合はポアソン方程式 :math:`\nabla^2 \phi = s` になる。英語：Laplace's equation

   調和関数
      ラプラス方程式 :math:`\nabla^2 f = 0` を満たす関数。各点の値が周囲の平均に等しく、定数でなければ領域の内部で最大値・最小値をとらない。英語：harmonic function

   極座標
      平面上の点を、原点からの距離 :math:`r` と :math:`x` 軸から測った角度 :math:`\theta` で表す座標系。英語：polar coordinates

   円柱座標
      空間の点を、:math:`z` 軸からの距離 :math:`\rho`、方位角 :math:`\phi`、高さ :math:`z` で表す座標系。軸対称な問題に向く。英語：cylindrical coordinates

   球座標
      空間の点を、原点からの距離 :math:`r`、:math:`z` 軸からの角度 :math:`\theta`\ （天頂角）、方位角 :math:`\phi` で表す座標系。球対称な問題に向く。英語：spherical coordinates

   直交曲線座標系
      各点で 3 つの基底ベクトルが互いに直交する曲線座標系。円柱座標と球座標はその例である。英語：orthogonal curvilinear coordinates

   スケール因子
      座標 :math:`u_i` の微小な変化を実際の距離に直す係数 :math:`h_i = |\partial \bm{r} / \partial u_i|`。英語：scale factor

   面素
      曲面の微小な部分の面積 :math:`dS`。単位法線ベクトルを掛けた :math:`d\bm{S} = \bm{n} \, dS` をベクトル面素という。英語：surface element

   体積素
      微小な体積 :math:`dV`。直交曲線座標系では :math:`h_1 h_2 h_3 \, du_1 \, du_2 \, du_3` である。英語：volume element

第 III 部 場の積分
------------------

.. glossary::

   重積分
      平面の領域や立体を細かく分けた和の極限として定義する積分。分布している量の合計を表す。英語：multiple integral

   累次積分
      1 変数の積分を繰り返して重積分を計算する方法。英語：iterated integral

   体積積分
      立体の上での 3 重積分。英語：volume integral

   ヤコビアン
      変数変換の偏導関数を並べた行列（ヤコビ行列）の行列式。変換によって微小な面積や体積が何倍になるかを表す。英語：Jacobian

   線積分
      曲線に沿った積分。スカラー場では :math:`\int_C f \, ds`、ベクトル場では :math:`\int_C \bm{F} \cdot d\bm{r}` である。英語：line integral

   閉曲線
      始点と終点が一致する曲線。英語：closed curve

   保存場
      線積分の値が経路によらないベクトル場。ポテンシャルの勾配として表せる。英語：conservative field

   ポテンシャル
      :math:`\bm{F} = \nabla \phi` を満たすスカラー場 :math:`\phi`。物理では負号を付けて :math:`\bm{F} = -\nabla U` とすることが多い。英語：potential

   単連結
      領域の中の任意の閉曲線を、領域からはみ出さずに連続的に縮めて 1 点にできる性質。英語：simply connected

   閉曲面
      空間の領域を囲む曲面。外向きの法線を正の向きとする。英語：closed surface

   面積分
      曲面上での積分。スカラー場では :math:`\iint_S f \, dS`、ベクトル場では流束 :math:`\iint_S \bm{F} \cdot d\bm{S}` である。英語：surface integral

第 IV 部 積分定理
-----------------

.. glossary::

   グリーンの定理
      平面の領域の境界に沿った線積分が、領域の中での回転の :math:`z` 成分（流束形では発散）の重積分に等しいという定理。英語：Green's theorem

   境界
      領域・曲面・立体の縁。:math:`\partial D`、:math:`\partial S`、:math:`\partial V` と書く。英語：boundary

   正の向き
      平面の領域の境界をたどる向きのうち、領域を常に左手に見て進む向き。穴のない領域では反時計回りになる。英語：positive orientation

   靴ひも公式
      多角形の面積を頂点の座標から :math:`A = \frac{1}{2} \sum_i (x_i y_{i+1} - x_{i+1} y_i)` で求める公式。グリーンの定理から導かれる。英語：shoelace formula

   プラニメーター
      図形の輪郭をなぞるだけで面積を測る機械式の器具。グリーンの定理を機械で実現したものである。英語：planimeter

   ガウスの発散定理
      閉曲面から外へ出る流束が、内部の発散の体積積分に等しいという定理。英語：divergence theorem, Gauss's theorem

   ガウスの法則
      閉曲面を通る電場の流束が、内部の電荷の合計を :math:`\varepsilon_0` で割ったものに等しいという法則。微分形は :math:`\nabla \cdot \bm{E} = \rho / \varepsilon_0` である。英語：Gauss's law

   連続の式
      質量の保存を表す式 :math:`\partial \rho / \partial t + \nabla \cdot (\rho \bm{v}) = 0`。:math:`\rho` は密度である。電荷など、他の保存量にも同じ形の式が成り立つ。英語：continuity equation

   非圧縮性
      流体の密度が変わらない性質。速度場は :math:`\nabla \cdot \bm{v} = 0` を満たす。英語：incompressibility

   グリーンの恒等式
      ガウスの発散定理を :math:`f \nabla g` に適用して得られる積分公式。部分積分を 3 次元に広げたものである。英語：Green's identities

   ストークスの定理
      曲面の境界に沿った循環が、曲面を通る回転の流束に等しいという定理。英語：Stokes' theorem

   右ねじの規則
      境界をたどる向きに右ねじを回したとき、ねじが進む向きを曲面の法線の向きとする約束。英語：right-hand rule

   アンペールの法則
      閉曲線に沿った磁束密度の循環が、閉曲線を貫く電流の :math:`\mu_0` 倍に等しいという法則。微分形は :math:`\nabla \times \bm{B} = \mu_0 \bm{J}` である。英語：Ampère's law

   ファラデーの電磁誘導の法則
      閉曲線に沿った電場の循環が、閉曲線を貫く磁束の時間変化に負号を付けたものに等しいという法則。微分形は :math:`\nabla \times \bm{E} = -\partial \bm{B} / \partial t` である。英語：Faraday's law of induction

   スカラーポテンシャル
      :math:`\bm{F} = \nabla \phi` となるスカラー場 :math:`\phi`。単にポテンシャルともいう。英語：scalar potential

   ベクトルポテンシャル
      :math:`\bm{B} = \nabla \times \bm{A}` となるベクトル場 :math:`\bm{A}`。英語：vector potential

   ゲージの自由度
      ベクトルポテンシャルに任意のスカラー場の勾配を足しても、回転が変わらないという自由度。英語：gauge freedom

   ヘルムホルツ分解
      ベクトル場を、渦なしの成分 :math:`\nabla \phi` と発散のない成分 :math:`\nabla \times \bm{A}` の和に分けること。英語：Helmholtz decomposition

   流れ関数
      2 次元の流れで :math:`\bm{v} = (\partial \psi / \partial y, -\partial \psi / \partial x)` となるスカラー場 :math:`\psi`。等高線が流線になる。英語：stream function

   ポアソン方程式
      :math:`\nabla^2 \phi = s` の形の偏微分方程式。湧き出しの分布 :math:`s` からポテンシャルを決める。英語：Poisson's equation

   基本解
      1 点に強さ 1 の湧き出しが集中している場合のポアソン方程式の解。3 次元では :math:`-1/(4\pi r)` になる。英語：fundamental solution

第 V 部 応用
------------

.. glossary::

   マクスウェル方程式
      電場と磁束密度のふるまいを決める 4 つの方程式。発散と回転で表される。英語：Maxwell's equations

   変位電流
      変位電流密度 :math:`\varepsilon_0 \, \partial \bm{E} / \partial t` のこと。アンペール・マクスウェルの法則では、:math:`\mu_0` を掛けた項 :math:`\mu_0 \varepsilon_0 \, \partial \bm{E} / \partial t` として現れる。電荷の保存と矛盾しないように、マクスウェルが付け加えた。英語：displacement current

   波動方程式
      :math:`\nabla^2 u = (1/c^2) \, \partial^2 u / \partial t^2` の形の方程式。速さ :math:`c` で伝わる波を表す。英語：wave equation

   速度ポテンシャル
      渦なしの流れで :math:`\bm{v} = \nabla \phi` となるスカラー場 :math:`\phi`。英語：velocity potential

   ポテンシャル流
      渦なしで非圧縮の流れ。速度ポテンシャルはラプラス方程式を満たす。英語：potential flow

   フーリエの法則
      熱流束が温度勾配に比例し、温度の低い向きに流れるという法則 :math:`\bm{q} = -\lambda \nabla T`。英語：Fourier's law

   熱伝導方程式
      物体の中の温度の時間変化を表す方程式。発熱がない場合は :math:`\partial T / \partial t = \alpha \nabla^2 T` である。英語：heat equation

   差分法
      微分を、近くの格子点での値の差で近似して計算する方法。英語：finite difference method

   打ち切り誤差
      テイラー展開を途中で打ち切って近似したことによる誤差。英語：truncation error

   丸め誤差
      浮動小数点数の桁数が有限であるために生じる誤差。英語：rounding error

   ヤコビ法
      すべての未知数を、1 つ前の段階の値から同時に更新する反復法。ラプラス方程式では、各点を隣の 4 点の平均で置き換えることを繰り返す。英語：Jacobi method

   符号付き距離関数
      物体の表面までの距離に、外側で正、内側で負の符号を付けた関数。勾配が表面の単位法線ベクトルになる。英語：signed distance function（SDF）

   ノーマルマップ
      表面の法線ベクトルの各成分を RGB の色として保存した画像。細かい凹凸の陰影を表現するのに使う。英語：normal map

   カールノイズ
      ノイズで作ったポテンシャルの回転を速度とし、発散のない流れを作る方法。英語：curl noise

   圧力投影
      ポアソン方程式を解いて速度の場から勾配の成分を取り除き、発散のない場を取り出す操作。英語：pressure projection

   微分形式
      線積分・面積分・体積積分の被積分関数を統一的に扱う量。外微分 :math:`d` が勾配・回転・発散に対応する。英語：differential form

   一般化されたストークスの定理
      :math:`\int_M d\omega = \int_{\partial M} \omega`。微分積分学の基本定理、勾配定理、ストークスの定理、ガウスの発散定理を 1 つにまとめた定理。英語：generalized Stokes' theorem
