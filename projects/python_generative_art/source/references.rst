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
* Adrian Secord, "Weighted Voronoi Stippling", Proceedings of the 2nd International Symposium on Non-Photorealistic Animation and Rendering (NPAR 2002), 2002. — 本資料の\ :ref:`stippling`\ で扱った、重み付きロイド緩和による点描の原論文。
* Edwin Catmull, Raphael Rom, "A Class of Local Interpolating Splines", in R.E. Barnhill, R.F. Riesenfeld (eds.), *Computer Aided Geometric Design*, Academic Press, 1974. — 本資料の\ :ref:`bezier`\ で扱った Catmull-Rom スプラインの原論文。

Web サイト・記事
-----------------

* `Inigo Quilez, "Domain Warping" <https://iquilezles.org/articles/warp/>`_ — 本資料の\ :doc:`noise`\ で扱ったドメインワーピング手法の元記事。fBm を用いたパターン生成から、多段階のワープ、彩色までを解説する。
* `Patricio Gonzalez Vivo, Jen Lowe, The Book of Shaders <https://thebookofshaders.com/>`_ — GLSL シェーダー向けの入門書だが、ノイズやフラクタルの考え方は言語に依存せず参考になる。smoothstep などの補間関数で図形の輪郭や濃淡を作る考え方も詳しく扱っている。
* Thomas Jakobsen, "Advanced Character Physics", Game Developers Conference, 2001. — 本資料の\ :doc:`particles`\ で扱った、Verlet 積分と距離拘束の反復によるロープ・クロスの表現の元になった講演資料。
* `Björn Ottosson, "A perceptual color space for image processing" <https://bottosson.github.io/posts/oklab/>`_, 2020. — 本資料の\ :ref:`oklab`\ で扱った OKLab 色空間を提案した記事。変換行列の導出や、CIELAB などほかの色空間との比較を扱う。
* `Maxim Gumin, "WaveFunctionCollapse" <https://github.com/mxgmn/WaveFunctionCollapse>`_ — 本資料の :ref:`wfc`\ で扱った Wave Function Collapse の考案者によるリポジトリ。simple tiled model と overlapping model の実装と解説を含む。
* `Pomax, "A Primer on Bézier Curves" <https://pomax.github.io/bezierinfo/>`_ — 本資料の\ :ref:`bezier`\ で扱ったベジェ曲線について、de Casteljau のアルゴリズム、バーンスタイン基底多項式、スプラインとの関係などを図とともに詳しく解説する Web 上の解説書。

ライブラリ公式ドキュメント
----------------------------

* `py5 <https://py5coding.org/>`_
* `pycairo <https://pycairo.readthedocs.io/>`_
