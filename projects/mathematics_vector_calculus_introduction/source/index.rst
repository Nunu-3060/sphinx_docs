ベクトル解析入門
================

温度や圧力のように空間の各点に数が決まっているもの、風や電場のように空間の各点に矢印が決まっているものを「場」という。ベクトル解析は、場を微分・積分するための数学であり、電磁気学、流体力学、熱伝導、コンピューターグラフィックス（CG）など、工学の多くの分野で使われている。

本書は、エンジニアと工学系の大学生を対象とした、ベクトル解析の入門書である。勾配・発散・回転という 3 つの微分と、グリーン・ガウス・ストークスの積分定理を中心に、図と数値計算で意味を確かめながら説明する。計算例は Python（NumPy、SciPy、SymPy、matplotlib）で示しており、本文からサンプルコードを閲覧し、ダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: はじめに

   ch01_introduction

.. toctree::
   :maxdepth: 2
   :caption: 第 I 部 準備

   ch02_vectors
   ch03_curves
   ch04_fields

.. toctree::
   :maxdepth: 2
   :caption: 第 II 部 場の微分

   ch05_gradient
   ch06_divergence
   ch07_rotation
   ch08_nabla_identities
   ch09_curvilinear

.. toctree::
   :maxdepth: 2
   :caption: 第 III 部 場の積分

   ch10_multiple_integrals
   ch11_line_integrals
   ch12_surface_integrals

.. toctree::
   :maxdepth: 2
   :caption: 第 IV 部 積分定理

   ch13_green
   ch14_gauss
   ch15_stokes
   ch16_potential

.. toctree::
   :maxdepth: 2
   :caption: 第 V 部 応用

   ch17_physics
   ch18_cg_numerical
   ch19_conclusion

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_a_formulas
   appendix_b_index_notation
   appendix_c_glossary
   appendix_d_references
   appendix_e_samples
