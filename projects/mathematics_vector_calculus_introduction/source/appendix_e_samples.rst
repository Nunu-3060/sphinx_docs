.. _appendix-e:

付録 E サンプルコード一覧
=========================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダーの中に次の構成でファイルが配置される。

.. code-block:: text
   :linenos:

   examples/
   ├── setup.cfg      flake8 と mypy の設定
   ├── vc_plot.py     図の描画の補助モジュール
   └── ch01_*.py 〜 ch18_*.py  各章のサンプル

実行と検査の方法
----------------

サンプルは ``examples`` フォルダーで実行する。図を描くサンプルは画面に図を表示し、計算をするサンプルは結果を表示する。多くのサンプルは補助モジュール ``vc_plot.py`` を import するので、個別にダウンロードした場合は、一覧の「必要なもの」の列に示したファイルも同じフォルダーに置く。必要なパッケージ（NumPy、matplotlib、SciPy、SymPy）は\ :ref:`第 1 章 <ch01>`\ を参照。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python ch05_gradient_contour.py

サンプルは、flake8（PEP 8 などのコーディング規約の検査）と mypy（型ヒントの検査）で違反がないことを確認している。``examples`` フォルダーで次のコマンドを実行すると、``setup.cfg`` の設定（行長 120 文字まで、mypy の strict モード）で検査できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m flake8 .
   $ python -m mypy .

SciPy、SymPy、matplotlib の 3 次元グラフの機能（``mpl_toolkits``）は型ヒントの情報を持たないため、``setup.cfg`` でこれらの import の検査を省略している。

はじめに・第 I 部 準備
------------------------

