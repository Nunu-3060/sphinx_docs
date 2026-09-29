第 7 章 最初のシェーダー
========================

この章では、オブジェクトを 1 色で塗りつぶすだけの、最も簡単なシェーダーを作る。簡単なシェーダーだが、URP のシェーダーに必要な要素はすべて含まれている。以降の章のシェーダーは、すべてこのシェーダーを元にしている。

この章のサンプルコードは、``examples/chapter07`` フォルダーにある。

シェーダーの作成
----------------

#. Project ウィンドウで ``Assets`` フォルダーを右クリックし、:menuselection:`Create --> Folder` で ``Shaders`` フォルダーを作成する。
#. ``Shaders`` フォルダーを右クリックし、:menuselection:`Create --> Shader --> Unlit Shader` を選ぶ。
#. シェーダーの名前を ``UnlitColor`` にする。
#. 作成したシェーダーをダブルクリックしてコードエディターで開き、内容をすべて次のコードに置き換えて保存する。

:menuselection:`Create --> Shader --> Unlit Shader` で作られるシェーダーは、ビルトインレンダーパイプライン向けの書き方になっているため、本資料では内容を置き換えて使う。

.. literalinclude:: ../../examples/chapter07/UnlitColor.shader
   :language: hlsl
   :caption: UnlitColor.shader
   :linenos:

:download:`UnlitColor.shader をダウンロード <../../examples/chapter07/UnlitColor.shader>`

シェーダーの確認
----------------

#. :menuselection:`GameObject --> 3D Object --> Sphere` で球を作成する。
#. Project ウィンドウで右クリックし、:menuselection:`Create --> Material` でマテリアルを作成する。
#. マテリアルの Inspector ウィンドウで、:guilabel:`Shader` を ``Introduction/Chapter07/UnlitColor`` にする。
#. マテリアルを、Scene ビューの球にドラッグ＆ドロップする。
#. マテリアルの :guilabel:`Base Color` を変えると、球の色が変わる。

球は、陰影のない 1 色の円に見える。このシェーダーはライトの計算を行わず、すべてのピクセルに同じ色を出力しているためである。ライトによる陰影は第 9 章で扱う。

.. note::

   シェーダーにエラーがあると、オブジェクトはマゼンタ（赤紫）色で表示される。エラーの内容は、シェーダーアセットを選択したときの Inspector ウィンドウと、Console ウィンドウに表示される。

コードの解説
------------

プロパティ
~~~~~~~~~~

``Properties`` ブロックで、``_BaseColor`` という色のプロパティを宣言している。既定値は白 ``(1, 1, 1, 1)`` である。色の各成分は、0～1 の範囲で赤、緑、青、アルファを表す。

サブシェーダーとパスのタグ
~~~~~~~~~~~~~~~~~~~~~~~~~~

サブシェーダーのタグで ``"RenderPipeline" = "UniversalPipeline"`` を指定し、このサブシェーダーが URP 用であることを示している。``Queue`` は ``Geometry``\ （不透明なオブジェクト）である。

パスのタグでは、``"LightMode" = "UniversalForward"`` を指定している。これにより、URP がオブジェクトの色を描画する段階で、このパスが使われる。

ライブラリの読み込み
~~~~~~~~~~~~~~~~~~~~

``#include`` で URP の ``Core.hlsl`` を読み込んでいる。頂点シェーダーで使っている ``TransformObjectToHClip`` 関数や、``CBUFFER_START`` マクロは、このファイルで定義されている。

入出力の構造体
~~~~~~~~~~~~~~

``Attributes`` 構造体は頂点シェーダーの入力で、``Varyings`` 構造体は頂点シェーダーからフラグメントシェーダーに渡すデータである。構造体の名前は自由に付けられるが、URP のシェーダーではこの 2 つの名前を使う習慣がある。

このシェーダーでは、入力として頂点の位置（``POSITION``）だけを受け取り、出力としてクリップ空間の位置（``SV_POSITION``）だけを渡している。

定数バッファー
~~~~~~~~~~~~~~

``CBUFFER_START(UnityPerMaterial)`` と ``CBUFFER_END`` の間で、``Properties`` ブロックで宣言した ``_BaseColor`` を HLSL の変数として宣言している。定数バッファーは、シェーダーの実行中に変わらない値をまとめて GPU に渡すための領域である。マテリアルのプロパティを ``UnityPerMaterial`` という名前の定数バッファーにまとめると、シェーダーが SRP Batcher に対応する（第 5 章を参照）。

``_BaseColor`` の型を ``half4`` にしているのは、色は ``half`` の精度で十分なためである。

頂点シェーダー
~~~~~~~~~~~~~~

``Vert`` 関数が頂点シェーダーである。``#pragma vertex Vert`` で、この関数を頂点シェーダーとして使うことを指定している。``TransformObjectToHClip`` 関数で、頂点の位置をオブジェクト空間からクリップ空間に変換している（第 3 章を参照）。

フラグメントシェーダー
~~~~~~~~~~~~~~~~~~~~~~

``Frag`` 関数がフラグメントシェーダーである。関数の後ろの ``: SV_Target`` は、戻り値が描画先に書き込む色であることを表す。このシェーダーでは、``_BaseColor`` をそのまま返している。

C# からプロパティを変更する
---------------------------

マテリアルのプロパティは、C# のスクリプトから変更できる。次のスクリプトは、``_BaseColor`` を時間とともに 2 つの色の間で変化させる。

.. literalinclude:: ../../examples/chapter07/ColorAnimator.cs
   :language: csharp
   :caption: ColorAnimator.cs
   :linenos:

:download:`ColorAnimator.cs をダウンロード <../../examples/chapter07/ColorAnimator.cs>`

スクリプトを、``UnlitColor`` のマテリアルを設定した球にアタッチして再生すると、球の色が赤と青の間で変化する。

このスクリプトのポイントは、次のとおりである。

* ``Shader.PropertyToID`` 関数で、プロパティの名前を整数の ID に変換している。名前の文字列で指定するより、ID で指定するほうが高速である。
* ``Renderer.material`` は、そのオブジェクト専用に複製したマテリアルを返す。複製を変更しても、同じマテリアルを使うほかのオブジェクトには影響しない。複製されたマテリアルは自動では破棄されないため、``OnDestroy`` 関数で破棄している。
* すべてのオブジェクトの色をまとめて変えたい場合は、``Renderer.sharedMaterial`` で元のマテリアルを変更する。ただし、エディターで再生中に変更すると、再生を止めたあとも変更がマテリアルのアセットに残る。

.. note::

   ``MaterialPropertyBlock`` を使ってオブジェクトごとに値を変える方法もあるが、``MaterialPropertyBlock`` を設定したオブジェクトは SRP Batcher の対象から外れる。URP では、オブジェクトごとにマテリアルを分けるほうが、SRP Batcher の効果を得やすい。
