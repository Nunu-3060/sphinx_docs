.. _appendix-d:

付録 D サンプルコード一覧
=========================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/generated/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダーの中に次の構成でファイルが配置される。各ファイルの内容は、この付録の後半の「ソースコード」で閲覧できる。

.. code-block:: text
   :linenos:

   examples/
   ├── setup.cfg         flake8 と mypy の設定
   ├── ode.py            微分方程式の数値解法の共通モジュール
   ├── plot_util.py      図の表示と保存の共通モジュール
   └── ch01_*.py 〜 ch12_*.py  各章のサンプル

実行と検査の方法
----------------

サンプルは ``examples`` フォルダーで実行する（:ref:`はじめに <ch00>` を参照）。多くのサンプルは、共通モジュールや、ほかの章のサンプルの関数を import する。個別にダウンロードした場合は、一覧の「必要なファイル」の列に示したファイルも同じフォルダーに置く。まとめて使う場合は、ZIP ファイルを使うと簡単である。

サンプルは、flake8（PEP 8 などのコーディング規約の検査、1 行は 120 文字まで）と mypy（型ヒントの検査、strict モード）で違反がないことを確認している。``examples`` フォルダーで次のコマンドを実行すると、``setup.cfg`` の設定で検査できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m pip install flake8 mypy
   $ python -m flake8 .
   $ python -m mypy .

matplotlib の 3 次元グラフの機能（``mpl_toolkits``）は型ヒントの情報を持たないため、``setup.cfg`` でこの import の検査を省略している。mypy は Windows ではシステムの文字コードで設定ファイルを読むので、``setup.cfg`` のコメントは英語で書いている。

共通モジュール
--------------

.. list-table:: 共通モジュール
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - :download:`ode.py <../examples/ode.py>`
     - 常微分方程式の数値解法（オイラー法、4 次のルンゲ＝クッタ法）。:ref:`第 3 章 <ch03>` で説明した。
   * - :download:`plot_util.py <../examples/plot_util.py>`
     - 日本語フォントの設定と、コマンドライン引数（``--save``）の処理。
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定。

第 I 部 力学系の基礎
--------------------

.. list-table:: 第 I 部 力学系の基礎のサンプル
   :header-rows: 1
   :widths: 28 13 39 20

   * - ファイル
     - 章
     - 内容
     - 必要なファイル
   * - :download:`ch01_first_systems.py <../examples/ch01_first_systems.py>`
     - :ref:`第 1 章 <ch01>`
     - 身近な力学系の例：離散時間の 3 つの写像と、連続時間の減衰振り子
     - ``ode.py``、``plot_util.py``
   * - :download:`ch02_cobweb.py <../examples/ch02_cobweb.py>`
     - :ref:`第 2 章 <ch02>`
     - 1 次元写像の反復を、クモの巣図（cobweb plot）で調べる
     - ``plot_util.py``
   * - :download:`ch02_newton.py <../examples/ch02_newton.py>`
     - :ref:`第 2 章 <ch02>`
     - ニュートン法を写像の反復として見る（2 の平方根を求める）
     - ``ch02_cobweb.py``、``plot_util.py``
   * - :download:`ch03_integrators.py <../examples/ch03_integrators.py>`
     - :ref:`第 3 章 <ch03>`
     - オイラー法と 4 次のルンゲ＝クッタ法の精度を、単振動で比べる
     - ``ode.py``、``plot_util.py``
   * - :download:`ch03_phase_portrait.py <../examples/ch03_phase_portrait.py>`
     - :ref:`第 3 章 <ch03>`
     - 2 次元の連続時間の力学系の相図（相平面上の流れの様子）を描く
     - ``plot_util.py``
   * - :download:`ch03_van_der_pol.py <../examples/ch03_van_der_pol.py>`
     - :ref:`第 3 章 <ch03>`
     - ファン・デル・ポール振動子のリミットサイクル
     - ``ode.py``、``plot_util.py``

第 II 部 カオス
---------------

