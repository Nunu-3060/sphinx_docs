第 1 章 はじめに
================

本書の目的
----------

本書の目的は、GLSL を初めて学ぶ人が、シェーダーがどのように動くのかを理解し、簡単なシェーダーを自分で書けるようになることです。文法の説明だけでなく、座標変換やライティングなど、シェーダーで実際によく行う処理を、動くサンプルとともに説明します。

対象読者と前提知識
------------------

本書は次のような読者を想定しています。

* C 言語、JavaScript、Python などのプログラミング言語で、変数、条件分岐、繰り返し、関数を使ったプログラムを書いたことがある人
* GPU やシェーダーについては知らない、または少し聞いたことがある程度の人

座標変換やライティングの章では、ベクトルと行列の計算を使います。必要な内容はその都度説明するので、事前に詳しく知っている必要はありません。

サンプルの JavaScript の部分は、WebGL の API を呼び出してシェーダーを動かすための準備です。本書の主題は GLSL なので、JavaScript についての説明は必要最小限にとどめます。

動作環境
--------

本書のサンプルは、次の環境で動作します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - GLSL のバージョン
     - GLSL ES 3.00（シェーダーの先頭に ``#version 300 es`` と書くバージョン）
   * - グラフィックス API
     - WebGL 2.0
   * - ブラウザー
     - WebGL 2.0 に対応したブラウザー（Google Chrome、Microsoft Edge、Mozilla Firefox、Safari の最新版など）
   * - 追加のソフトウェア
     - 不要

サンプルが表示されない場合は、ブラウザーを最新版に更新してください。それでも表示されない場合は、ブラウザーの設定でハードウェアアクセラレーション（GPU の利用）が有効になっているか確認してください。

本書の構成
----------

本書は次の 5 部と付録で構成されています。前の章の内容を前提に説明するので、初めて読む場合は順番に読むことをお勧めします。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 部
     - 章
     - 内容
   * - 導入
     - 第 1 章〜第 3 章
     - シェーダーと GPU の仕組み、サンプルを動かすための準備
   * - GLSL の基礎
     - 第 4 章〜第 6 章
     - 文法、組み込み関数、シェーダーへのデータの受け渡し
   * - 描画の基本
     - 第 7 章〜第 10 章
     - 頂点シェーダーによる座標変換、フラグメントシェーダーによる色の計算、テクスチャ、ライティング
   * - 応用
     - 第 11 章〜第 14 章
     - アニメーション、ノイズ、ポストエフェクト、レイマーチング
   * - 開発の実践
     - 第 15 章
     - エラーの調べ方、デバッグの方法、性能の考え方
   * - 付録
     - 付録 A〜付録 D
     - 組み込み変数・関数の一覧、GLSL のバージョンによる違い、用語集、参考資料

表記規則
--------

本書では、次の表記を使います。

* ``vec3`` や ``gl_Position`` のような等幅の文字は、ソースコード中のキーワードや識別子を表します。
* サンプルでは、変数の役割が分かるように、名前の先頭に次の文字を付けています。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 接頭辞
     - 例
     - 意味
   * - ``a``
     - ``aPosition``
     - 頂点属性（attribute）。頂点ごとに異なる入力（第 6 章）
   * - ``u``
     - ``uResolution``
     - uniform 変数。描画 1 回の間は共通の入力（第 6 章）
   * - ``v``
     - ``vColor``
     - 頂点シェーダーからフラグメントシェーダーへ渡す変数（第 6 章）

* 浮動小数点数の定数は、``1.0`` のように必ず小数点を付けて書きます。GLSL ES 3.00 では ``int`` から ``float`` への暗黙の型変換が行われないためです（第 4 章）。

.. _sample-list:

サンプルコード
--------------

各サンプルは 1 つの HTML ファイルで完結しており、シェーダーと、それを動かす JavaScript をすべて含んでいます。外部のライブラリは使用していません。

「ブラウザーで開く」のリンクから、ブラウザー上で動作を確認できます。「ダウンロード」のリンクから保存したファイルは、ブラウザーで直接開くだけで動作します。テキストエディターでシェーダーを書き換え、ブラウザーで再読み込みすると、変更の結果を確かめられます。

「シェーダー」のリンクからは、HTML ファイルに含まれるシェーダーだけを取り出したファイルをダウンロードできます。頂点シェーダーは拡張子 ``.vert``、フラグメントシェーダーは拡張子 ``.frag`` のファイルです。これらは HTML ファイルの内容から自動的に作成した閲覧用のファイルで、本文に掲載しているシェーダーもこのファイルから読み込んでいます。サンプルを動かす場合は HTML ファイルを使ってください。

