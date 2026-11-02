第 4 章　パターンとマテリアル
============================================================

本章では、第 3 章のノイズと規則的な図形を組み合わせて、レンガ・石畳・木目・大理石・錆のような素材のテクスチャを作る。\ **テクスチャ**\ とは、3D モデルの表面に貼る画像のことである。モデルの表面の各点には、画像上の位置を表す 2 次元の座標が割り当てられている。この座標を\ **UV 座標**\ と呼ぶ（画像の横方向が u、縦方向が v）。

手続きで作るテクスチャ（\ **プロシージャルテクスチャ**\ ）は、UV 座標を入力とし、色を出力する関数である。本章の手法は、第 3 章と同じく関数型に当たる。画像として書き出してモデルに貼ってもよいし、シェーダーの中で描画のたびに計算してもよい。

本章の図は、次のスクリプトで作っている。

* :download:`patterns_regular.py <../examples/python/patterns_regular.py>`: 座標の分割と規則パターン
* :download:`sdf2d.py <../examples/python/sdf2d.py>`: 2 次元の距離関数
* :download:`voronoi_patterns.py <../examples/python/voronoi_patterns.py>`: ボロノイ図を使った模様
* :download:`materials.py <../examples/python/materials.py>`: ノイズを組み合わせた素材
* :download:`normal_map.py <../examples/python/normal_map.py>`: ハイトマップから法線マップを作る
* :download:`seamless.py <../examples/python/seamless.py>`: 繰り返し可能なテクスチャ
* :download:`pbr_maps.py <../examples/python/pbr_maps.py>`: PBR 用のテクスチャ一式

いくつかの共通の処理（smoothstep、法線の計算、陰影付けなど）は :download:`texture.py <../examples/python/texture.py>` にまとめた。

座標の分割による繰り返し
------------------------------------------------------------

タイル・レンガ・格子柄のような規則的な模様は、平面を同じ形の\ **セル**\ に分け、各セルに同じ図形を描くことで作る。この分割には、座標の整数部と小数部を使う。

* ``floor(x)``\ （整数部）: 点がどのセルにあるかを表す\ **セルの番号**\ 。
* ``fract(x) = x - floor(x)``\ （小数部）: セルの中での位置を表す 0〜1 の\ **セル内の座標**\ 。

座標を :math:`k` 倍してから分割すると、単位長さあたり :math:`k` 個のセルができる。:numref:`fig-patterns-repeat` は、この操作を順に示したものである。セル内の座標を使って図形を 1 つ描けば、それが全セルに繰り返される。さらに、セルの番号をハッシュ関数に入れれば、セルごとに違う乱数が得られ、図形の大きさや色をセルごとに変えられる。第 3 章のノイズの格子も、この分割そのものである。

.. _fig-patterns-repeat:

.. figure:: _generated/patterns_regular/repeat.png
   :alt: 座標、セルの番号、セル内の座標、セルごとに大きさを変えた円の 4 枚の画像

   座標の分割。座標とセル内の座標は、x を赤、y を緑で表した。右端は、半径をセルの乱数で変えた円

規則パターン
------------------------------------------------------------

この考え方で、基本的な規則パターンを作る（:numref:`fig-patterns-regular`）。

.. _fig-patterns-regular:

.. figure:: _generated/patterns_regular/regular.png
   :alt: 斜めの縞、チェッカー、レンガ、六角形タイルの 4 枚の画像

   規則パターン。レンガと六角形タイルは、セルの乱数で色を変えた

**縞**\ は、縞に直交する向きの座標 :math:`u = x \cos\theta + y \sin\theta` を 1 次元で分割したものである。``fract(u)`` が ``duty`` より小さい所を明るくすると、明るい部分の割合が ``duty`` の縞になる。

.. literalinclude:: ../examples/python/patterns_regular.py
   :language: python
   :pyobject: stripes
   :lineno-match:
   :caption: examples/python/patterns_regular.py（stripes）

境界を ``smoothstep`` で 1 画素程度ぼかしているのは、\ **エイリアシング**\ （画素の格子で境界がギザギザになったり、細かい模様が偽の模様に化けたりする現象）を抑えるためである。白か黒かを ``x < duty`` で決めると、境界が階段状になる。

