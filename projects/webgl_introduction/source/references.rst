参考文献
========

仕様
----

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - `WebGL 2.0 Specification <https://registry.khronos.org/webgl/specs/latest/2.0/>`__\ （Khronos Group）
     - WebGL 2.0 の仕様。OpenGL ES 3.0 との差分として記述されています
   * - `OpenGL ES 3.0 Specification <https://registry.khronos.org/OpenGL/specs/es/3.0/es_spec_3.0.pdf>`__\ （Khronos Group）
     - WebGL 2.0 のもとになっている OpenGL ES 3.0 の仕様（PDF）
   * - `The OpenGL ES Shading Language 3.00 <https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf>`__\ （Khronos Group）
     - GLSL ES 3.00 の仕様（PDF）。組み込み関数や std140 レイアウトの規則も記載されています
   * - `WebGL Extension Registry <https://registry.khronos.org/webgl/extensions/>`__\ （Khronos Group）
     - WebGL の拡張機能の一覧と仕様
   * - `WebGPU <https://www.w3.org/TR/webgpu/>`__\ （W3C）
     - WebGPU の仕様

リファレンスと解説
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - `WebGL API <https://developer.mozilla.org/ja/docs/Web/API/WebGL_API>`__\ （MDN Web Docs）
     - WebGL の API リファレンスとチュートリアル
   * - `WebGL2RenderingContext <https://developer.mozilla.org/en-US/docs/Web/API/WebGL2RenderingContext>`__\ （MDN Web Docs）
     - WebGL 2.0 のコンテキストのメソッドと定数の一覧
   * - `WebGL best practices <https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices>`__\ （MDN Web Docs）
     - 性能と互換性のための推奨事項
   * - `WebGL2 Fundamentals <https://webgl2fundamentals.org/>`__
     - WebGL 2.0 の解説サイト。本書で扱わない技法（シャドウマッピングなど）も多数解説しています
   * - `LearnOpenGL <https://learnopengl.com/>`__
     - OpenGL の解説サイト。ライティング、ガンマ補正、PBR などの解説は WebGL にも応用できます
   * - `Can I use: WebGL 2.0 <https://caniuse.com/webgl2>`__
     - ブラウザーごとの WebGL 2.0 の対応状況

ツールとライブラリ
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 名前
     - 内容
   * - `Spector.js <https://spector.babylonjs.com/>`__
     - WebGL の関数呼び出しを記録して調べるデバッグツール（\ :numref:`chap-debug`\ ）
   * - `three.js <https://threejs.org/>`__
     - WebGL を使った代表的な 3D ライブラリ
   * - `Babylon.js <https://www.babylonjs.com/>`__
     - WebGL と WebGPU に対応した 3D エンジン
   * - `glTF <https://www.khronos.org/gltf/>`__\ （Khronos Group）
     - 3D モデルのファイル形式
   * - `Pillow <https://pillow.readthedocs.io/en/stable/>`__
     - 本書の ``gen_texture.py`` で使っている Python の画像処理ライブラリ
