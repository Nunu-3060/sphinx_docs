##################################################
付録 B 参考文献
##################################################

GLSL と実行環境
===============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - Khronos Group, `The OpenGL ES Shading Language, Version 3.00 <https://registry.khronos.org/OpenGL/specs/es/3.0/GLSL_ES_Specification_3.00.pdf>`_
     - 本資料のサンプルが準拠する GLSL ES 3.00 の仕様書
   * - Khronos Group, `OpenGL ES 3 Reference Pages <https://registry.khronos.org/OpenGL-Refpages/es3/>`_
     - GLSL の組み込み関数のリファレンス
   * - `Shadertoy <https://www.shadertoy.com/>`_
     - ブラウザーでシェーダーを作成・共有できるサイト。本資料のサンプルと同じ形式でシェーダーを書ける。
   * - `WebGL2 Fundamentals <https://webgl2fundamentals.org/>`_
     - WebGL2 の解説。付属のビューアーの仕組みを理解するのに役立つ。
   * - P. G. Vivo, J. Lowe, `The Book of Shaders <https://thebookofshaders.com/>`_
     - フラグメントシェーダーによる 2 次元の描画の入門書。ノイズなどの解説が詳しい。

レイマーチングと SDF
====================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - J. C. Hart, "Sphere tracing: a geometric method for the antialiased ray tracing of implicit surfaces," The Visual Computer, 12(10), pp. 527--545, 1996. `doi:10.1007/s003710050084 <https://doi.org/10.1007/s003710050084>`_
     - スフィアトレーシングの原論文。リプシッツ連続な関数による形状の表現と、その交差判定を扱う。
   * - I. Quilez, `Distance functions <https://iquilezles.org/articles/distfunctions/>`_
     - 3 次元の基本形状の SDF と、合成・変形の操作の一覧
   * - I. Quilez, `2D distance functions <https://iquilezles.org/articles/distfunctions2d/>`_
     - 2 次元の基本形状の SDF の一覧
   * - I. Quilez, `Smooth minimum <https://iquilezles.org/articles/smin/>`_
     - smooth min の各種の式とその性質
   * - I. Quilez, `Normals for an SDF <https://iquilezles.org/articles/normalsSDF/>`_
     - 中心差分と四面体による法線の推定
   * - I. Quilez, `Soft shadows in raymarched SDFs <https://iquilezles.org/articles/rmshadows/>`_
     - ソフトシャドウの近似とその改良
   * - B. Keinert, H. Schäfer, J. Korndörfer, U. Ganse, M. Stamminger, "Enhanced Sphere Tracing," Smart Tools and Apps for Graphics, 2014. `doi:10.2312/stag.20141233 <https://doi.org/10.2312/stag.20141233>`_
     - 第 9 章で扱った過緩和などによるスフィアトレーシングの改良
   * - J. Amanatides, A. Woo, "A fast voxel traversal algorithm for ray tracing," Eurographics '87, pp. 3--10, 1987.
     - 第 15 章で扱った 3D DDA の原論文
   * - A. Patel, `Hexagonal Grids <https://www.redblobgames.com/grids/hexagons/>`_, Red Blob Games.
     - 六角形の格子の座標系、隣接するセル、距離などの詳しい解説
   * - S. Laine, T. Karras, `Efficient Sparse Voxel Octrees <https://research.nvidia.com/publication/2010-02_efficient-sparse-voxel-octrees>`_, ACM SIGGRAPH Symposium on Interactive 3D Graphics and Games, 2010.
     - 第 15 章で紹介したスパースボクセル八分木の構造と、その効率的な走査

