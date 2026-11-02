第 6 章　メッシュの基礎と生成
============================================================

第 I 部では、平面上の各点の色を決めるテクスチャを作った。第 II 部では、立体の形を作る。ゲームや映像で立体の形を表す最も一般的な方法は、表面を多数の三角形で覆った\ **メッシュ**\ である。本章では、メッシュがどのようなデータでできているかを確認し、格子・円柱・球のような基本形状から、回転体やスイープ（断面を曲線に沿って動かす方法）による形状までを手続きで作る。ここで作る関数は、第 7 章の地形や第 8 章の樹木でも使う。

本章の手法は、第 1 章の分類では関数型に当たる。形を「パラメーター :math:`(u, v)` から 3 次元の点への関数」として書き、それを格子状に評価して三角形をつなぐ。

本章の図は、次のスクリプトで作っている。メッシュを作る関数は、ライブラリ ``meshgen.py`` にまとめた。

* :download:`meshgen.py <../examples/python/meshgen.py>`: 基本形状・回転体・スイープを作る関数（ライブラリ）
* :download:`mesh_basics.py <../examples/python/mesh_basics.py>`: メッシュの表現と基本形状の図
* :download:`mesh_sweep.py <../examples/python/mesh_sweep.py>`: 回転体・スイープの図と OBJ ファイルの書き出し

本章の座標系は、図を描く matplotlib に合わせて z 軸を上にとる。Godot など y 軸を上にとるツールに渡すときの変換は、最後の節で扱う。

メッシュの表現
------------------------------------------------------------

頂点配列とインデックス配列
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

メッシュの角の点を\ **頂点**\ 、頂点を結んでできる多角形を\ **面**\ と呼ぶ。GPU は三角形を最も効率よく描けるので、四角形以上の面も最終的には三角形に分けて扱う。

三角形を「3 つの頂点の座標」の組で並べると、隣り合う三角形が共有する頂点の座標を何度も書くことになる。そこで、頂点の座標を 1 回ずつ並べた\ **頂点配列**\ と、各三角形がどの頂点を使うかを番号で並べた\ **インデックス配列**\ の 2 つに分けて持つ。:numref:`fig-mesh-buffers` の例では、三角形 4 枚分の 12 個の角を、6 個の頂点で表している。共有を明示できるので、頂点を 1 つ動かすだけで、それを使うすべての三角形の形が変わる。GPU に渡すデータもこの形で、それぞれ頂点バッファー・インデックスバッファーと呼ばれる。

.. _fig-mesh-buffers:

.. figure:: _generated/mesh_basics/mesh_buffers.png
   :alt: 6 個の頂点と 4 枚の三角形からなる長方形のメッシュと、頂点配列・インデックス配列の表

   頂点配列（各頂点の座標）とインデックス配列（各三角形が使う頂点の番号）

本書では、メッシュを次のクラスで表す。頂点ごとの値（座標、後で述べる UV）は、頂点番号を行の番号とする配列に入れる。

.. literalinclude:: ../examples/python/mesh.py
   :language: python
   :start-at: @dataclass
   :end-before: def face_normals
   :lineno-match:
   :caption: examples/python/mesh.py（Mesh）

頂点の並び順と表裏
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

三角形には表と裏がある。どちらが表かは、インデックス配列に書いた 3 頂点の並び順（\ **ワインディング**\ ）で決める。本書と OBJ 形式（後述）では、表から見て反時計回りに並べる（:numref:`fig-mesh-winding`）。並び順を逆にすると表裏が入れ替わる。

.. _fig-mesh-winding:

.. figure:: _generated/mesh_basics/winding.png
   :alt: 頂点を反時計回りに並べた三角形と、時計回りに並べた三角形

   頂点の並び順と表裏。数字はインデックス配列に書いた順番

表裏を区別するのは、閉じた立体の裏側（カメラから見て奥を向いた面）を描画から省くためである。この処理を\ **背面カリング**\ と呼び、描く三角形がおよそ半分になる。並び順を間違えると、形は正しいのに一部の面が消えて見える。手続きで三角形を作るときに最も多い誤りの 1 つである。どちらの並び順を表とするかはツールによって異なり、Godot は時計回りを表とする。ツールの間でメッシュを受け渡すときは、この違いに注意する。

