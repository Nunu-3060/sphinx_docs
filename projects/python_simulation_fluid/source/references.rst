参考文献
========

本書の内容に関連する主な文献と情報源を挙げる。

書籍
----

* R. Bridson, *Fluid Simulation for Computer Graphics*, 2nd ed., CRC Press, 2015.

  コンピューターグラフィックスのための流体シミュレーションの定番の教科書。スタガード格子(MAC 格子)、圧力投影、FLIP 法などを詳しく扱う(第 7 章、第 11 章)。

* T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva, E. M. Viggen, *The Lattice Boltzmann Method: Principles and Practice*, Springer, 2017.

  格子ボルツマン法の理論と実装を網羅した教科書(第 10 章)。

論文
----

時間積分法と差分法
~~~~~~~~~~~~~~~~~~

* E. Hairer, C. Lubich, G. Wanner, "Geometric numerical integration illustrated by the Störmer–Verlet method," *Acta Numerica*, vol. 12, pp. 399–450, 2003.

  ベルレ法とシンプレクティック積分法の性質の解説(第 2 章)。

* R. Courant, K. Friedrichs, H. Lewy, "Über die partiellen Differenzengleichungen der mathematischen Physik," *Mathematische Annalen*, vol. 100, pp. 32–74, 1928.

  CFL 条件の由来となった論文(第 6 章)。

粒子の衝突
~~~~~~~~~~

* P. A. Cundall, O. D. L. Strack, "A discrete numerical model for granular assemblies," *Géotechnique*, vol. 29, no. 1, pp. 47–65, 1979.

  個別要素法(DEM)の原論文(第 4 章)。

格子法による流体の計算
~~~~~~~~~~~~~~~~~~~~~~

* A. J. Chorin, "Numerical solution of the Navier-Stokes equations," *Mathematics of Computation*, vol. 22, no. 104, pp. 745–762, 1968.

  射影法の原論文(第 8 章)。

* F. H. Harlow, J. E. Welch, "Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface," *Physics of Fluids*, vol. 8, no. 12, pp. 2182–2189, 1965.

  スタガード格子(MAC 法)の原論文(第 7 章)。

* J. Stam, "Stable Fluids," *Proceedings of SIGGRAPH 99*, pp. 121–128, 1999.

  Stable Fluids 法の原論文(第 7 章)。

* J. Stam, "Real-Time Fluid Dynamics for Games," *Proceedings of the Game Developer Conference*, 2003.

  Stable Fluids 法の実装を短いコードで解説した文献(第 7 章)。

* R. Fedkiw, J. Stam, H. W. Jensen, "Visual simulation of smoke," *Proceedings of SIGGRAPH 2001*, pp. 15–22, 2001.

  煙の表現と渦度閉じ込め(vorticity confinement)の論文(第 7 章)。

* U. Ghia, K. N. Ghia, C. T. Shin, "High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method," *Journal of Computational Physics*, vol. 48, no. 3, pp. 387–411, 1982.

  正方キャビティ流れの参照解として広く使われる論文(第 8 章)。

SPH
~~~

* L. B. Lucy, "A numerical approach to the testing of the fission hypothesis," *The Astronomical Journal*, vol. 82, pp. 1013–1024, 1977.
* R. A. Gingold, J. J. Monaghan, "Smoothed particle hydrodynamics: theory and application to non-spherical stars," *Monthly Notices of the Royal Astronomical Society*, vol. 181, pp. 375–389, 1977.

  SPH の原論文(第 9 章)。

* J. J. Monaghan, "Smoothed particle hydrodynamics," *Annual Review of Astronomy and Astrophysics*, vol. 30, pp. 543–574, 1992.

  SPH の解説。人工粘性やカーネル関数を扱う(第 9 章)。

* J. J. Monaghan, "Simulating free surface flows with SPH," *Journal of Computational Physics*, vol. 110, no. 2, pp. 399–406, 1994.

  弱圧縮性 SPH による自由表面流れの計算(第 9 章)。

* J. C. Martin, W. J. Moyce, "An experimental study of the collapse of liquid columns on a rigid horizontal plane," *Philosophical Transactions of the Royal Society of London. Series A*, vol. 244, no. 882, pp. 312–324, 1952.

  ダムブレイクの実験。SPH の検証によく使われる(第 9 章)。

ダムブレイクの理論解
~~~~~~~~~~~~~~~~~~~~

* A. Ritter, "Die Fortpflanzung der Wasserwellen," *Zeitschrift des Vereines Deutscher Ingenieure*, vol. 36, no. 33, pp. 947–954, 1892.

  水の流出(ダムブレイク)を浅水波理論で解いたリッターの解の原論文(第 9 章)。

円柱まわりの流れ
~~~~~~~~~~~~~~~~

* C. H. K. Williamson, "Vortex dynamics in the cylinder wake," *Annual Review of Fluid Mechanics*, vol. 28, pp. 477–539, 1996.

  円柱の後流とカルマン渦列についての総説。ストローハル数とレイノルズ数の関係を扱う(第 10 章)。

ソフトウェアと Web サイト
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - 内容
   * - `NumPy <https://numpy.org/>`_
     - 本書のサンプルコードで使った数値計算ライブラリ
   * - `matplotlib <https://matplotlib.org/>`_
     - 本書のサンプルコードで使ったグラフ描画ライブラリ
   * - `CFD Python <https://github.com/barbagroup/CFDPython>`_
     - L. A. Barba らによる、Python で流体の差分法を 12 のステップで学ぶ教材
   * - `Numba <https://numba.pydata.org/>`_
     - Python の関数を機械語にコンパイルして高速化するライブラリ
   * - `Taichi <https://www.taichi-lang.org/>`_
     - Python から GPU などで並列計算を行うための言語
   * - `OpenFOAM <https://www.openfoam.com/>`_
     - オープンソースの格子法による流体解析ソフトウェア
   * - `DualSPHysics <https://github.com/DualSPHysics/DualSPHysics>`_
     - オープンソースの SPH による流体解析ソフトウェア
   * - `PySPH <https://github.com/pypr/pysph>`_
     - Python による SPH のフレームワーク
   * - `Palabos <https://palabos.unige.ch/>`_
     - オープンソースの格子ボルツマン法のライブラリ