ハッシュとノイズ
================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - K. Perlin, "An image synthesizer," Proceedings of SIGGRAPH '85, pp. 287--296, 1985.
     - 勾配ノイズ（Perlin ノイズ）の原論文
   * - K. Perlin, "Improving noise," ACM Transactions on Graphics, 21(3), pp. 681--682, 2002.
     - 5 次の補間などによる Perlin ノイズの改良
   * - M. Jarzynski, M. Olano, `Hash Functions for GPU Rendering <https://jcgt.org/published/0009/03/02/>`_, Journal of Computer Graphics Techniques, 9(3), 2020.
     - 第 10 章で使った PCG ハッシュを含む、GPU 向けのハッシュ関数の比較
   * - I. Quilez, `Gradient noise derivatives <https://iquilezles.org/articles/gradientnoise/>`_
     - 勾配ノイズとその微分の計算
   * - I. Quilez, `fBm <https://iquilezles.org/articles/fbm/>`_
     - fBm のパラメーターと、自然物の形状との関係
   * - I. Quilez, `Domain warping <https://iquilezles.org/articles/warp/>`_
     - ドメインワーピングの手法と作例
   * - I. Quilez, `Terrain raymarching <https://iquilezles.org/articles/terrainmarching/>`_
     - 高さの関数で表した地形のレイマーチング
   * - P. G. Vivo, J. Lowe, `The Book of Shaders: Noise <https://thebookofshaders.com/11/>`_
     - ノイズの考え方を図とともに解説した入門
   * - I. Quilez, `Biplanar mapping <https://iquilezles.org/articles/biplanar/>`_
     - トライプラナーマッピングと、2 つの平面だけを使う軽量な方法
   * - K. Perlin, "Noise hardware," Real-Time Shading, SIGGRAPH 2001 Course Notes, 2001.
     - シンプレックスノイズの原典
   * - S. Gustavson, "Simplex noise demystified," Linköping University, 2005.
     - シンプレックスノイズの仕組みと実装の解説
   * - I. Quilez, `Value noise derivatives <https://iquilezles.org/articles/morenoise/>`_
     - ノイズの解析的な微分と、それを使った地形の表現
   * - S. Worley, "A cellular texture basis function," Proceedings of SIGGRAPH '96, pp. 291--294, 1996.
     - セルラーノイズ（Worley ノイズ）の原論文
   * - I. Quilez, `Voronoi edges <https://iquilezles.org/articles/voronoilines/>`_
     - 第 10 章で使ったボロノイの境界までの正確な距離の計算
   * - P. G. Vivo, J. Lowe, `The Book of Shaders: Cellular Noise <https://thebookofshaders.com/12/>`_
     - セルラーノイズの考え方を図とともに解説した入門
   * - R. Bridson, J. Houriham, M. Nordenstam, `Curl-noise for procedural fluid flow <https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf>`_, ACM Transactions on Graphics, 26(3), 2007.
     - カールノイズの原論文
   * - C. Peters, `Free blue noise textures <https://momentsingraphics.de/BlueNoise.html>`_
     - 第 16 章で紹介したブルーノイズのテクスチャと、その性質の解説

照明と色
========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - K. Narkowicz, `ACES Filmic Tone Mapping Curve <https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/>`_
     - 第 7 章で使ったトーンマッピングの近似式
   * - I. Quilez, `Palettes <https://iquilezles.org/articles/palettes/>`_
     - 第 7 章で使った余弦関数によるパレット
   * - B. Ottosson, `A perceptual color space for image processing <https://bottosson.github.io/posts/oklab/>`_, 2020.
     - 第 7 章で使った Oklab 色空間の定義と変換式
   * - B. Walter, S. R. Marschner, H. Li, K. E. Torrance, "Microfacet models for refraction through rough surfaces," Eurographics Symposium on Rendering, 2007.
     - GGX 分布の原論文
   * - B. Karis, `Real Shading in Unreal Engine 4 <https://blog.selfshadow.com/publications/s2013-shading-course/>`_, SIGGRAPH 2013 Course: Physically Based Shading in Theory and Practice.
     - 第 12 章で使った金属度と粗さによる材質の指定、幾何減衰項の近似、split-sum 近似

フラクタル
==========

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - I. Quilez, `Menger fractal <https://iquilezles.org/articles/menger/>`_
     - メンガーのスポンジの SDF
   * - I. Quilez, `Mandelbulb <https://iquilezles.org/articles/mandelbulb/>`_
     - マンデルバルブの距離推定関数と描画
   * - D. White, `The Unravelling of the Real 3D Mandelbulb <https://www.skytopia.com/project/fractal/mandelbulb.html>`_
     - マンデルバルブの考案の経緯
   * - I. Quilez, `3D Julia sets <https://iquilezles.org/articles/juliasets3d/>`_
     - 第 14 章で扱った四元数ジュリア集合の距離推定関数
   * - T. Lowe, `What is a Mandelbox? <https://sites.google.com/site/mandelbox/what-is-a-mandelbox>`_
     - マンデルボックスの考案者による解説

4 次元の形状
============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - N. Johnson, `Hopf Fibration Video <https://nilesjohnson.net/hopf.html>`_
     - ホップファイバーとステレオ投影の解説と映像

パストレーシングとボリュームレンダリング
========================================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 文献
     - 内容
   * - M. Pharr, W. Jakob, G. Humphreys, `Physically Based Rendering: From Theory to Implementation <https://pbr-book.org/>`_
     - 物理ベースレンダリングの教科書。レンダリング方程式、モンテカルロ積分、関与媒質などを詳しく扱う。オンラインで無料で公開されている。
   * - J. T. Kajiya, "The rendering equation," Proceedings of SIGGRAPH '86, pp. 143--150, 1986.
     - レンダリング方程式とパストレーシングの原論文
   * - M. Pharr, W. Jakob, G. Humphreys, `Projective Camera Models <https://www.pbr-book.org/4ed/Cameras_and_Film/Projective_Camera_Models>`_, Physically Based Rendering, 4th ed.
     - 第 17 章で扱った薄レンズモデルによる被写界深度
   * - T. Nishita, T. Sirai, K. Tadamura, E. Nakamae, "Display of the Earth taking into account atmospheric scattering," Proceedings of SIGGRAPH '93, pp. 175--182, 1993.
     - 第 16 章で扱った大気の単一散乱のモデル
   * - E. Bruneton, F. Neyret, "Precomputed atmospheric scattering," Computer Graphics Forum, 27(4), pp. 1079--1086, 2008.
     - 多重散乱を含む大気の散乱をあらかじめ計算しておく方法
