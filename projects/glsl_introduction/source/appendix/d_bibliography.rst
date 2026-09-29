付録 D 参考資料
===============

仕様書
------

* `The OpenGL ES Shading Language, Version 3.00 <https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf>`_\ （Khronos Group）

  GLSL ES 3.00 の仕様書です。組み込み関数の正確な定義や、未定義の動作などを調べるときに参照します。

* `OpenGL ES 3.0 Reference Pages <https://registry.khronos.org/OpenGL-Refpages/es3.0/>`_\ （Khronos Group）

  OpenGL ES 3.0 の API と、GLSL ES 3.00 の組み込み関数のリファレンスです。

* `WebGL 2.0 Specification <https://registry.khronos.org/webgl/specs/latest/2.0/>`_\ （Khronos Group）

  WebGL 2.0 の仕様書です。OpenGL ES 3.0 との違いが記載されています。

論文
----

第 12 章で扱った、ハッシュ関数とノイズに関する論文です。

* George Marsaglia, `Xorshift RNGs <https://www.jstatsoft.org/article/view/v008i14>`_, Journal of Statistical Software, Vol. 8, No. 14, 2003.

  Xorshift による擬似乱数の生成方法を発表した論文です。

* Melissa E. O'Neill, `PCG: A Family of Better Random Number Generators <https://www.pcg-random.org/>`_, 2014.

  PCG の考案者によるサイトです。PCG の解説と論文が公開されています。

* Mark Jarzynski, Marc Olano, `Hash Functions for GPU Rendering <https://jcgt.org/published/0009/03/02/>`_, Journal of Computer Graphics Techniques, Vol. 9, No. 3, 2020.

  GPU で使われるさまざまなハッシュ関数の品質と速さを比較した論文です。第 12 章の ``pcg`` 関数は、この論文に掲載されているものです。

* Ken Perlin, `Improving Noise <https://mrl.cs.nyu.edu/~perlin/paper445.pdf>`_, SIGGRAPH 2002.

  パーリンノイズの改良版（5 次の補間曲線など）を発表した論文です。

Web 上の解説
------------

* `WebGL API <https://developer.mozilla.org/ja/docs/Web/API/WebGL_API>`_\ （MDN Web Docs）

  WebGL の API のリファレンスとチュートリアルです。

* `WebGL2 Fundamentals <https://webgl2fundamentals.org/webgl/lessons/ja/>`_

  WebGL 2.0 の基礎から応用までを、順を追って解説したサイトです。

* `The Book of Shaders <https://thebookofshaders.com/?lan=jp>`_

  フラグメントシェーダーによる図形、模様、ノイズの描き方を、ブラウザー上で試しながら学べるサイトです。

* `Inigo Quilez - articles <https://iquilezles.org/articles/>`_

  距離関数、なめらかな合成（``smoothMin``）、ソフトシャドウ、ドメインワーピングなど、本書の第 8 章、第 12 章、第 14 章で扱った手法の解説があります。特に、2 次元と 3 次元の距離関数の一覧は、図形を追加するときに役立ちます。

  * `2D distance functions <https://iquilezles.org/articles/distfunctions2d/>`_
  * `3D distance functions <https://iquilezles.org/articles/distfunctions/>`_

ツール
------

* `Spector.js <https://spector.babylonjs.com/>`_

  WebGL の描画命令や、テクスチャ、シェーダーの状態を 1 フレーム単位で調べられるツールです。ブラウザーの拡張機能として利用できます（第 15 章）。

* `Shadertoy <https://www.shadertoy.com/>`_

  フラグメントシェーダーを書いて公開できるサイトです。多くの作品のソースコードを読むことができます。レイマーチングやノイズを使った作品が多数あります。
