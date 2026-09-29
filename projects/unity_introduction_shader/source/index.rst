Unity シェーダー・グラフィックス入門
==================================

本資料は、Unity と C# の基本操作を身に付けた人が、シェーダーを自分で書けるようになるための入門資料である。コンピューターグラフィックスの数学と GPU の描画のしくみを学んだうえで、Unity 6 の Universal Render Pipeline（URP）向けのシェーダーを ShaderLab と HLSL で書く。後半では、ポストエフェクトと Shader Graph も扱う。

サンプルコードは、各章の本文から閲覧・ダウンロードできる。すべてのサンプルをまとめた zip ファイルは、:download:`こちら <_generated/unity_introduction_shader_examples.zip>` からダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: 第 1 部 導入と理論

   chapters/ch01_introduction
   chapters/ch02_cg_math
   chapters/ch03_coordinate_transform
   chapters/ch04_rendering_pipeline
   chapters/ch05_unity_rendering

.. toctree::
   :maxdepth: 2
   :caption: 第 2 部 シェーダーの基本

   chapters/ch06_shaderlab_hlsl
   chapters/ch07_first_shader
   chapters/ch08_texture_uv

.. toctree::
   :maxdepth: 2
   :caption: 第 3 部 ライティング

   chapters/ch09_lighting
   chapters/ch10_normal_map
   chapters/ch11_shadow

.. toctree::
   :maxdepth: 2
   :caption: 第 4 部 表現の幅を広げる

   chapters/ch12_transparency
   chapters/ch13_vertex_animation
   chapters/ch14_effects
   chapters/ch15_post_effect
   chapters/ch16_shader_graph
   chapters/ch17_debug_optimize

.. toctree::
   :maxdepth: 2
   :caption: 付録

   appendix/glossary
   appendix/formulas
   appendix/references