.. list-table:: はじめに・第 I 部 準備のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch01_sympy_partial.py <../examples/ch01_sympy_partial.py>`
     - SymPy で多変数関数を偏微分する最小の例。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch02_cross_product.py <../examples/ch02_cross_product.py>`
     - 外積 :math:`\bm{a} \times \bm{b}` の向きと大きさを 3 次元の図で示す。
     - 図
     - vc_plot.py
   * - :download:`ch02_vector_ops.py <../examples/ch02_vector_ops.py>`
     - ベクトルの内積、外積、三重積を NumPy で計算する。
     - 実行結果
     - vc_plot.py
   * - :download:`ch03_circular_motion.py <../examples/ch03_circular_motion.py>`
     - 等速円運動の速度ベクトルと加速度ベクトルを描く。
     - 図
     - vc_plot.py
   * - :download:`ch03_curve_quantities.py <../examples/ch03_curve_quantities.py>`
     - らせんの弧長と曲率を、公式（SymPy）と数値計算（SciPy、NumPy）で求めて比べる。
     - 実行結果
     - SciPy、SymPy、vc_plot.py
   * - :download:`ch03_helix.py <../examples/ch03_helix.py>`
     - らせんと、その上の単位接線ベクトル :math:`\bm{T}` と単位法線ベクトル :math:`\bm{N}` を描く。
     - 図
     - vc_plot.py
   * - :download:`ch04_partial.py <../examples/ch04_partial.py>`
     - 偏微分、偏微分の順序交換、1 次近似、連鎖律を SymPy と数値計算で確かめる。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch04_scalar_field.py <../examples/ch04_scalar_field.py>`
     - スカラー場 :math:`f(x, y) = x e^{-(x^2 + y^2)}` を、等高線図と曲面で描く。
     - 図
     - vc_plot.py
   * - :download:`ch04_streamline.py <../examples/ch04_streamline.py>`
     - ベクトル場 :math:`\bm{F}(x, y) = (-y, x)` の流線を、常微分方程式を解いて求める。
     - 実行結果
     - SciPy、vc_plot.py
   * - :download:`ch04_vector_field.py <../examples/ch04_vector_field.py>`
     - ベクトル場 :math:`\bm{F}(x, y) = (x - y, x + y)` を、矢印図と流線で描く。
     - 図
     - vc_plot.py

第 II 部 場の微分
-------------------

.. list-table:: 第 II 部 場の微分のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch05_directional.py <../examples/ch05_directional.py>`
     - 方向微分を勾配との内積で求め、差分による近似値と比べる。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch05_gradient_contour.py <../examples/ch05_gradient_contour.py>`
     - 2 つの山がある地形の等高線と、勾配ベクトルを重ねて描く。
     - 図
     - vc_plot.py
   * - :download:`ch05_gradient_descent.py <../examples/ch05_gradient_descent.py>`
     - 勾配降下法で関数の最小点を探し、ステップ幅による進み方の違いを描く。
     - 図
     - vc_plot.py
   * - :download:`ch06_box_flux.py <../examples/ch06_box_flux.py>`
     - 微小な直方体からの正味の流出量を体積で割った値が、発散に近づくことを確かめる。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch06_divergence_fields.py <../examples/ch06_divergence_fields.py>`
     - 発散が正・負・0 の 2 次元のベクトル場を並べて描く。
     - 図
     - vc_plot.py
   * - :download:`ch07_circulation.py <../examples/ch07_circulation.py>`
     - 微小な正方形を一周する循環を面積で割った値が、回転の :math:`z` 成分に近づくことを確かめる。
     - 実行結果
     - SciPy、SymPy、vc_plot.py
   * - :download:`ch07_rotation_fields.py <../examples/ch07_rotation_fields.py>`
     - 剛体回転、自由渦、せん断流の 3 つの流れに羽根車を流したとき、羽根車が自転するかを描く。
     - 図
     - vc_plot.py
   * - :download:`ch08_identities.py <../examples/ch08_identities.py>`
     - ナブラを含む公式が成り立つことを、SymPy の記号計算で確かめる。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch08_laplacian_bump.py <../examples/ch08_laplacian_bump.py>`
     - 山の形をしたスカラー場と、そのラプラシアンを並べて描く。
     - 図
     - vc_plot.py
   * - :download:`ch08_laplacian_mean.py <../examples/ch08_laplacian_mean.py>`
     - 小さな円の上での平均と中心の値の差から、ラプラシアンを求める。
     - 実行結果
     - SciPy、SymPy、vc_plot.py
   * - :download:`ch09_orthogonal_ops.py <../examples/ch09_orthogonal_ops.py>`
     - スケール因子から、直交曲線座標系での勾配・発散・回転・ラプラシアンを SymPy で計算する。
     - 実行結果
     - SymPy
   * - :download:`ch09_polar_basis.py <../examples/ch09_polar_basis.py>`
     - 極座標の基底ベクトル :math:`\bm{e}_r` と :math:`\bm{e}_\theta` が、点の位置によって向きを変える様子を描く。
     - 図
     - vc_plot.py
   * - :download:`ch09_spherical_basis.py <../examples/ch09_spherical_basis.py>`
     - 球座標 :math:`(r, \theta, \phi)` の意味と、点 P での基底ベクトル :math:`\bm{e}_r, \bm{e}_\theta, \bm{e}_\phi` を描く。
     - 図
     - vc_plot.py

第 III 部 場の積分
--------------------

.. list-table:: 第 III 部 場の積分のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch10_polar_cell.py <../examples/ch10_polar_cell.py>`
     - 極座標の微小な領域（:math:`r` から :math:`r + \Delta r`、:math:`\theta` から :math:`\theta + \Delta\theta`）の面積がおよそ :math:`r \Delta r \Delta\theta` になる様子を描く。
     - 図
     - vc_plot.py
   * - :download:`ch10_region_order.py <../examples/ch10_region_order.py>`
     - 領域 :math:`D: x^2 \le y \le x` を、縦の帯（先に :math:`y` で積分）と横の帯（先に :math:`x` で積分）に分ける様子を描く。
     - 図
     - vc_plot.py
   * - :download:`ch10_scipy_integrals.py <../examples/ch10_scipy_integrals.py>`
     - SciPy の dblquad と tplquad で重積分を数値計算し、手計算の値と比べる。
     - 実行結果
     - SciPy
   * - :download:`ch11_helix.py <../examples/ch11_helix.py>`
     - らせん状の針金の質量（スカラー場の線積分）と、重力がする仕事（ベクトル場の線積分）を計算する。
     - 実行結果
     - SciPy
   * - :download:`ch11_potential.py <../examples/ch11_potential.py>`
     - 保存場 :math:`\bm{F} = (2xy + z, x^2 + 2yz, x + y^2 + 3z^2)` のポテンシャルを SymPy で求める。
     - 実行結果
     - SymPy
   * - :download:`ch11_two_paths.py <../examples/ch11_two_paths.py>`
     - 2 つのベクトル場 :math:`\bm{F}_1 = (y, x)` と :math:`\bm{F}_2 = (-y, x)` を、3 つの経路に沿って線積分して比べる。
     - 図・実行結果
     - SciPy、vc_plot.py
   * - :download:`ch12_sphere_normals.py <../examples/ch12_sphere_normals.py>`
     - 球面のパラメーター表示 :math:`\bm{r}(\theta, \phi)` と、接ベクトル :math:`\bm{r}_\theta, \bm{r}_\phi`、外向きの法線ベクトル :math:`\bm{r}_\theta \times \bm{r}_\phi` を描く。
     - 図
     - vc_plot.py
   * - :download:`ch12_surface_integrals.py <../examples/ch12_surface_integrals.py>`
     - パラメーター表示された曲面の面積、スカラー場の面積分、ベクトル場の流束を数値計算する。
     - 実行結果
     - SciPy

第 IV 部 積分定理
-------------------

