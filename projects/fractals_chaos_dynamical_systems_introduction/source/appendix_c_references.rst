.. _appendix-c:

付録 C 参考文献
===============

本書の執筆で参考にした文献と、さらに学ぶための文献を挙げる。

入門書・教科書
--------------

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - 文献
     - 内容
   * - S. H. Strogatz, *Nonlinear Dynamics and Chaos*, 2nd ed., Westview Press, 2015.（邦訳：S. H. ストロガッツ『非線形ダイナミクスとカオス』、田中久陽・中尾裕也・千葉逸人 訳、丸善出版、2015 年）
     - 力学系とカオスの標準的な教科書。第 I 部、第 II 部の内容を、より詳しく学べる。
   * - K. T. Alligood, T. D. Sauer, J. A. Yorke, *Chaos: An Introduction to Dynamical Systems*, Springer, 1996.
     - 写像を中心にカオスを解説した教科書。リアプノフ指数、フラクタル次元、カオスの定義に詳しい。
   * - R. L. Devaney, *An Introduction to Chaotic Dynamical Systems*, 2nd ed., Addison-Wesley, 1989.
     - 1 次元写像と複素力学系の数学的な入門書。第 5 章のカオスの定義はこの本による。
   * - H.-O. Peitgen, H. Jürgens, D. Saupe, *Chaos and Fractals: New Frontiers of Science*, 2nd ed., Springer, 2004.
     - カオスとフラクタルを、多数の図とともに幅広く解説した本。本書の第 III 部の内容の多くを詳しく扱う。
   * - K. Falconer, *Fractal Geometry: Mathematical Foundations and Applications*, 3rd ed., Wiley, 2014.
     - フラクタル幾何学の数学的な教科書。ハウスドルフ次元、ボックスカウント次元、IFS を厳密に扱う。
   * - B. B. Mandelbrot, *The Fractal Geometry of Nature*, W. H. Freeman, 1982.（邦訳：B. マンデルブロ『フラクタル幾何学』、広中平祐 監訳、日経サイエンス社、1985 年）
     - フラクタルという概念を提唱した本。自然の形の幾何学としてのフラクタルを論じる。
   * - M. F. Barnsley, *Fractals Everywhere*, Academic Press, 1988.
     - IFS、カオスゲーム、コラージュ定理の教科書。バーンズリーのシダはこの本で紹介された。
   * - P. Prusinkiewicz, A. Lindenmayer, *The Algorithmic Beauty of Plants*, Springer, 1990.
     - L-system による植物の形の生成を体系的に解説した本。著者らにより、オンラインで公開されている。
   * - J. C. Sprott, *Strange Attractors: Creating Patterns in Chaos*, M&T Books, 1993.
     - 2 次の写像などのパラメータをランダムに選んでストレンジアトラクタを探す方法を、多数の作例とともに解説した本。第 12 章の自動探索はこの本の方法に基づく。
   * - J. Gleick, *Chaos: Making a New Science*, Viking, 1987.（邦訳：J. グリック『カオス―新しい科学をつくる』、大貫昌子 訳、新潮文庫、1991 年）
     - カオスの研究の歴史を、研究者たちの物語として描いた一般向けの本。
   * - K. Kaneko, I. Tsuda, *Complex Systems: Chaos and Beyond*, Springer, 2001.
     - 結合写像格子を含む、多数の要素からなるカオス的な系を扱った本。

