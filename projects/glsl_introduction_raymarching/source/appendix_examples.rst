##################################################
付録 A サンプルコード一覧
##################################################

本資料のサンプルコードの一覧と、その全体を掲載する。各ファイルは、表のリンクからダウンロードするか、ブラウザーで実行できる。

ファイルの構成
==============================

サンプルコードは、次のフォルダーに置かれている。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - フォルダー
     - 内容
   * - ``examples/shaders``
     - Shadertoy 形式のフラグメントシェーダー（拡張子 ``.frag``）。ファイル名の先頭の数字は章の番号を表す。
   * - ``examples/viewer``
     - シェーダーをブラウザーで実行するスクリプトと、実行結果の画像を撮影するスクリプト

シェーダーの一覧
==============================

.. list-table::
   :header-rows: 1
   :widths: 30 12 34 14 10

   * - ファイル
     - 章
     - 内容
     - ダウンロード
     - 実行
   * - :ref:`01_uv.frag <example-01_uv>`
     - 第 1 章
     - ピクセル座標を色として出力する
     - :download:`ダウンロード <../examples/shaders/01_uv.frag>`
     - `実行 <demos/01_uv.html>`__
   * - :ref:`01_circle2d.frag <example-01_circle2d>`
     - 第 1 章
     - 2 次元の SDF で円を描く
     - :download:`ダウンロード <../examples/shaders/01_circle2d.frag>`
     - `実行 <demos/01_circle2d.html>`__
   * - :ref:`02_first_sphere.frag <example-02_first_sphere>`
     - 第 2 章
     - スフィアトレーシングで球を描く
     - :download:`ダウンロード <../examples/shaders/02_first_sphere.frag>`
     - `実行 <demos/02_first_sphere.html>`__
   * - :ref:`02_step_count.frag <example-02_step_count>`
     - 第 2 章
     - 反復回数を可視化する
     - :download:`ダウンロード <../examples/shaders/02_step_count.frag>`
     - `実行 <demos/02_step_count.html>`__
   * - :ref:`03_primitives.frag <example-03_primitives>`
     - 第 3 章
     - 基本形状の SDF
     - :download:`ダウンロード <../examples/shaders/03_primitives.frag>`
     - `実行 <demos/03_primitives.html>`__
   * - :ref:`04_boolean.frag <example-04_boolean>`
     - 第 4 章
     - ブーリアン演算
     - :download:`ダウンロード <../examples/shaders/04_boolean.frag>`
     - `実行 <demos/04_boolean.html>`__
   * - :ref:`04_smooth_union.frag <example-04_smooth_union>`
     - 第 4 章
     - スムース合成
     - :download:`ダウンロード <../examples/shaders/04_smooth_union.frag>`
     - `実行 <demos/04_smooth_union.html>`__
   * - :ref:`04_repetition.frag <example-04_repetition>`
     - 第 4 章
     - 空間の繰り返し、回転、対称化
     - :download:`ダウンロード <../examples/shaders/04_repetition.frag>`
     - `実行 <demos/04_repetition.html>`__
   * - :ref:`04_hex_repeat.frag <example-04_hex_repeat>`
     - 第 4 章
     - 六角形の繰り返し
     - :download:`ダウンロード <../examples/shaders/04_hex_repeat.frag>`
     - `実行 <demos/04_hex_repeat.html>`__
   * - :ref:`04_polar.frag <example-04_polar>`
     - 第 4 章
     - 回転方向の繰り返し
     - :download:`ダウンロード <../examples/shaders/04_polar.frag>`
     - `実行 <demos/04_polar.html>`__
   * - :ref:`04_log_polar.frag <example-04_log_polar>`
     - 第 4 章
     - 対数極座標による拡大方向の繰り返し
     - :download:`ダウンロード <../examples/shaders/04_log_polar.frag>`
     - `実行 <demos/04_log_polar.html>`__
   * - :ref:`05_lighting.frag <example-05_lighting>`
     - 第 5 章
     - 法線、拡散反射、鏡面反射、天空光、ガンマ補正
     - :download:`ダウンロード <../examples/shaders/05_lighting.frag>`
     - `実行 <demos/05_lighting.html>`__
   * - :ref:`06_shadow.frag <example-06_shadow>`
     - 第 6 章
     - ハードシャドウとソフトシャドウ
     - :download:`ダウンロード <../examples/shaders/06_shadow.frag>`
     - `実行 <demos/06_shadow.html>`__
   * - :ref:`06_ao.frag <example-06_ao>`
     - 第 6 章
     - アンビエントオクルージョン
     - :download:`ダウンロード <../examples/shaders/06_ao.frag>`
     - `実行 <demos/06_ao.html>`__
   * - :ref:`07_camera.frag <example-07_camera>`
     - 第 7 章
     - カメラの操作、空、フォグ、トーンマッピング、アンチエイリアス
     - :download:`ダウンロード <../examples/shaders/07_camera.frag>`
     - `実行 <demos/07_camera.html>`__
   * - :ref:`07_orthographic.frag <example-07_orthographic>`
     - 第 7 章
     - 平行投影によるアイソメトリック表示
     - :download:`ダウンロード <../examples/shaders/07_orthographic.frag>`
     - `実行 <demos/07_orthographic.html>`__
   * - :ref:`07_color.frag <example-07_color>`
     - 第 7 章
     - HSV、余弦関数によるパレット、色の補間
     - :download:`ダウンロード <../examples/shaders/07_color.frag>`
     - `実行 <demos/07_color.html>`__
   * - :ref:`08_scene.frag <example-08_scene>`
     - 第 8 章
     - 完成したシーン
     - :download:`ダウンロード <../examples/shaders/08_scene.frag>`
     - `実行 <demos/08_scene.html>`__
   * - :ref:`09_debug.frag <example-09_debug>`
     - 第 9 章
     - デバッグ用の可視化
     - :download:`ダウンロード <../examples/shaders/09_debug.frag>`
     - `実行 <demos/09_debug.html>`__
   * - :ref:`09_relaxation.frag <example-09_relaxation>`
     - 第 9 章
     - 過緩和によるスフィアトレーシングの高速化
     - :download:`ダウンロード <../examples/shaders/09_relaxation.frag>`
     - `実行 <demos/09_relaxation.html>`__
   * - :ref:`10_noise2d.frag <example-10_noise2d>`
     - 第 10 章
     - ハッシュとノイズの比較
     - :download:`ダウンロード <../examples/shaders/10_noise2d.frag>`
     - `実行 <demos/10_noise2d.html>`__
   * - :ref:`10_cellular.frag <example-10_cellular>`
     - 第 10 章
     - セルラーノイズとミンコフスキー距離
     - :download:`ダウンロード <../examples/shaders/10_cellular.frag>`
     - `実行 <demos/10_cellular.html>`__
   * - :ref:`10_cracks.frag <example-10_cracks>`
     - 第 10 章
     - セルラーノイズによる石畳とひび割れた岩
     - :download:`ダウンロード <../examples/shaders/10_cracks.frag>`
     - `実行 <demos/10_cracks.html>`__
   * - :ref:`10_curl.frag <example-10_curl>`
     - 第 10 章
     - 勾配の場とカールノイズによる移流の比較
     - :download:`ダウンロード <../examples/shaders/10_curl.frag>`
     - `実行 <demos/10_curl.html>`__
   * - :ref:`10_terrain.frag <example-10_terrain>`
     - 第 10 章
     - fBm による地形
     - :download:`ダウンロード <../examples/shaders/10_terrain.frag>`
     - `実行 <demos/10_terrain.html>`__
   * - :ref:`10_texture.frag <example-10_texture>`
     - 第 10 章
     - トライプラナーマッピングとバンプマッピング
     - :download:`ダウンロード <../examples/shaders/10_texture.frag>`
     - `実行 <demos/10_texture.html>`__
   * - :ref:`10_quadtree_pattern.frag <example-10_quadtree_pattern>`
     - 第 10 章
     - 手続き的な四分木による模様
     - :download:`ダウンロード <../examples/shaders/10_quadtree_pattern.frag>`
     - `実行 <demos/10_quadtree_pattern.html>`__
   * - :ref:`11_reflection_refraction.frag <example-11_reflection_refraction>`
     - 第 11 章
     - 反射と屈折
     - :download:`ダウンロード <../examples/shaders/11_reflection_refraction.frag>`
     - `実行 <demos/11_reflection_refraction.html>`__
   * - :ref:`12_pbr.frag <example-12_pbr>`
     - 第 12 章
     - GGX、金属度と粗さによる材質
     - :download:`ダウンロード <../examples/shaders/12_pbr.frag>`
     - `実行 <demos/12_pbr.html>`__
   * - :ref:`12_sss.frag <example-12_sss>`
     - 第 12 章
     - サブサーフェススキャッタリングの近似
     - :download:`ダウンロード <../examples/shaders/12_sss.frag>`
     - `実行 <demos/12_sss.html>`__
   * - :ref:`13_menger.frag <example-13_menger>`
     - 第 13 章
     - メンガーのスポンジ
     - :download:`ダウンロード <../examples/shaders/13_menger.frag>`
     - `実行 <demos/13_menger.html>`__
   * - :ref:`13_mandelbulb.frag <example-13_mandelbulb>`
     - 第 13 章
     - マンデルバルブ
     - :download:`ダウンロード <../examples/shaders/13_mandelbulb.frag>`
     - `実行 <demos/13_mandelbulb.html>`__
   * - :ref:`13_mandelbox.frag <example-13_mandelbox>`
     - 第 13 章
     - マンデルボックス
     - :download:`ダウンロード <../examples/shaders/13_mandelbox.frag>`
     - `実行 <demos/13_mandelbox.html>`__
   * - :ref:`13_kifs.frag <example-13_kifs>`
     - 第 13 章
     - 折り返しによるフラクタル（KIFS）
     - :download:`ダウンロード <../examples/shaders/13_kifs.frag>`
     - `実行 <demos/13_kifs.html>`__
   * - :ref:`14_slice.frag <example-14_slice>`
     - 第 14 章
     - 4 次元の超立方体の 3 次元の断面
     - :download:`ダウンロード <../examples/shaders/14_slice.frag>`
     - `実行 <demos/14_slice.html>`__
   * - :ref:`14_stereographic.frag <example-14_stereographic>`
     - 第 14 章
     - クリフォードトーラスのステレオ投影
     - :download:`ダウンロード <../examples/shaders/14_stereographic.frag>`
     - `実行 <demos/14_stereographic.html>`__
   * - :ref:`14_julia.frag <example-14_julia>`
     - 第 14 章
     - 四元数ジュリア集合
     - :download:`ダウンロード <../examples/shaders/14_julia.frag>`
     - `実行 <demos/14_julia.html>`__
   * - :ref:`15_voxel.frag <example-15_voxel>`
     - 第 15 章
     - 3D DDA によるボクセルの描画
     - :download:`ダウンロード <../examples/shaders/15_voxel.frag>`
     - `実行 <demos/15_voxel.html>`__
   * - :ref:`15_city.frag <example-15_city>`
     - 第 15 章
     - グリッドの走査とスフィアトレーシングの組み合わせ
     - :download:`ダウンロード <../examples/shaders/15_city.frag>`
     - `実行 <demos/15_city.html>`__
   * - :ref:`15_tri_grid.frag <example-15_tri_grid>`
     - 第 15 章
     - 三角形の格子の走査
     - :download:`ダウンロード <../examples/shaders/15_tri_grid.frag>`
     - `実行 <demos/15_tri_grid.html>`__
   * - :ref:`15_hex_columns.frag <example-15_hex_columns>`
     - 第 15 章
     - 六角形の格子の走査
     - :download:`ダウンロード <../examples/shaders/15_hex_columns.frag>`
     - `実行 <demos/15_hex_columns.html>`__
   * - :ref:`15_quadtree_city.frag <example-15_quadtree_city>`
     - 第 15 章
     - 手続き的な四分木による街並み
     - :download:`ダウンロード <../examples/shaders/15_quadtree_city.frag>`
     - `実行 <demos/15_quadtree_city.html>`__
   * - :ref:`15_octree.frag <example-15_octree>`
     - 第 15 章
     - 手続き的な八分木と空の空間の飛ばし
     - :download:`ダウンロード <../examples/shaders/15_octree.frag>`
     - `実行 <demos/15_octree.html>`__
   * - :ref:`16_volume.frag <example-16_volume>`
     - 第 16 章
     - ボリュームレンダリングによる雲
     - :download:`ダウンロード <../examples/shaders/16_volume.frag>`
     - `実行 <demos/16_volume.html>`__
   * - :ref:`16_atmosphere.frag <example-16_atmosphere>`
     - 第 16 章
     - 大気の散乱
     - :download:`ダウンロード <../examples/shaders/16_atmosphere.frag>`
     - `実行 <demos/16_atmosphere.html>`__
   * - :ref:`17_path_tracing.frag <example-17_path_tracing>`
     - 第 17 章
     - パストレーシング
     - :download:`ダウンロード <../examples/shaders/17_path_tracing.frag>`
     - `実行 <demos/17_path_tracing.html>`__
   * - :ref:`17_progressive.frag <example-17_progressive>`
     - 第 17 章
     - 複数パスによる蓄積、被写界深度、モーションブラー
     - :download:`ダウンロード <../examples/shaders/17_progressive.frag>`
     - `実行 <demos/17_progressive.html>`__
   * - :ref:`18_landscape.frag <example-18_landscape>`
     - 第 18 章
     - 夕暮れの風景（複数パス）
     - :download:`ダウンロード <../examples/shaders/18_landscape.frag>`
     - `実行 <demos/18_landscape.html>`__
   * - :ref:`18_landscape_debug.frag <example-18_landscape_debug>`
     - 第 18 章
     - 夕暮れの風景のデバッグ版
     - :download:`ダウンロード <../examples/shaders/18_landscape_debug.frag>`
     - `実行 <demos/18_landscape_debug.html>`__
   * - :ref:`19_night_city.frag <example-19_night_city>`
     - 第 19 章
     - ボクセルの都市の夜景
     - :download:`ダウンロード <../examples/shaders/19_night_city.frag>`
     - `実行 <demos/19_night_city.html>`__
   * - :ref:`19_night_city_debug.frag <example-19_night_city_debug>`
     - 第 19 章
     - ボクセルの都市の夜景のデバッグ版
     - :download:`ダウンロード <../examples/shaders/19_night_city_debug.frag>`
     - `実行 <demos/19_night_city_debug.html>`__
   * - :ref:`20_still_life.frag <example-20_still_life>`
     - 第 20 章
     - パストレーシングによる静物画（複数パス）
     - :download:`ダウンロード <../examples/shaders/20_still_life.frag>`
     - `実行 <demos/20_still_life.html>`__
   * - :ref:`20_still_life_debug.frag <example-20_still_life_debug>`
     - 第 20 章
     - パストレーシングによる静物画のデバッグ版
     - :download:`ダウンロード <../examples/shaders/20_still_life_debug.frag>`
     - `実行 <demos/20_still_life_debug.html>`__

