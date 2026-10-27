付録 C サンプルコード一覧
==================================================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダにすべてのファイルが置かれる。

実行方法
--------

サンプルは、``examples`` フォルダで実行する。図を描くサンプルは補助モジュール ``dsp_plot.py`` を import するので、個別にダウンロードした場合は、同じフォルダに ``dsp_plot.py`` も置く。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python fourier_series.py
   $ python spectrogram.py

各サンプルは、計算の結果を画面に表示する関数 ``report()`` をもつ。図を描くサンプルは、さらに図を作る関数 ``create_figure()`` をもち、結果を表示した後に図をウィンドウに表示する。本文に載せた実行結果と図は、本書のビルド時に、これらの関数を呼び出して作ったものである。計算時間を測るサンプル（``fft_radix2.py`` と ``fast_convolution.py``）の結果は、実行する計算機によって変わる。

検査の方法
----------

サンプルは、flake8（PEP 8 などのコーディング規約の検査、行の長さは 120 文字まで許容）と mypy（``strict = True`` での型ヒントの検査）で違反がないことを確認している。``examples`` フォルダで次のコマンドを実行すると、同じフォルダの ``setup.cfg`` の設定で検査できる。mypy で SciPy の型を検査するには、``scipy-stubs`` パッケージが必要である。

.. code-block:: console
   :linenos:

   $ python -m pip install flake8 mypy scipy-stubs
   $ cd examples
   $ python -m flake8 .
   $ python -m mypy .

ファイルの一覧
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - ファイル
     - 内容
     - 章
   * - :download:`dsp_plot.py <../examples/dsp_plot.py>`
     - 図の描画の補助モジュール（日本語フォントの設定、デシベルへの変換など）
     - ―
   * - :download:`fourier_series.py <../examples/fourier_series.py>`
     - 矩形波のフーリエ係数の数値計算、部分和とギブス現象
     - 第 2 章
   * - :download:`fourier_transform_pairs.py <../examples/fourier_transform_pairs.py>`
     - 代表的なフーリエ変換の対を数値積分で確かめる
     - 第 3 章
   * - :download:`aliasing.py <../examples/aliasing.py>`
     - エイリアシングによる見かけの周波数を求める
     - 第 4 章
   * - :download:`convolution.py <../examples/convolution.py>`
     - 畳み込み和を定義どおりに計算し、``np.convolve()`` と比べる
     - 第 5 章
   * - :download:`dft_naive.py <../examples/dft_naive.py>`
     - DFT を定義どおりに計算し、``np.fft.fft()`` と比べる。DFT の性質を確かめる
     - 第 6 章
   * - :download:`fft_radix2.py <../examples/fft_radix2.py>`
     - 基数 2 の FFT の実装と、計算量と計算時間の比較
     - 第 7 章
   * - :download:`spectrum_analysis.py <../examples/spectrum_analysis.py>`
     - 窓関数を使った振幅スペクトルの計算と、スペクトル漏れの比較
     - 第 8 章
   * - :download:`spectrogram.py <../examples/spectrogram.py>`
     - 線形チャープ信号のスペクトログラム
     - 第 8 章
   * - :download:`fir_filter_design.py <../examples/fir_filter_design.py>`
     - 窓関数法による FIR ローパスフィルタの設計
     - 第 9 章
   * - :download:`iir_filter_design.py <../examples/iir_filter_design.py>`
     - 双一次変換によるバタワース IIR ローパスフィルタの設計
     - 第 9 章
   * - :download:`noise_reduction.py <../examples/noise_reduction.py>`
     - FFT、バタワース LPF、移動平均による雑音の除去の比較
     - 第 10 章
   * - :download:`fast_convolution.py <../examples/fast_convolution.py>`
     - オーバーラップ加算法による高速な畳み込み
     - 第 10 章
   * - :download:`dtmf_detection.py <../examples/dtmf_detection.py>`
     - DTMF 信号の生成と、ゲルツェル法による検出
     - 第 10 章
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル
     - ―
