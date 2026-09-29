第 6 章 データの受け渡し
========================

シェーダーは単独では動作せず、JavaScript から渡されたデータを使って計算します。また、頂点シェーダーの計算結果はフラグメントシェーダーに渡されます。この章では、これらのデータの受け渡しの方法を説明します。

データの種類
------------

シェーダーが受け取ったり出力したりするデータには、次の種類があります。

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - 種類
     - 宣言
     - 値が変わる単位
     - 値の設定元
   * - 頂点属性
     - 頂点シェーダーの ``in`` 変数
     - 頂点ごと
     - JavaScript（頂点バッファー）
   * - uniform 変数
     - ``uniform`` 変数
     - 描画 1 回ごと
     - JavaScript
   * - ステージ間の変数
     - 頂点シェーダーの ``out`` 変数とフラグメントシェーダーの ``in`` 変数
     - フラグメントごと（補間される）
     - 頂点シェーダー
   * - フラグメントの出力
     - フラグメントシェーダーの ``out`` 変数
     - フラグメントごと
     - フラグメントシェーダー

サンプル 02 では、これらをすべて使っています。

.. rubric:: サンプル 02：頂点カラーと uniform 変数

`ブラウザーで開く <../examples/02_vertex_color.html>`__／:download:`ダウンロード <../../examples/02_vertex_color.html>`／シェーダー：:download:`02_vertex_color.vert <../../examples/shaders/02_vertex_color.vert>`、:download:`02_vertex_color.frag <../../examples/shaders/02_vertex_color.frag>`

.. raw:: html

   <iframe src="../examples/02_vertex_color.html" title="サンプル 02：頂点カラーと uniform 変数" loading="lazy" style="width: 100%; height: 500px; border: 1px solid #ccc;"></iframe>

.. literalinclude:: ../../examples/shaders/02_vertex_color.vert
   :language: glsl
   :caption: 02_vertex_color.vert（頂点シェーダー）

.. literalinclude:: ../../examples/shaders/02_vertex_color.frag
   :language: glsl
   :caption: 02_vertex_color.frag（フラグメントシェーダー）

頂点属性
--------

頂点属性は、頂点ごとに異なる値を持つ入力です。頂点シェーダーで ``in`` を付けて宣言します。

.. code-block:: glsl

   layout(location = 0) in vec2 aPosition;
   layout(location = 1) in vec3 aColor;

``layout(location = 番号)`` は、頂点属性に番号（ロケーション）を割り当てます。JavaScript からは、この番号を指定してデータの読み込み方を設定します。``layout`` を省略した場合は、リンク時に番号が自動的に割り当てられ、JavaScript から ``gl.getAttribLocation(program, "aColor")`` で番号を調べることになります。

JavaScript での設定
~~~~~~~~~~~~~~~~~~~

サンプル 02 では、1 つのバッファーに位置と色を交互に並べています。

.. literalinclude:: ../../examples/02_vertex_color.html
   :language: javascript
   :start-after: // ---- 頂点データ（位置と色を交互に並べる） ----
   :end-before: // ---- 頂点データここまで ----
   :dedent: 4
   :caption: 頂点データの設定

``vertexAttribPointer`` の引数は、次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 引数
     - 内容
   * - ``index``
     - 頂点属性の番号（``layout(location = …)`` で指定した番号）
   * - ``size``
     - 1 頂点あたりの成分数（1〜4）
   * - ``type``
     - データの型（``gl.FLOAT`` など）
   * - ``normalized``
     - 整数のデータを 0.0〜1.0（符号付きなら -1.0〜1.0）に変換するかどうか。``float`` のデータでは無視されます。
   * - ``stride``
     - 次の頂点のデータまでのバイト数。0 を指定すると、データが隙間なく並んでいるものとして自動的に計算されます。
   * - ``offset``
     - バッファーの先頭から、最初のデータまでのバイト数

サンプル 02 では、1 頂点が ``float`` 5 個（20 バイト）なので ``stride`` は 20 です。色のデータは各頂点の 3 個目の ``float`` から始まるので、``offset`` は 8 です。

.. note::

   シェーダーで宣言した成分数より少ない成分数のデータを渡すと、足りない成分は y、z が 0.0、w が 1.0 で補われます。例えば ``in vec4 aPosition;`` に 3 成分のデータを渡すと、w は 1.0 になります。

uniform 変数
------------

uniform 変数は、1 回の描画の間、すべての頂点とフラグメントで共通の値を持つ入力です。変換行列、光源の向き、経過時間、画面の大きさなどを渡すのに使います。頂点シェーダーとフラグメントシェーダーのどちらでも宣言でき、両方で同じ名前と型で宣言すれば、同じ値を参照できます。

