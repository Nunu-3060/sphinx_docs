参考文献
========

本資料の作成にあたって参考にした文献と、さらに学ぶための資料を挙げる。

教科書
------

* Steve Marschner, Peter Shirley, Fundamentals of Computer Graphics, 5th Edition, CRC Press, 2021.

  CG の基礎を網羅した教科書である。ラスタライズ、座標変換、シェーディング、テクスチャ、レイトレーシングなど、本資料で扱った内容の多くを、より詳しく説明している。

* Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki, Sébastien Hillaire, Real-Time Rendering, 4th Edition, CRC Press, 2018. `公式サイト <https://www.realtimerendering.com/>`__

  GPU によるリアルタイム CG の技法を体系的にまとめた本である。物理ベースレンダリング、影、アンチエイリアシングなどの実用的な手法が詳しい。

* Matt Pharr, Wenzel Jakob, Greg Humphreys, Physically Based Rendering: From Theory to Implementation, 4th Edition, MIT Press, 2023. `オンライン版 <https://pbr-book.org/>`__

  物理ベースのレイトレーサーを、ソースコードとともに解説した本である。レンダリング方程式、モンテカルロ法、BVH を本格的に学べる。オンライン版を無料で読める。

Web サイト
----------

* Peter Shirley, Trevor David Black, Steve Hollasch, `Ray Tracing in One Weekend <https://raytracing.github.io/>`__.

  小さなレイトレーサーを、短いコードで順に作っていく入門書である。本資料の\ :doc:`raytracing`\ の次に読むのに向いている。

* Joey de Vries, `LearnOpenGL <https://learnopengl.com/>`__.

  OpenGL によるリアルタイム CG の入門サイトである。本資料の内容を GPU で実装する方法を学べる。

* `Scratchapixel <https://www.scratchapixel.com/>`__.

  ラスタライズ、透視投影の行列、レイトレーシングなどの CG のアルゴリズムを、数式とコードで丁寧に解説しているサイトである。

* Khronos Group, `OpenGL Registry <https://registry.khronos.org/OpenGL/index_gl.php>`__.

  OpenGL と GLSL の仕様書が公開されている。

規格
----

* IEC 61966-2-1:1999, Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB.

  sRGB の色空間とガンマ補正の式を定めた国際規格である。

論文
----

本資料で扱ったアルゴリズムを最初に提案した論文を、発表の順に挙げる。

* Jack E. Bresenham, Algorithm for computer control of a digital plotter, IBM Systems Journal, 4(1), pp. 25-30, 1965. `doi:10.1147/sj.41.0025 <https://doi.org/10.1147/sj.41.0025>`__

  ブレゼンハムのアルゴリズムを提案した論文である。

* Henri Gouraud, Continuous Shading of Curved Surfaces, IEEE Transactions on Computers, C-20(6), pp. 623-629, 1971. `doi:10.1109/T-C.1971.223313 <https://doi.org/10.1109/T-C.1971.223313>`__

  頂点の明るさを補間するグーローシェーディングを提案した論文である。

* Edwin Catmull, A Subdivision Algorithm for Computer Display of Curved Surfaces, Ph.D. Thesis, University of Utah, 1974.

  Z バッファー法とテクスチャマッピングの考え方を示した博士論文である。

* Bui Tuong Phong, Illumination for computer generated pictures, Communications of the ACM, 18(6), pp. 311-317, 1975. `doi:10.1145/360825.360839 <https://doi.org/10.1145/360825.360839>`__

  フォンの反射モデルと、法線を補間するフォンシェーディングを提案した論文である。

* James F. Blinn, Models of light reflection for computer synthesized pictures, Proceedings of SIGGRAPH '77, pp. 192-198, 1977. `doi:10.1145/563858.563893 <https://doi.org/10.1145/563858.563893>`__

  ハーフベクトルを使うブリン-フォンの反射モデルを提案した論文である。

* Turner Whitted, An improved illumination model for shaded display, Communications of the ACM, 23(6), pp. 343-349, 1980. `doi:10.1145/358876.358882 <https://doi.org/10.1145/358876.358882>`__

  影、反射、屈折を再帰的に扱うレイトレーシングを提案した論文である。

* Lance Williams, Pyramidal parametrics, ACM SIGGRAPH Computer Graphics, 17(3), pp. 1-11, 1983. `doi:10.1145/964967.801126 <https://doi.org/10.1145/964967.801126>`__

  ミップマップを提案した論文である。

* Thomas Porter, Tom Duff, Compositing digital images, ACM SIGGRAPH Computer Graphics, 18(3), pp. 253-259, 1984. `doi:10.1145/964965.808606 <https://doi.org/10.1145/964965.808606>`__

  アルファ値による画像の合成と、over 演算子などの合成の演算を体系化した論文である。

* James T. Kajiya, The rendering equation, ACM SIGGRAPH Computer Graphics, 20(4), pp. 143-150, 1986. `doi:10.1145/15886.15902 <https://doi.org/10.1145/15886.15902>`__

  レンダリング方程式と、それを解くパストレーシングを提案した論文である。

* Juan Pineda, A parallel algorithm for polygon rasterization, Proceedings of SIGGRAPH '88, pp. 17-20, 1988. `doi:10.1145/54852.378457 <https://doi.org/10.1145/54852.378457>`__

  エッジ関数による並列的なラスタライズを提案した論文である。

* Tomas Möller, Ben Trumbore, Fast, Minimum Storage Ray-Triangle Intersection, Journal of Graphics Tools, 2(1), pp. 21-28, 1997. `doi:10.1080/10867651.1997.10487468 <https://doi.org/10.1080/10867651.1997.10487468>`__

  メラー-トランボアの方法による、レイと三角形の交差判定を提案した論文である。
