サンプルコード一覧
==================

本書のサンプルコードの一覧です。「開く」のリンクでブラウザーで実行し、「ダウンロード」のリンクでファイルを個別にダウンロードできます。

一括ダウンロード
----------------

すべてのサンプルと補助スクリプト、テクスチャ画像を 1 つにまとめた zip ファイルを用意しています。

* `webgl_introduction_examples.zip をダウンロード <webgl_introduction_examples.zip>`__

zip ファイルを展開すると ``examples`` フォルダーができます。テクスチャを使うサンプル（10 と 17）を動かすには、\ ``examples`` フォルダーで ``python serve.py`` を実行し、\ ``http://localhost:8000/`` を開いてください。

HTML のサンプル
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 34 12 12 12

   * - ファイル
     - 内容
     - 章
     - 開く
     - ダウンロード
   * - ``01_check_support.html``
     - WebGL 2.0 への対応と実装の情報を表示します
     - :numref:`chap-setup`
     - `開く <examples/01_check_support.html>`__
     - :download:`ダウンロード <../examples/01_check_support.html>`
   * - ``02_clear.html``
     - 画面のクリアと描画ループ
     - :numref:`chap-first-drawing`
     - `開く <examples/02_clear.html>`__
     - :download:`ダウンロード <../examples/02_clear.html>`
   * - ``03_triangle.html``
     - シェーダーを使って三角形を描画します
     - :numref:`chap-shader`
     - `開く <examples/03_triangle.html>`__
     - :download:`ダウンロード <../examples/03_triangle.html>`
   * - ``04_vertex_color.html``
     - 頂点カラーとインターリーブ配置
     - :numref:`chap-buffer`
     - `開く <examples/04_vertex_color.html>`__
     - :download:`ダウンロード <../examples/04_vertex_color.html>`
   * - ``05_index_buffer.html``
     - インデックスバッファーと描画モード
     - :numref:`chap-buffer`
     - `開く <examples/05_index_buffer.html>`__
     - :download:`ダウンロード <../examples/05_index_buffer.html>`
   * - ``06_matrix_test.html``
     - ベクトルと行列の関数のテスト（WebGL は使わない）
     - :numref:`chap-math`
     - `開く <examples/06_matrix_test.html>`__
     - :download:`ダウンロード <../examples/06_matrix_test.html>`
   * - ``07_transform.html``
     - 平行移動・回転・拡大縮小と、変換の順序
     - :numref:`chap-transform`
     - `開く <examples/07_transform.html>`__
     - :download:`ダウンロード <../examples/07_transform.html>`
   * - ``08_rotating_cube.html``
     - 回転する立方体（透視投影と正射影）
     - :numref:`chap-transform`
     - `開く <examples/08_rotating_cube.html>`__
     - :download:`ダウンロード <../examples/08_rotating_cube.html>`
   * - ``09_depth_test.html``
     - 深度テストと背面カリング
     - :numref:`chap-depth`
     - `開く <examples/09_depth_test.html>`__
     - :download:`ダウンロード <../examples/09_depth_test.html>`
   * - ``10_texture.html``
     - テクスチャのフィルタリング、ラッピング、複数テクスチャ（画像を使用）
     - :numref:`chap-texture`
     - `開く <examples/10_texture.html>`__
     - :download:`ダウンロード <../examples/10_texture.html>`
   * - ``11_lighting.html``
     - 環境光・拡散反射・鏡面反射、平行光源と点光源
     - :numref:`chap-lighting`
     - `開く <examples/11_lighting.html>`__
     - :download:`ダウンロード <../examples/11_lighting.html>`
   * - ``12_camera_control.html``
     - マウスとキーボードによるカメラ操作、canvas のリサイズ
     - :numref:`chap-interaction`
     - `開く <examples/12_camera_control.html>`__
     - :download:`ダウンロード <../examples/12_camera_control.html>`
   * - ``13_blend.html``
     - ブレンドと半透明
     - :numref:`chap-advanced`
     - `開く <examples/13_blend.html>`__
     - :download:`ダウンロード <../examples/13_blend.html>`
   * - ``14_framebuffer.html``
     - フレームバッファーとポストエフェクト
     - :numref:`chap-advanced`
     - `開く <examples/14_framebuffer.html>`__
     - :download:`ダウンロード <../examples/14_framebuffer.html>`
   * - ``15_instancing.html``
     - インスタンス描画
     - :numref:`chap-advanced`
     - `開く <examples/15_instancing.html>`__
     - :download:`ダウンロード <../examples/15_instancing.html>`
   * - ``16_ubo.html``
     - Uniform Buffer Object
     - :numref:`chap-advanced`
     - `開く <examples/16_ubo.html>`__
     - :download:`ダウンロード <../examples/16_ubo.html>`
   * - ``17_scene.html``
     - 総合演習（画像を使用）
     - :numref:`chap-scene`
     - `開く <examples/17_scene.html>`__
     - :download:`ダウンロード <../examples/17_scene.html>`

Python のスクリプトと画像
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 46 12 12

   * - ファイル
     - 内容
     - 章
     - ダウンロード
   * - ``serve.py``
     - サンプルを閲覧するためのローカル HTTP サーバー
     - :numref:`chap-setup`
     - :download:`ダウンロード <../examples/serve.py>`
   * - ``gen_vertices.py``
     - 立方体と球の頂点データを JavaScript のコードとして出力します
     - :numref:`chap-buffer`
     - :download:`ダウンロード <../examples/gen_vertices.py>`
   * - ``gen_texture.py``
     - テクスチャ画像を生成します（Pillow が必要）
     - :numref:`chap-texture`
     - :download:`ダウンロード <../examples/gen_texture.py>`
   * - ``assets/checker.png``
     - 市松模様のテクスチャ
     - :numref:`chap-texture`
     - :download:`ダウンロード <../examples/assets/checker.png>`
   * - ``assets/uvgrid.png``
     - UV グリッドのテクスチャ
     - :numref:`chap-texture`
     - :download:`ダウンロード <../examples/assets/uvgrid.png>`

Python のスクリプトは Python 3.10 以降で動作します。いずれも型ヒントを記述しており、flake8 と mypy（\ ``--strict``\ ）で警告が出ないことを確認しています。