シェーダービューアー
==============================

``shader_viewer.py`` は、Shadertoy 形式のシェーダーをブラウザーで実行するためのスクリプトである。Python 3.9 以降の標準ライブラリだけで動作し、追加のパッケージは不要である。

使い方
--------------------

.. code-block:: text
   :linenos:

   python shader_viewer.py [-h] [-o OUTPUT] [--no-open] shader

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 引数
     - 説明
   * - ``shader``
     - ``mainImage`` 関数を含む GLSL ファイル
   * - ``-o OUTPUT``, ``--output OUTPUT``
     - 出力する HTML ファイル。省略すると、シェーダーと同じフォルダーに拡張子を ``.html`` に変えたファイルを作る。
   * - ``--no-open``
     - HTML ファイルを作るだけで、ブラウザーを開かない。

生成される HTML ファイルは、シェーダーのソースコードを埋め込んだ単一のファイルで、他のファイルに依存しない。シェーダーのコンパイルに失敗した場合は、エラーメッセージが画面の上部に表示される。エラーメッセージの行番号は、シェーダーのファイルの行番号と一致する。

URL の末尾（``#`` の後）には、次のパラメーターを ``&`` でつなげて指定できる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - パラメーター
     - 説明
   * - ``t=2.5``
     - ``iTime`` を指定した秒数に固定する。
   * - ``frame=0``
     - ``iFrame`` を指定した値に固定する。
   * - ``frames=16``
     - 読み込み直後に指定した数のフレームだけを描画して止める。``iFrame`` は 0 から始まる。描画の速さによらず同じ結果が得られるので、図の撮影に使う。