**チェッカー**\ （市松模様）は、セルの番号の和 ``floor(x) + floor(y)`` の偶奇で塗り分ける。

.. literalinclude:: ../examples/python/patterns_regular.py
   :language: python
   :pyobject: checker
   :lineno-match:
   :caption: examples/python/patterns_regular.py（checker）

**レンガ**\ は、横長のセルを、段（行）の番号が奇数の段だけ半個分ずらして並べる。目地は、セル内の座標から最も近い辺までの距離が一定以下の所である。

.. literalinclude:: ../examples/python/patterns_regular.py
   :language: python
   :pyobject: bricks
   :lineno-match:
   :caption: examples/python/patterns_regular.py（bricks）

**六角形タイル**\ は、正方形の格子では作れない。そこで、間隔 :math:`1 \times \sqrt{3}` の長方形の格子を 2 組、半周期ずらして重ね、各点で近いほうの格子の中心を選ぶ。2 組の格子の中心を合わせると、どの中心からも隣の 6 個の中心が等距離にある配置になり、最も近い中心の領域が正六角形になる。

.. literalinclude:: ../examples/python/patterns_regular.py
   :language: python
   :pyobject: hex_cells
   :lineno-match:
   :caption: examples/python/patterns_regular.py（hex_cells）

.. list-table:: 規則パターンのパラメーター
   :header-rows: 1
   :widths: 25 75

   * - パラメーター
     - 制御できること
   * - 座標の倍率
     - セルの大きさ（模様の繰り返しの細かさ）
   * - 縞の角度・``duty``
     - 縞の向きと、明るい部分の太さ
   * - レンガの縦横比・ずらし量
     - レンガの形と積み方（コードではずらし量を半個に固定）。ずらし量を 0 にすると芋目地（縦の目地が通る積み方）になる
   * - 目地の太さ
     - タイルやレンガの間の隙間
   * - セルの乱数の使い方
     - タイルごとの色・明るさ・欠けなどのばらつき

.. _patterns-sdf:

2 次元の距離関数による図形
------------------------------------------------------------

セルの中に円や四角形を描くとき、「点が図形の内側か」を判定するだけでなく、「図形の境界までどれだけ離れているか」を計算しておくと便利である。点から図形の境界までの距離に、内側なら負、外側なら正の符号を付けた関数を\ **符号付き距離関数**\ （SDF、signed distance function）と呼ぶ。

円の SDF は、中心までの距離から半径を引くだけである。長方形の SDF は、各軸について辺から外にはみ出した量を求め、外側では最も近い辺または角までの距離、内側では最も近い辺までの距離（負）を返す。

.. literalinclude:: ../examples/python/sdf2d.py
   :language: python
   :pyobject: sd_circle
   :lineno-match:
   :caption: examples/python/sdf2d.py（sd_circle）

.. literalinclude:: ../examples/python/sdf2d.py
   :language: python
   :pyobject: sd_box
   :lineno-match:
   :caption: examples/python/sdf2d.py（sd_box）

:numref:`fig-patterns-sdf-shapes` は、塗りつぶした図形と、距離そのものを色で表したものである。外側を橙、内側を青で塗り、距離 0.1 ごとに等高線を入れ、境界（距離 0）を白線で描いた。長方形の外側の等高線は、角の近くで丸くなる。

.. _fig-patterns-sdf-shapes:

.. figure:: _generated/sdf2d/sdf_shapes.png
   :alt: 円と長方形の塗りつぶしと、距離を等高線付きの色で表した画像

   円と長方形の距離関数

距離が分かっていると、次のことが簡単にできる。

* **境界のぼかし**: ``smoothstep(w, -w, d)`` で、境界を幅 :math:`w` だけ滑らかにする。:math:`w` を 1 画素にすればエイリアシングが消える。
* **太らせる・縁取る**: :math:`d - r` で図形を :math:`r` だけ太らせて角を丸める。:math:`|d| - t` で太さ :math:`2t` の輪郭線になる。
* **高さや陰影**: 境界からの距離を高さに変えれば、縁が斜めに削れた（面取りした）形になる。後で述べる法線マップの材料になる。

