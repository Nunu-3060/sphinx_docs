参考文献
========

本資料の作成にあたって参考にした文献と、さらに学ぶための資料を挙げる。

規格と指針
----------

* IEC 61966-2-1:1999, Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB.

  sRGB の色空間とガンマ補正の式を定めた国際規格である。

* W3C, `Web Content Accessibility Guidelines (WCAG) 2.2 <https://www.w3.org/TR/WCAG22/>`_.

  コントラスト比（達成基準 1.4.3、1.4.6、1.4.11）と色の使用（達成基準 1.4.1）の基準を定めている。

* International Color Consortium, `ICC <https://www.color.org/>`_.

  ICC プロファイルの仕様を定めている団体のサイトである。カラーマネジメントの解説もある。

* W3C, `CSS Color Module Level 4 <https://www.w3.org/TR/css-color-4/>`_.

  CSS で ``oklab()``、``oklch()``、``lab()`` などの色の指定方法を定めている。色空間の変換式と、色域への収め方の考え方も記されている。

色空間
------

* Björn Ottosson, `A perceptual color space for image processing <https://bottosson.github.io/posts/oklab/>`_, 2020.

  OKLab を提案した記事である。変換の行列と、設計の考え方が記されている。

データ可視化の配色
------------------

* Matplotlib, `Choosing Colormaps in Matplotlib <https://matplotlib.org/stable/users/explain/colors/colormaps.html>`_.

  カラーマップの種類と、明度の変化にもとづくカラーマップの比較が記されている。

* David Borland, Russell M. Taylor II, Rainbow Color Map (Still) Considered Harmful, IEEE Computer Graphics and Applications, 27(2), pp. 14-17, 2007. `doi:10.1109/MCG.2007.323435 <https://doi.org/10.1109/MCG.2007.323435>`_

  虹色のカラーマップの問題点を論じた論文である。

* Fabio Crameri, Grace E. Shephard, Philip J. Heron, The misuse of colour in science communication, Nature Communications, 11, 5444, 2020. `doi:10.1038/s41467-020-19160-7 <https://doi.org/10.1038/s41467-020-19160-7>`_

  科学的なデータの可視化で色が誤って使われる例と、知覚的に均等なカラーマップの必要性を論じた論文である。

色覚の多様性
------------

* Gustavo M. Machado, Manuel M. Oliveira, Leandro A. F. Fernandes, A Physiologically-based Model for Simulation of Color Vision Deficiency, IEEE Transactions on Visualization and Computer Graphics, 15(6), pp. 1291-1298, 2009. `doi:10.1109/TVCG.2009.113 <https://doi.org/10.1109/TVCG.2009.113>`_

  :doc:`accessibility`\ で使った、色覚の多様性の見え方をシミュレーションする行列を提案した論文である。

* Masataka Okabe, Kei Ito, `Color Universal Design (CUD) - How to make figures and presentations that are friendly to Colorblind people <https://jfly.uni-koeln.de/color/>`_.

  色覚の多様性に配慮した図の作り方と、:doc:`dataviz`\ で使った 8 色の配色を提案している。
