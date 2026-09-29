付録
====

.. _appendix-symbols:

記号の一覧
----------

本資料で使う主な記号は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 記号
     - 意味
   * - :math:`n`
     - データの個数（標本の大きさ）
   * - :math:`x_i`
     - :math:`i` 番目のデータ
   * - :math:`\sum_{i=1}^{n} x_i`
     - :math:`x_1 + x_2 + \cdots + x_n`\ （総和）
   * - :math:`\bar{x}`
     - 標本平均
   * - :math:`s^2`、:math:`s`
     - 標本分散（:math:`n` で割る分散）、その正の平方根
   * - :math:`u^2`、:math:`u`
     - 不偏分散（:math:`n - 1` で割る分散）、その正の平方根
   * - :math:`\mu`、:math:`\sigma^2`、:math:`\sigma`
     - 母平均（期待値）、母分散、母標準偏差
   * - :math:`E[X]`、:math:`V[X]`
     - 確率変数 :math:`X` の期待値、分散
   * - :math:`P(A)`
     - 事象 :math:`A` が起こる確率
   * - :math:`N(\mu, \sigma^2)`
     - 平均値 :math:`\mu`、分散 :math:`\sigma^2` の正規分布
   * - :math:`t_{0.025}(n - 1)`
     - 自由度 :math:`n - 1` の t 分布で上側の確率が 0.025 になる値
   * - :math:`H_0`、:math:`H_1`
     - 帰無仮説、対立仮説
   * - :math:`\alpha`、:math:`\beta`
     - 有意水準（第一種の過誤の確率）、第二種の過誤の確率
   * - :math:`r`
     - ピアソンの相関係数
   * - :math:`\hat{y}`
     - 回帰直線による予測値
   * - :math:`R^2`
     - 決定係数

用語集
------

本資料で使う主な用語と、対応する英語は次のとおりです。英語の用語は、ライブラリの関数名や英語の資料を調べるときに役立ちます。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 用語
     - 英語
     - 説明している章
   * - 母集団
     - population
     - :doc:`data_basics`
   * - 標本
     - sample
     - :doc:`data_basics`
   * - 欠損値
     - missing value
     - :doc:`data_basics`
   * - 平均値
     - mean
     - :doc:`descriptive_statistics`
   * - 中央値
     - median
     - :doc:`descriptive_statistics`
   * - 最頻値
     - mode
     - :doc:`descriptive_statistics`
   * - 分散
     - variance
     - :doc:`descriptive_statistics`
   * - 標準偏差
     - standard deviation
     - :doc:`descriptive_statistics`
   * - 四分位範囲
     - interquartile range (IQR)
     - :doc:`descriptive_statistics`
   * - ヒストグラム
     - histogram
     - :doc:`visualization`
   * - 箱ひげ図
     - box plot
     - :doc:`visualization`
   * - 散布図
     - scatter plot
     - :doc:`visualization`
   * - 確率変数
     - random variable
     - :doc:`probability_distribution`
   * - 確率質量関数
     - probability mass function (PMF)
     - :doc:`probability_distribution`
   * - 確率密度関数
     - probability density function (PDF)
     - :doc:`probability_distribution`
   * - 累積分布関数
     - cumulative distribution function (CDF)
     - :doc:`probability_distribution`
   * - 期待値
     - expected value
     - :doc:`probability_distribution`
   * - 二項分布
     - binomial distribution
     - :doc:`probability_distribution`
   * - ポアソン分布
     - Poisson distribution
     - :doc:`probability_distribution`
   * - 正規分布
     - normal distribution
     - :doc:`probability_distribution`
   * - 標準誤差
     - standard error
     - :doc:`sampling_distribution`
   * - 大数の法則
     - law of large numbers
     - :doc:`sampling_distribution`
   * - 中心極限定理
     - central limit theorem
     - :doc:`sampling_distribution`
   * - 不偏推定量
     - unbiased estimator
     - :doc:`estimation`
   * - 信頼区間
     - confidence interval
     - :doc:`estimation`
   * - 帰無仮説
     - null hypothesis
     - :doc:`hypothesis_testing`
   * - 対立仮説
     - alternative hypothesis
     - :doc:`hypothesis_testing`
   * - p 値
     - p-value
     - :doc:`hypothesis_testing`
   * - 有意水準
     - significance level
     - :doc:`hypothesis_testing`
   * - 検出力
     - power
     - :doc:`hypothesis_testing`
   * - 多重比較
     - multiple comparisons
     - :doc:`hypothesis_testing`
   * - 分割表
     - contingency table
     - :doc:`statistical_tests`
   * - 分散分析
     - analysis of variance (ANOVA)
     - :doc:`statistical_tests`
   * - 相関係数
     - correlation coefficient
     - :doc:`correlation_regression`
   * - 回帰分析
     - regression analysis
     - :doc:`correlation_regression`
   * - 決定係数
     - coefficient of determination
     - :doc:`correlation_regression`

