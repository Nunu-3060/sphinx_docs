GPU とリアルタイム CG
=====================

本資料のレンダラーは Python で書かれており、小さな画像 1 枚を描くのにも 0.1 秒から数秒かかる。ゲームのようなリアルタイム CG では、1 秒間に 60 枚以上の画像を描く必要がある。これを可能にしているのが GPU（Graphics Processing Unit）である。本章では、GPU による描画の仕組みと、ここまでに作ったコードとの対応を説明する。

GPU の特徴
----------

CG の計算には、次の特徴がある。

* 同じ計算を、多数のデータに対して繰り返す。数万から数百万の頂点に同じ行列を掛け、数百万の画素に同じ照明の計算を行う。
* それぞれのデータの計算は、互いに独立している。ある画素の色の計算は、隣の画素の結果を必要としない。

GPU は、このような計算に特化した演算装置である。CPU が少数の高性能なコアで複雑な処理を順に実行するのに対し、GPU は数千の単純な演算器で、同じ命令を多数のデータに対して同時に実行する。本資料のレンダラーで、画素ごとの計算を NumPy の配列演算でまとめて行ったのと同じ考え方である。

この性質は CG 以外の計算にも有効なので、GPU は機械学習や科学技術計算にも広く使われている。

描画パイプラインとの対応
------------------------

GPU で 3 次元の物体を描く処理の流れを、描画パイプライン（グラフィックスパイプライン）という。パイプラインの段階には、プログラムで処理の内容を書けるもの（プログラマブルステージ）と、GPU の回路で決まった処理を行うもの（固定機能ステージ）がある。プログラマブルステージで実行するプログラムを、シェーダーという。

.. list-table::
   :header-rows: 1
   :widths: 25 15 30 30

   * - 段階
     - 種類
     - 処理
     - 本資料のコード
   * - 頂点シェーダー
     - プログラマブル
     - 頂点ごとに座標変換を行い、クリップ座標と、補間する属性を出力する。
     - ``to_clip()``、``transform_normals()``
   * - クリッピング、透視除算、ビューポート変換
     - 固定機能
     - 画面の外にはみ出す三角形を切り取り、スクリーン座標を求める。
     - ``draw_mesh()`` の前半
   * - 背面カリング
     - 固定機能
     - 裏を向いた三角形を捨てる。
     - ``draw_mesh()`` の ``cull_back``
   * - ラスタライザー
     - 固定機能
     - 三角形が覆う画素を求め、属性を透視補正補間する。
     - ``draw_mesh()`` の後半
   * - フラグメントシェーダー
     - プログラマブル
     - 画素ごとに色を計算する。テクスチャをサンプリングする。
     - ``shade()``、``sample_trilinear()``
   * - 深度テスト、ブレンド
     - 固定機能
     - Z バッファーで前後関係を判定し、半透明の色を合成して書き込む。
     - ``draw_mesh()`` の深度テスト、``over()``

GPU では、フラグメントシェーダーの前に深度テストを行い、隠れる画素の色の計算を省く最適化（アーリー Z）も行われる。本資料のレンダラーで、深度テストの後に見えている画素だけの色を計算したのと同じ効果がある。

シェーダーの例
--------------

シェーダーは、GLSL（OpenGL）、HLSL（Direct3D）、MSL（Metal）、WGSL（WebGPU）などの専用の言語で書く。次の例は、:doc:`shading`\ のブリン-フォンの照明モデルを GLSL で書いたものである。

まず、頂点シェーダーである。``gl_Position`` に書き込んだクリップ座標を使って、GPU がラスタライズを行う。``out`` を付けた変数は、ラスタライザーによって画素ごとに補間され、フラグメントシェーダーに渡される。

.. code-block:: glsl
   :linenos:

   #version 330 core

   layout(location = 0) in vec3 aPosition;  // 頂点の位置(モデル座標)
   layout(location = 1) in vec3 aNormal;    // 頂点の法線(モデル座標)

   uniform mat4 uModel;
   uniform mat4 uView;
   uniform mat4 uProjection;

   out vec3 vPosition;  // ワールド座標の位置
   out vec3 vNormal;    // ワールド座標の法線

   void main() {
       vec4 world = uModel * vec4(aPosition, 1.0);
       vPosition = world.xyz;
       vNormal = mat3(transpose(inverse(uModel))) * aNormal;
       gl_Position = uProjection * uView * world;
   }