.. list-table:: 第 IV 部 積分定理のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch13_green_check.py <../examples/ch13_green_check.py>`
     - グリーンの定理の両辺を数値積分で別々に計算し、一致を確かめる。
     - 実行結果
     - SciPy、vc_plot.py
   * - :download:`ch13_shoelace.py <../examples/ch13_shoelace.py>`
     - 靴ひも公式と線積分で多角形の面積を求め、境界の向きを図に描く。
     - 図・実行結果
     - SciPy、vc_plot.py
   * - :download:`ch13_small_rectangles.py <../examples/ch13_small_rectangles.py>`
     - 領域を微小な長方形に分け、各長方形の循環を足すと内部の辺が打ち消し合う様子を描く。
     - 図
     - vc_plot.py
   * - :download:`ch14_gauss_check.py <../examples/ch14_gauss_check.py>`
     - ガウスの発散定理の両辺を数値積分で別々に計算し、一致を確かめる。
     - 実行結果
     - SciPy、vc_plot.py
   * - :download:`ch14_point_charge.py <../examples/ch14_point_charge.py>`
     - 点電荷の場 :math:`\bm{r}/r^3` が閉曲面を通る流束を求め、原点を囲むかどうかで値が変わることを確かめる。
     - 図・実行結果
     - SciPy、vc_plot.py
   * - :download:`ch15_stokes_check.py <../examples/ch15_stokes_check.py>`
     - ストークスの定理の両辺を数値積分で別々に計算し、境界が同じなら曲面によらないことを確かめる。
     - 実行結果
     - SciPy、vc_plot.py
   * - :download:`ch15_surfaces.py <../examples/ch15_surfaces.py>`
     - 同じ境界（単位円）を持つ円板と半球面、境界の向きと法線ベクトルの関係を描く。
     - 図
     - vc_plot.py
   * - :download:`ch16_helmholtz.py <../examples/ch16_helmholtz.py>`
     - 2 次元のベクトル場を、渦なしの成分と発散のない成分の和として組み立てて描く。
     - 図・実行結果
     - SymPy、vc_plot.py
   * - :download:`ch16_potential_sympy.py <../examples/ch16_potential_sympy.py>`
     - 原点から直線に沿って積分する公式で、スカラーポテンシャルとベクトルポテンシャルを SymPy で求める。
     - 実行結果
     - SymPy、vc_plot.py
   * - :download:`ch16_vortex.py <../examples/ch16_vortex.py>`
     - 自由渦 :math:`\bm{F} = (-y, x)/(x^2 + y^2)` の循環が、閉曲線が原点を囲むかどうかで変わることを確かめる。
     - 図・実行結果
     - SciPy、SymPy、vc_plot.py

第 V 部 応用
--------------

.. list-table:: 第 V 部 応用のサンプル
   :header-rows: 1
   :widths: 30 46 10 14

   * - ファイル
     - 内容
     - 出力
     - 必要なもの
   * - :download:`ch17_em_wave.py <../examples/ch17_em_wave.py>`
     - 真空中の平面電磁波がマクスウェル方程式を満たすことを SymPy で確かめる。
     - 実行結果
     - SymPy
   * - :download:`ch17_heat_decay.py <../examples/ch17_heat_decay.py>`
     - 1 次元の熱伝導方程式の厳密解で、温度の山がならされていく様子を描く。
     - 図
     - vc_plot.py
   * - :download:`ch17_potential_flow.py <../examples/ch17_potential_flow.py>`
     - 円柱を過ぎるポテンシャル流（一様流と二重湧き出しの重ね合わせ）を流線で描く。
     - 図
     - vc_plot.py
   * - :download:`ch18_curl_noise.py <../examples/ch18_curl_noise.py>`
     - ノイズをそのまま速度にした流れと、カールノイズで作った流れを比べる。
     - 図・実行結果
     - vc_plot.py
   * - :download:`ch18_finite_difference.py <../examples/ch18_finite_difference.py>`
     - 前進差分と中心差分の誤差が、刻み幅 :math:`h` とともにどう小さくなるかを比べる。
     - 図・実行結果
     - vc_plot.py
   * - :download:`ch18_jacobi_laplace.py <../examples/ch18_jacobi_laplace.py>`
     - 正方形の板の定常温度分布（ラプラス方程式）をヤコビ法で解く。
     - 図・実行結果
     - vc_plot.py
   * - :download:`ch18_normal_map.py <../examples/ch18_normal_map.py>`
     - 高さの分布（ハイトマップ）の勾配から法線を求め、ノーマルマップと陰影を描く。
     - 図
     - vc_plot.py
   * - :download:`ch18_np_gradient.py <../examples/ch18_np_gradient.py>`
     - 格子上の値から、差分で発散・回転・ラプラシアンを求め、厳密な値と比べる。
     - 実行結果
     - －
   * - :download:`ch18_projection.py <../examples/ch18_projection.py>`
     - ベクトル場から勾配の成分を取り除き、発散のない場を取り出す（圧力投影）。
     - 図・実行結果
     - vc_plot.py

補助モジュールと設定ファイル
----------------------------

.. list-table:: 補助モジュールと設定ファイル
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - :download:`vc_plot.py <../examples/vc_plot.py>`
     - 日本語フォントの設定、座標平面の準備、ベクトルの矢印、3 次元のグラフなど、図の描画で共通に使う関数をまとめたモジュール。
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル。
