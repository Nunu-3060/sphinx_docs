################################
Pyxel によるレトロゲーム作成入門
################################

はじめに
========

本書は、Python のレトロゲームエンジン Pyxel を使い、小さなゲームを 1 本、企画から公開まで自分だけで作り上げるための入門書である。プログラムを書くことはできるが、ゲームを作ったことも、ドット絵を描いたことも、曲を作ったこともないエンジニアを読者として想定している。

ゲーム制作には、プログラミング以外にも企画、グラフィックス、サウンド、調整、公開といった多くの作業がある。本書ではそれぞれを 1 章ずつ取り上げ、題材のゲームを少しずつ完成に近づけながら説明する。

本書で作るゲーム
----------------

題材は縦スクロールのシューティングゲーム「COSMO RUSH」である。自機を操作して弾を撃ち、次々に現れる敵を倒してスコアを稼ぐ。ステージの最後にはボスが現れ、倒すと難易度が上がって次のステージが始まる。

.. list-table::
   :class: screens
   :widths: 33 33 34

   * - .. image:: images/screens/game_title.png
          :class: pixel
          :alt: タイトル画面
     - .. image:: images/screens/game_play.png
          :class: pixel
          :alt: プレイ画面
     - .. image:: images/screens/game_boss.png
          :class: pixel
          :alt: ボス戦
   * - タイトル画面
     - プレイ画面
     - ボス戦

完成版はブラウザで遊べる。`COSMO RUSH を遊ぶ <play/cosmo_rush.html>`__\ （矢印キーで移動、Z キーまたはスペースキーでショット）。

対象読者と前提知識
------------------

本書は次の読者を想定している。

* Python の文法、クラス、型ヒントを理解している。
* コマンドラインで ``pip`` や仮想環境（venv）を使える。
* ゲーム制作、ドット絵、作曲の経験はない。

Python 自体の説明は行わない。一方で、ゲーム制作に固有の考え方（ゲームループ、座標、当たり判定、スプライト、効果音の作り方など）は最初から説明する。

本書の構成
----------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 章
     - 内容
   * - :doc:`ch01_setup`
     - Pyxel の特徴を知り、開発環境を整える。
   * - :doc:`ch02_planning`
     - 作るゲームを決め、画面遷移と必要な素材を洗い出す。
   * - :doc:`ch03_basics`
     - ゲームループ、描画、入力、動き、当たり判定などの基礎を学ぶ。
   * - :doc:`ch04_graphics`
     - Pyxel Editor でドット絵とタイルマップを作る。
   * - :doc:`ch05_sound`
     - Pyxel Editor で効果音と BGM を作る。
   * - :doc:`ch06_prototype`
     - 図形だけを使って、遊べる最小限のゲームを作る。
   * - :doc:`ch07_polish`
     - シーン、素材、背景、音、演出、敵の種類、ボスを加えて完成させる。
   * - :doc:`ch08_testing`
     - テストプレイと単体テストで品質を上げる。
   * - :doc:`ch09_publish`
     - ゲームをパッケージにまとめ、Web で公開する。
   * - :doc:`ch10_next`
     - 次に挑戦するとよいことを紹介する。

第 1 章から順に読むことを想定している。ゲームプログラミングの経験がある読者は、第 3 章を飛ばしてもよい。

動作確認環境
------------

本書の内容は次の環境で確認した。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ソフトウェア
     - バージョン
   * - OS
     - Windows 11
   * - Python
     - 3.14.6
   * - Pyxel
     - 2.9.9
   * - flake8
     - 7.4.1
   * - mypy
     - 2.4.0
   * - pytest
     - 9.1.1

Pyxel は更新が活発で、バージョンによって API や Pyxel Editor の画面が変わることがある。本書と異なる動きをする場合は、バージョンを 2.9.9 にそろえて試すとよい（:ref:`ch01-install`\ を参照）。

サンプルコード
--------------

本書のサンプルコードと素材は、次のリンクから zip ファイルでまとめてダウンロードできる。各章の本文からも、個別のファイルをダウンロードできる。

* `examples.zip <downloads/examples.zip>`__

zip ファイルを展開すると、次の構成の ``examples`` ディレクトリができる。

.. code-block:: text
   :linenos:

   examples/
   ├── setup.cfg          flake8・mypy・pytest の設定
   ├── assets/            素材（リソースファイルと、それを生成するスクリプト）
   ├── ch01_hello/        第 1 章のサンプルコード
   ├── ch03_basics/       第 3 章のサンプルコード
   ├── ch06_step1/ ～ ch06_step4/    第 6 章のサンプルコード（ステップごと）
   ├── ch07_step5/ ～ ch07_step9/    第 7 章のサンプルコード（ステップごと）
   ├── cosmo_rush/        完成版のゲーム
   └── tests/             第 8 章の単体テスト

サンプルコードはすべて ``examples`` ディレクトリで次のように実行する。

.. code-block:: console
   :linenos:

   > cd examples
   > pyxel run ch06_step1/main.py

本書の表記
----------

* コード例の左端の数字は行番号である。ファイルの一部を抜き出したコード例では、ファイル内の行番号をそのまま示す。
* コマンドの例では、先頭の ``>`` がプロンプトを表す。``>`` は入力しない。
* ``pyxel.btn()`` のように書いた場合、Pyxel のモジュール ``pyxel`` にある関数を表す。
* 「Pyxel」は製品名、``pyxel`` はコマンド名とパッケージ名を表す。

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 目次

   ch01_setup
   ch02_planning
   ch03_basics
   ch04_graphics
   ch05_sound
   ch06_prototype
   ch07_polish
   ch08_testing
   ch09_publish
   ch10_next

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_api
   appendix_editor
   appendix_samples
   glossary
   references
