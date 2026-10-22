参考資料
========

書籍
----

* `Daniel Shiffman, The Nature of Code <https://natureofcode.com/>`_ — 乱数、ベクトル、力学、パーティクルシステム、群れ行動（Boids）、セルオートマトン、フラクタル、進化的アルゴリズムなどを扱う定番書。原著は Processing/JavaScript 向けだが、アルゴリズム自体はそのまま Python + NumPy に移植できる。全文が無料で公開されている。
* Matt Pearson, *Generative Art: A Practical Guide Using Processing*, Manning Publications, 2011. — ジェネラティブアートの考え方と、具体的な作品例（対称性、フラクタル、粒子系、タイリングなど）を Processing のコードとともに解説する書籍。
* H.S.M. Coxeter, *Introduction to Geometry*, 2nd ed., Wiley, 1969. — 万華鏡・壁紙群・双曲タイリングなど、鏡映によって生成される対称性を統一的に扱うコクセター群の基礎を解説する古典的教科書。
* Tommaso Toffoli, Norman Margolus, *Cellular Automata Machines: A New Environment for Modeling*, MIT Press, 1987. — Brian's Brain を含む、ライフゲーム以外の多様なセルオートマトンとその実装手法を扱う古典。
* Robert Penner, *Robert Penner's Programming Macromedia Flash MX*, McGraw-Hill/Osborne, 2002. — 本資料の\ :ref:`easing`\ で扱ったイージング関数を体系的に整理し、ease-in / ease-out / ease-in-out という呼び名を広めた書籍。

論文
----