法線
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

面に垂直で、表の側を向く長さ 1 のベクトルを\ **法線**\ と呼ぶ。法線は陰影の計算に使う。最も簡単なランバート反射（拡散反射）では、光の来る向きを単位ベクトル :math:`\boldsymbol{l}` として、面の明るさを法線 :math:`\boldsymbol{n}` との内積 :math:`\max(0, \boldsymbol{n} \cdot \boldsymbol{l})` に比例させる。光に正対する面ほど明るく、光と平行な面は暗い。本書の図では、影の部分が真っ黒にならないように、これに一定の明るさを足している（``mesh.py`` の ``shade``）。

三角形の頂点を反時計回りに :math:`\boldsymbol{p}_0, \boldsymbol{p}_1, \boldsymbol{p}_2` とすると、2 辺の外積が表の側を向く垂直なベクトルになる（付録 A）。これを正規化したものが\ **面の法線**\ である。

.. math::

   \boldsymbol{n} = \frac{(\boldsymbol{p}_1 - \boldsymbol{p}_0) \times (\boldsymbol{p}_2 - \boldsymbol{p}_0)}{|(\boldsymbol{p}_1 - \boldsymbol{p}_0) \times (\boldsymbol{p}_2 - \boldsymbol{p}_0)|}

一方、GPU は法線を頂点ごとに受け取る。曲面を近似したメッシュでは、頂点を共有するすべての三角形の法線を平均したものを\ **頂点の法線**\ とする。平均するときに三角形の面積で重みを付けると、細長い小さな三角形の影響が小さくなる。外積の長さは三角形の面積の 2 倍なので、外積を正規化せずにそのまま足せばよい。

.. literalinclude:: ../examples/python/mesh.py
   :language: python
   :pyobject: Mesh.vertex_normals
   :lineno-match:
   :caption: examples/python/mesh.py（Mesh.vertex_normals）

``np.add.at`` は、同じ番号が何度現れても、そのたびに足し込む。``normals[faces[:, k]] += weighted`` と書くと、重複した番号には 1 回しか足されないので注意する。

.. _fig-mesh-normals:

.. figure:: _generated/mesh_basics/normals_2d.png
   :alt: 正八角形の各辺に垂直な法線と、各頂点で平均した法線と、その間を補間した法線

   面の法線（左）と頂点の法線（右）。円を正八角形で近似したものを断面で見ている

描画のときは、頂点の法線を三角形の内部で補間して、画素ごとに陰影を計算する（:numref:`fig-mesh-normals` の右の橙の矢印）。こうすると、平らな三角形の集まりでも、法線が滑らかに変わるので、曲面のように見える。これを\ **スムーズシェーディング**\ と呼ぶ。面の法線をそのまま使い、三角形ごとに一様な明るさで塗るものを\ **フラットシェーディング**\ と呼ぶ。

.. _fig-mesh-shading:

.. figure:: _generated/mesh_basics/shading.png
   :alt: 角ばって見える球と滑らかに見える球、角が丸く汚れて見える円柱と角がはっきりした円柱

   フラットシェーディングとスムーズシェーディング（左 2 つ）、円柱の縁の頂点を共有した場合と分割した場合（右 2 つ）

:numref:`fig-mesh-shading` の左 2 つは、同じ 12 × 8 分割の球である。スムーズシェーディングでは三角形の境目がほとんど見えないが、輪郭の折れ線は残る。陰影はごまかせても、形そのものは三角形のままだからである。

右 2 つは円柱である。側面とふたが縁の頂点を共有すると、縁の頂点の法線は側面の法線とふたの法線の平均（斜め 45 度）になる。その結果、側面とふたの陰影が縁に向かってぼやけ、角が丸く汚れて見える。角を鋭く見せたい所（\ **ハードエッジ**\ ）では、同じ位置に頂点を 2 つ置き、側面用とふた用に別々の法線を持たせる。頂点は「位置」ではなく「位置・法線・UV などの属性の組」であり、属性が 1 つでも違えば別の頂点になる。

UV 座標
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

