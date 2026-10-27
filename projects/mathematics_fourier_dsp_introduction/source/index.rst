フーリエ解析・デジタル信号処理入門
==================================================

音声、振動、電波、心電図、画像など、工学で扱う多くのデータは「信号」である。フーリエ解析は、信号を周波数の異なる正弦波の重ね合わせとして捉える数学であり、デジタル信号処理は、その考え方を計算機の上で実現する技術である。本書は、エンジニアと工学系の大学生を対象とした、フーリエ解析とデジタル信号処理の入門書である。

本書では、数式の厳密な証明よりも、式の意味と導出の流れを重視する。各章では「数式 → 図 → コード」の順に説明し、Python と NumPy、SciPy のサンプルコードで結果を確かめる。サンプルコードは本文から閲覧し、ダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: はじめに

   intro

.. toctree::
   :maxdepth: 2
   :caption: 第 I 部 連続時間のフーリエ解析

   ch01_signals
   ch02_fourier_series
   ch03_fourier_transform

.. toctree::
   :maxdepth: 2
   :caption: 第 II 部 離散時間の信号とシステム

   ch04_sampling
   ch05_lti_systems
   ch06_dtft_dft
   ch07_fft

.. toctree::
   :maxdepth: 2
   :caption: 第 III 部 実践

   ch08_spectrum_analysis
   ch09_digital_filters
   ch10_applications
   ch11_further_study

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_a_glossary
   appendix_b_symbols
   appendix_c_samples
   appendix_d_references
