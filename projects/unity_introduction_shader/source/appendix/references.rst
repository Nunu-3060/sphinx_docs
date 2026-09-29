付録 C 参考資料
===============

本資料の内容をさらに深く学ぶための資料を紹介する。

Unity の公式ドキュメント
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 資料
     - 内容
   * - `Unity マニュアル：コードによるシェーダーの記述 <https://docs.unity3d.com/ja/6000.0/Manual/shader-writing.html>`_
     - ShaderLab と HLSL によるシェーダーの書き方の全般
   * - `Unity マニュアル：ShaderLab 言語のリファレンス <https://docs.unity3d.com/ja/6000.0/Manual/SL-Reference.html>`_
     - ShaderLab のブロック、コマンド、タグの一覧
   * - `Unity マニュアル：Writing custom shaders in URP <https://docs.unity3d.com/6000.0/Documentation/Manual/urp/writing-custom-shaders-urp.html>`_
     - URP 向けのシェーダーの書き方の例
   * - `Unity マニュアル：ShaderLab Pass tags in URP reference <https://docs.unity3d.com/6000.0/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html>`_
     - URP の ``LightMode`` タグの値の一覧
   * - `Unity マニュアル：Full Screen Pass Renderer Feature reference for URP <https://docs.unity3d.com/6000.0/Documentation/Manual/urp/renderer-features/renderer-feature-full-screen-pass.html>`_
     - Full Screen Pass Renderer Feature の設定項目
   * - `Unity マニュアル：コンピュートシェーダー <https://docs.unity3d.com/ja/6000.0/Manual/class-ComputeShader.html>`_
     - コンピュートシェーダーの作成、実行、複数の環境への対応
   * - `Shader Graph マニュアル <https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/index.html>`_
     - Shader Graph の使い方と、各ノードの説明

URP のシェーダーライブラリ
--------------------------

URP のシェーダーライブラリのコードは、Unity のプロジェクトの Project ウィンドウで :guilabel:`Packages` の下の :guilabel:`Universal RP` を開くと読める。関数の正確な動作や、URP の標準のシェーダーの書き方を知りたいときに参考になる。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - ファイル
     - 内容
   * - ``ShaderLibrary/Core.hlsl``
     - 座標変換、テクスチャーのマクロなど
   * - ``ShaderLibrary/Lighting.hlsl``
     - ライトの取得、ライティングの計算
   * - ``ShaderLibrary/Shadows.hlsl``
     - 影の計算
   * - ``Shaders/Lit.shader``
     - URP の標準の Lit シェーダー。パスの構成やキーワードの宣言の参考になる
   * - ``Shaders/Unlit.shader``
     - URP の標準の Unlit シェーダー

HLSL
----

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 資料
     - 内容
   * - `HLSL のリファレンス（Microsoft） <https://learn.microsoft.com/ja-jp/windows/win32/direct3dhlsl/dx-graphics-hlsl-reference>`_
     - HLSL の文法、データ型、組み込み関数の一覧
   * - `HLSL の組み込み関数（Microsoft） <https://learn.microsoft.com/ja-jp/windows/win32/direct3dhlsl/dx-graphics-hlsl-intrinsic-functions>`_
     - ``dot``、``lerp``、``saturate`` などの組み込み関数の説明

ツール
------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 資料
     - 内容
   * - `RenderDoc <https://renderdoc.org/>`_
     - GPU の描画を詳しく調べるツール（第 17 章を参照）
