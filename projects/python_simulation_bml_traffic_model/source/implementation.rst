==========
実装の解説
==========

モジュール構成
==============

本プロジェクトの実装は、 6 個の Python ファイルで構成されています。モデルのロジックと GUI の実装を分離しており、 ``BML`` クラスは tkinter に依存せず単体で利用できる構成になっています。各ファイルの全文は :doc:`appendix` からダウンロードできます。

.. list-table:: モジュール構成
   :header-rows: 1
   :widths: 25 75

   * - ファイル
     - 役割
   * - ``BML.py``
     - BML モデル本体。格子の初期化と更新ロジックを numpy によるベクトル化演算で実装しています。
   * - ``utility.py``
     - HSV 表色系から RGB 表色系への変換関数 ``hsv2rgb`` を提供します。
   * - ``BMLImage.py``
     - ``BML`` を継承し、格子の状態を画像（ Pillow の ``Image`` ）に変換する機能を追加します。
   * - ``FrameBML.py``
     - ``BMLImage`` の画像を一定間隔で更新・表示する tkinter フレームです。
   * - ``TkWidget.py``
     - 色選択・盤面サイズ選択・密度スケールなど、 GUI の部品となる tkinter フレーム群です。
   * - ``BMLGUI.pyw``
     - 上記の部品を組み合わせたメインアプリケーションと、起動用の ``main`` 関数です。

これらのモジュールの依存関係は、 ``BML`` → ``BMLImage`` → ``FrameBML`` → ``BMLGUI`` という継承・利用関係になっており、 ``utility`` と ``TkWidget`` はそれぞれ ``BMLImage`` と ``BMLGUI`` から利用されます。

BML クラス（モデル本体）
=========================

``BML`` クラスは、格子の状態を表す 2 次元 numpy 配列 ``lattice`` を保持し、初期化と 1 ステップ分の更新処理を提供します。

.. literalinclude:: ../script/BML.py
   :language: python
   :caption: BML.py
   :linenos:

コンストラクタでは、幅・高さ・密度 ``probability`` を受け取り、 :doc:`theory` で示した確率に従って各セルへ 0 ・ 1 ・ 2 の値を割り当てています。 ``next`` メソッドでは、 ``np.roll`` を用いて格子全体を上下・左右にずらした配列を作成し、ブールインデックス（条件を満たすセルだけを一括で書き換える手法）によってループを使わずに 1 ステップ分の更新を計算しています。前半で南北方向の車（値 1 ）を、後半で東西方向の車（値 2 ）を、それぞれ :doc:`theory` の更新規則に従って動かしており、 1 回の ``next`` 呼び出しで両方向の車が 1 回ずつ移動します。

utility モジュール（色変換）
=============================

``BMLImage`` で車の色を指定する際に、直感的に調整しやすい HSV 表色系（色相・彩度・明度）を RGB 表色系に変換するための関数です。

.. literalinclude:: ../script/utility.py
   :language: python
   :caption: utility.py
   :linenos:

引数 ``h`` ・ ``s`` ・ ``v`` にはそれぞれ 1 つの ``float`` 値、または同じ形状の numpy 配列のいずれかを渡すことができ、配列を渡した場合は各要素に対応する RGB 値をまとめて計算します。

BMLImage クラス（可視化）
==========================

``BMLImage`` クラスは ``BML`` を継承し、格子の状態を画像として描画する機能を追加します。

.. literalinclude:: ../script/BMLImage.py
   :language: python
   :caption: BMLImage.py
   :linenos:

``image_np`` メソッドで、格子の値 0 ・ 1 ・ 2 をそれぞれ色 ``c0`` ・ ``c1`` ・ ``c2`` に対応させた RGB 画像配列を作成し、 ``image_pil`` メソッドで Pillow の ``Image`` オブジェクトへ変換した上で、指定した ``pixel`` 倍率に拡大します。 ``image_tk`` メソッドは、この画像を tkinter で表示できる ``ImageTk.PhotoImage`` 形式に変換します。拡大時の補間方式に最近傍法（ ``Image.Resampling.NEAREST`` ）を用いているため、格子の 1 マス 1 マスが 1 つの色の塊としてはっきり表示されます。

GUI（ TkWidget ・ FrameBML ・ BMLGUI ）
========================================

GUI 部分は 3 つのモジュールに分かれています。

``FrameBML`` は、 ``BMLImage`` の画像を ``ttk.Label`` に表示し、 tkinter の ``after`` メソッドを用いて一定間隔（既定では 10 ミリ秒）ごとに ``next`` メソッドを呼び出して画像を更新し続けます。

.. literalinclude:: ../script/FrameBML.py
   :language: python
   :caption: FrameBML.py
   :linenos:

``TkWidget`` には、色（ HSV ）を選択する ``FrameHSV`` 、盤面サイズを選択する ``FrameRadioButton`` 、密度を選択する ``FrameScale`` の 3 つの部品クラスが定義されています。いずれも ``get`` メソッドで現在の設定値を取得し、 ``set`` メソッドで値を設定できます。

``BMLGUI`` は、これらの部品を配置してメインウィンドウを構成するクラスです。「 start 」ボタンで新しいウィンドウを開いてシミュレーションを開始し、「 stop 」ボタンでそのウィンドウを閉じます。「 reset 」ボタンで密度・盤面サイズの設定を既定値に戻し、「 color 」ボタンで車の色をランダムに選び直すことができます。 GUI の具体的な操作方法は :doc:`usage` で説明します。