メッシュにテクスチャ（画像）を貼るには、各頂点が画像のどこに対応するかを決める。この 2 次元の座標を\ **UV 座標**\ と呼び、横を :math:`u`、縦を :math:`v` として 0〜1 の範囲で表すことが多い。三角形の内部では、頂点の UV を補間した位置の画素が使われる。立体の表面を切り開いて平面に広げ、画像の上に置く操作と考えるとよい。この平面の配置を\ **UV 展開**\ と呼ぶ。

.. _fig-mesh-uv:

.. figure:: _generated/mesh_basics/uv_mapping.png
   :alt: チェッカー模様の正方形の上に球の三角形を展開した図と、チェッカー模様を貼った球と円柱

   UV 展開した球の三角形（左）と、UV に従ってチェッカー模様を貼った球と円柱

次節の作り方では、形を作るためのパラメーター :math:`(u, v)` をそのまま UV 座標に使える（:numref:`fig-mesh-uv`）。このとき次の 2 点に注意する。

* **継ぎ目**: 球や円柱を 1 周させると、経度 0 度と 360 度が同じ位置になる。位置は同じでも、UV は :math:`u = 0` と :math:`u = 1` で異なるので、継ぎ目の頂点は 2 つずつ持つ（前項と同じく、属性が違えば別の頂点）。
* **ゆがみ**: 球の UV 展開では、極に近いほど三角形が横に引き伸ばされる。チェッカー模様のマスが極の近くで細くなっているのはこのためである。ゆがみの無い展開は一般には存在せず、どこにゆがみや継ぎ目を置くかを用途に合わせて選ぶ。

基本形状を手続きで作る
------------------------------------------------------------

格子
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

多くの形は、2 つのパラメーター :math:`(u, v)` から点 :math:`\boldsymbol{P}(u, v)` を返す関数（\ **パラメトリック曲面**\ ）として書ける。:math:`u` と :math:`v` をそれぞれ等間隔に分けて評価すると、点が格子状に並ぶ。隣り合う 4 点が作る四角形を 2 枚の三角形に分ければ、メッシュができる。三角形の分け方は形によらず同じなので、関数にしておく。

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: grid_faces
   :lineno-match:
   :caption: examples/python/meshgen.py（grid_faces）

四角形の 4 頂点を :math:`a` （左下）、:math:`b` （右下）、:math:`c` （右上）、:math:`d` （左上）とし、:math:`(a, b, c)` と :math:`(a, c, d)` の 2 枚にする。:math:`u` の増える向きから :math:`v` の増える向きへ反時計回りになるので、:math:`\partial \boldsymbol{P} / \partial u \times \partial \boldsymbol{P} / \partial v` の向きが表になる。形を作るときは、この外積が外を向くように :math:`u` と :math:`v` の向きを選べばよい。

点の格子から、三角形と UV を付けたメッシュを作る関数は次のとおりである。球の極のように点が 1 か所に集まる所では面積 0 の三角形ができるので、取り除いておく。

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: parametric_surface
   :lineno-match:
   :caption: examples/python/meshgen.py（parametric_surface）

円柱と球
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

半径 :math:`r`、高さ :math:`h` の円柱の側面と、半径 :math:`r` の球は、:math:`0 \le u, v \le 1` を使って次のように書ける。

.. math::

   \text{円柱}: \boldsymbol{P}(u, v) &= (r \cos 2\pi u,\ r \sin 2\pi u,\ h v) \\
   \text{球}: \boldsymbol{P}(u, v) &= (r \cos \phi \cos 2\pi u,\ r \cos \phi \sin 2\pi u,\ r \sin \phi), \quad \phi = \pi (v - 1/2)

球の :math:`u` は経度、:math:`\phi` は緯度に当たる。この作り方の球を\ **UV 球**\ と呼ぶ。円柱には、中心の頂点から扇形に三角形を張ったふたを付ける。ふたは側面と頂点を共有させず、ハードエッジにする。

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: cylinder
   :lineno-match:
   :caption: examples/python/meshgen.py（cylinder）

:numref:`fig-mesh-primitives` は、格子・円柱・球を作り、三角形の辺（\ **ワイヤーフレーム**\ ）と陰影付きで描いたものである。格子は、頂点の z 座標を後から書き換えるだけで起伏のある面になる。第 7 章では、この z 座標をハイトマップ（高さの 2 次元配列）から与えて地形を作る。

.. _fig-mesh-primitives:

.. figure:: _generated/mesh_basics/primitives.png
   :alt: 起伏のある格子、円柱、球のワイヤーフレームと陰影付きの表示

   手続きで作った基本形状。上はワイヤーフレーム、下は陰影付き（フラットシェーディング）

分割数は、形の滑らかさと三角形の数（描画の負荷）の釣り合いを決めるパラメーターである。経度 :math:`m`、緯度 :math:`n` 分割の UV 球の三角形は、極の周りでは 1 マス 1 枚になるので :math:`2m(n - 1)` 枚になる（:numref:`fig-mesh-sphere-resolution`）。分割数を 2 倍にすると三角形は約 4 倍になるが、輪郭の折れ線は分割数 24 程度で目立たなくなる。ゲームでは、遠くの物体ほど分割数の少ないメッシュに切り替えて負荷を下げる。これを\ **LOD**\ （level of detail）と呼ぶ（第 7 章）。

.. _fig-mesh-sphere-resolution:

.. figure:: _generated/mesh_basics/sphere_resolution.png
   :alt: 分割数を 6 × 4 から 48 × 24 まで変えた 4 個の球

   UV 球の分割数（経度 × 緯度）と三角形の数

UV 球は極の近くに細い三角形が集まる。三角形の大きさをそろえたい場合は、正二十面体の各三角形を 4 つに分け、頂点を球面に押し出す操作を繰り返す方法（\ **アイコスフィア**\ ）が使われる。

押し出し・回転体・スイープ
------------------------------------------------------------

複雑な形も、「2 次元の断面」と「それを動かす経路」に分けて考えると、少ないパラメーターで作れる。

* **押し出し**: 断面を直線に沿って動かす。平面図の多角形から壁や柱を作る。
* **回転体**: 断面を軸の周りに回す。壺・瓶・グラス・ろうそくなど、ろくろで作れる形。
* **スイープ**: 断面を曲線に沿って動かす。パイプ・ロープ・枝・道路・線路。

押し出しは、経路が直線のスイープの特別な場合なので、以下では回転体とスイープを扱う。

回転体: 壺
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

半径と高さの組 :math:`(r_k, z_k)` を並べた断面の曲線を、z 軸の周りに 1 周させる。断面の点の番号を :math:`v`、回転角を :math:`u` とすれば、円柱と同じ格子になる。円柱は、断面が縦の線分の回転体である。

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: lathe
   :lineno-match:
   :caption: examples/python/meshgen.py（lathe）

形の良し悪しは断面の曲線で決まる。壺の断面を、底・胴・首・口の 4 つの制御点で決めることにする。制御点の間は、すべての制御点を通る滑らかな曲線（Catmull-Rom スプライン、後述）でつなぐ。厚みを持たせるため、断面は底の中心から外側を上り、口で折り返して内側を下りる。

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :pyobject: vase_profile
   :lineno-match:
   :caption: examples/python/mesh_sweep.py（vase_profile）

.. _fig-mesh-lathe:

.. figure:: _generated/mesh_sweep/lathe.png
   :alt: 制御点と壺の断面の曲線、パラメーターの異なる 3 個の壺

   壺の断面の曲線（左）と、パラメーターを変えた回転体

:numref:`fig-mesh-lathe` のように、6 個の数（底・胴・首・口の半径、胴の高さの割合、全体の高さ）を変えるだけで、さまざまな壺ができる。これらの数を乱数で決めれば、形の異なる壺を大量に作れる。ただし、すべてを独立に乱数で決めると「口が胴より広い」ような不格好な組み合わせも出る。「首の半径は胴の半径の 0.3〜0.7 倍」のように、パラメーターの間の関係を範囲で決めておくと、結果を制御しやすい。この考え方は第 17 章で改めて扱う。

断面の 1 点が回転軸の上（:math:`r = 0`）にあると、そこでは 1 周分の頂点が 1 点に重なる。底の中心がこれに当たり、面積 0 の三角形は ``parametric_surface`` が取り除く。

スイープと曲線に沿った座標系
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