.. note::

   サンプルの HTML ファイルにシェーダーを含めているのは、ローカルに保存した HTML ファイルからは、ブラウザーのセキュリティ制限により、同じフォルダーにあるほかのファイルを JavaScript で読み込めないためです。シェーダーを別のファイルにすると、Web サーバーを用意しなければサンプルが動かなくなります。

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - サンプル
     - 対応する章
     - リンク
   * - 01 三角形の描画
     - 第 3 章
     - `ブラウザーで開く <../examples/01_triangle.html>`__／:download:`ダウンロード <../../examples/01_triangle.html>`／シェーダー：:download:`01_triangle.vert <../../examples/shaders/01_triangle.vert>`、:download:`01_triangle.frag <../../examples/shaders/01_triangle.frag>`
   * - 02 頂点カラーと uniform 変数
     - 第 6 章
     - `ブラウザーで開く <../examples/02_vertex_color.html>`__／:download:`ダウンロード <../../examples/02_vertex_color.html>`／シェーダー：:download:`02_vertex_color.vert <../../examples/shaders/02_vertex_color.vert>`、:download:`02_vertex_color.frag <../../examples/shaders/02_vertex_color.frag>`
   * - 03 座標変換
     - 第 7 章
     - `ブラウザーで開く <../examples/03_transform.html>`__／:download:`ダウンロード <../../examples/03_transform.html>`／シェーダー：:download:`03_transform.vert <../../examples/shaders/03_transform.vert>`、:download:`03_transform.frag <../../examples/shaders/03_transform.frag>`
   * - 04 フラグメントシェーダーで図形を描く
     - 第 8 章
     - `ブラウザーで開く <../examples/04_fragment_shapes.html>`__／:download:`ダウンロード <../../examples/04_fragment_shapes.html>`／シェーダー：:download:`04_fragment_shapes.vert <../../examples/shaders/04_fragment_shapes.vert>`、:download:`04_fragment_shapes.frag <../../examples/shaders/04_fragment_shapes.frag>`
   * - 05 距離関数による図形の合成
     - 第 8 章
     - `ブラウザーで開く <../examples/05_sdf_2d.html>`__／:download:`ダウンロード <../../examples/05_sdf_2d.html>`／シェーダー：:download:`05_sdf_2d.vert <../../examples/shaders/05_sdf_2d.vert>`、:download:`05_sdf_2d.frag <../../examples/shaders/05_sdf_2d.frag>`
   * - 06 テクスチャ
     - 第 9 章
     - `ブラウザーで開く <../examples/06_texture.html>`__／:download:`ダウンロード <../../examples/06_texture.html>`／シェーダー：:download:`06_texture.vert <../../examples/shaders/06_texture.vert>`、:download:`06_texture.frag <../../examples/shaders/06_texture.frag>`
   * - 07 ライティング
     - 第 10 章
     - `ブラウザーで開く <../examples/07_lighting.html>`__／:download:`ダウンロード <../../examples/07_lighting.html>`／シェーダー：:download:`07_lighting.vert <../../examples/shaders/07_lighting.vert>`、:download:`07_lighting.frag <../../examples/shaders/07_lighting.frag>`
   * - 08 アニメーション
     - 第 11 章
     - `ブラウザーで開く <../examples/08_animation.html>`__／:download:`ダウンロード <../../examples/08_animation.html>`／シェーダー：:download:`08_animation_wave.vert <../../examples/shaders/08_animation_wave.vert>`、:download:`08_animation_wave.frag <../../examples/shaders/08_animation_wave.frag>`、:download:`08_animation_easing.vert <../../examples/shaders/08_animation_easing.vert>`、:download:`08_animation_easing.frag <../../examples/shaders/08_animation_easing.frag>`
   * - 09 ノイズ
     - 第 12 章
     - `ブラウザーで開く <../examples/09_noise.html>`__／:download:`ダウンロード <../../examples/09_noise.html>`／シェーダー：:download:`09_noise.vert <../../examples/shaders/09_noise.vert>`、:download:`09_noise.frag <../../examples/shaders/09_noise.frag>`
   * - 10 ポストエフェクト
     - 第 13 章
     - `ブラウザーで開く <../examples/10_post_effect.html>`__／:download:`ダウンロード <../../examples/10_post_effect.html>`／シェーダー：:download:`10_post_effect_scene.vert <../../examples/shaders/10_post_effect_scene.vert>`、:download:`10_post_effect_scene.frag <../../examples/shaders/10_post_effect_scene.frag>`、:download:`10_post_effect_post.vert <../../examples/shaders/10_post_effect_post.vert>`、:download:`10_post_effect_post.frag <../../examples/shaders/10_post_effect_post.frag>`
   * - 11 レイマーチング
     - 第 14 章
     - `ブラウザーで開く <../examples/11_raymarching.html>`__／:download:`ダウンロード <../../examples/11_raymarching.html>`／シェーダー：:download:`11_raymarching.vert <../../examples/shaders/11_raymarching.vert>`、:download:`11_raymarching.frag <../../examples/shaders/11_raymarching.frag>`
   * - 12 シェーダーエディター
     - 第 15 章
     - `ブラウザーで開く <../examples/12_shader_editor.html>`__／:download:`ダウンロード <../../examples/12_shader_editor.html>`

サンプル 12 は、フラグメントシェーダーをページ上で書き換えてすぐに実行できるエディターです。本書のフラグメントシェーダーのコード片を試すときにも利用できます。サンプル 12 のフラグメントシェーダーは、ページ上で編集する文字列として JavaScript の中に書いているため、シェーダーのファイルは用意していません。
