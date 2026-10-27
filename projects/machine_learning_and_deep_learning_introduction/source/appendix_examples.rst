サンプルコード一覧
==================

本書のサンプルコードの一覧を次に示す。ファイル名のリンクからダウンロードできる。実行方法と動作確認環境は「:doc:`intro`」を参照してほしい。

型検査と静的解析の設定ファイル :download:`setup.cfg <../examples/setup.cfg>` も用意した。サンプルコードを置いたディレクトリで次のコマンドを実行すると、flake8 と mypy による検査を行える（flake8 と mypy のインストールが必要である）。

.. code-block:: console
   :linenos:

   python -m flake8 .
   python -m mypy .

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 10 45 45

   * - 章
     - ファイル
     - 内容
   * - 2
     - :download:`ch02_numpy_basics.py <../examples/ch02_numpy_basics.py>`
     - NumPy によるベクトル・行列の計算と、数値微分による勾配の計算
   * - 3
     - :download:`ch03_preprocessing.py <../examples/ch03_preprocessing.py>`
     - 欠損値の補完、標準化、one-hot 符号化、データの分割
   * - 4
     - :download:`ch04_linear_regression_scratch.py <../examples/ch04_linear_regression_scratch.py>`
     - 正規方程式と勾配降下法による線形回帰（NumPy）
   * - 4
     - :download:`ch04_linear_regression_sklearn.py <../examples/ch04_linear_regression_sklearn.py>`
     - scikit-learn による線形回帰と多項式回帰
   * - 5
     - :download:`ch05_logistic_regression_scratch.py <../examples/ch05_logistic_regression_scratch.py>`
     - 勾配降下法によるロジスティック回帰（NumPy）
   * - 5
     - :download:`ch05_classifiers_sklearn.py <../examples/ch05_classifiers_sklearn.py>`
     - ロジスティック回帰、k 近傍法、SVM の比較
   * - 6
     - :download:`ch06_overfitting.py <../examples/ch06_overfitting.py>`
     - 過学習、正則化、交差検証、グリッドサーチ
   * - 6
     - :download:`ch06_metrics.py <../examples/ch06_metrics.py>`
     - 混同行列、適合率、再現率、F1 値、ROC AUC
   * - 7
     - :download:`ch07_tree_split_scratch.py <../examples/ch07_tree_split_scratch.py>`
     - ジニ不純度による決定木の分割の探索（NumPy）
   * - 7
     - :download:`ch07_tree_ensemble_sklearn.py <../examples/ch07_tree_ensemble_sklearn.py>`
     - 決定木、ランダムフォレスト、勾配ブースティングの比較
   * - 8
     - :download:`ch08_unsupervised.py <../examples/ch08_unsupervised.py>`
     - k-means 法（NumPy）、主成分分析、Isolation Forest による異常検知
   * - 9
     - :download:`ch09_two_layer_net.py <../examples/ch09_two_layer_net.py>`
     - 2 層ニューラルネットワークと誤差逆伝播法、勾配確認（NumPy）
   * - 10
     - :download:`ch10_optimizers.py <../examples/ch10_optimizers.py>`
     - SGD、モメンタム、Adam の実装と比較（NumPy）
   * - 10
     - :download:`ch10_pytorch_mlp.py <../examples/ch10_pytorch_mlp.py>`
     - PyTorch による多層パーセプトロンの学習（AdamW、バッチ正規化、ドロップアウト、早期終了）
   * - 11
     - :download:`ch11_convolution_numpy.py <../examples/ch11_convolution_numpy.py>`
     - 畳み込み演算と最大プーリング（NumPy）
   * - 11
     - :download:`ch11_cnn_pytorch.py <../examples/ch11_cnn_pytorch.py>`
     - PyTorch による CNN の学習
   * - 12
     - :download:`ch12_attention.py <../examples/ch12_attention.py>`
     - Scaled Dot-Product Attention と因果マスク（NumPy）
   * - 12
     - :download:`ch12_transformer_pytorch.py <../examples/ch12_transformer_pytorch.py>`
     - PyTorch による小さな Transformer エンコーダの学習
   * - 13
     - :download:`ch13_pipeline.py <../examples/ch13_pipeline.py>`
     - パイプライン、交差検証によるモデル選択、モデルの保存、順列重要度
