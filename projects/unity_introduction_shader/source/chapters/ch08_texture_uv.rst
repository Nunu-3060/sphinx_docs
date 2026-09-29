第 8 章 テクスチャーと UV
=========================

この章では、オブジェクトにテクスチャー（画像）を貼る方法を説明する。さらに、テクスチャーの位置を時間とともにずらし、流れる水や動くベルトコンベアのような表現を作る。

この章のサンプルコードは、``examples/chapter08`` フォルダーにある。

UV 座標
-------

メッシュの各頂点には、その頂点がテクスチャーのどの位置に対応するかを表す座標が設定されている。この座標を UV 座標という。U が横方向、V が縦方向で、テクスチャーの左下が (0, 0)、右上が (1, 1) になる。

UV 座標は、モデリングツールでメッシュを作るときに設定する。Unity に用意されている Cube、Sphere、Plane、Quad などのメッシュにも、UV 座標が設定されている。

フラグメントシェーダーでは、頂点の UV 座標を補間した値を使って、テクスチャーの色を読み取る。この処理をサンプリングという。

テクスチャーをスクロールするシェーダー
--------------------------------------

次のシェーダーは、テクスチャーに ``_BaseColor`` の色を掛けて表示し、さらに UV 座標を時間とともにずらしてテクスチャーをスクロールさせる。

.. literalinclude:: ../../examples/chapter08/TextureScroll.shader
   :language: hlsl
   :caption: TextureScroll.shader
   :linenos:

:download:`TextureScroll.shader をダウンロード <../../examples/chapter08/TextureScroll.shader>`

マテリアルの :guilabel:`Base Map` に任意のテクスチャーを設定し、Plane や Cube に適用すると、テクスチャーが横方向に流れる。:guilabel:`Scroll Speed` の x と y で、横方向と縦方向の速さを変えられる。

.. note::

   テクスチャーの端が途切れずにつながるように、テクスチャーのインポート設定の :guilabel:`Wrap Mode` を :guilabel:`Repeat`\ （既定値）にしておく。:guilabel:`Clamp` にすると、UV 座標が 0～1 の範囲を超えた部分では、テクスチャーの端の色が引き伸ばされる。

テクスチャーの宣言
------------------

URP のシェーダーでは、テクスチャーとサンプラーを次のマクロで宣言する。

.. code-block:: hlsl

   TEXTURE2D(_BaseMap);
   SAMPLER(sampler_BaseMap);

``TEXTURE2D`` はテクスチャー本体、``SAMPLER`` はサンプラーである。サンプラーは、テクスチャーの読み取り方（フィルターモードやラップモード）の設定を持つ。サンプラーの名前を ``sampler_`` + テクスチャー名にすると、そのテクスチャーのインポート設定がサンプラーに反映される。

テクスチャーとサンプラーは、``UnityPerMaterial`` の定数バッファーの外で宣言する。定数バッファーに入れられるのは、数値のデータだけである。

これらのマクロは、グラフィックス API ごとの書き方の違いを吸収するために用意されている。例えば Direct3D 11 では、``TEXTURE2D(_BaseMap)`` は ``Texture2D _BaseMap`` に展開される。

Tiling と Offset
----------------

マテリアルの Inspector ウィンドウでは、テクスチャーのプロパティごとに :guilabel:`Tiling` と :guilabel:`Offset` を設定できる。この値は、テクスチャー名に ``_ST`` を付けた名前の ``float4`` 型の変数に入る。xy に Tiling、zw に Offset が入る。

``TRANSFORM_TEX`` マクロは、この値を UV 座標に適用する。

.. code-block:: hlsl

   // 次の 2 行は同じ計算
   output.uv = TRANSFORM_TEX(input.uv, _BaseMap);
   output.uv = input.uv * _BaseMap_ST.xy + _BaseMap_ST.zw;

Tiling を (2, 2) にすると、UV 座標が 0～2 の範囲になり、テクスチャーが縦横に 2 回ずつ繰り返される。

サンプリング
------------

``SAMPLE_TEXTURE2D`` マクロで、テクスチャーの色を読み取る。引数は、テクスチャー、サンプラー、UV 座標である。戻り値は ``half4`` 型の色（RGBA）になる。

.. code-block:: hlsl

   half4 texColor = SAMPLE_TEXTURE2D(_BaseMap, sampler_BaseMap, input.uv);

``SAMPLE_TEXTURE2D`` は、フラグメントシェーダーの中で使う。使うミップマップのレベルを自動的に選ぶために、隣り合うピクセルの間での UV 座標の変化量が必要で、この値はフラグメントシェーダーでしか得られないためである（この章の「フィルターモードとミップマップ」を参照）。

時間によるスクロール
--------------------

``_Time`` は、Unity が設定する経過時間の変数で、``Core.hlsl`` を読み込むと使える。各成分には、次の値が入っている。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 成分
     - 値
   * - ``_Time.x``
     - 経過時間（秒）÷ 20
   * - ``_Time.y``
     - 経過時間（秒）
   * - ``_Time.z``
     - 経過時間（秒）× 2
   * - ``_Time.w``
     - 経過時間（秒）× 3

サンプルでは、UV 座標に ``_ScrollSpeed.xy * _Time.y`` を加えている。UV 座標は時間とともに大きくなり続けるが、:guilabel:`Wrap Mode` が :guilabel:`Repeat` なら、1 を超えた部分はテクスチャーの最初に戻って繰り返される。

.. note::

   ``_Time.y`` はゲームを長時間実行すると大きな値になり、``float`` の精度が落ちてスクロールが滑らかでなくなることがある。長時間動かし続ける場合は、``frac`` 関数で UV 座標のずれを 0～1 の範囲に収めるとよい。

フィルターモードとミップマップ
------------------------------

テクスチャーのインポート設定の :guilabel:`Filter Mode` は、テクスチャーの画素（テクセル）の間の色の求め方を決める。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Filter Mode
     - 内容
   * - Point (no filter)
     - 最も近いテクセルの色をそのまま使う。拡大すると画素がはっきり見える。ドット絵に向いている。
   * - Bilinear
     - 周囲の 4 つのテクセルの色を補間する。拡大すると滑らかにぼける。
   * - Trilinear
     - Bilinear に加えて、ミップマップのレベルの間も補間する。

ミップマップは、テクスチャーを 1/2、1/4、1/8 と段階的に縮小した画像をあらかじめ用意しておくしくみである。遠くにあって小さく表示されるオブジェクトには縮小した画像を使うことで、ちらつき（エイリアシング）を減らし、読み取りも高速になる。ミップマップは、インポート設定の :guilabel:`Generate Mipmap` で有効にする（既定で有効）。``SAMPLE_TEXTURE2D`` は、表示される大きさに応じて、使うミップマップのレベルを自動的に選ぶ。

ミップマップのレベルは、テクスチャーの LOD とも呼ばれる。0 が元の大きさの画像で、1 増えるごとに縦横が 1/2 になる。頂点シェーダーでテクスチャーを読み取る場合は、レベルを自動的に選べないため、``SAMPLE_TEXTURE2D_LOD`` マクロでレベルを直接指定する。例えば、高さのテクスチャーを読み取って頂点を動かす場合に使う。

.. code-block:: hlsl

   // 頂点シェーダーの中で、ミップマップのレベル 0 を読み取る
   half height = SAMPLE_TEXTURE2D_LOD(_HeightMap, sampler_HeightMap, input.uv, 0).r;