組み合わせ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2 つの図形の SDF :math:`a, b` から、図形の和・積・差の SDF（またはそれに近い関数）が、最小値と最大値で得られる。

.. literalinclude:: ../examples/python/sdf2d.py
   :language: python
   :start-at: def op_union
   :end-before: def visualize
   :lineno-match:
   :caption: examples/python/sdf2d.py（組み合わせの演算）

和の :math:`\min(a, b)` は、境界の角でとがった形になる。\ **滑らかな和**\ （smooth min）は、:math:`a` と :math:`b` の差が :math:`k` より小さい範囲だけ、2 つの値を滑らかに混ぜ、さらに少し引く。2 つの図形が、粘土を寄せたように丸くつながる（:numref:`fig-patterns-sdf-ops`、:numref:`fig-patterns-sdf-smooth`）。この式は Inigo Quilez が紹介した多項式による smooth min である。

.. _fig-patterns-sdf-ops:

.. figure:: _generated/sdf2d/sdf_ops.png
   :alt: 円と長方形の和、積、差、滑らかな和を距離の色で表した 4 枚の画像

   SDF の組み合わせ（a: 円、b: 長方形）

.. _fig-patterns-sdf-smooth:

.. figure:: _generated/sdf2d/sdf_smooth.png
   :alt: 接した 2 つの円を、k を 0、0.1、0.25、0.5 にした滑らかな和でつないだ画像

   滑らかな和の :math:`k` による違い

最小値・最大値で作った関数は、境界の位置は正しいが、境界から離れた所では正確な距離にならないことがある（:numref:`fig-patterns-sdf-ops` の和の内側や積の外側で、等高線が境界と平行でない部分）。境界の形だけを使う用途では問題にならない。3 次元の SDF とレイマーチングによる描画は第 9 章で扱う。

.. _patterns-voronoi:

ボロノイ図を用いた模様
------------------------------------------------------------

第 3 章のセルラーノイズは、平面を不規則な多角形の領域（ボロノイ領域）に分ける。規則パターンのセルを、このボロノイ領域に置き換えると、石畳・ひび割れ・細胞のような自然な分割の模様になる（:numref:`fig-patterns-voronoi`）。

.. _fig-patterns-voronoi:

.. figure:: _generated/voronoi_patterns/voronoi_patterns.png
   :alt: セルラーノイズで作った石畳、ひび割れ、細胞の 3 枚の画像

   ボロノイ図を用いた模様

石畳は、次の手順で作る（:numref:`fig-patterns-voronoi-steps`）。

1. 座標を小さなノイズで歪めてから、セルラーノイズの :math:`F_2 - F_1`\ （境界からの距離）を求める。歪めることで、石の輪郭が直線でなくなる。
2. :math:`F_2 - F_1` を ``smoothstep`` で 0〜1 に変え、目地と石を分けるマスクにする。
3. 最も近い特徴点のセルの乱数（``cell``）で、石ごとの色を選ぶ。
4. 境界に近いほど暗くして丸みを出し、細かい fBm で表面のざらつきを加える。

.. _fig-patterns-voronoi-steps:

.. figure:: _generated/voronoi_patterns/voronoi_steps.png
   :alt: F2−F1、目地のマスク、石ごとの色、完成した石畳の 4 枚の画像

   石畳を作る手順

.. literalinclude:: ../examples/python/voronoi_patterns.py
   :language: python
   :pyobject: cobblestone
   :lineno-match:
   :caption: examples/python/voronoi_patterns.py（cobblestone）

**ひび割れ**\ は、:math:`F_2 - F_1` がごく小さい所だけを暗くした細い網目である。大きさの違う 2 段階の網目を重ね、細かいほうを薄くすると、大きな割れ目から小さな割れ目が枝分かれしたように見える。座標を歪める量を増やすほど、割れ目が曲がりくねる。