ファイルの中に ``// ==== Buffer A ====`` と ``// ==== Image ====`` の行を置くと、それぞれを Buffer A と Image のパスとして実行する（第 17 章）。Buffer A は 32 ビット浮動小数点数のテクスチャに描画され、Buffer A の ``iChannel0`` には自分自身の前のフレームの結果が、Image の ``iChannel0`` には Buffer A の今のフレームの結果が入る。さらに ``// ==== Common ====`` の行を置くと、その行から次の区切りまでのコードが、Shadertoy の Common のタブと同じく、すべてのパスの先頭に加えられる（第 18 章）。

ソースコード
--------------------

.. literalinclude:: ../examples/viewer/shader_viewer.py
   :language: python
   :linenos:
   :caption: shader_viewer.py

.. rst-class:: example-links

:download:`shader_viewer.py をダウンロード <../examples/viewer/shader_viewer.py>`

画像の撮影
==============================

本資料の図は、``capture_images.py`` でシェーダーの実行結果を撮影したものである。このスクリプトは、``shader_viewer.py`` で作った HTML を Chrome または Edge の headless モードで開き、スクリーンショットを ``source/_static/images`` に保存する。WebGL は CPU で動作する SwiftShader で実行するため、GPU は不要である。

画像が存在しないか、シェーダーより古い画像だけを撮影し直す。html のビルド時にも conf.py から同じ処理が呼び出されるため、シェーダーを編集してビルドすれば、図も自動的に更新される。ブラウザーが見つからない場合、ビルドは既存の画像を使って続行する。