* `Ken Perlin, "Improving Noise" <https://mrl.cs.nyu.edu/~perlin/paper445.pdf>`_, ACM Transactions on Graphics 21(3), 2002. — 本資料の自前パーリンノイズ実装が採用している改良版アルゴリズム（fade 関数によるバイリニア補間）の原論文。
* Craig W. Reynolds, "Flocks, Herds, and Schools: A Distributed Behavioral Model", Computer Graphics 21(4) (SIGGRAPH '87), 1987. — 本資料の\ :doc:`particles`\ で扱った Boids モデルの原論文。
* Jon Louis Bentley, "Multidimensional Binary Search Trees Used for Associative Searching", Communications of the ACM 18(9), 1975. — 本資料の\ :ref:`neighbor-search`\ で触れた k-d 木の原論文。
* Josh Barnes, Piet Hut, "A Hierarchical O(N log N) Force-Calculation Algorithm", Nature 324, 1986. — 本資料の\ :ref:`neighbor-search`\ で触れた、四分木（3 次元では八分木）で遠くの粒子の集まりを近似する Barnes-Hut 法の原論文。
* Robert Bridson, "Fast Poisson Disk Sampling in Arbitrary Dimensions", SIGGRAPH 2007 Sketches, 2007. — 本資料の\ :doc:`shapes`\ で扱ったポアソン円盤サンプリングのアルゴリズムの原論文。
* Johan Gielis, "A Generic Geometric Transformation that Unifies a Wide Range of Natural and Abstract Shapes", American Journal of Botany 90(3), 2003. — 本資料の\ :doc:`spirals`\ で扱ったスーパーフォーミュラの原論文。
* O. Biham, A.A. Middleton, D. Levine, "Self-organization and a dynamical transition in traffic-flow models", Physical Review A 46(10), 1992. — 本資料の\ :doc:`automata`\ で扱った BML 交通モデルの原論文。密度によって流れが渋滞へ相転移する現象を報告している。
* Stuart P. Lloyd, "Least Squares Quantization in PCM", IEEE Transactions on Information Theory 28(2), 1982. — 本資料の\ :ref:`lloyd`\ で扱ったロイド緩和の原論文。1957 年に社内報告としてまとめられた内容を論文として発表したもの。
* Steven Worley, "A Cellular Texture Basis Function", Proceedings of SIGGRAPH '96, 1996. — 本資料の :ref:`worley`\ で扱った Worley ノイズの原論文。
* Robert Bridson, Jim Houriham, Marcus Nordenstam, "Curl-Noise for Procedural Fluid Flow", ACM Transactions on Graphics 26(3) (SIGGRAPH 2007), 2007. — 本資料の\ :ref:`curl-noise`\ で扱ったカールノイズの原論文。流れ関数の回転から発散が 0 の速度場を作る考え方と、障害物の周りを回り込む流れへの拡張を扱う。
* Richard L. Gregory, Priscilla Heard, "Border Locking and the Café Wall Illusion", Perception 8(4), 1979. — 本資料の\ :doc:`illusions`\ で扱ったカフェウォール錯視を報告し、目地の明るさや太さとの関係を調べた論文。
* Alan Fraser, Kimerly J. Wilcox, "Perception of Illusory Movement", Nature 281, 1979. — 本資料の\ :doc:`illusions`\ で扱った周辺ドリフト錯視を最初に報告した論文。
* Akiyoshi Kitaoka, Hiroshi Ashida, "Phenomenal Characteristics of the Peripheral Drift Illusion", VISION 15(4), 2003. — 明るさの異なる 4 色の並びで周辺ドリフト錯視を強める方法と、動いて見える向きを示した論文。
* Michael Schrauf, Bernd Lingelbach, Eugene R. Wist, "The Scintillating Grid Illusion", Vision Research 37(8), 1997. — 本資料の\ :doc:`illusions`\ で扱ったきらめき格子錯視について、見え方の条件を調べた論文。
* T. A. Witten, L. M. Sander, "Diffusion-Limited Aggregation, a Kinetic Critical Phenomenon", Physical Review Letters 47(19), 1981. — 本資料の\ :ref:`dla`\ で扱った拡散律速凝集の原論文。
* Adam Runions, Martin Fuhrer, Brendan Lane, Pavol Federl, Anne-Gaëlle Rolland-Lagan, Przemyslaw Prusinkiewicz, "Modeling and Visualization of Leaf Venation Patterns", ACM Transactions on Graphics 24(3) (SIGGRAPH 2005), 2005. — 本資料の\ :ref:`space-colonization`\ の考え方を、葉脈の生成に用いた論文。
* Adam Runions, Brendan Lane, Przemyslaw Prusinkiewicz, "Modeling Trees with a Space Colonization Algorithm", Eurographics Workshop on Natural Phenomena, 2007. — 本資料の\ :ref:`space-colonization`\ で扱った、樹木を生成する空間植民アルゴリズムの論文。
* John C. Hart, "Sphere Tracing: A Geometric Method for the Antialiased Ray Tracing of Implicit Surfaces", The Visual Computer 12(10), 1996. — 本資料の :ref:`raymarching`\ で扱ったスフィアトレーシングの原論文。
* M. E. J. Newman, "Power Laws, Pareto Distributions and Zipf's Law", Contemporary Physics 46(5), 2005. — 本資料の\ :ref:`random-distribution`\ で扱ったべき分布について、性質や現実のデータでの現れ方を解説する論文。
* Adrian Secord, "Weighted Voronoi Stippling", Proceedings of the 2nd International Symposium on Non-Photorealistic Animation and Rendering (NPAR 2002), 2002. — 本資料の\ :ref:`stippling`\ で扱った、重み付きロイド緩和による点描の原論文。
* Edwin Catmull, Raphael Rom, "A Class of Local Interpolating Splines", in R.E. Barnhill, R.F. Riesenfeld (eds.), *Computer Aided Geometric Design*, Academic Press, 1974. — 本資料の\ :ref:`bezier`\ で扱った Catmull-Rom スプラインの原論文。

Web サイト・記事
-----------------

* `Inigo Quilez, "Domain Warping" <https://iquilezles.org/articles/warp/>`_ — 本資料の\ :doc:`noise`\ で扱ったドメインワーピング手法の元記事。fBm を用いたパターン生成から、多段階のワープ、彩色までを解説する。
* `Patricio Gonzalez Vivo, Jen Lowe, The Book of Shaders <https://thebookofshaders.com/>`_ — GLSL シェーダー向けの入門書だが、ノイズやフラクタルの考え方は言語に依存せず参考になる。smoothstep などの補間関数で図形の輪郭や濃淡を作る考え方も詳しく扱っている。
* `北岡明佳, 「北岡明佳の錯視のページ」 <https://www.ritsumei.ac.jp/~akitaoka/>`_ — 本資料の\ :doc:`illusions`\ で扱った周辺ドリフト錯視（「蛇の回転」など）をはじめ、多数の錯視図形とその解説を公開している。
* `Anders Hoff, "Differential Line" <https://inconvergent.net/generative/differential-line/>`_ — 本資料の\ :ref:`differential-growth`\ で扱った差分成長の作品と、そのアルゴリズムの解説。
* `Inigo Quilez, "Distance Functions" <https://iquilezles.org/articles/distfunctions/>`_ — 本資料の :ref:`raymarching`\ で扱った 3 次元の距離関数を、多数の図形について一覧にした記事。
* `W3C, "Scalable Vector Graphics (SVG) 2" <https://www.w3.org/TR/SVG2/>`_ — 本資料の\ :ref:`hatching`\ で書き出した SVG 形式の仕様。
* Thomas Jakobsen, "Advanced Character Physics", Game Developers Conference, 2001. — 本資料の\ :doc:`particles`\ で扱った、Verlet 積分と距離拘束の反復によるロープ・クロスの表現の元になった講演資料。
* `Björn Ottosson, "A perceptual color space for image processing" <https://bottosson.github.io/posts/oklab/>`_, 2020. — 本資料の\ :ref:`oklab`\ で扱った OKLab 色空間を提案した記事。変換行列の導出や、CIELAB などほかの色空間との比較を扱う。
* `Maxim Gumin, "WaveFunctionCollapse" <https://github.com/mxgmn/WaveFunctionCollapse>`_ — 本資料の :ref:`wfc`\ で扱った Wave Function Collapse の考案者によるリポジトリ。simple tiled model と overlapping model の実装と解説を含む。
* `Pomax, "A Primer on Bézier Curves" <https://pomax.github.io/bezierinfo/>`_ — 本資料の\ :ref:`bezier`\ で扱ったベジェ曲線について、de Casteljau のアルゴリズム、バーンスタイン基底多項式、スプラインとの関係などを図とともに詳しく解説する Web 上の解説書。

ライブラリ公式ドキュメント
----------------------------

* `py5 <https://py5coding.org/>`_
* `pycairo <https://pycairo.readthedocs.io/>`_