**細胞**\ は、同じセルラーノイズから 3 つの要素を取り出したものである。:math:`F_1` が小さい所（特徴点の近く）を核、:math:`F_2 - F_1` が小さい所を細胞膜、セルの乱数を細胞ごとの色に使う。

このように、セルラーノイズの :math:`F_1`、:math:`F_2 - F_1`、セルの乱数は、それぞれ「領域の中心からの距離」「領域の境界からの距離」「領域の番号」を表す。この 3 つをどう色や形に対応付けるかで、同じノイズから多様な模様が作れる。

.. _patterns-materials:

ノイズの組み合わせによる素材
------------------------------------------------------------

自然の素材の模様は、その素材ができた過程を反映している。木目は年輪、大理石は地層が熱と圧力で流れた跡、錆は金属の表面から広がる腐食である。プロシージャルテクスチャでは、この過程を厳密に再現するのではなく、「何がどう並んでいるか」を少数の関数で真似る。:numref:`fig-patterns-materials` に 4 つの例を示す。

.. _fig-patterns-materials:

.. figure:: _generated/materials/materials.png
   :alt: ノイズで作った木目、大理石、雲、錆の 4 枚の画像

   ノイズを組み合わせた素材

木目
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

木の幹には、中心から同心円状に年輪が並ぶ。幹を縦に切った板の表面には、年輪の断面が縦に長い山形の曲線として現れる。そこで、板の外に年輪の中心を置き、縦方向を縮めた距離 :math:`r` で縞 ``fract(r × 年輪の数)`` を作る。距離に fBm を足して年輪を不規則に揺らし、縦に引き伸ばした細かいノイズで繊維の筋を加える。

.. literalinclude:: ../examples/python/materials.py
   :language: python
   :pyobject: wood
   :lineno-match:
   :caption: examples/python/materials.py（wood）

1 本の年輪の中では、色が明るい部分（春から夏に育つ早材）から暗い部分（夏から秋に育つ晩材）へ徐々に変わり、次の年輪の始まりで急に明るく戻る。``smoothstep(0.55, 0.95, ring)`` は、この非対称な変化を表している。

大理石
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

大理石の脈は、Perlin が 1985 年の論文で示した古典的な例である。斜めの縞 :math:`\sin(\omega u)` の位相を、第 3 章の乱流 :math:`T` でずらす。

.. math::

   v = \sin\bigl(\omega u + s \, T(x, y)\bigr)

縞の値が 0 に近い所（:math:`1 - |v|` が 1 に近い所）だけに灰色の脈を入れると、白地に細い脈が流れた模様になる（:numref:`fig-patterns-marble-steps`）。:math:`\omega` で脈の間隔、:math:`s` で脈の乱れ方を制御できる。

.. literalinclude:: ../examples/python/materials.py
   :language: python
   :pyobject: marble_value
   :lineno-match:
   :caption: examples/python/materials.py（marble_value）

.. _fig-patterns-marble-steps:

.. figure:: _generated/materials/marble_steps.png
   :alt: 斜めの縞、乱流、乱流で歪めた縞、色を付けた大理石の 4 枚の画像

   大理石を作る手順

雲と錆
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**雲**\ は、fBm を雲の密度とみなし、しきい値 ``cover`` より大きい所を雲にする。``cover`` を下げると空を覆う雲の量が増える。少しずらした位置の密度との差で下側を暗くすると、雲に厚みが出る。

**錆**\ は、複数のノイズの役割を分けて組み合わせた例である。

.. literalinclude:: ../examples/python/materials.py
   :language: python
   :pyobject: rust
   :lineno-match:
   :caption: examples/python/materials.py（rust）

* 金属の地: 一方向に引き伸ばしたバリューノイズで、こすった筋（ヘアライン）を付ける。
* 錆の分布: 大きな fBm をしきい値で切ってマスクにする。しきい値を ``amount`` で動かすと、錆の量を 0（新品）から 1（全面の錆）まで連続的に変えられる。細かい fBm を足して、境界を崩す。
* 錆の色: 別の fBm で、濃い茶から橙までの色を選ぶ。
* 孔食: セルラーノイズの :math:`F_1` が小さい所を、錆の内側だけ暗い点にする。