.. literalinclude:: ../../examples/02_vertex_color.html
   :language: javascript
   :start-after: // ---- uniform 変数の設定と描画 ----
   :end-before: // ---- 描画ここまで ----
   :dedent: 4
   :caption: uniform 変数の設定

JavaScript からの設定手順は次のとおりです。

1. プログラムのリンク後に、``gl.getUniformLocation`` で uniform 変数の場所を取得しておく。
2. ``gl.useProgram`` で、値を設定するプログラムを選ぶ。
3. 型に合った ``gl.uniform*`` 関数で値を設定する。

設定した値は、次に設定し直すまでプログラムに保持されます。型と設定用の関数の対応は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - GLSL の型
     - 設定用の関数
   * - ``float``
     - ``gl.uniform1f(location, x)``
   * - ``vec2``、``vec3``、``vec4``
     - ``gl.uniform2f``、``gl.uniform3f``、``gl.uniform4f``\ （配列で渡す場合は ``gl.uniform3fv(location, array)`` など）
   * - ``int``、``bool``、サンプラー型
     - ``gl.uniform1i(location, x)``\ （``bool`` は 0 が ``false``、それ以外が ``true``）
   * - ``uint``
     - ``gl.uniform1ui(location, x)``
   * - ``mat3``、``mat4``
     - ``gl.uniformMatrix3fv(location, false, array)``、``gl.uniformMatrix4fv(location, false, array)``

.. note::

   シェーダーで宣言しても計算に使われていない uniform 変数は、コンパイル時の最適化で取り除かれることがあります。その場合、``getUniformLocation`` は ``null`` を返し、``null`` に対する値の設定は何もせずに無視されます。値を設定したのに効果がない場合は、その変数が実際に使われているかを確認してください。

複数の uniform 変数をまとめて扱う uniform ブロック（uniform バッファーオブジェクト）という仕組みもあります。多数のプログラムで同じ値（カメラの行列など）を共有したい場合に便利ですが、本書では扱いません。

ステージ間の変数と補間
----------------------

頂点シェーダーで ``out`` を付けて宣言した変数は、フラグメントシェーダーで同じ名前と型の ``in`` 変数として受け取れます。

.. code-block:: glsl

   // 頂点シェーダー
   out vec3 vColor;

   // フラグメントシェーダー
   in vec3 vColor;

頂点シェーダーは頂点ごとに実行されますが、フラグメントシェーダーはフラグメントごとに実行されます。そのため、フラグメントが受け取る値は、三角形の 3 頂点の値を、フラグメントの位置に応じて補間したものになります。三角形の 3 頂点の値を :math:`v_0, v_1, v_2` とすると、補間された値は次の式で表されます。

.. math::

   v = \lambda_0 v_0 + \lambda_1 v_1 + \lambda_2 v_2 \quad (\lambda_0 + \lambda_1 + \lambda_2 = 1)

:math:`\lambda_0, \lambda_1, \lambda_2` は、フラグメントが各頂点にどれだけ近いかを表す重み（重心座標）です。フラグメントが頂点 0 の上にあれば :math:`\lambda_0 = 1`、三角形の中心にあれば 3 つとも :math:`1/3` になります。サンプル 02 で、頂点の赤、緑、青が三角形の内部でなめらかに混ざるのはこのためです。

.. note::

   正確には、3D の透視投影で奥行きがある三角形を正しく補間できるよう、奥行きを考慮した補間（パースペクティブ補正）が行われます。

補間の方法は、変数に修飾子を付けて指定できます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 修飾子
     - 内容
   * - ``smooth``
     - パースペクティブ補正付きで補間します（既定）。
   * - ``flat``
     - 補間しません。三角形のすべてのフラグメントが、プロボーキング頂点（WebGL では三角形の最後の頂点）の値を受け取ります。``int`` などの整数型の変数には、``flat`` を付ける必要があります。

サンプル 02 で「flat 修飾子の変数を使う」を選ぶと、三角形全体が最後の頂点（右下）の色である青になります。

フラグメントシェーダーの出力
----------------------------

フラグメントシェーダーで ``out`` を付けて宣言した変数が、フラグメントの色になります。

.. code-block:: glsl

   out vec4 outColor;

出力先のフレームバッファーに複数の色の書き込み先がある場合は、``layout(location = 番号)`` で出力変数ごとに書き込み先を指定できます（マルチレンダーターゲット）。出力変数が 1 つだけの場合は、``layout`` を省略すると 0 番になります。

.. note::

   GLSL ES 1.00（WebGL 1.0）では、頂点属性を ``attribute``、ステージ間の変数を ``varying`` で宣言し、フラグメントの色は組み込み変数 ``gl_FragColor`` に書き込んでいました。古い資料を読むときは、付録 B の対応表を参照してください。