使い方
--------------------

.. code-block:: text
   :linenos:

   python capture_images.py [-h] [--force] [--jobs JOBS]
                            [--shader-dir SHADER_DIR] [--output-dir OUTPUT_DIR]
                            [names ...]

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 引数
     - 説明
   * - ``names``
     - 撮影するシェーダーの名前（例: ``05_lighting``）。省略するとすべてのシェーダーが対象になる。
   * - ``--force``
     - 画像が新しくても撮影し直す。
   * - ``--jobs JOBS``
     - 同時に実行するブラウザーの数（既定: 4）
   * - ``--shader-dir SHADER_DIR``
     - シェーダーのフォルダー（既定: ``examples/shaders``）
   * - ``--output-dir OUTPUT_DIR``
     - 画像の出力先のフォルダー（既定: ``source/_static/images``）

ブラウザーは、環境変数 ``SHADER_BROWSER`` に指定された実行ファイル、Chrome と Edge の標準のインストール先、PATH 上のコマンドの順に探す。撮影時は ``iTime`` を 1 秒に固定し、1 フレームだけを描画する。一部のシェーダーは、撮影する時刻やフレーム数を個別に指定している（スクリプトの ``CAPTURE_SETTINGS``）。例えば、17_progressive.frag は 64 フレーム分を蓄積してから撮影する。描画するフレーム数を固定しているので、同じシェーダーからは常に同じ画像が得られる。

