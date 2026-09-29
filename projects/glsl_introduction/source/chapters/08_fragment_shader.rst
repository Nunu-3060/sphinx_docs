第 8 章 フラグメントシェーダー
==============================

フラグメントシェーダーは、フラグメントごとに実行され、その色を決めます。画面に表示される色はすべてフラグメントシェーダーが計算したものなので、見た目の表現の多くはフラグメントシェーダーで行います。この章では、フラグメントシェーダーだけで図形や模様を描く方法を通して、フラグメントシェーダーの考え方を説明します。

フラグメントシェーダーの組み込み変数
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 変数
     - 型
     - 内容
   * - ``gl_FragCoord``
     - ``vec4``
     - 入力。フラグメントのウィンドウ座標です。``xy`` はピクセル単位の位置、``z`` は深度値です。
   * - ``gl_FrontFacing``
     - ``bool``
     - 入力。フラグメントが表向きの三角形のものなら ``true`` です。
   * - ``gl_PointCoord``
     - ``vec2``
     - 入力。点を描くときの、点の中での位置（0.0〜1.0）です。
   * - ``gl_FragDepth``
     - ``float``
     - 出力。深度値を書き換えたい場合に書き込みます。

``gl_FragCoord.xy`` は、キャンバスの左下を原点とするピクセル単位の座標です。値はピクセルの中心を指すので、左下のピクセルでは (0.5, 0.5) になります。

画面全体を覆う描画
------------------

フラグメントシェーダーだけで絵を描く場合は、画面全体を覆う図形を描いて、画面のすべてのピクセルでフラグメントシェーダーを実行させます。本書のサンプルでは、次の頂点シェーダーで、画面全体を覆う大きな三角形を描いています。

.. literalinclude:: ../../examples/shaders/04_fragment_shapes.vert
   :language: glsl
   :caption: 04_fragment_shapes.vert（頂点シェーダー）

``gl_VertexID`` は描画中の頂点の番号で、``drawArrays(gl.TRIANGLES, 0, 3)`` で描くと 0、1、2 になります。この番号で配列から座標を選ぶので、頂点バッファーを用意する必要がありません。3 つの頂点 (-1, -1)、(3, -1)、(-1, 3) を結ぶ三角形は、画面全体（-1〜1 の正方形）を完全に覆います。画面の外にはみ出た部分は、クリッピングで取り除かれます。

座標の正規化
------------

``gl_FragCoord.xy`` はピクセル単位なので、キャンバスの大きさによって値の範囲が変わります。そこで、キャンバスの大きさ（``uResolution``）で割って、扱いやすい範囲に変換します。

.. code-block:: glsl

   // uv：左下が (0, 0)、右上が (1, 1)
   vec2 uv = gl_FragCoord.xy / uResolution;

   // p：画面の中心が (0, 0)、短辺方向が -1 から 1（縦横比を補正する）
   vec2 p = (gl_FragCoord.xy * 2.0 - uResolution) / min(uResolution.x, uResolution.y);

``uv`` は縦横で長さの単位が異なるため、``uv`` で円を描くと、横長のキャンバスでは横に伸びた楕円になります。``p`` は縦横を同じ長さで割っているので、図形の形を正しく保てます。図形を描くときは ``p``、画面全体の割合で考えたいときは ``uv`` を使うとよいでしょう。

サンプル 04 では、この 2 つの座標を使って、いくつかの図形と模様を描いています。

.. rubric:: サンプル 04：フラグメントシェーダーで図形を描く

`ブラウザーで開く <../examples/04_fragment_shapes.html>`__／:download:`ダウンロード <../../examples/04_fragment_shapes.html>`／シェーダー：:download:`04_fragment_shapes.vert <../../examples/shaders/04_fragment_shapes.vert>`、:download:`04_fragment_shapes.frag <../../examples/shaders/04_fragment_shapes.frag>`

.. raw:: html

   <iframe src="../examples/04_fragment_shapes.html" title="サンプル 04：フラグメントシェーダーで図形を描く" loading="lazy" style="width: 100%; height: 500px; border: 1px solid #ccc;"></iframe>

.. literalinclude:: ../../examples/shaders/04_fragment_shapes.frag
   :language: glsl
   :caption: 04_fragment_shapes.frag（フラグメントシェーダー）

グラデーション
--------------

座標をそのまま色の成分にすると、位置によって色が変わるグラデーションになります。``vec3(uv, 0.5)`` では、右に行くほど赤が、上に行くほど緑が強くなります。座標を色として表示するこの方法は、座標の値を確かめるデバッグにも使えます（第 15 章）。

円
--

中心からの距離 ``length(p)`` が半径以下の部分を白くすると、円になります。

.. code-block:: glsl

   float d = length(p);
   color = vec3(step(d, 0.5));   // d <= 0.5 なら 1.0（白）

``step`` を使うと、境界で値が 0.0 から 1.0 に急に変わるため、輪郭がギザギザになります（エイリアシング）。``smoothstep`` を使って境界の 1〜2 ピクセルの範囲で値をなめらかに変化させると、輪郭がなめらかに見えます。

.. code-block:: glsl

   float pixel = 2.0 / min(uResolution.x, uResolution.y);  // 1 ピクセルの長さ
   color = vec3(1.0 - smoothstep(0.5 - 2.0 * pixel, 0.5, d));

