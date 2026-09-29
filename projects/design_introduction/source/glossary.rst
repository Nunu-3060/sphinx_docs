用語集と参考資料
================

用語集
------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 用語
     - 意味
   * - アクセントカラー
     - 最も注目してほしい箇所だけに、小さな面積で使う色。
   * - アフォーダンス
     - 物と人の間にある、その物で何ができるかという関係。J. J. Gibson が提唱した。
   * - アンチエイリアス
     - 図形や文字の輪郭に中間色を置き、ギザギザを目立たなくする処理。
   * - エイリアシング
     - 画像を縮小するときなどに、表現しきれない細かい模様が、元の画像にはない模様として現れる現象。折り返しひずみとも呼ぶ。
   * - ガター
     - グリッドシステムで、カラムとカラムの間の余白。
   * - カラム
     - グリッドシステムで、画面を等しい幅に分割した列。
   * - カラーマップ
     - 数値を色で表すときに使う、色の並び。
   * - 行送り
     - 行の基準線（ベースライン）どうしの間隔。CSS の ``line-height`` に相当します。
   * - 行間
     - 行と行の間の空き。行送りから文字の大きさを引いたもの。
   * - 禁則処理
     - 句読点や閉じ括弧などが行頭に来ないように、折り返す位置を調整すること。
   * - ゲシュタルトの法則
     - 人の視覚が、個々の要素をまとまりとして捉える性質をまとめたもの。近接・類同・共通領域・連続などの法則がある。
   * - コントラスト比
     - 2 色のうち明るい方と暗い方の相対輝度に、それぞれ 0.05 を加えた値の比。WCAG で定義され、1 から 21 までの値を取ります。
   * - 色覚シミュレーション
     - 一般的な色覚とは異なる色覚での見え方を、計算によって近似すること。
   * - シグニファイア
     - その物で何ができるかを、人に伝える手がかり。
   * - ジャンプ率
     - 見出しと本文の文字の大きさの比率。
   * - スーパーサンプリング
     - 目的の大きさより大きく描画してから縮小し、輪郭を滑らかにする方法。
   * - スクリム
     - 写真の上の文字を読みやすくするために重ねる、半透明の層。
   * - セーフエリア
     - アイコンのグリッドのうち、図形を収める範囲。
   * - 相対輝度
     - 色の明るさを、黒を 0、白を 1 として表した値。ガンマ補正を取り除いた RGB から計算します。
   * - チャートジャンク
     - グラフのうち、データを表さず、読み手の注意をそらす装飾。
   * - データインク比
     - グラフの描画に使うインクのうち、データそのものを表すインクの割合。
   * - デザイントークン
     - 色・余白・文字の大きさなど、見た目を決める値に用途で名前を付けたもの。
   * - トリミング
     - 画像の一部を切り抜くこと。
   * - ヒックの法則
     - 選択肢から 1 つを選ぶまでの時間が、選択肢の数の対数に比例して増えるという法則。
   * - フィッツの法則
     - 目標を指し示すまでの時間が、目標までの距離と目標の大きさで決まるという法則。
   * - ベースカラー
     - 背景など、最も広い面積に使う色。
   * - マージン
     - 画面や用紙の端と、内容の間の余白。
   * - メインカラー
     - 見出しや帯など、全体の印象を決める色。
   * - ユーザビリティ
     - 利用者が、目的を効果的かつ効率的に、満足して達成できる度合い。

参考資料
--------

書籍
~~~~

* Robin Williams 著『ノンデザイナーズ・デザインブック』（マイナビ出版）：デザインの 4 原則を紹介した入門書。
* Donald A. Norman 著『誰のためのデザイン？ 増補・改訂版』（新曜社）：アフォーダンスとシグニファイアを解説した書籍。
* Edward R. Tufte 著『The Visual Display of Quantitative Information』（Graphics Press）：データインク比とチャートジャンクを提唱した書籍。

論文
~~~~

* G. M. Machado, M. M. Oliveira, L. A. F. Fernandes, "A Physiologically-based Model for Simulation of Color Vision Deficiency", IEEE Transactions on Visualization and Computer Graphics, 15(6), 2009：色覚シミュレーションに使った変換行列の出典。

Web サイト
~~~~~~~~~~

* `Web Content Accessibility Guidelines (WCAG) 2.2 <https://www.w3.org/TR/WCAG22/>`_：コントラスト比の定義と達成基準。
* `WCAG 2.2 解説書：達成基準 1.4.3 コントラスト（最低限） <https://waic.jp/translations/WCAG22/Understanding/contrast-minimum>`_：ウェブアクセシビリティ基盤委員会（WAIC）による日本語訳。
* `10 Usability Heuristics for User Interface Design <https://www.nngroup.com/articles/ten-usability-heuristics/>`_：Nielsen Norman Group によるユーザビリティの 10 原則。
* `Color Universal Design (CUD) <https://jfly.uni-koeln.de/color/>`_：Okabe と Ito による、色覚の多様性に配慮した配色の提案。
* `Choosing Colormaps in Matplotlib <https://matplotlib.org/stable/users/explain/colors/colormaps.html>`_：matplotlib のカラーマップの分類と選び方。
* `Pillow（PIL Fork）ドキュメント <https://pillow.readthedocs.io/en/stable/>`_：``Image``、``ImageDraw``、``ImageOps`` などの API リファレンス。
* `tkinter.ttk --- Tk のテーマ付きウィジェット <https://docs.python.org/ja/3/library/tkinter.ttk.html>`_：ttk とスタイルの公式ドキュメント。