html のビルド時に撮影を行わないようにするには、環境変数 ``SKIP_SHADER_CAPTURE`` に ``1`` を設定する。

ソースコード
--------------------

.. literalinclude:: ../examples/viewer/capture_images.py
   :language: python
   :linenos:
   :caption: capture_images.py

.. rst-class:: example-links

:download:`capture_images.py をダウンロード <../examples/viewer/capture_images.py>`

シェーダーのソースコード
==============================

.. _example-01_uv:

01_uv.frag
--------------

第 1 章：ピクセル座標を色として出力する

.. literalinclude:: ../examples/shaders/01_uv.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`01_uv.frag をダウンロード <../examples/shaders/01_uv.frag>` ｜ `ブラウザーで実行 <demos/01_uv.html>`__

.. _example-01_circle2d:

01_circle2d.frag
--------------------

第 1 章：2 次元の SDF で円を描く

.. literalinclude:: ../examples/shaders/01_circle2d.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`01_circle2d.frag をダウンロード <../examples/shaders/01_circle2d.frag>` ｜ `ブラウザーで実行 <demos/01_circle2d.html>`__

.. _example-02_first_sphere:

02_first_sphere.frag
------------------------

第 2 章：スフィアトレーシングで球を描く

.. literalinclude:: ../examples/shaders/02_first_sphere.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`02_first_sphere.frag をダウンロード <../examples/shaders/02_first_sphere.frag>` ｜ `ブラウザーで実行 <demos/02_first_sphere.html>`__

.. _example-02_step_count:

02_step_count.frag
----------------------

第 2 章：反復回数を可視化する

.. literalinclude:: ../examples/shaders/02_step_count.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`02_step_count.frag をダウンロード <../examples/shaders/02_step_count.frag>` ｜ `ブラウザーで実行 <demos/02_step_count.html>`__

.. _example-03_primitives:

03_primitives.frag
----------------------

第 3 章：基本形状の SDF

.. literalinclude:: ../examples/shaders/03_primitives.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`03_primitives.frag をダウンロード <../examples/shaders/03_primitives.frag>` ｜ `ブラウザーで実行 <demos/03_primitives.html>`__

.. _example-04_boolean:

04_boolean.frag
-------------------

第 4 章：ブーリアン演算

.. literalinclude:: ../examples/shaders/04_boolean.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_boolean.frag をダウンロード <../examples/shaders/04_boolean.frag>` ｜ `ブラウザーで実行 <demos/04_boolean.html>`__

.. _example-04_smooth_union:

04_smooth_union.frag
------------------------

第 4 章：スムース合成

.. literalinclude:: ../examples/shaders/04_smooth_union.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_smooth_union.frag をダウンロード <../examples/shaders/04_smooth_union.frag>` ｜ `ブラウザーで実行 <demos/04_smooth_union.html>`__

.. _example-04_repetition:

04_repetition.frag
----------------------

第 4 章：空間の繰り返し、回転、対称化

.. literalinclude:: ../examples/shaders/04_repetition.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_repetition.frag をダウンロード <../examples/shaders/04_repetition.frag>` ｜ `ブラウザーで実行 <demos/04_repetition.html>`__

.. _example-04_hex_repeat:

04_hex_repeat.frag
----------------------

第 4 章：六角形の繰り返し

.. literalinclude:: ../examples/shaders/04_hex_repeat.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_hex_repeat.frag をダウンロード <../examples/shaders/04_hex_repeat.frag>` ｜ `ブラウザーで実行 <demos/04_hex_repeat.html>`__

.. _example-04_polar:

04_polar.frag
-----------------

第 4 章：回転方向の繰り返し