曲線 :math:`\boldsymbol{C}(s)` に沿って断面を動かすには、曲線の各点で、断面を置く平面の向きを決める必要がある。各点に、曲線の進む向き :math:`\boldsymbol{T}` （接線）と、それに垂直な 2 本の単位ベクトル :math:`\boldsymbol{N}, \boldsymbol{B}` を置く。この 3 本の組を\ **標構**\ （フレーム）と呼ぶ。断面の 2 次元座標 :math:`(x, y)` は、次の点に置く。

.. math::

   \boldsymbol{P}(x, y, s) = \boldsymbol{C}(s) + x \boldsymbol{N}(s) + y \boldsymbol{B}(s)

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: sweep
   :lineno-match:
   :caption: examples/python/meshgen.py（sweep）

問題は :math:`\boldsymbol{N}` の決め方である。数学の教科書で習う\ **フレネ標構**\ では、接線の変化の向き（曲線が曲がっていく向き）を :math:`\boldsymbol{N}` とし、:math:`\boldsymbol{B} = \boldsymbol{T} \times \boldsymbol{N}` とする。曲線の形だけで決まる自然な定義だが、次の欠点がある。

* 直線の部分では曲がる向きが無いので、:math:`\boldsymbol{N}` が決まらない。
* S 字の曲線の変曲点（曲がる向きが左から右へ変わる点）で、:math:`\boldsymbol{N}` が急に反対を向く。
* 曲線がねじれていると、:math:`\boldsymbol{N}` も曲線の周りを回る。

パイプのように断面が円なら形は変わらないが、UV で貼った模様や、道路のように向きのある断面は、途中で急に回ってしまう。

そこで、曲線の周りの余計な回転が最も少なくなるように :math:`\boldsymbol{N}` を運ぶ\ **回転最小化標構**\ （rotation minimizing frame）を使う。最初の点で :math:`\boldsymbol{N}` を適当に決め、次の点へは「前の接線を今の接線に重ねる最小の回転」で :math:`\boldsymbol{N}` を運ぶ。離散的な点列では、Wang らが 2008 年に示した\ **二重反射法**\ で簡単に計算できる。点 :math:`\boldsymbol{x}_i` での標構を、2 回の鏡映（面に関する反射）で次の点へ移す。

.. math::

   \boldsymbol{v}_1 &= \boldsymbol{x}_{i+1} - \boldsymbol{x}_i, \quad
   \boldsymbol{N}^L = \boldsymbol{N}_i - \frac{2 (\boldsymbol{v}_1 \cdot \boldsymbol{N}_i)}{\boldsymbol{v}_1 \cdot \boldsymbol{v}_1} \boldsymbol{v}_1, \quad
   \boldsymbol{T}^L = \boldsymbol{T}_i - \frac{2 (\boldsymbol{v}_1 \cdot \boldsymbol{T}_i)}{\boldsymbol{v}_1 \cdot \boldsymbol{v}_1} \boldsymbol{v}_1 \\
   \boldsymbol{v}_2 &= \boldsymbol{T}_{i+1} - \boldsymbol{T}^L, \quad
   \boldsymbol{N}_{i+1} = \boldsymbol{N}^L - \frac{2 (\boldsymbol{v}_2 \cdot \boldsymbol{N}^L)}{\boldsymbol{v}_2 \cdot \boldsymbol{v}_2} \boldsymbol{v}_2

1 回目の反射は、2 点を結ぶ線分の垂直二等分面に関するもので、点 :math:`\boldsymbol{x}_i` を :math:`\boldsymbol{x}_{i+1}` に移す。反射は向きを裏返すので、2 回目の反射で、反射後の接線 :math:`\boldsymbol{T}^L` を目標の接線 :math:`\boldsymbol{T}_{i+1}` に重ねながら向きを元に戻す。反射を 2 回続けると回転になり、しかも余計なねじれをほとんど生まない。

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :pyobject: rotation_minimizing_frames
   :lineno-match:
   :caption: examples/python/meshgen.py（rotation_minimizing_frames）

:numref:`fig-mesh-frames` は、変曲点を持つ曲線に沿って、断面の一部を赤く塗ったパイプを作り、2 つの標構を比べたものである。フレネ標構では変曲点で赤い帯が反対側へ飛ぶ。回転最小化標構では、帯が曲線の上側に沿って滑らかに続く。

.. _fig-mesh-frames:

.. figure:: _generated/mesh_sweep/frames.png
   :alt: S 字に曲がるパイプを 2 本並べた図。左は途中で赤い帯が裏側へ回り、右は帯が上側に沿って続く

   フレネ標構（左）と回転最小化標構（右）で作ったパイプ。赤い帯は断面の 1/8 の区画

閉じた曲線の場合、回転最小化標構で 1 周して戻ってきた :math:`\boldsymbol{N}` は、一般に出発したときの :math:`\boldsymbol{N}` と一致しない。そのままでは始点と終点で断面の向きが食い違い、模様に継ぎ目ができる。食い違いの角度を求め、曲線全体に少しずつ割り振って打ち消す。

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :pyobject: closed_frames
   :lineno-match:
   :caption: examples/python/mesh_sweep.py（closed_frames）

断面の大きさを点ごとに変えると、先細りの形ができる。:numref:`fig-mesh-pipe` の右は、少しずつ向きを変えながら伸びる経路を乱数で作り、根元から先へ細くなる円をスイープしたものである。曲がり方の滑らかさ（乱数を混ぜる割合）と、太さの減り方が、形を制御するパラメーターになる。第 8 章では、同じ考え方で樹木の枝を作る。

.. _fig-mesh-pipe:

.. figure:: _generated/mesh_sweep/pipe.png
   :alt: 三葉結び目の形のパイプと、先細りの触手のような 5 本の管

   三葉結び目に沿ったパイプ（左）と、太さを変えながらスイープした触手（右）

スイープ: 道路
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

道路は、経路と断面の両方に向きがあるスイープの例である。経路は、少数の制御点を置いて、その間を滑らかな曲線で補う。ここでは、すべての制御点を通る\ **Catmull-Rom スプライン**\ を使う。制御点 :math:`\boldsymbol{p}_1` と :math:`\boldsymbol{p}_2` の間の区間は、前後の制御点 :math:`\boldsymbol{p}_0, \boldsymbol{p}_3` も使って、:math:`0 \le t \le 1` の 3 次式で表す。

.. math::

   \boldsymbol{C}(t) = \frac{1}{2} \bigl( 2\boldsymbol{p}_1 + (\boldsymbol{p}_2 - \boldsymbol{p}_0) t + (2\boldsymbol{p}_0 - 5\boldsymbol{p}_1 + 4\boldsymbol{p}_2 - \boldsymbol{p}_3) t^2 + (3\boldsymbol{p}_1 - \boldsymbol{p}_0 - 3\boldsymbol{p}_2 + \boldsymbol{p}_3) t^3 \bigr)

区間の端での接線は、前後の制御点を結ぶ向き :math:`(\boldsymbol{p}_2 - \boldsymbol{p}_0) / 2` になり、隣の区間と一致するので、つなぎ目で折れない。制御点を動かすと、その前後 2 区間だけが変わる。

道路では、断面を横に傾けたくない（左右の向きを常に水平に保ちたい）。そこで、回転最小化標構ではなく、上向きのベクトル :math:`\boldsymbol{U} = (0, 0, 1)` を基準にして、左右の向きを :math:`\boldsymbol{U} \times \boldsymbol{T}` で決める。坂道でも路面は左右に水平のままで、上の向きだけが進行方向に合わせて前後に傾く。

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :pyobject: road_frames
   :lineno-match:
   :caption: examples/python/mesh_sweep.py（road_frames）

この方法は、経路が真上や真下を向くと左右の向きが決まらないが、道路ではそのような経路は無いので問題にならない。カーブで内側に傾けたい（カント）場合は、左右の向きを接線の周りに回転させる角度をパラメーターとして与える。

断面は、道の中心からの位置と高さの組を左から右へ並べる。区間ごとに種類（法面・縁石・路面・中央線）を決め、三角形の色に使う。中央線は、道のり 4 m ごとに路面の色に戻して破線にした。

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :start-at: # 道路の断面
   :end-before: ROAD_COLORS
   :lineno-match:
   :caption: examples/python/mesh_sweep.py（道路の断面）

.. _fig-mesh-road:

.. figure:: _generated/mesh_sweep/road.png
   :alt: 道路の断面の図、制御点とスプラインに沿った道路を上から見た図、道路の立体

   道路の断面（左）、6 個の制御点から作った道路を上から見た図（中央）と立体（右）