繰り返し模様
------------

``fract`` は値の小数部分を返すので、``fract(uv.x * 10.0)`` は、横方向に 0 から 1 の変化を 10 回繰り返す値になります。これを ``step`` で 0.0 と 1.0 に分けると縞模様になります。

.. code-block:: glsl

   color = vec3(step(0.5, fract(uv.x * 10.0)));

``floor`` で座標を整数に切り捨てると、マス目の番号が得られます。横と縦の番号の和が偶数か奇数かで色を変えると、市松模様になります。

.. code-block:: glsl

   vec2 cell = floor(uv * vec2(12.0, 8.0));
   color = vec3(mod(cell.x + cell.y, 2.0));

図形の合成
----------

複数の図形は ``mix`` で重ねられます。図形の内側で 1.0、外側で 0.0 になる値を作っておき、それを ``mix`` の割合にすると、背景の色と図形の色を切り替えられます。後から ``mix`` した図形ほど手前に描かれます。

.. code-block:: glsl

   color = mix(background, vec3(1.0, 0.8, 0.2), circle);  // 円を重ねる
   color = mix(color, vec3(0.3, 0.9, 1.0), ring);         // その上にリングを重ねる

discard
-------

``discard`` は、そのフラグメントを捨てて、色を書き込まないようにする命令です。``discard`` したフラグメントでは、フレームバッファーに元から描かれていた色（サンプル 04 では背景色）がそのまま残ります。

.. code-block:: glsl

   vec2 cell = fract(uv * vec2(6.0, 4.0)) - 0.5;
   if (length(cell) > 0.4) {
       discard;
   }

``discard`` は、葉や金網のように、テクスチャの透明な部分をくり抜いて表示したい場合などに使います。

距離関数による図形
------------------

距離関数（SDF、Signed Distance Function）は、ある点から図形の表面までの距離を返す関数です。点が図形の外側にあれば正の値、内側にあれば負の値、表面上にあれば 0 を返します。

例えば、原点を中心とする半径 r の円の距離関数は、次のようになります。

.. math::

   d(p) = |p| - r

長方形の距離関数は少し複雑ですが、次のように書けます。``b`` は長方形の幅と高さの半分です。

.. code-block:: glsl

   float sdCircle(vec2 p, float r) {
       return length(p) - r;
   }

   float sdBox(vec2 p, vec2 b) {
       vec2 d = abs(p) - b;
       return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
   }

図形を移動するには、距離関数に渡す座標のほうを逆向きに移動します。例えば ``sdCircle(p - vec2(0.5, 0.0), 0.3)`` は、中心が (0.5, 0.0) の円になります。

距離関数による合成
~~~~~~~~~~~~~~~~~~

距離関数で表した図形は、距離の値を ``min`` や ``max`` で組み合わせるだけで合成できます。2 つの図形の距離を a、b とすると、次のようになります。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 合成
     - 式
     - 結果
   * - 和
     - ``min(a, b)``
     - どちらかの図形の内側
   * - 積
     - ``max(a, b)``
     - 両方の図形の内側
   * - 差
     - ``max(a, -b)``
     - a の内側で、かつ b の外側
   * - なめらかな和
     - ``smoothMin(a, b, k)``
     - 和と同じだが、境目が幅 k でなめらかにつながる

なめらかな和には、次の関数がよく使われます。

.. code-block:: glsl

   float smoothMin(float a, float b, float k) {
       float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
       return mix(b, a, h) - k * h * (1.0 - h);
   }

距離関数では、形の情報が「距離」という 1 つの値で表されるので、``smoothstep`` による輪郭のぼかし、輪郭線の描画、影の計算など、さまざまな処理を簡単に行えます。第 14 章のレイマーチングでは、3 次元の距離関数を使って立体を描きます。

.. rubric:: サンプル 05：距離関数による図形の合成

`ブラウザーで開く <../examples/05_sdf_2d.html>`__／:download:`ダウンロード <../../examples/05_sdf_2d.html>`／シェーダー：:download:`05_sdf_2d.vert <../../examples/shaders/05_sdf_2d.vert>`、:download:`05_sdf_2d.frag <../../examples/shaders/05_sdf_2d.frag>`

.. raw:: html

   <iframe src="../examples/05_sdf_2d.html" title="サンプル 05：距離関数による図形の合成" loading="lazy" style="width: 100%; height: 520px; border: 1px solid #ccc;"></iframe>

「距離の値を等高線で表示」を選ぶと、各点の距離の値が色で表示されます。オレンジ色の部分が図形の外側（距離が正）、青色の部分が内側（距離が負）で、白い線が表面（距離が 0）です。

.. literalinclude:: ../../examples/shaders/05_sdf_2d.frag
   :language: glsl
   :caption: 05_sdf_2d.frag（フラグメントシェーダー）

試してみよう
------------

* サンプル 04 の縞模様を、縦方向の縞や斜めの縞（``fract((uv.x + uv.y) * 10.0)``）に変える。
* サンプル 04 の円の中心を動かしたり、円を 2 つ描いたりする。
* サンプル 05 に、別の位置にもう 1 つ円を追加し、3 つの図形を ``smoothMin`` でつなげる。
