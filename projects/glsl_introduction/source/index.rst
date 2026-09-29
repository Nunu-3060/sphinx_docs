GLSL 入門
=========

本書は、GPU で動作するプログラム「シェーダー」を記述するための言語 GLSL（OpenGL Shading Language）の入門資料です。WebGL 2.0 を実行環境とし、ブラウザーだけで動作するサンプルを動かしながら、GLSL の文法、座標変換、テクスチャ、ライティングから、アニメーション、ノイズ、ポストエフェクト、レイマーチングまでを順に解説します。

.. toctree::
   :maxdepth: 2
   :caption: 導入

   chapters/01_introduction
   chapters/02_gpu_and_shader
   chapters/03_setup

.. toctree::
   :maxdepth: 2
   :caption: GLSL の基礎

   chapters/04_syntax
   chapters/05_builtin_functions
   chapters/06_data_flow

.. toctree::
   :maxdepth: 2
   :caption: 描画の基本

   chapters/07_vertex_shader
   chapters/08_fragment_shader
   chapters/09_texture
   chapters/10_lighting

.. toctree::
   :maxdepth: 2
   :caption: 応用

   chapters/11_animation
   chapters/12_noise
   chapters/13_post_effect
   chapters/14_raymarching

.. toctree::
   :maxdepth: 2
   :caption: 開発の実践

   chapters/15_debug_performance

.. toctree::
   :maxdepth: 2
   :caption: 付録

   appendix/a_reference
   appendix/b_versions
   appendix/c_glossary
   appendix/d_bibliography