次に、フラグメントシェーダーである。``shading.py`` の ``shade()`` と同じ計算を、1 つの画素について書いている。GPU は、このプログラムを全ての画素について並列に実行する。

.. code-block:: glsl
   :linenos:

   #version 330 core

   in vec3 vPosition;
   in vec3 vNormal;

   uniform vec3 uEye;        // カメラの位置
   uniform vec3 uLightDir;   // 表面から光源へ向かう向き
   uniform vec3 uBaseColor;  // 表面の色(線形な値)
   uniform float uShininess;

   out vec4 fragColor;

   void main() {
       vec3 n = normalize(vNormal);
       vec3 l = normalize(uLightDir);
       vec3 v = normalize(uEye - vPosition);
       vec3 h = normalize(l + v);

       float diffuse = max(dot(n, l), 0.0);
       float specular = 0.0;
       if (diffuse > 0.0) {
           specular = pow(max(dot(n, h), 0.0), uShininess);
       }
       vec3 color = 0.08 * uBaseColor + diffuse * uBaseColor
                    + 0.5 * specular;
       fragColor = vec4(color, 1.0);
   }

``uniform`` を付けた変数は、全ての頂点や画素で共通の値で、CPU 側のプログラムから設定する。補間された法線は長さが 1 とは限らないので、フラグメントシェーダーで正規化し直す必要がある。これは ``shade()`` で ``normalize(normal)`` を行っているのと同じ理由である。

出力した線形な値は、フレームバッファーを sRGB の形式にしておけば、GPU が書き込むときに自動的に sRGB の値に変換する。

グラフィックス API
------------------

アプリケーションから GPU に描画を指示するには、グラフィックス API を使う。主なものは次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - API
     - 主な環境
     - 特徴
   * - OpenGL
     - Windows、Linux、macOS（非推奨）
     - 歴史が長く、資料が多い。学習に向いている。
   * - Vulkan
     - Windows、Linux、Android
     - OpenGL の後継。GPU を細かく制御でき、高速だが、記述量が多い。
   * - Direct3D 12
     - Windows、Xbox
     - Microsoft の API。Windows のゲームで広く使われている。
   * - Metal
     - macOS、iOS
     - Apple の API。
   * - WebGL、WebGPU
     - Web ブラウザー
     - Web ページから GPU を使う API。WebGL は OpenGL ES、WebGPU は新しい世代の API にもとづく。

実際のアプリケーション開発では、これらの API を直接使わずに、Unity や Unreal Engine のようなゲームエンジン、three.js のようなライブラリを使うことも多い。その場合でも、内部では本資料で説明した処理が行われている。

リアルタイムのレイトレーシング
------------------------------

近年の GPU は、レイと三角形の交差判定と、BVH の探索を高速に行う専用の回路を備えている。Direct3D 12 の DirectX Raytracing（DXR）や Vulkan のレイトレーシング拡張を使うと、リアルタイムでもレイトレーシングを利用できる。

ただし、全ての画素で多数のレイを飛ばすには、まだ計算量が大きすぎる。そのため、現在のゲームでは、基本の描画をラスタライズ法で行い、影、反射、大域照明だけをレイトレーシング法で計算するハイブリッドな方法が主流である。少ないサンプル数によるノイズは、デノイザーで取り除いている。

次に学ぶこと
------------

本資料で学んだ内容を土台に、さらに学ぶとよい分野を挙げる。

* GPU のプログラミング: OpenGL や WebGL で、本資料のレンダラーと同じものを作ってみる。シェーダーだけで絵を描く方法（レイマーチング）も、交差判定とライティングの練習になる。
* 物理ベースレンダリング: マイクロファセットの BRDF、エネルギー保存、画像にもとづく照明（IBL）。
* 影の技法: シャドウマップと、その輪郭をなめらかにする方法。
* アニメーション: キーフレーム、スケルトンによる変形、四元数による回転の補間。
* パストレーシングの高速化: 重点的サンプリング、BVH の構築、デノイザー。

参考になる書籍と Web サイトは、:doc:`references`\ にまとめている。
