付録 B GLSL のバージョンによる違い
==================================

本書で扱った GLSL ES 3.00 と、WebGL 1.0 で使う GLSL ES 1.00、デスクトップ向けの OpenGL で使う GLSL 3.30 の主な違いをまとめます。古い資料のシェーダーを読むときや、ほかの環境にシェーダーを移植するときの参考にしてください。

主な違い
--------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - 項目
     - GLSL ES 1.00（WebGL 1.0）
     - GLSL ES 3.00（WebGL 2.0）
     - GLSL 3.30（OpenGL 3.3）
   * - バージョンの指定
     - ``#version 100``\ （省略可）
     - ``#version 300 es``
     - ``#version 330`` または ``#version 330 core``
   * - 頂点属性
     - ``attribute vec3 aPosition;``
     - ``in vec3 aPosition;``
     - ``in vec3 aPosition;``
   * - ステージ間の変数
     - ``varying``\ （両方のシェーダー）
     - 頂点シェーダーは ``out``、フラグメントシェーダーは ``in``
     - 頂点シェーダーは ``out``、フラグメントシェーダーは ``in``
   * - フラグメントの出力
     - 組み込み変数 ``gl_FragColor``
     - ``out vec4 outColor;`` のように自分で宣言する
     - ``out vec4 outColor;`` のように自分で宣言する
   * - テクスチャの読み出し
     - ``texture2D``、``textureCube``
     - ``texture``
     - ``texture``
   * - 精度修飾子
     - フラグメントシェーダーでは ``float`` の精度の指定が必要
     - フラグメントシェーダーでは ``float`` の精度の指定が必要
     - 書いてもよいが、意味を持たない
   * - 暗黙の型変換
     - なし
     - なし
     - ``int`` から ``float`` などへの変換あり
   * - ``layout(location = …)``
     - なし
     - 頂点シェーダーの入力と、フラグメントシェーダーの出力に使える
     - 頂点シェーダーの入力と、フラグメントシェーダーの出力に使える
   * - 符号なし整数、ビット演算
     - なし
     - あり
     - あり
   * - ループ
     - 繰り返し回数が定数で決まる形だけ（制限あり）
     - 制限なし
     - 制限なし
   * - 配列
     - 配列のコンストラクターなし
     - 配列のコンストラクターあり
     - 配列のコンストラクターあり
   * - 使えるシェーダーの種類
     - 頂点、フラグメント
     - 頂点、フラグメント
     - 頂点、フラグメント、ジオメトリ

GLSL ES 1.00 から GLSL ES 3.00 への書き換え
-------------------------------------------

WebGL 1.0 向けの古いシェーダーを WebGL 2.0 で使う場合は、次のように書き換えます。

.. code-block:: glsl

   // GLSL ES 1.00（WebGL 1.0）
   precision mediump float;
   varying vec2 vTexCoord;
   uniform sampler2D uTexture;

   void main() {
       gl_FragColor = texture2D(uTexture, vTexCoord);
   }

.. code-block:: glsl

   // GLSL ES 3.00（WebGL 2.0）
   #version 300 es
   precision mediump float;
   in vec2 vTexCoord;
   uniform sampler2D uTexture;
   out vec4 outColor;

   void main() {
       outColor = texture(uTexture, vTexCoord);
   }

なお、WebGL 2.0 でも、``#version 300 es`` を書かなければ GLSL ES 1.00 のシェーダーとしてそのまま使えます。ただし、頂点シェーダーとフラグメントシェーダーのバージョンはそろえる必要があります。

デスクトップ向けの GLSL への移植
--------------------------------

GLSL ES 3.00 のシェーダーをデスクトップ向けの OpenGL で使う場合は、主に次の点を変更します。

* ``#version 300 es`` を ``#version 330 core`` などに変更する。
* 精度修飾子は削除してもかまいません（残しても無視されます）。

逆に、デスクトップ向けのシェーダーを WebGL 2.0 に移植する場合は、暗黙の型変換に頼っている部分（``float x = 1;`` など）の修正と、フラグメントシェーダーへの ``precision`` 文の追加が必要です。また、ジオメトリシェーダーなど、GLSL ES 3.00 にない機能は使えません。

新しいバージョンで追加された主な機能
------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - バージョン
     - 主な追加機能
   * - GLSL ES 3.10（OpenGL ES 3.1）
     - コンピュートシェーダー、配列の配列、シェーダーストレージバッファー
   * - GLSL ES 3.20（OpenGL ES 3.2）
     - ジオメトリシェーダー、テッセレーションシェーダー
   * - GLSL 4.00 以降（OpenGL 4.0 以降）
     - テッセレーションシェーダー（4.00）、コンピュートシェーダー（4.30）、``double`` 型（4.00）など

WebGL 2.0 で使えるのは GLSL ES 3.00 までです。Web で GPU の計算機能をより広く使いたい場合は、WebGPU と、そのシェーダー言語である WGSL を利用する方法もあります。