.. literalinclude:: ../examples/shaders/04_polar.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_polar.frag をダウンロード <../examples/shaders/04_polar.frag>` ｜ `ブラウザーで実行 <demos/04_polar.html>`__

.. _example-04_log_polar:

04_log_polar.frag
---------------------

第 4 章：対数極座標による拡大方向の繰り返し

.. literalinclude:: ../examples/shaders/04_log_polar.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`04_log_polar.frag をダウンロード <../examples/shaders/04_log_polar.frag>` ｜ `ブラウザーで実行 <demos/04_log_polar.html>`__

.. _example-05_lighting:

05_lighting.frag
--------------------

第 5 章：法線、拡散反射、鏡面反射、天空光、ガンマ補正

.. literalinclude:: ../examples/shaders/05_lighting.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`05_lighting.frag をダウンロード <../examples/shaders/05_lighting.frag>` ｜ `ブラウザーで実行 <demos/05_lighting.html>`__

.. _example-06_shadow:

06_shadow.frag
------------------

第 6 章：ハードシャドウとソフトシャドウ

.. literalinclude:: ../examples/shaders/06_shadow.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`06_shadow.frag をダウンロード <../examples/shaders/06_shadow.frag>` ｜ `ブラウザーで実行 <demos/06_shadow.html>`__

.. _example-06_ao:

06_ao.frag
--------------

第 6 章：アンビエントオクルージョン

.. literalinclude:: ../examples/shaders/06_ao.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`06_ao.frag をダウンロード <../examples/shaders/06_ao.frag>` ｜ `ブラウザーで実行 <demos/06_ao.html>`__

.. _example-07_camera:

07_camera.frag
------------------

第 7 章：カメラの操作、空、フォグ、トーンマッピング、アンチエイリアス

.. literalinclude:: ../examples/shaders/07_camera.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`07_camera.frag をダウンロード <../examples/shaders/07_camera.frag>` ｜ `ブラウザーで実行 <demos/07_camera.html>`__

.. _example-07_orthographic:

07_orthographic.frag
------------------------

第 7 章：平行投影によるアイソメトリック表示

.. literalinclude:: ../examples/shaders/07_orthographic.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`07_orthographic.frag をダウンロード <../examples/shaders/07_orthographic.frag>` ｜ `ブラウザーで実行 <demos/07_orthographic.html>`__

.. _example-07_color:

07_color.frag
-----------------

第 7 章：HSV、余弦関数によるパレット、色の補間

.. literalinclude:: ../examples/shaders/07_color.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`07_color.frag をダウンロード <../examples/shaders/07_color.frag>` ｜ `ブラウザーで実行 <demos/07_color.html>`__

.. _example-08_scene:

08_scene.frag
-----------------

第 8 章：完成したシーン

.. literalinclude:: ../examples/shaders/08_scene.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`08_scene.frag をダウンロード <../examples/shaders/08_scene.frag>` ｜ `ブラウザーで実行 <demos/08_scene.html>`__

.. _example-09_debug:

09_debug.frag
-----------------

第 9 章：デバッグ用の可視化

.. literalinclude:: ../examples/shaders/09_debug.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`09_debug.frag をダウンロード <../examples/shaders/09_debug.frag>` ｜ `ブラウザーで実行 <demos/09_debug.html>`__

.. _example-09_relaxation:

09_relaxation.frag
----------------------

第 9 章：過緩和によるスフィアトレーシングの高速化

.. literalinclude:: ../examples/shaders/09_relaxation.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`09_relaxation.frag をダウンロード <../examples/shaders/09_relaxation.frag>` ｜ `ブラウザーで実行 <demos/09_relaxation.html>`__

.. _example-10_noise2d:

10_noise2d.frag
-------------------

第 10 章：ハッシュとノイズの比較

.. literalinclude:: ../examples/shaders/10_noise2d.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_noise2d.frag をダウンロード <../examples/shaders/10_noise2d.frag>` ｜ `ブラウザーで実行 <demos/10_noise2d.html>`__

.. _example-10_cellular:

10_cellular.frag
--------------------

第 10 章：セルラーノイズとミンコフスキー距離

.. literalinclude:: ../examples/shaders/10_cellular.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_cellular.frag をダウンロード <../examples/shaders/10_cellular.frag>` ｜ `ブラウザーで実行 <demos/10_cellular.html>`__

.. _example-10_cracks:

10_cracks.frag
------------------

第 10 章：セルラーノイズによる石畳とひび割れた岩

.. literalinclude:: ../examples/shaders/10_cracks.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_cracks.frag をダウンロード <../examples/shaders/10_cracks.frag>` ｜ `ブラウザーで実行 <demos/10_cracks.html>`__

.. _example-10_curl:

10_curl.frag
----------------

第 10 章：勾配の場とカールノイズによる移流の比較

.. literalinclude:: ../examples/shaders/10_curl.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_curl.frag をダウンロード <../examples/shaders/10_curl.frag>` ｜ `ブラウザーで実行 <demos/10_curl.html>`__

.. _example-10_terrain:

10_terrain.frag
-------------------

第 10 章：fBm による地形

.. literalinclude:: ../examples/shaders/10_terrain.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_terrain.frag をダウンロード <../examples/shaders/10_terrain.frag>` ｜ `ブラウザーで実行 <demos/10_terrain.html>`__

.. _example-10_texture:

10_texture.frag
-------------------

第 10 章：トライプラナーマッピングとバンプマッピング

