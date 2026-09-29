第 5 章 組み込み関数
====================

GLSL には、シェーダーでよく使う計算のための関数が多数組み込まれています。組み込み関数は GPU の命令に直接対応していることが多く、同じ計算を自分で書くよりも速く動作することが期待できます。

この章では、よく使う組み込み関数を、使い方とともに説明します。組み込み関数の一覧は付録 A にあります。

組み込み関数の多くは、``float`` だけでなく ``vec2``、``vec3``、``vec4`` も引数に取り、成分ごとに計算します。例えば ``abs(vec3(-1.0, 2.0, -3.0))`` は ``vec3(1.0, 2.0, 3.0)`` になります。以下の説明で ``x`` や ``y`` と書いた引数は、特に断らない限り ``float`` とベクトルのどちらでもかまいません。

三角関数
--------

``sin``、``cos``、``tan`` と、その逆関数 ``asin``、``acos``、``atan`` があります。角度の単位はラジアンです。度とラジアンの変換には ``radians`` と ``degrees`` を使います。

``atan`` には、引数が 1 つの ``atan(y_over_x)`` と、2 つの ``atan(y, x)`` があります。2 引数の ``atan(y, x)`` は、点 (x, y) の方向の角度を -π から π の範囲で返します。点の位置から角度を求めたい場合は、こちらを使います。

.. code-block:: glsl

   vec2 p = vec2(-1.0, 1.0);
   float angle = atan(p.y, p.x);   // 3π/4（135 度）

指数関数
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 内容
   * - ``pow(x, y)``
     - :math:`x^y`。``x < 0`` の場合、または ``x = 0`` かつ ``y <= 0`` の場合の結果は未定義です。
   * - ``exp(x)``、``log(x)``
     - :math:`e^x` と自然対数。``log`` は ``x <= 0`` の場合の結果が未定義です。
   * - ``exp2(x)``、``log2(x)``
     - :math:`2^x` と 2 を底とする対数
   * - ``sqrt(x)``
     - 平方根。``x < 0`` の場合の結果は未定義です。
   * - ``inversesqrt(x)``
     - :math:`1 / \sqrt{x}`

「結果が未定義」とは、GPU によって異なる値が返る可能性があるという意味です。NaN（非数）が返って画面に黒い点や何も表示されない部分が現れる原因になるので、引数が範囲外にならないようにしてください（第 15 章）。

数値の丸めと範囲の制限
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 内容
   * - ``abs(x)``、``sign(x)``
     - 絶対値と符号（-1.0、0.0、1.0 のいずれか）
   * - ``floor(x)``、``ceil(x)``
     - 小数点以下の切り捨て（x 以下の最大の整数）と切り上げ
   * - ``round(x)``、``trunc(x)``
     - 最も近い整数への丸めと、0 の方向への切り捨て
   * - ``fract(x)``
     - 小数部分。:math:`x - \lfloor x \rfloor` で、結果は常に 0 以上 1 未満です。
   * - ``mod(x, y)``
     - 剰余。:math:`x - y \lfloor x / y \rfloor` で、``y`` が正なら結果は 0 以上 ``y`` 未満です。
   * - ``min(x, y)``、``max(x, y)``
     - 小さい方と大きい方
   * - ``clamp(x, minVal, maxVal)``
     - ``x`` を ``minVal`` 以上 ``maxVal`` 以下の範囲に収めた値。``min(max(x, minVal), maxVal)`` と同じです。

``fract`` と ``mod`` は、模様を繰り返すときによく使います（第 8 章）。``mod`` は負の数に対しても 0 以上の値を返す点が、C 言語の ``fmod`` 関数や ``%`` 演算子と異なります。例えば ``mod(-0.5, 1.0)`` は ``0.5`` です。

補間と閾値
----------

``mix``、``step``、``smoothstep`` は、シェーダーで特によく使う関数です。

mix
~~~

``mix(x, y, a)`` は、``x`` と ``y`` を割合 ``a`` で線形補間します。

.. math::

   \mathrm{mix}(x, y, a) = x (1 - a) + y a

``a = 0.0`` のとき ``x``、``a = 1.0`` のとき ``y``、``a = 0.5`` のとき中間の値になります。2 つの色を混ぜたり、ある値からある値へ徐々に変化させたりするときに使います。

.. code-block:: glsl

   vec3 red = vec3(1.0, 0.0, 0.0);
   vec3 blue = vec3(0.0, 0.0, 1.0);
   vec3 purple = mix(red, blue, 0.5);   // (0.5, 0.0, 0.5)

step
~~~~

``step(edge, x)`` は、``x`` が ``edge`` より小さければ 0.0、そうでなければ 1.0 を返します。``if`` 文を使わずに、値を 0.0 と 1.0 に振り分けられます。

.. math::

   \mathrm{step}(e, x) = \begin{cases} 0 & (x < e) \\ 1 & (x \geq e) \end{cases}

引数の順序が「閾値、値」である点に注意してください。

smoothstep
~~~~~~~~~~

