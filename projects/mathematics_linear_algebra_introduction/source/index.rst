線形代数入門
============

線形代数は、ベクトルと行列を使って「線形」な関係を扱う数学である。3D グラフィックスの座標変換、機械学習のデータ処理、回路や構造物の解析、制御、信号処理など、工学のほとんどの分野で使われている。本書は、エンジニアと工学系の大学生を対象とした線形代数の入門書である。

本書では、抽象的な定義から入るのではなく、2 次元と 3 次元の図で直観をつかんでから一般化する。また、「行列は空間を変形する写像である」という見方を全体の軸にして、行列の積、行列式、固有値、特異値分解を説明する。計算の例は Python と NumPy のサンプルコードで示しており、本文からコードを閲覧し、ダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: はじめに

   ch01_introduction

.. toctree::
   :maxdepth: 2
   :caption: 第 I 部 ベクトルと行列

   ch02_vectors
   ch03_matrices
   ch04_linear_maps
   ch05_linear_equations
   ch06_inverse_determinant

.. toctree::
   :maxdepth: 2
   :caption: 第 II 部 ベクトル空間

   ch07_vector_spaces
   ch08_rank_subspaces
   ch09_orthogonality

.. toctree::
   :maxdepth: 2
   :caption: 第 III 部 固有値と行列の分解

   ch10_eigenvalues
   ch11_symmetric
   ch12_svd

.. toctree::
   :maxdepth: 2
   :caption: 第 IV 部 実践

   ch13_numerical
   ch14_applications
   ch15_conclusion

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_a_symbols
   appendix_b_glossary
   appendix_c_references
   appendix_d_samples