.. literalinclude:: ../examples/shaders/10_texture.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_texture.frag をダウンロード <../examples/shaders/10_texture.frag>` ｜ `ブラウザーで実行 <demos/10_texture.html>`__

.. _example-10_quadtree_pattern:

10_quadtree_pattern.frag
----------------------------

第 10 章：手続き的な四分木による模様

.. literalinclude:: ../examples/shaders/10_quadtree_pattern.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`10_quadtree_pattern.frag をダウンロード <../examples/shaders/10_quadtree_pattern.frag>` ｜ `ブラウザーで実行 <demos/10_quadtree_pattern.html>`__

.. _example-11_reflection_refraction:

11_reflection_refraction.frag
---------------------------------

第 11 章：反射と屈折

.. literalinclude:: ../examples/shaders/11_reflection_refraction.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`11_reflection_refraction.frag をダウンロード <../examples/shaders/11_reflection_refraction.frag>` ｜ `ブラウザーで実行 <demos/11_reflection_refraction.html>`__

.. _example-12_pbr:

12_pbr.frag
---------------

第 12 章：GGX、金属度と粗さによる材質

.. literalinclude:: ../examples/shaders/12_pbr.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`12_pbr.frag をダウンロード <../examples/shaders/12_pbr.frag>` ｜ `ブラウザーで実行 <demos/12_pbr.html>`__

.. _example-12_sss:

12_sss.frag
---------------

第 12 章：サブサーフェススキャッタリングの近似

.. literalinclude:: ../examples/shaders/12_sss.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`12_sss.frag をダウンロード <../examples/shaders/12_sss.frag>` ｜ `ブラウザーで実行 <demos/12_sss.html>`__

.. _example-13_menger:

13_menger.frag
------------------

第 13 章：メンガーのスポンジ

.. literalinclude:: ../examples/shaders/13_menger.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`13_menger.frag をダウンロード <../examples/shaders/13_menger.frag>` ｜ `ブラウザーで実行 <demos/13_menger.html>`__

.. _example-13_mandelbulb:

13_mandelbulb.frag
----------------------

第 13 章：マンデルバルブ

.. literalinclude:: ../examples/shaders/13_mandelbulb.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`13_mandelbulb.frag をダウンロード <../examples/shaders/13_mandelbulb.frag>` ｜ `ブラウザーで実行 <demos/13_mandelbulb.html>`__

.. _example-13_mandelbox:

13_mandelbox.frag
---------------------

第 13 章：マンデルボックス

.. literalinclude:: ../examples/shaders/13_mandelbox.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`13_mandelbox.frag をダウンロード <../examples/shaders/13_mandelbox.frag>` ｜ `ブラウザーで実行 <demos/13_mandelbox.html>`__

.. _example-13_kifs:

13_kifs.frag
----------------

第 13 章：折り返しによるフラクタル（KIFS）

.. literalinclude:: ../examples/shaders/13_kifs.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`13_kifs.frag をダウンロード <../examples/shaders/13_kifs.frag>` ｜ `ブラウザーで実行 <demos/13_kifs.html>`__

.. _example-14_slice:

14_slice.frag
-----------------

第 14 章：4 次元の超立方体の 3 次元の断面

.. literalinclude:: ../examples/shaders/14_slice.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`14_slice.frag をダウンロード <../examples/shaders/14_slice.frag>` ｜ `ブラウザーで実行 <demos/14_slice.html>`__

.. _example-14_stereographic:

14_stereographic.frag
-------------------------

第 14 章：クリフォードトーラスのステレオ投影

.. literalinclude:: ../examples/shaders/14_stereographic.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`14_stereographic.frag をダウンロード <../examples/shaders/14_stereographic.frag>` ｜ `ブラウザーで実行 <demos/14_stereographic.html>`__

.. _example-14_julia:

14_julia.frag
-----------------

第 14 章：四元数ジュリア集合

.. literalinclude:: ../examples/shaders/14_julia.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`14_julia.frag をダウンロード <../examples/shaders/14_julia.frag>` ｜ `ブラウザーで実行 <demos/14_julia.html>`__

.. _example-15_voxel:

15_voxel.frag
-----------------

第 15 章：3D DDA によるボクセルの描画

.. literalinclude:: ../examples/shaders/15_voxel.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_voxel.frag をダウンロード <../examples/shaders/15_voxel.frag>` ｜ `ブラウザーで実行 <demos/15_voxel.html>`__

.. _example-15_city:

15_city.frag
----------------

第 15 章：グリッドの走査とスフィアトレーシングの組み合わせ

.. literalinclude:: ../examples/shaders/15_city.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_city.frag をダウンロード <../examples/shaders/15_city.frag>` ｜ `ブラウザーで実行 <demos/15_city.html>`__

.. _example-15_tri_grid:

15_tri_grid.frag
--------------------

第 15 章：三角形の格子の走査

.. literalinclude:: ../examples/shaders/15_tri_grid.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_tri_grid.frag をダウンロード <../examples/shaders/15_tri_grid.frag>` ｜ `ブラウザーで実行 <demos/15_tri_grid.html>`__