.. _appendix-examples:

サンプルコードの一覧
--------------------

本資料のサンプルコードとサンプルデータは、次のリンクからダウンロードできます。保存するときのフォルダー構成は、:doc:`introduction`\ を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - ファイル
     - 内容
   * - :download:`ch02_data_basics.py <../examples/ch02_data_basics.py>`
     - データの読み込みと確認、欠損値の処理
   * - :download:`ch03_descriptive_statistics.py <../examples/ch03_descriptive_statistics.py>`
     - 代表値と散布度、標準化
   * - :download:`ch04_visualization.py <../examples/ch04_visualization.py>`
     - ヒストグラム、箱ひげ図、散布図、棒グラフ
   * - :download:`ch05_probability_distribution.py <../examples/ch05_probability_distribution.py>`
     - 二項分布、ポアソン分布、正規分布
   * - :download:`ch06_sampling_distribution.py <../examples/ch06_sampling_distribution.py>`
     - 大数の法則と中心極限定理のシミュレーション
   * - :download:`ch07_estimation.py <../examples/ch07_estimation.py>`
     - 母平均の信頼区間
   * - :download:`ch08_hypothesis_testing.py <../examples/ch08_hypothesis_testing.py>`
     - p 値、第一種の過誤、検出力、多重比較
   * - :download:`ch09_statistical_tests.py <../examples/ch09_statistical_tests.py>`
     - t 検定、カイ二乗検定、一元配置分散分析、U 検定
   * - :download:`ch10_correlation_regression.py <../examples/ch10_correlation_regression.py>`
     - 相関係数、単回帰分析
   * - :download:`make_scores_data.py <../examples/make_scores_data.py>`
     - サンプルデータの作成
   * - :download:`scores.csv <../examples/data/scores.csv>`
     - サンプルデータ（``data`` フォルダーに保存する）
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定

サンプルコードは、flake8 と mypy（``--strict`` 相当の設定）で問題が検出されないことを確認しています。``setup.cfg`` をサンプルコードと同じフォルダーに保存し、そのフォルダーで次のコマンドを実行すると確認できます。SciPy と pandas は型情報を同梱していないため、``setup.cfg`` でこれらの import に関するエラーを抑止しています。

.. code-block:: text

   pip install flake8 mypy
   flake8 .
   mypy .

.. _appendix-dataset:

サンプルデータの作成方法
------------------------

サンプルデータ ``scores.csv`` は、次のプログラムで作成しました。乱数のシードを固定しているため、実行するたびに同じデータが作成されます。

:download:`make_scores_data.py をダウンロードする <../examples/make_scores_data.py>`

.. literalinclude:: ../examples/make_scores_data.py
   :language: python
   :linenos:

各列は次のように作成しています。

* クラスは、生徒番号 1 ～ 50 を A クラス、51 ～ 100 を B クラスとしています。
* 部活動は、運動部 40 %、文化部 30 %、所属なし 30 % の確率で無作為に割り当てています。クラスとは無関係に割り当てているため、クラスと部活動は独立です。
* 学習時間は、0.0 ～ 6.0 時間の一様分布に従う乱数を、小数第 1 位に丸めた値です。
* 数学の点数は、:math:`35 + 6 \times \text{学習時間}` に、B クラスなら 5 点、文化部なら 4 点を加え、さらに平均値 0、標準偏差 10 の正規分布に従う誤差を加えた値です。
* 英語の点数は、:math:`40 + 4 \times \text{学習時間}` に、平均値 0、標準偏差 12 の正規分布に従う誤差を加えた値です。
* 点数は整数に丸め、0 ～ 100 点の範囲に収めています。

参考資料
--------

各ライブラリの公式ドキュメントです。関数の引数や計算方法の詳細は、こちらを参照してください。

* `NumPy documentation <https://numpy.org/doc/stable/>`_
* `SciPy: Statistical functions (scipy.stats) <https://docs.scipy.org/doc/scipy/reference/stats.html>`_
* `pandas documentation <https://pandas.pydata.org/docs/>`_
* `Matplotlib documentation <https://matplotlib.org/stable/>`_