経路の制御点・断面の形・破線の間隔が、そのまま道路のパラメーターになる（:numref:`fig-mesh-road`）。断面を差し替えれば、同じ経路から線路や川（断面を下に凹ませる）も作れる。第 11 章で作る街路網の各道を、この方法で立体にできる。

OBJ 形式での出力
------------------------------------------------------------

手続きで作ったメッシュを、Blender や Godot などのツールで使うには、ファイルに保存する。\ **OBJ 形式**\ （Wavefront OBJ）は、ほとんどの 3D ツールが読み書きできるテキスト形式で、中身を目で確かめやすい。1 行に 1 つの要素を書き、行の先頭の記号で種類を表す。

.. list-table:: OBJ 形式の主な行
   :header-rows: 1
   :widths: 15 40 45

   * - 記号
     - 内容
     - 例
   * - ``v``
     - 頂点の位置 :math:`(x, y, z)`
     - ``v 0.5 0.0 -0.5``
   * - ``vt``
     - UV 座標 :math:`(u, v)`
     - ``vt 1.0 0.0``
   * - ``vn``
     - 法線
     - ``vn 0.0 1.0 0.0``
   * - ``f``
     - 面。頂点ごとに「位置/UV/法線」の番号を書く
     - ``f 1/1/1 2/2/2 4/4/4``

番号は、それぞれの種類の行を出てきた順に 1 から数える（配列の番号は 0 からなので、書き出すときに 1 を足す）。OBJ では位置・UV・法線に別々の番号を付けられるが、本書のメッシュは頂点ごとに 3 つの属性をそろえて持っているので、3 つとも同じ番号を書く。

.. literalinclude:: ../examples/python/mesh.py
   :language: python
   :pyobject: write_obj
   :lineno-match:
   :caption: examples/python/mesh.py（write_obj）

本章の図は z 軸を上としているが、OBJ 形式を読み込む多くのツールや Godot は y 軸を上とする。そのため、書き出す前に x 軸の周りに回転して、z 軸を y 軸に移す。回転（行列式が 1 の変換）なので、三角形の表裏は変わらない。単に y と z を入れ替えると鏡に映した形になり、表裏が逆転するので注意する。

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :pyobject: to_y_up
   :lineno-match:
   :caption: examples/python/mesh_sweep.py（to_y_up）

1 × 1 の四角形（三角形 2 枚）を書き出すと、次のようになる。

.. literalinclude:: _generated/mesh_sweep/quad.obj
   :language: text
   :linenos:
   :caption: _generated/mesh_sweep/quad.obj

Godot は OBJ ファイルをそのままメッシュとして読み込める。ただし、ファイルを介すると、生成はゲームを作る段階で 1 回行うことになる。ゲームの実行中にシードやプレイヤーの行動に応じてメッシュを作るには、Godot の ``SurfaceTool`` や ``ArrayMesh`` で、本章と同じ頂点配列とインデックス配列を直接組み立てる。その方法は第 15 章で扱う。

まとめ
------------------------------------------------------------

* メッシュは、頂点配列（位置・法線・UV などの属性）と、三角形ごとの頂点番号を並べたインデックス配列で表す。
* 三角形の表裏は頂点の並び順で決まる。本書と OBJ 形式は反時計回りを表とする。
* 面の法線は 2 辺の外積で求め、頂点の法線は周りの面の法線を面積で重み付けして平均する。角を鋭く見せたい所では頂点を分割する。
* UV 座標はテクスチャのどこを貼るかを表す。継ぎ目では位置が同じでも頂点を分け、極の近くではゆがみが生じる。
* パラメトリック曲面を格子状に評価すれば、格子・円柱・球・回転体・スイープを同じ三角形分割の関数で作れる。分割数は滑らかさと負荷の釣り合いを決める。
* 回転体は断面の曲線、スイープは断面と経路で形が決まる。少数の制御点とその関係をパラメーターにすると、形を制御しやすい。
* スイープの断面の向きには回転最小化標構（二重反射法）を使うと、ねじれや急な反転が起きない。道路のように水平を保ちたい場合は上向きのベクトルを基準にする。
* OBJ 形式で書き出せば、ほかのツールで使える。y 軸が上のツールに渡すときは、鏡映ではなく回転で座標を変換する。