論文
----

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - 文献
     - 内容
   * - E. N. Lorenz, "Deterministic Nonperiodic Flow," *Journal of the Atmospheric Sciences*, 20, 130–141, 1963.
     - ローレンツ方程式と初期値鋭敏性を示した論文（第 6 章）。
   * - T.-Y. Li, J. A. Yorke, "Period Three Implies Chaos," *The American Mathematical Monthly*, 82, 985–992, 1975.
     - 周期 3 の点があればあらゆる周期の点があることを示した論文（第 4 章）。
   * - R. M. May, "Simple mathematical models with very complicated dynamics," *Nature*, 261, 459–467, 1976.
     - ロジスティック写像の複雑な振る舞いを紹介した論文（第 4 章）。
   * - M. Hénon, "A two-dimensional mapping with a strange attractor," *Communications in Mathematical Physics*, 50, 69–77, 1976.
     - エノン写像を提案した論文（第 6 章）。
   * - O. E. Rössler, "An equation for continuous chaos," *Physics Letters A*, 57, 397–398, 1976.
     - レスラー方程式を提案した論文（第 6 章）。
   * - M. J. Feigenbaum, "Quantitative universality for a class of nonlinear transformations," *Journal of Statistical Physics*, 19, 25–52, 1978.
     - 周期倍分岐の普遍性とファイゲンバウム定数を示した論文（第 4 章）。
   * - B. V. Chirikov, "A universal instability of many-dimensional oscillator systems," *Physics Reports*, 52, 263–379, 1979.
     - 標準写像を使って、保存系のカオスを調べた論文（第 6 章）。
   * - B. B. Mandelbrot, "How Long Is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension," *Science*, 156, 636–638, 1967.
     - 海岸線の長さとフラクタル次元を論じた論文（第 7 章）。
   * - J. E. Hutchinson, "Fractals and self similarity," *Indiana University Mathematics Journal*, 30, 713–747, 1981.
     - 縮小写像の組が自己相似な集合をただ 1 つ決めることを示した論文（第 8 章）。
   * - P. Grassberger, I. Procaccia, "Measuring the strangeness of strange attractors," *Physica D*, 9, 189–208, 1983.
     - 相関次元を提案した論文（第 10 章）。
   * - J. L. Kaplan, J. A. Yorke, "Chaotic behavior of multidimensional difference equations," in *Functional Differential Equations and Approximation of Fixed Points*, Lecture Notes in Mathematics 730, Springer, 204–227, 1979.
     - リアプノフ次元（カプラン＝ヨーク次元）を提案した論文（第 10 章）。
   * - F. Takens, "Detecting strange attractors in turbulence," in *Dynamical Systems and Turbulence, Warwick 1980*, Lecture Notes in Mathematics 898, Springer, 366–381, 1981.
     - 遅れ座標による埋め込みの定理を示した論文（第 10 章）。
   * - A. Fournier, D. Fussell, L. Carpenter, "Computer rendering of stochastic models," *Communications of the ACM*, 25, 371–384, 1982.
     - 中点変位法による地形などの生成を提案した論文（第 11 章）。
   * - A. M. Turing, "The chemical basis of morphogenesis," *Philosophical Transactions of the Royal Society of London B*, 237, 37–72, 1952.
     - 反応拡散による模様の形成を提案した論文（第 11 章）。
   * - L. M. Pecora, T. L. Carroll, "Synchronization in chaotic systems," *Physical Review Letters*, 64, 821–824, 1990.
     - カオス同期を示した論文（第 11 章）。
   * - E. Ott, C. Grebogi, J. A. Yorke, "Controlling chaos," *Physical Review Letters*, 64, 1196–1199, 1990.
     - カオスの制御の方法（OGY 法）を提案した論文（第 11 章）。
   * - J. E. Pearson, "Complex patterns in a simple system," *Science*, 261, 189–192, 1993.
     - グレイ＝スコット・モデルの多様な模様を分類した論文（第 11 章）。

Web 上の資料
------------

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - 資料
     - 内容
   * - S. Draves, E. Reckase, "The Fractal Flame Algorithm," https://flam3.com/flame_draves.pdf
     - フラクタル・フレームの考案者による、アルゴリズムの解説（第 12 章）。
   * - P. Bourke, "Clifford Attractors," https://paulbourke.net/fractals/clifford/
     - クリフォード・アトラクタの式と作例（第 6 章、第 12 章）。
   * - P. Bourke, "Peter de Jong Attractors," https://paulbourke.net/fractals/peterdejong/
     - ピーター・デ・ヨング・アトラクタの式と作例（第 6 章）。
   * - NumPy Documentation, https://numpy.org/doc/stable/
     - 本書のサンプルで使った NumPy の関数の説明。
   * - Matplotlib Documentation, https://matplotlib.org/stable/
     - 本書のサンプルで使った matplotlib の関数とカラーマップの説明。
   * - Pillow Documentation, https://pillow.readthedocs.io/en/stable/
     - GIF アニメーションの保存に使った Pillow の説明。
