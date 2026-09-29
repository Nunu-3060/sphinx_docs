第 15 章 ポストエフェクト
=========================

ポストエフェクトは、シーンを描画し終えた画面全体の画像に対して、あとから加工を行う処理である。色調の補正、白黒化、画面の周辺を暗くする、ぼかすなどの表現に使う。この章では、URP の Full Screen Pass Renderer Feature を使って、自作のポストエフェクトを画面に適用する。

この章のサンプルコードは、``examples/chapter15`` フォルダーにある。

ポストエフェクトのしくみ
------------------------

ポストエフェクトは、次の手順で行う。

#. シーンを通常どおり描画し、結果の画像をテクスチャーとして保持する。
#. 画面全体を覆う図形を描画する。その図形のフラグメントシェーダーで、1 で保持したテクスチャーを読み取り、加工した色を出力する。

2 のフラグメントシェーダーは、画面のピクセルごとに 1 回実行される。UV 座標は画面の位置に対応し、左下が (0, 0)、右上が (1, 1) になる。

URP には、Bloom、Vignette、Color Adjustments などのポストエフェクトが、Volume の機能として用意されている。用意されているもので足りる場合は、Volume を使うのが簡単である。自作のポストエフェクトが必要な場合に、この章の方法を使う。

グレースケール
--------------

次のシェーダーは、画面全体を白黒にする。

.. literalinclude:: ../../examples/chapter15/Grayscale.shader
   :language: hlsl
   :caption: Grayscale.shader
   :linenos:

:download:`Grayscale.shader をダウンロード <../../examples/chapter15/Grayscale.shader>`

これまでのシェーダーとの違いは、次のとおりである。

* ``Blit.hlsl`` を読み込み、そこで定義されている頂点シェーダー ``Vert`` をそのまま使っている。``Vert`` は、画面全体を覆う三角形を描画し、``Varyings`` の ``texcoord`` に画面の UV 座標を入れる。そのため、``Attributes`` と ``Varyings`` の構造体は自分で定義しない。
* 画面の画像は、``Blit.hlsl`` で宣言されている ``_BlitTexture`` から読み取る。サンプラーには、URP のライブラリで宣言されている ``sampler_LinearClamp``\ （Filter Mode が Bilinear、Wrap Mode が Clamp のサンプラー）を使う。
* ``_BlitTexture`` は、VR などで左右の目の画像を 1 つのテクスチャーにまとめる場合に備えて ``TEXTURE2D_X`` で宣言されている。そのため、読み取りには ``SAMPLE_TEXTURE2D_X`` マクロを使う。``UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX`` マクロも、同じ理由で呼んでいる。
* 画面全体を覆うだけなので、``ZWrite Off``、``ZTest Always``、``Cull Off`` を指定している。

輝度の計算
~~~~~~~~~~

色を白黒にするには、RGB の各成分から明るさ（輝度）を求め、その値を RGB のすべてに入れる。人の目は緑に最も敏感で、青に最も鈍感なため、単純な平均ではなく、次の重みを付けた和を使う。

.. math::

   Y = 0.2126 R + 0.7152 G + 0.0722 B

これは、ITU-R BT.709 という規格で定められた係数で、Linear の色空間の RGB に対して使う。本資料の前提の環境では、カラースペースは Linear である（第 1 章を参照）。

Full Screen Pass Renderer Feature の設定
----------------------------------------

作成したシェーダーを、次の手順で画面に適用する。

#. ``Grayscale.shader`` をプロジェクトに追加し、このシェーダーを使うマテリアルを作成する。
#. Project ウィンドウで、使っている Universal Renderer Data アセットを選択する。Universal 3D テンプレートでは、``Assets/Settings`` フォルダーにある ``PC_Renderer`` などのアセットである。
#. Inspector ウィンドウの下部にある :guilabel:`Add Renderer Feature` を押し、:guilabel:`Full Screen Pass Renderer Feature` を選ぶ。
#. 追加した Renderer Feature の :guilabel:`Pass Material` に、1 で作成したマテリアルを設定する。
#. :guilabel:`Injection Point` が :guilabel:`After Rendering Post Processing`\ （既定値）になっていることを確認する。
#. :guilabel:`Fetch Color Buffer` にチェックを入れる。

Game ビューで、画面全体が白黒になることを確認する。マテリアルの :guilabel:`Intensity` を変えると、白黒の度合いが変わる。

各項目の意味は、次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 意味
   * - :guilabel:`Pass Material`
     - 画面全体の描画に使うマテリアル。
   * - :guilabel:`Injection Point`
     - URP の描画の流れの中で、どのタイミングでこの処理を行うか。:guilabel:`After Rendering Post Processing` は、URP の Volume のポストエフェクトのあとである。
   * - :guilabel:`Fetch Color Buffer`
     - それまでに描画された画面の画像を、``_BlitTexture`` としてシェーダーに渡すかどうか。
   * - :guilabel:`Pass`
     - マテリアルのシェーダーのどのパスを使うか。既定では表示されず、Renderer Feature の右上の :guilabel:`⋮` メニューで :guilabel:`Advanced Properties` を有効にすると表示される。

.. note::

   PC とスマートフォンで異なる Universal Renderer Data アセットを使っている場合は（Universal 3D テンプレートでは ``PC_Renderer`` と ``Mobile_Renderer``）、それぞれに Renderer Feature を追加する必要がある。どのアセットが使われているかは、:menuselection:`Edit --> Project Settings --> Quality` で選ばれている品質レベルの URP Asset から確認できる。

ビネット
--------

次のシェーダーは、画面の中心から離れるほど暗くする。

.. literalinclude:: ../../examples/chapter15/Vignette.shader
   :language: hlsl
   :caption: Vignette.shader
   :linenos:

:download:`Vignette.shader をダウンロード <../../examples/chapter15/Vignette.shader>`

グレースケールと同じ手順で、別の Full Screen Pass Renderer Feature を追加して設定する。複数の Renderer Feature を追加した場合は、同じ :guilabel:`Injection Point` の中では、リストの上にあるものから順に処理される。

画面の UV 座標から 0.5 を引くと、画面の中心が原点になる。そのまま距離を求めると、横長の画面では暗くなる範囲が横に伸びた楕円になる。そこで、x 座標に画面の縦横比（幅 ÷ 高さ）を掛けてから距離を求め、円形に暗くなるようにしている。``_ScreenParams`` は、Unity が設定する変数で、x に描画先の幅、y に高さがピクセル単位で入っている。

.. note::

   Full Screen Pass Renderer Feature は、URP に用意されている Renderer Feature である。より複雑な処理（複数回の描画を組み合わせるなど）が必要な場合は、C# で独自の Renderer Feature を書く。Unity 6 の URP では、Renderer Feature の描画処理を Render Graph と呼ばれるしくみで記述する。独自の Renderer Feature の書き方は、本資料の範囲を超えるため扱わない。
