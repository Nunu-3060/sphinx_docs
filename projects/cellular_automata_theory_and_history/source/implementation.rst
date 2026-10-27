Python による実装
=================

本章では、CA を Python で実装するときの基本的な方法と注意点をまとめる。本書のサンプルコードはすべてこの章の方針で書かれている。各サンプルの一覧と実行方法は、付録の「\ :doc:`examples`\ 」を参照してほしい。

基本方針
--------

CA の実装で最も重要なのは、次の 2 点である。

* **同期更新を正しく実装する**\ ：次の時刻の配置は、必ず現在の配置だけから計算する。現在の配置を表す配列を書き換えながら計算してはいけない（第 2 章「\ :doc:`basics`\ 」を参照）。
* **セルごとのループを避ける**\ ：Python の ``for`` 文でセルを 1 つずつ処理すると非常に遅い。NumPy の配列演算を使って、全セルの計算を一度に行う。

NumPy の配列演算は新しい配列を返すので、2 つ目の点に従えば 1 つ目の点も自然に満たされる。

1 次元 CA の実装
----------------

ECA の 1 ステップの実装は第 4 章「\ :doc:`one_dimensional`\ 」で示した。時空図全体は、各時刻の配置を 2 次元配列の行に順に格納していけば得られる。

.. literalinclude:: ../examples/elementary_ca.py
   :language: python
   :pyobject: evolve
   :linenos:

時空図の配列は ``matplotlib`` の ``imshow`` でそのまま画像として表示できる。``interpolation="nearest"`` を指定しないと、セルの境界がぼやけて表示されることがある。

.. code-block:: python
   :linenos:

   import matplotlib.pyplot as plt

   from elementary_ca import evolve, single_seed

   history = evolve(30, single_seed(201), 100)
   plt.imshow(history, cmap="binary", interpolation="nearest")
   plt.show()

2 次元 CA の実装：近傍の数え方
------------------------------

ライフゲームのような外部総和型 CA では、各セルの周囲にある生きたセルの数を数えることが計算の中心になる。代表的な方法が 2 つある。

``np.roll`` による方法
^^^^^^^^^^^^^^^^^^^^^^

第 5 章「\ :doc:`two_dimensional`\ 」で示した ``count_neighbors`` は、盤面全体を 8 方向に 1 セルずつ巡回的にずらした配列を足し合わせる。``np.roll`` は端からはみ出した要素を反対側の端に回り込ませるので、周期境界条件が自動的に実現される。

畳み込みによる方法
^^^^^^^^^^^^^^^^^^

周囲のセルの数を数える操作は、中心が 0 で周囲が 1 の 3 × 3 のカーネルによる畳み込みである。SciPy の ``scipy.signal.convolve2d`` を使うと、次のように書ける（SciPy は本書のサンプルコードには不要なので、試す場合は ``pip install scipy`` で別途インストールする）。``boundary="wrap"`` が周期境界条件を表す。

.. code-block:: python
   :linenos:

   import numpy as np
   from scipy.signal import convolve2d

   KERNEL = np.array([[1, 1, 1],
                      [1, 0, 1],
                      [1, 1, 1]], dtype=np.uint8)


   def step_life(grid: np.ndarray) -> np.ndarray:
       """ライフゲーム (B3/S23) を 1 世代進める."""
       n = convolve2d(grid, KERNEL, mode="same", boundary="wrap")
       return ((n == 3) | ((grid == 1) & (n == 2))).astype(np.uint8)

畳み込みによる方法は、カーネルを取り替えるだけで近傍の形や重みを自由に変えられる。たとえば、第 8 章「\ :doc:`advanced`\ 」で扱った Lenia のように広い範囲の重み付き平均を使う規則では、高速フーリエ変換（FFT）による畳み込みを使うと効率がよい。

2 つの方法の比較
^^^^^^^^^^^^^^^^

本書の執筆環境で、512 × 512 の盤面のライフゲームを 1 世代進める時間を測ったところ、``np.roll`` による方法と畳み込みによる方法はどちらも約 10 ms で、ほぼ同等であった。一方、同じ処理を Python の 4 重の ``for`` 文で書くと 1 世代に約 0.7 秒かかり、NumPy を使う方法の約 70 倍遅かった。具体的な時間は環境によって異なるが、セルごとのループを避けることの効果は大きい。