このように「分布」「色のばらつき」「細部」を別々のノイズに担当させると、それぞれを独立に調整できる。錆の量だけを増やしたい、色だけを赤くしたいといった意図を、対応するパラメーター 1 つで実現できる。

.. _patterns-normal-map:

ハイトマップから法線マップを作る
------------------------------------------------------------

ここまでの模様は色だけで、光の当たり方は表していない。3D の描画では、表面の各点の\ **法線**\ （面に垂直な向きの単位ベクトル）と光の向きから明るさを計算する。光に正対する面は明るく、光に対して傾いた面は暗い。

細かな凹凸を本当に形（メッシュ）として作ると、頂点の数が膨大になる。そこで、形は平らなままにして、法線だけを画素ごとに変える。このための画像を\ **法線マップ**\ と呼ぶ。平らな板でも、法線マップに従って陰影が付くので、凹凸があるように見える。

法線は、表面の高さを画素ごとに記録した\ **ハイトマップ**\ :math:`h(x, y)` から計算できる。高さが x 方向に :math:`\partial h / \partial x`、y 方向に :math:`\partial h / \partial y` の割合で変わる面の法線は、

.. math::

   \boldsymbol{n} = \frac{(-s \, \partial h / \partial x, \ -s \, \partial h / \partial y, \ 1)}{\| (-s \, \partial h / \partial x, \ -s \, \partial h / \partial y, \ 1) \|}

である。:math:`s` は凹凸の強さ（高さの倍率）で、偏微分は隣の画素との差（中心差分）で近似する。

.. literalinclude:: ../examples/python/texture.py
   :language: python
   :pyobject: height_to_normal
   :lineno-match:
   :caption: examples/python/texture.py（height_to_normal）

法線の各成分は -1〜1 なので、:math:`(n + 1) / 2` で 0〜1 に写して RGB の画像として保存する（``encode_normal``）。平らな所の法線 :math:`(0, 0, 1)` は RGB :math:`(0.5, 0.5, 1)` になるので、法線マップは全体に青紫色の画像になる。

:numref:`fig-patterns-normal-map` は、セルラーノイズで作った石のハイトマップから法線マップを作り、光の向きを変えて陰影を付けたものである。同じ法線マップでも、光の向きに応じて明るい縁と暗い縁が入れ替わる。:numref:`fig-patterns-normal-strength` のように :math:`s` を大きくすると凹凸が強調されるが、大きすぎると細かいノイズまで強調されて汚く見える。

.. _fig-patterns-normal-map:

.. figure:: _generated/normal_map/normal_map.png
   :alt: 石のハイトマップ、法線マップ、左上からの光と右からの光で陰影を付けた画像

   ハイトマップから作った法線マップと、それによる陰影

.. _fig-patterns-normal-strength:

.. figure:: _generated/normal_map/normal_strength.png
   :alt: 凹凸の強さを 6、25、100 にした陰影の画像

   凹凸の強さ :math:`s` による違い

法線マップの y 成分（緑）の向きには 2 つの流儀がある。画像の上向きを +y とする\ **OpenGL 方式**\ と、下向きを +y とする\ **DirectX 方式**\ である。本書の ``height_to_normal`` は OpenGL 方式で、Godot や Blender はこの方式を使う。DirectX 方式のツールで使う場合は、緑の成分を反転する（:math:`G' = 1 - G`）。方式を取り違えると、凹凸が上下だけ逆に見える。

なお、ゲームで使う法線マップは、通常、面に沿った座標系（\ **接空間**\ 。面の u 方向・v 方向・法線方向を軸とする）で表す。こうしておくと、同じ法線マップを、曲面を含むどの面にも貼れる。本節の計算は平らな面を前提としているが、得られる画像は、そのまま接空間の法線マップとして使える。

.. _patterns-seamless:

シームレスなテクスチャ
------------------------------------------------------------

テクスチャは、広い面に同じ画像を何枚も並べて貼ることが多い。画像の右端と左端、上端と下端の模様がつながっていないと、並べたときに継ぎ目（シーム）が格子状に見える。繰り返して並べても継ぎ目が見えないテクスチャを\ **シームレス**\ （タイリング可能）なテクスチャと呼ぶ。

