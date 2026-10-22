サンプルコード一覧
==================

本書のサンプルコードは、次のリンクからダウンロードできる。ブロック崩しの各段階のファイルは、それぞれ単独で動作する。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル
     - 内容
   * - :download:`step01_window.py <../examples/step01_window.py>`
     - Step 1: ウィンドウを表示し、ゲームループを回す
   * - :download:`step02_paddle.py <../examples/step02_paddle.py>`
     - Step 2: キー入力でパドルを動かす
   * - :download:`step03_ball.py <../examples/step03_ball.py>`
     - Step 3: ボールを動かし、壁とパドルで反射させる
   * - :download:`step04_blocks.py <../examples/step04_blocks.py>`
     - Step 4: ブロックを並べ、当たったら壊す
   * - :download:`step05_score.py <../examples/step05_score.py>`
     - Step 5: スコアと残機、クリアとゲームオーバーの判定
   * - :download:`step06_scenes.py <../examples/step06_scenes.py>`
     - Step 6: タイトル・プレイ・結果のシーンに分ける
   * - :download:`step07_polish.py <../examples/step07_polish.py>`
     - Step 7: 効果音と演出を加えた完成版
   * - :download:`test_breakout.py <../examples/test_breakout.py>`
     - Step 7 の計算部分の単体テスト
   * - :download:`make_sprites.py <../examples/make_sprites.py>`
     - Pillow でスプライトシートを生成するスクリプト
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定ファイル

実行に必要なライブラリー
------------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ライブラリー
     - 使用するファイル
   * - pygame-ce
     - step01_window.py から step07_polish.py まで、test_breakout.py
   * - Pillow
     - make_sprites.py

.. code-block:: powershell
   :linenos:
   :caption: ライブラリーのインストール

   py -m pip install pygame-ce pillow

コードの検査
------------

サンプルコードは、ダウンロードしたファイルと ``setup.cfg`` を同じフォルダーに置き、次のコマンドで検査できる。

.. code-block:: powershell
   :linenos:
   :caption: サンプルコードの検査とテスト

   py -m pip install flake8 mypy
   py -m flake8
   py -m mypy .
   py -m unittest test_breakout
