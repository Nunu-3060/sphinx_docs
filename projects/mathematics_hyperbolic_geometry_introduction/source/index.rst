双曲幾何学入門
==============

「直線の外の 1 点を通り、その直線と交わらない直線はちょうど 1 本ある」という平行線の性質は、学校で学ぶユークリッド幾何学の前提の 1 つである。この前提を「無数にある」に置き換えても、矛盾のない幾何学が成り立つ。それが双曲幾何学である。双曲幾何学は 19 世紀に数学の問題として生まれたが、現在では特殊相対論、機械学習（階層構造を持つデータの埋め込み）、複雑ネットワーク、情報可視化、マイクロ波回路のスミスチャートなど、工学の多くの場面に現れる。

本書は、エンジニアと工学系の大学生を対象とした、双曲幾何学の入門書である。公理から定理を導く代わりに、双曲平面を座標と計量を持つ具体的な「モデル」として扱い、距離、角度、面積を計算しながら性質を確かめる。計算例と図は Python（NumPy、matplotlib）で示しており、本文からサンプルコードを閲覧し、ダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: はじめに

   ch00_introduction

.. toctree::
   :maxdepth: 2
   :caption: 第 I 部 双曲幾何学への入口

   ch01_history
   ch02_curvature

.. toctree::
   :maxdepth: 2
   :caption: 第 II 部 モデルと計量

   ch03_models
   ch04_distance
   ch05_isometries

.. toctree::
   :maxdepth: 2
   :caption: 第 III 部 双曲平面の図形

   ch06_trigonometry
   ch07_circles
   ch08_tiling

.. toctree::
   :maxdepth: 2
   :caption: 第 IV 部 応用と計算

   ch09_applications
   ch10_python

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_a_hyperbolic_functions
   appendix_b_mobius
   appendix_c_glossary
   appendix_d_references
   appendix_e_samples