.. _example-15_hex_columns:

15_hex_columns.frag
-----------------------

第 15 章：六角形の格子の走査

.. literalinclude:: ../examples/shaders/15_hex_columns.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_hex_columns.frag をダウンロード <../examples/shaders/15_hex_columns.frag>` ｜ `ブラウザーで実行 <demos/15_hex_columns.html>`__

.. _example-15_quadtree_city:

15_quadtree_city.frag
-------------------------

第 15 章：手続き的な四分木による街並み

.. literalinclude:: ../examples/shaders/15_quadtree_city.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_quadtree_city.frag をダウンロード <../examples/shaders/15_quadtree_city.frag>` ｜ `ブラウザーで実行 <demos/15_quadtree_city.html>`__

.. _example-15_octree:

15_octree.frag
------------------

第 15 章：手続き的な八分木と空の空間の飛ばし

.. literalinclude:: ../examples/shaders/15_octree.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`15_octree.frag をダウンロード <../examples/shaders/15_octree.frag>` ｜ `ブラウザーで実行 <demos/15_octree.html>`__

.. _example-16_volume:

16_volume.frag
------------------

第 16 章：ボリュームレンダリングによる雲

.. literalinclude:: ../examples/shaders/16_volume.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`16_volume.frag をダウンロード <../examples/shaders/16_volume.frag>` ｜ `ブラウザーで実行 <demos/16_volume.html>`__

.. _example-16_atmosphere:

16_atmosphere.frag
----------------------

第 16 章：大気の散乱

.. literalinclude:: ../examples/shaders/16_atmosphere.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`16_atmosphere.frag をダウンロード <../examples/shaders/16_atmosphere.frag>` ｜ `ブラウザーで実行 <demos/16_atmosphere.html>`__

.. _example-17_path_tracing:

17_path_tracing.frag
------------------------

第 17 章：パストレーシング

.. literalinclude:: ../examples/shaders/17_path_tracing.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`17_path_tracing.frag をダウンロード <../examples/shaders/17_path_tracing.frag>` ｜ `ブラウザーで実行 <demos/17_path_tracing.html>`__

.. _example-17_progressive:

17_progressive.frag
-----------------------

第 17 章：複数パスによる蓄積、被写界深度、モーションブラー

.. literalinclude:: ../examples/shaders/17_progressive.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`17_progressive.frag をダウンロード <../examples/shaders/17_progressive.frag>` ｜ `ブラウザーで実行 <demos/17_progressive.html>`__

.. _example-18_landscape:

18_landscape.frag
---------------------

第 18 章：夕暮れの風景（複数パス）

.. literalinclude:: ../examples/shaders/18_landscape.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`18_landscape.frag をダウンロード <../examples/shaders/18_landscape.frag>` ｜ `ブラウザーで実行 <demos/18_landscape.html>`__

.. _example-18_landscape_debug:

18_landscape_debug.frag
---------------------------

第 18 章：夕暮れの風景のデバッグ版

.. literalinclude:: ../examples/shaders/18_landscape_debug.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`18_landscape_debug.frag をダウンロード <../examples/shaders/18_landscape_debug.frag>` ｜ `ブラウザーで実行 <demos/18_landscape_debug.html>`__

.. _example-19_night_city:

19_night_city.frag
----------------------

第 19 章：ボクセルの都市の夜景

.. literalinclude:: ../examples/shaders/19_night_city.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`19_night_city.frag をダウンロード <../examples/shaders/19_night_city.frag>` ｜ `ブラウザーで実行 <demos/19_night_city.html>`__

.. _example-19_night_city_debug:

19_night_city_debug.frag
----------------------------

第 19 章：ボクセルの都市の夜景のデバッグ版

.. literalinclude:: ../examples/shaders/19_night_city_debug.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`19_night_city_debug.frag をダウンロード <../examples/shaders/19_night_city_debug.frag>` ｜ `ブラウザーで実行 <demos/19_night_city_debug.html>`__

.. _example-20_still_life:

20_still_life.frag
----------------------

第 20 章：パストレーシングによる静物画（複数パス）

.. literalinclude:: ../examples/shaders/20_still_life.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`20_still_life.frag をダウンロード <../examples/shaders/20_still_life.frag>` ｜ `ブラウザーで実行 <demos/20_still_life.html>`__

.. _example-20_still_life_debug:

20_still_life_debug.frag
----------------------------

第 20 章：パストレーシングによる静物画のデバッグ版

.. literalinclude:: ../examples/shaders/20_still_life_debug.frag
   :language: glsl
   :linenos:

.. rst-class:: example-links

:download:`20_still_life_debug.frag をダウンロード <../examples/shaders/20_still_life_debug.frag>` ｜ `ブラウザーで実行 <demos/20_still_life_debug.html>`__