.. list-table:: 第 II 部 カオスのサンプル
   :header-rows: 1
   :widths: 28 13 39 20

   * - ファイル
     - 章
     - 内容
     - 必要なファイル
   * - :download:`ch04_logistic.py <../examples/ch04_logistic.py>`
     - :ref:`第 4 章 <ch04>`
     - ロジスティック写像の時系列、分岐図、ファイゲンバウム定数
     - ``plot_util.py``
   * - :download:`ch04_stretch_fold.py <../examples/ch04_stretch_fold.py>`
     - :ref:`第 4 章 <ch04>`
     - カオスを生む「引き伸ばし」の仕組みを、テント写像とパイこね変換で見る
     - ``plot_util.py``
   * - :download:`ch05_lyapunov.py <../examples/ch05_lyapunov.py>`
     - :ref:`第 5 章 <ch05>`
     - ロジスティック写像のリアプノフ指数を計算し、分岐図と並べる
     - ``ch04_logistic.py``、``plot_util.py``
   * - :download:`ch05_precision.py <../examples/ch05_precision.py>`
     - :ref:`第 5 章 <ch05>`
     - 浮動小数点数の丸め誤差がカオスの計算に与える影響を調べる
     - ``plot_util.py``
   * - :download:`ch05_sensitivity.py <../examples/ch05_sensitivity.py>`
     - :ref:`第 5 章 <ch05>`
     - 初期値鋭敏性：わずかに異なる 2 つの初期値から出た軌道が離れていく様子を見る
     - ``ch04_logistic.py``、``plot_util.py``
   * - :download:`ch06_clifford.py <../examples/ch06_clifford.py>`
     - :ref:`第 6 章 <ch06>`
     - クリフォード・アトラクタとピーター・デ・ヨング・アトラクタ
     - ``plot_util.py``
   * - :download:`ch06_double_pendulum.py <../examples/ch06_double_pendulum.py>`
     - :ref:`第 6 章 <ch06>`
     - 二重振り子：摩擦のない（エネルギーが保存される）系のカオス
     - ``ode.py``、``plot_util.py``
   * - :download:`ch06_henon.py <../examples/ch06_henon.py>`
     - :ref:`第 6 章 <ch06>`
     - エノン写像のストレンジアトラクタと、その層状の構造
     - ``plot_util.py``
   * - :download:`ch06_lorenz.py <../examples/ch06_lorenz.py>`
     - :ref:`第 6 章 <ch06>`
     - ローレンツ方程式のストレンジアトラクタ、初期値鋭敏性、ローレンツ写像
     - ``ode.py``、``plot_util.py``
   * - :download:`ch06_rossler.py <../examples/ch06_rossler.py>`
     - :ref:`第 6 章 <ch06>`
     - レスラー方程式のアトラクタと、ポアンカレ断面による解析
     - ``ode.py``、``plot_util.py``
   * - :download:`ch06_standard_map.py <../examples/ch06_standard_map.py>`
     - :ref:`第 6 章 <ch06>`
     - 標準写像（チリコフ写像）：保存系で、規則的な運動とカオス的な運動が混在する様子
     - ``plot_util.py``

第 III 部 フラクタル
--------------------

.. list-table:: 第 III 部 フラクタルのサンプル
   :header-rows: 1
   :widths: 28 13 39 20

   * - ファイル
     - 章
     - 内容
     - 必要なファイル
   * - :download:`ch07_box_counting.py <../examples/ch07_box_counting.py>`
     - :ref:`第 7 章 <ch07>`
     - ボックスカウント法でフラクタル次元を推定する
     - ``ch07_classic_fractals.py``、``plot_util.py``
   * - :download:`ch07_classic_fractals.py <../examples/ch07_classic_fractals.py>`
     - :ref:`第 7 章 <ch07>`
     - 古典的なフラクタル：カントール集合、コッホ曲線、シェルピンスキーのギャスケット
     - ``plot_util.py``
   * - :download:`ch08_ifs.py <../examples/ch08_ifs.py>`
     - :ref:`第 8 章 <ch08>`
     - 反復関数系（IFS）：決定的な反復、カオスゲーム、バーンズリーのシダ
     - ``plot_util.py``
   * - :download:`ch08_lsystem.py <../examples/ch08_lsystem.py>`
     - :ref:`第 8 章 <ch08>`
     - L-system（リンデンマイヤー・システム）：文字列の書き換えでフラクタル図形を描く
     - ``plot_util.py``
   * - :download:`ch09_mandelbrot_julia.py <../examples/ch09_mandelbrot_julia.py>`
     - :ref:`第 9 章 <ch09>`
     - マンデルブロ集合とジュリア集合を、脱出時間アルゴリズムで描く
     - ``ch04_logistic.py``、``plot_util.py``
   * - :download:`ch09_newton_fractal.py <../examples/ch09_newton_fractal.py>`
     - :ref:`第 9 章 <ch09>`
     - ニュートン法フラクタル：複素平面の各点から出発したニュートン法が、どの解に収束するかで色分けする
     - ``ch04_logistic.py``、``ch09_mandelbrot_julia.py``、``plot_util.py``
   * - :download:`ch10_correlation_dimension.py <../examples/ch10_correlation_dimension.py>`
     - :ref:`第 10 章 <ch10>`
     - ストレンジアトラクタのフラクタル次元を、相関次元（グラスバーガー＝プロカッチャ法）で推定する
     - ``ch06_henon.py``、``ch06_lorenz.py``、``ch07_box_counting.py``、``ch07_classic_fractals.py``、``ode.py``、``plot_util.py``
   * - :download:`ch10_magnetic_pendulum.py <../examples/ch10_magnetic_pendulum.py>`
     - :ref:`第 10 章 <ch10>`
     - 磁気振り子：3 つの磁石のどれに引き寄せられて止まるかで、初期位置を色分けする
     - ``ode.py``、``plot_util.py``

