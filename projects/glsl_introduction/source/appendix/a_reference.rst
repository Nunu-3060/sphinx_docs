付録 A 組み込み変数・関数の一覧
===============================

GLSL ES 3.00 の主な組み込み変数と組み込み関数の一覧です。使い方の説明は、表の「参照」の章を見てください。関数の引数の ``genType`` は ``float``、``vec2``、``vec3``、``vec4`` のいずれかを表し、ベクトルの場合は成分ごとに計算されます。

組み込み変数
------------

.. list-table::
   :header-rows: 1
   :widths: 22 18 12 36 12

   * - 変数
     - シェーダー
     - 型
     - 内容
     - 参照
   * - ``gl_Position``
     - 頂点（出力）
     - ``vec4``
     - 頂点のクリップ座標
     - 第 7 章
   * - ``gl_PointSize``
     - 頂点（出力）
     - ``float``
     - 点の大きさ（ピクセル）
     - 第 7 章
   * - ``gl_VertexID``
     - 頂点（入力）
     - ``int``
     - 頂点の番号
     - 第 8 章
   * - ``gl_InstanceID``
     - 頂点（入力）
     - ``int``
     - インスタンスの番号
     - 第 7 章
   * - ``gl_FragCoord``
     - フラグメント（入力）
     - ``vec4``
     - フラグメントのウィンドウ座標と深度値
     - 第 8 章
   * - ``gl_FrontFacing``
     - フラグメント（入力）
     - ``bool``
     - 表向きの三角形なら ``true``
     - 第 8 章
   * - ``gl_PointCoord``
     - フラグメント（入力）
     - ``vec2``
     - 点の中での位置（0.0〜1.0）
     - 第 8 章
   * - ``gl_FragDepth``
     - フラグメント（出力）
     - ``float``
     - フラグメントの深度値
     - 第 8 章

組み込み関数
------------

角度と三角関数
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``radians(degrees)``、``degrees(radians)``
     - 度とラジアンの変換
     - 第 5 章
   * - ``sin(x)``、``cos(x)``、``tan(x)``
     - 三角関数
     - 第 5 章
   * - ``asin(x)``、``acos(x)``、``atan(y_over_x)``、``atan(y, x)``
     - 逆三角関数
     - 第 5 章
   * - ``sinh(x)``、``cosh(x)``、``tanh(x)``、``asinh(x)``、``acosh(x)``、``atanh(x)``
     - 双曲線関数とその逆関数
     -

指数関数
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``pow(x, y)``
     - べき乗
     - 第 5 章
   * - ``exp(x)``、``log(x)``、``exp2(x)``、``log2(x)``
     - 指数関数と対数関数
     - 第 5 章
   * - ``sqrt(x)``、``inversesqrt(x)``
     - 平方根とその逆数
     - 第 5 章

共通の関数
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``abs(x)``、``sign(x)``
     - 絶対値と符号
     - 第 5 章
   * - ``floor(x)``、``ceil(x)``、``round(x)``、``roundEven(x)``、``trunc(x)``
     - 整数への丸め
     - 第 5 章
   * - ``fract(x)``、``mod(x, y)``、``modf(x, out i)``
     - 小数部分と剰余
     - 第 5 章
   * - ``min(x, y)``、``max(x, y)``、``clamp(x, minVal, maxVal)``
     - 最小値、最大値、範囲の制限
     - 第 5 章
   * - ``mix(x, y, a)``
     - 線形補間
     - 第 5 章
   * - ``step(edge, x)``、``smoothstep(edge0, edge1, x)``
     - 閾値による 0 と 1 への振り分けと、なめらかな変化
     - 第 5 章
   * - ``isnan(x)``、``isinf(x)``
     - NaN と無限大の判定
     - 第 15 章
   * - ``floatBitsToInt(x)``、``intBitsToFloat(x)`` など
     - ``float`` のビット列と整数の相互変換
     -
   * - ``packHalf2x16(v)``、``unpackHalf2x16(u)`` など
     - 2 つの値を 1 つの ``uint`` に詰める変換と、その逆変換
     -

幾何関数
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``length(x)``、``distance(p0, p1)``
     - ベクトルの長さと 2 点間の距離
     - 第 5 章
   * - ``dot(x, y)``、``cross(x, y)``
     - 内積と外積
     - 第 5 章
   * - ``normalize(x)``
     - 単位ベクトル
     - 第 5 章
   * - ``reflect(I, N)``、``refract(I, N, eta)``
     - 反射と屈折の方向
     - 第 5 章
   * - ``faceforward(N, I, Nref)``
     - ``dot(Nref, I) < 0`` なら ``N``、そうでなければ ``-N``
     -

行列関数
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``matrixCompMult(x, y)``
     - 成分ごとの積
     - 第 5 章
   * - ``outerProduct(c, r)``
     - 列ベクトルと行ベクトルの積
     - 第 5 章
   * - ``transpose(m)``、``inverse(m)``、``determinant(m)``
     - 転置行列、逆行列、行列式
     - 第 5 章

ベクトルの比較
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``lessThan``、``lessThanEqual``、``greaterThan``、``greaterThanEqual``
     - 成分ごとの大小の比較
     - 第 5 章
   * - ``equal``、``notEqual``
     - 成分ごとの等しいかどうかの比較
     - 第 5 章
   * - ``any(b)``、``all(b)``、``not(b)``
     - ``bvec`` の成分の論理演算
     - 第 5 章

テクスチャ関数
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``texture(sampler, coord)``
     - テクスチャのサンプリング
     - 第 9 章
   * - ``textureLod(sampler, coord, lod)``
     - ミップマップのレベルを指定したサンプリング
     - 第 9 章
   * - ``texelFetch(sampler, texel, level)``
     - テクセルの番号を指定した読み出し
     - 第 9 章
   * - ``textureSize(sampler, level)``
     - テクスチャの大きさ
     - 第 9 章
   * - ``textureProj``、``textureOffset``、``textureGrad`` など
     - 射影付き、位置をずらした、微分値を指定したサンプリングなど
     -

フラグメントシェーダー専用の関数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - 関数
     - 内容
     - 参照
   * - ``dFdx(p)``、``dFdy(p)``
     - 隣のフラグメントとの値の差（画面の x 方向と y 方向の偏微分の近似）
     -
   * - ``fwidth(p)``
     - ``abs(dFdx(p)) + abs(dFdy(p))``
     -

``fwidth`` は、値が 1 ピクセルでどれだけ変化するかを求めるのに使えます。例えば、第 8 章で 1 ピクセルの長さを ``pixel`` として計算した部分は、``fwidth(d)`` を使って ``smoothstep(-fwidth(d), fwidth(d), d)`` のようにも書けます。