``smoothstep(edge0, edge1, x)`` は、``x`` が ``edge0`` 以下なら 0.0、``edge1`` 以上なら 1.0 を返し、その間はなめらかな曲線で変化します。

.. math::

   t = \mathrm{clamp}\left(\frac{x - e_0}{e_1 - e_0}, 0, 1\right), \quad
   \mathrm{smoothstep}(e_0, e_1, x) = t^2 (3 - 2t)

``step`` の境界をなめらかにしたいとき、例えば図形の輪郭をぼかしてギザギザを目立たなくするときに使います（第 8 章）。

.. warning::

   ``edge0 >= edge1`` の場合の結果は未定義です。値が大きいほど 0.0 に近づけたい場合は、``smoothstep(0.8, 0.3, x)`` と書くのではなく、``1.0 - smoothstep(0.3, 0.8, x)`` と書いてください。

幾何関数
--------

ベクトルの計算のための関数です。ライティング（第 10 章）で特によく使います。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 内容
   * - ``length(x)``
     - ベクトルの長さ :math:`\sqrt{x_1^2 + x_2^2 + \cdots}`
   * - ``distance(p0, p1)``
     - 2 点間の距離。``length(p0 - p1)`` と同じです。
   * - ``dot(x, y)``
     - 内積 :math:`x_1 y_1 + x_2 y_2 + \cdots`
   * - ``cross(x, y)``
     - 外積。``vec3`` だけに使えます。
   * - ``normalize(x)``
     - 同じ向きで長さが 1 のベクトル（単位ベクトル）。長さが 0 のベクトルを渡した場合の結果は未定義です。
   * - ``reflect(I, N)``
     - 入射方向 ``I`` のベクトルが、法線 ``N`` の面で反射した方向。``N`` は正規化されている必要があります。
   * - ``refract(I, N, eta)``
     - 屈折の方向。``eta`` は屈折率の比です。

内積には、2 つの単位ベクトルのなす角を θ とすると、:math:`\mathrm{dot}(a, b) = \cos\theta` になるという性質があります。向きが同じなら 1、直交していれば 0、逆向きなら -1 です。この性質を使うと、面が光源の方を向いているかどうかを計算できます（第 10 章）。

``reflect(I, N)`` は次の式で計算されます。

.. math::

   \mathrm{reflect}(I, N) = I - 2 (N \cdot I) N

行列関数
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 内容
   * - ``transpose(m)``
     - 転置行列
   * - ``inverse(m)``
     - 逆行列。逆行列が存在しない場合の結果は未定義です。
   * - ``determinant(m)``
     - 行列式
   * - ``matrixCompMult(x, y)``
     - 成分ごとの積（``*`` 演算子は行列の積になるため）
   * - ``outerProduct(c, r)``
     - 列ベクトル ``c`` と行ベクトル ``r`` の積からなる行列

``inverse`` は計算量が多い関数です。頂点やフラグメントごとに同じ行列の逆行列を求めるのは無駄なので、可能なら JavaScript 側で 1 回だけ計算して uniform 変数で渡します（第 10 章）。

ベクトルの比較
--------------

比較演算子 ``<`` などはスカラーにしか使えないため、ベクトルの成分ごとの比較には関数を使います。結果は ``bvec`` 型になります。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 関数
     - 内容
   * - ``lessThan(x, y)``、``lessThanEqual(x, y)``
     - 成分ごとの ``<`` と ``<=``
   * - ``greaterThan(x, y)``、``greaterThanEqual(x, y)``
     - 成分ごとの ``>`` と ``>=``
   * - ``equal(x, y)``、``notEqual(x, y)``
     - 成分ごとの ``==`` と ``!=``
   * - ``any(b)``、``all(b)``、``not(b)``
     - ``bvec`` のいずれかの成分が真か、すべての成分が真か、各成分の否定

.. code-block:: glsl

   vec2 uv = vec2(0.3, 1.2);
   // uv のどちらかの成分が 0.0〜1.0 の範囲外なら true
   bool outside = any(lessThan(uv, vec2(0.0))) || any(greaterThan(uv, vec2(1.0)));

テクスチャ関数
--------------

``texture``、``texelFetch``、``textureSize`` などのテクスチャを読むための関数は、第 9 章で説明します。

試してみよう
------------

:ref:`サンプル 12（シェーダーエディター） <sample-list>` で、次のコードの ``value`` の計算式を ``step(0.5, uv.x)``、``smoothstep(0.2, 0.8, uv.x)``、``fract(uv.x * 5.0)``、``abs(sin(uv.x * 10.0))`` などに書き換えて、関数の形を確かめてください。

.. code-block:: glsl

   #version 300 es
   precision highp float;

   uniform vec2 uResolution;
   out vec4 outColor;

   void main() {
       vec2 uv = gl_FragCoord.xy / uResolution;
       float value = uv.x;   // ここを書き換える

       // 関数のグラフ：y 座標が value に近い部分を白い線で描く
       float line = 1.0 - smoothstep(0.0, 0.01, abs(uv.y - value));
       vec3 color = vec3(value) * 0.5 + vec3(line);
       outColor = vec4(color, 1.0);
   }
