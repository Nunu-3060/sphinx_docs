================
実装の全体構成
================

モジュール間の依存関係
=======================

本実装は、役割の異なる複数のモジュールが層状に積み重なる構成になっている。下位の層は上位の層のことを知らず、上位の層が下位の層を利用するという一方向の依存関係になっている。

.. list-table:: モジュールの層構成（上位ほど GUI に近い）
   :header-rows: 1
   :widths: 20 30 50

   * - 層
     - モジュール
     - 主な依存先
   * - アプリケーション層
     - :file:`LifeGameGUI.pyw`
     - :file:`FrameLifeGame.py`、:file:`TkWidget.py`、:file:`LifeGameImage.py`
   * - GUI 部品層
     - :file:`FrameLifeGame.py` / :file:`TkWidget.py`
     - :file:`LifeGameImage.py`、:file:`utility.py`
   * - 可視化層
     - :file:`LifeGameImage.py`
     - :file:`LifeGame.py`、:file:`utility.py`
   * - モデル層
     - :file:`LifeGame.py`
     - （なし）
   * - ユーティリティ
     - :file:`utility.py`
     - （なし）

* **モデル層**: :file:`LifeGame.py` は状態と更新ロジックのみを持ち、画像表示や GUI には一切関与しない。
* **ユーティリティ**: :file:`utility.py` は ``hsv2rgb`` 関数のみを提供する、どの層にも依存しない共通モジュールである。可視化層（:file:`LifeGameImage.py`）と GUI 部品層（:file:`TkWidget.py`）の双方から利用される。
* **可視化層**: :file:`LifeGameImage.py` は :class:`~LifeGame.LifeGame` を継承し、格子の状態を色付き画像に変換する機能を追加する。
* **GUI 部品層**: :file:`FrameLifeGame.py` は画像を表示・アニメーションさせる Tkinter ウィジェット、:file:`TkWidget.py` はルールや色などを指定するための入力ウィジェット群を提供する。
* **アプリケーション層**: :file:`LifeGameGUI.pyw` は上記すべてのモジュールを組み合わせて 1 つのアプリケーションにまとめる。:class:`~LifeGameImage.LifeGameImage` は、:class:`~FrameLifeGame.FrameLifeGame` 経由だけでなく、シミュレーション開始時のパラメータ組み立てにも直接利用される。

このように層を分離しておくことで、たとえば GUI を使わずに :class:`~LifeGame.LifeGame` だけをスクリプトから利用したり、Tkinter 以外のフロントエンドに差し替えたりすることが容易になる。

使用ライブラリの役割分担
=========================

本実装では、目的の異なる 3 つのライブラリを組み合わせている。

* **NumPy**: 格子の状態を 2 次元配列として保持し、``np.roll`` による近傍セル数の計算や、ブールマスクによるルールの適用など、格子全体に対する演算をループを使わずに一括で行う。
* **Pillow (PIL)**: NumPy 配列として表現された格子の状態を、``Image.fromarray`` によって画像に変換し、``resize`` で拡大表示する。
* **Tkinter**: ``ttk`` ウィジェットを用いて GUI を構築し、``after()`` メソッドによる定期実行でアニメーションを実現する。

いずれも Python の標準的なライブラリ（Tkinter は標準ライブラリ、NumPy・Pillow はサードパーティ製の定番ライブラリ）であり、追加の依存関係を最小限に抑えている。