境界条件の実装
--------------

``np.roll`` や ``boundary="wrap"`` が実現するのは周期境界条件である。固定境界条件や反射境界条件を使うには、``np.pad`` で配列の外側に仮想的なセル（ゴースト・セル）を付け足してから近傍を計算し、最後に内側の部分だけを取り出す。

.. code-block:: python
   :linenos:

   import numpy as np


   def count_neighbors_padded(grid: np.ndarray, mode: str) -> np.ndarray:
       """固定境界 (mode="constant") または反射境界 (mode="symmetric") で周囲 8 セルの和を求める."""
       padded = np.pad(grid, 1, mode=mode)  # 外側に 1 セルずつ付け足す
       rows, cols = grid.shape
       total = np.zeros(grid.shape, dtype=np.int32)
       for dy in (0, 1, 2):
           for dx in (0, 1, 2):
               if dy == 1 and dx == 1:
                   continue
               total += padded[dy:dy + rows, dx:dx + cols]
       return total

``mode="constant"`` は外側を 0 で埋めるので、外側を静止状態に固定した固定境界条件になる。``mode="symmetric"`` は端のセル自身を鏡に映した値で埋めるので、\ :numref:`fig-boundaries` の反射境界条件になる。

可視化とアニメーション
----------------------

2 次元 CA の時間変化は、``matplotlib.animation.FuncAnimation`` でアニメーションとして表示できる（サンプルコード ``game_of_life.py`` の ``main`` 関数を参照）。アニメーションを GIF ファイルとして保存するには、次のように ``PillowWriter`` を使う。

.. code-block:: python
   :linenos:

   from matplotlib.animation import FuncAnimation, PillowWriter

   animation = FuncAnimation(fig, update, frames=200, interval=100)
   animation.save("life.gif", writer=PillowWriter(fps=10))

``FuncAnimation`` が返すオブジェクトは、表示が終わるまで変数に保持しておく必要がある。変数に代入しないと、オブジェクトがガベージコレクションで回収され、アニメーションが止まってしまう。

実装上の注意
------------

データ型とオーバーフロー
^^^^^^^^^^^^^^^^^^^^^^^^

2 状態の CA では、メモリを節約するために配列のデータ型を ``np.uint8`` にすることが多い。ただし、近傍の和を ``np.uint8`` のまま計算すると、和が 255 を超えたときに桁あふれ（オーバーフロー）が起きて誤った値になる。ライフゲームの周囲 8 セルの和は最大 8 なので問題ないが、近傍が広い規則や状態数が多い規則では、和を計算する配列を ``np.int32`` などにする必要がある。

乱数の扱い
^^^^^^^^^^

確率的 CA では、``np.random.default_rng(seed)`` で乱数生成器を作り、シードを指定できるようにしておくとよい。同じシードを使えば同じ結果が再現されるので、デバッグや結果の比較がしやすくなる。本書の図は、すべてシードを固定して生成している。

さらなる高速化
^^^^^^^^^^^^^^

さらに大規模な計算が必要な場合は、次のような方法がある。

.. list-table:: 高速化の方法
   :header-rows: 1
   :widths: 25 75

   * - 方法
     - 概要
   * - ビット演算
     - 1 セルを 1 ビットで表し、64 セルを 1 つの 64 ビット整数に詰め込んで、ビット演算でまとめて計算する。メモリ使用量も 1/8 になる。
   * - JIT コンパイル
     - Numba などを使って Python の関数を機械語にコンパイルし、ループのまま高速に実行する。
   * - GPU
     - CuPy や PyTorch などを使い、配列演算を GPU で並列に実行する。CA は全セルが同じ計算をするので、GPU と相性がよい。
   * - HashLife
     - 盤面を四分木で表し、同じ部分パターンの未来の計算結果を記憶して再利用する [Gosper1984]_。規則的な構造が多いパターンでは、何兆世代もの計算を短時間で行える。

ライフゲームなどの CA を手軽に試すには、HashLife を実装したソフトウェア Golly [Golly]_ を使うのもよい。