格子を使うノイズは、格子点の番号を周期 :math:`P` で折り返すだけで、周期 :math:`P` の関数になる。格子点 :math:`i` と :math:`i + P` に同じ乱数（または勾配）が割り当てられるので、:math:`x` と :math:`x + P` で値が一致する。

.. literalinclude:: ../examples/python/noise.py
   :language: python
   :pyobject: _wrap
   :lineno-match:
   :caption: examples/python/noise.py（_wrap）

画像 1 枚の範囲を座標 0〜:math:`P` に対応させれば、画像の端どうしがつながる。fBm では、周波数 :math:`L^k` 倍のオクターブの周期を :math:`P L^k` にする（第 3 章の ``fbm`` の ``period`` 引数）。:math:`P L^k` が整数でないと格子が周期に合わないので、lacunarity は 2 のような整数にする。

:numref:`fig-patterns-seamless` は、同じ画像を 2 × 2 に並べたものである。三角の印が継ぎ目の位置を示す。周期を持たないノイズでは継ぎ目で模様が途切れるが、``period`` を与えたノイズでは継ぎ目が分からない。

.. _fig-patterns-seamless:

.. figure:: _generated/seamless/seamless.png
   :alt: 周期を持たないノイズと周期を持つノイズを、それぞれ 2 × 2 に並べた 4 枚の画像

   シームレスなテクスチャ。各画像は 1 枚のテクスチャを 2 × 2 に並べたもの

``period`` を持たないノイズ（本書の ``simplex2`` など）でシームレスな画像を作るには、ほかに次の方法がある。

* **高次元の円周に沿って読む**: x 方向の周期を円 :math:`(\cos 2\pi u, \sin 2\pi u)` に、y 方向を別の円に対応させ、4 次元ノイズを読む。第 3 章のループするアニメーションと同じ考え方である。
* **端を混ぜる**: ずらした画像と元の画像を、端に近いほど重みを変えて混ぜる。簡単だが、混ぜた部分のコントラストが下がる。

周期を持つテクスチャでも、広い面に並べると同じ模様の繰り返しが目に付く。これを避けるには、繰り返しの単位を大きくするか、別の大きなノイズで色や明るさを変調する。

.. _patterns-pbr:

PBR 用テクスチャ一式
------------------------------------------------------------

現在のゲームエンジンや 3D ソフトウェアの多くは、\ **物理ベースレンダリング**\ （PBR、physically based rendering）で描画する。PBR では、光の反射を物理的な法則に近い式で計算し、材質を少数の分かりやすいパラメーターで表す。パラメーターを画素ごとに変えるため、材質は次のような複数のテクスチャ（\ **マップ**\ ）の組で与える。

.. list-table:: PBR で使う主なマップ
   :header-rows: 1
   :widths: 22 78

   * - マップ
     - 内容
   * - ベースカラー
     - 表面の色。陰影や光沢を含まない、素材そのものの色（アルベド）
   * - ラフネス
     - 表面の粗さ（0〜1）。小さいほど鏡のように鋭いハイライトになり、大きいほどぼやけた反射になる
   * - メタリック
     - 金属かどうか（通常は 0 か 1）。金属は反射光に自分の色が付き、拡散反射をほとんど持たない
   * - 法線
     - 前節の法線マップ。細かな凹凸を表す
   * - ハイト・AO
     - 高さ（視差や変位に使う）と、くぼみに光が届きにくい度合い（アンビエントオクルージョン）

写真から作るテクスチャでは、これらのマップを別々に作って整合をとる必要がある。手続きで作る場合は、\ **すべてのマップを同じ手続き・同じ中間データから出力**\ できるのが大きな利点である。錆の例では、錆のマスク 1 枚から、ベースカラー（錆の色）・ラフネス（錆は粗い）・メタリック（錆は金属でない）・高さ（錆は盛り上がる）を決める。マスクを変えれば、すべてのマップが矛盾なく一緒に変わる。