第 IV 部 応用と表現
-------------------

.. list-table:: 第 IV 部 応用と表現のサンプル
   :header-rows: 1
   :widths: 28 13 39 20

   * - ファイル
     - 章
     - 内容
     - 必要なファイル
   * - :download:`ch11_coupled_map_lattice.py <../examples/ch11_coupled_map_lattice.py>`
     - :ref:`第 11 章 <ch11>`
     - 結合写像格子（CML）：1 次元に並べたカオス写像を隣どうしで結合した系の時空パターン
     - ``plot_util.py``
   * - :download:`ch11_reaction_diffusion.py <../examples/ch11_reaction_diffusion.py>`
     - :ref:`第 11 章 <ch11>`
     - グレイ＝スコット・モデル：反応と拡散だけで、斑点や縞の模様が自然に生まれる
     - ``plot_util.py``
   * - :download:`ch11_synchronization.py <../examples/ch11_synchronization.py>`
     - :ref:`第 11 章 <ch11>`
     - カオス同期（ペコラ＝キャロルの方法）：2 つのローレンツ系を、1 つの変数を共有させて同期させる
     - ``ch06_lorenz.py``、``ode.py``、``plot_util.py``
   * - :download:`ch11_terrain.py <../examples/ch11_terrain.py>`
     - :ref:`第 11 章 <ch11>`
     - 中点変位法で、フラクタルな地形（山の稜線と地形図）を作る
     - ``plot_util.py``
   * - :download:`ch12_attractor_art.py <../examples/ch12_attractor_art.py>`
     - :ref:`第 12 章 <ch12>`
     - ストレンジアトラクタをジェネラティブアートとして描く
     - ``ch06_clifford.py``、``plot_util.py``
   * - :download:`ch12_fractal_flame.py <../examples/ch12_fractal_flame.py>`
     - :ref:`第 12 章 <ch12>`
     - フラクタル・フレーム（の簡易版）：IFS に非線形の変形と色を加えて描く
     - ``plot_util.py``

ソースコード
------------

すべてのサンプルの全文を示す。

ode.py
^^^^^^

.. literalinclude:: ../examples/ode.py
   :linenos:

plot_util.py
^^^^^^^^^^^^

.. literalinclude:: ../examples/plot_util.py
   :linenos:

ch01_first_systems.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch01_first_systems.py
   :linenos:

ch02_cobweb.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch02_cobweb.py
   :linenos:

ch02_newton.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch02_newton.py
   :linenos:

ch03_integrators.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_integrators.py
   :linenos:

ch03_phase_portrait.py
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_phase_portrait.py
   :linenos:

ch03_van_der_pol.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch03_van_der_pol.py
   :linenos:

ch04_logistic.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch04_logistic.py
   :linenos:

ch04_stretch_fold.py
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch04_stretch_fold.py
   :linenos:

ch05_lyapunov.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_lyapunov.py
   :linenos:

ch05_precision.py
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_precision.py
   :linenos:

ch05_sensitivity.py
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch05_sensitivity.py
   :linenos:

ch06_clifford.py
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_clifford.py
   :linenos:

ch06_double_pendulum.py
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_double_pendulum.py
   :linenos:

ch06_henon.py
^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_henon.py
   :linenos:

ch06_lorenz.py
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_lorenz.py
   :linenos:

ch06_rossler.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_rossler.py
   :linenos:

ch06_standard_map.py
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch06_standard_map.py
   :linenos:

ch07_box_counting.py
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch07_box_counting.py
   :linenos:

ch07_classic_fractals.py
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch07_classic_fractals.py
   :linenos:

ch08_ifs.py
^^^^^^^^^^^

.. literalinclude:: ../examples/ch08_ifs.py
   :linenos:

ch08_lsystem.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch08_lsystem.py
   :linenos:

ch09_mandelbrot_julia.py
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch09_mandelbrot_julia.py
   :linenos:

ch09_newton_fractal.py
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch09_newton_fractal.py
   :linenos:

ch10_correlation_dimension.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch10_correlation_dimension.py
   :linenos:

ch10_magnetic_pendulum.py
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch10_magnetic_pendulum.py
   :linenos:

ch11_coupled_map_lattice.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_coupled_map_lattice.py
   :linenos:

ch11_reaction_diffusion.py
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_reaction_diffusion.py
   :linenos:

ch11_synchronization.py
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_synchronization.py
   :linenos:

ch11_terrain.py
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch11_terrain.py
   :linenos:

ch12_attractor_art.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch12_attractor_art.py
   :linenos:

ch12_fractal_flame.py
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/ch12_fractal_flame.py
   :linenos:

setup.cfg
^^^^^^^^^

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