.. literalinclude:: ../examples/python/pbr_maps.py
   :language: python
   :pyobject: pbr_maps
   :lineno-match:
   :caption: examples/python/pbr_maps.py（pbr_maps）

:numref:`fig-patterns-pbr` の右端は、各マップを使って陰影を付けた例である。拡散反射に、ラフネスが小さいほど鋭く強いハイライトを足した簡単な式で、ゲームエンジンの PBR の計算とは異なるが、マップの役割は確かめられる。金属の部分には鋭いハイライトが、錆の部分には凹凸による陰影が付く。

.. _fig-patterns-pbr:

.. figure:: _generated/pbr_maps/pbr_maps.png
   :alt: 錆びた金属のベースカラー、ラフネス、メタリック、法線マップと、陰影を付けた画像

   同じ手続きから出力した PBR 用のマップ

スクリプトは、各マップを個別の PNG ファイルとしても保存する（:download:`base_color.png <_generated/pbr_maps/base_color.png>`、:download:`roughness.png <_generated/pbr_maps/roughness.png>`、:download:`metallic.png <_generated/pbr_maps/metallic.png>`、:download:`normal.png <_generated/pbr_maps/normal.png>`）。Godot の StandardMaterial3D などのマテリアルの各項目に割り当てれば、そのまま使える。ベースカラーは sRGB の画像、ラフネス・メタリック・法線は色ではなく数値を格納した画像（線形のデータ）として読み込むように設定する。

.. _patterns-glsl:

GLSL での実装
------------------------------------------------------------

GLSL のデモでは、レンガ・六角形タイル・石畳・木目・大理石を切り替え、目地の太さ・歪み・色のばらつきなどを調整できる。各模様の関数は色と高さを返し、高さの差分から法線を求めて陰影を付けている。光の向きを回すと、法線マップと同じ仕組みで凹凸が浮かび上がる。

`ブラウザーで開く <_static/glsl/patterns.html>`__ ／ :download:`patterns.html をダウンロード <../examples/glsl/patterns.html>`

レンガの関数を示す。Python の ``bricks`` と同じ手順で目地までの距離 ``edge`` を求め、色と高さの両方をこの距離から決めている。

.. literalinclude:: ../examples/glsl/patterns.html
   :language: glsl
   :start-at: // レンガ:
   :end-before: // 六角形タイル:
   :lineno-match:
   :caption: examples/glsl/patterns.html（bricks）

``main`` では、模様の関数を 3 回（その画素と、右と上に 1 画素ずれた位置で）呼び、高さの差から法線を求める。画像として保存した法線マップの代わりに、その場で法線を計算していることになる。

.. literalinclude:: ../examples/glsl/patterns.html
   :language: glsl
   :start-at: // ---- メイン
   :end-before: // [shader-end]
   :lineno-match:
   :caption: examples/glsl/patterns.html（main）

まとめ
------------------------------------------------------------

* ``floor`` で求めたセルの番号と ``fract`` で求めたセル内の座標を使い、1 つの図形を描けば繰り返し模様になる。セルの番号をハッシュに入れると、セルごとのばらつきを付けられる。
* レンガは段ごとのずらし、六角形はずらした 2 組の格子で作る。境界は ``smoothstep`` でぼかしてエイリアシングを抑える。
* 符号付き距離関数（SDF）は、図形の境界までの距離を返す。最小値・最大値・smooth min で図形を組み合わせられ、ぼかし・縁取り・高さにも使える。
* セルラーノイズの :math:`F_1`・:math:`F_2 - F_1`・セルの乱数を使い分けると、石畳・ひび割れ・細胞などの模様になる。
* 木目・大理石・雲・錆は、素材の成り立ちを少数のノイズで真似て作る。役割ごとにノイズを分けると、意図どおりに調整しやすい。
* ハイトマップの差分から法線を求め、RGB に符号化すると法線マップになる。y の向き（OpenGL 方式と DirectX 方式）に注意する。
* 格子の番号を周期で折り返すと、継ぎ目の無いテクスチャになる。
* PBR のマップ（ベースカラー・ラフネス・メタリック・法線）は、同じ手続きの中間データから出力すると互いに整合する。
