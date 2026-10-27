はじめに
========

本書の目的
----------

ゲームを自作しようとしたエンジニアが最初につまずくのは、プログラムではなく絵であることが多い。素材集を使う方法もあるが、キャラクターやアイコンを少しだけ自分で用意したい場面は意外に多い。

\ :term:`ドット絵`\ は、こうした場面で最初に取り組む絵の形式として向いている。扱うピクセルの数が少なく、1 つ 1 つのピクセルを意図をもって置くため、「なぜその色をそこに置くのか」を言葉で説明しやすい。つまり、絵の経験が無くても、規則と手順を理解すれば一定の品質に到達できる。

本書の目的は、ドット絵の基本的な規則と制作の手順を理解し、16×16 ピクセル程度のキャラクターやタイルを自分で描けるようになることである。

対象読者と前提知識
------------------

本書は次のような読者を想定している。

* ゲーム制作の経験は無いが、Python などでプログラムを書いたことがある。
* 絵を描いた経験はほとんど無いが、自作のゲームやツールで使う絵を自分で用意したい。

絵画やデザインの知識は前提としない。Python の知識は、サンプルコードを読んで実行するために使う。ドット絵を描くこと自体には Python は不要である。

本書の構成
----------

本書の構成を次の表に示す。第 2 章から第 3 章で準備を整え、第 4 章から第 9 章で描き方を学び、第 10 章で Python による後処理を扱う。

.. list-table:: 本書の構成
   :header-rows: 1
   :widths: 10 25 65

   * - 章
     - タイトル
     - 内容
   * - 1
     - はじめに
     - 本書の目的、構成、サンプルコードの使い方
   * - 2
     - ドット絵とは
     - ピクセルと解像度、代表的な大きさ、拡大の方法
   * - 3
     - 道具を準備する
     - エディタの選び方と設定、保存形式
   * - 4
     - 線を描く
     - きれいな直線と曲線、避けるべき線
   * - 5
     - 色を選ぶ
     - パレットとカラーランプ、色相をずらす方法
   * - 6
     - 陰影と立体感
     - 光源、陰とハイライト、ディザリング、アンチエイリアス
   * - 7
     - キャラクターを描く
     - シルエットから仕上げまでの手順、アウトライン
   * - 8
     - タイルと背景
     - 継ぎ目の無いタイル、マップの組み立て
   * - 9
     - アニメーション
     - フレームとタイミング、スプライトシート
   * - 10
     - Python で後処理する
     - 拡大、減色、検査などの自動化

巻末には\ :doc:`用語集 <glossary>`\ と\ :doc:`参考文献 <references>`\ を付けた。本文中の用語のリンクから用語集の説明を参照できる。

制作の流れ
----------

本書で扱うドット絵の制作の流れを次の図に示す。第 4 章から第 9 章は、おおむねこの順に並んでいる。

.. graphviz::
   :caption: ドット絵の制作の流れ
   :align: center

   digraph flow {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#e8ecf0", color="#222034", fontsize=11];
       edge [color="#222034"];
       plan [label="大きさと\nパレットを決める"];
       silhouette [label="シルエットを\n描く"];
       line [label="線を整える"];
       color [label="基本色を塗る"];
       shade [label="陰影を付ける"];
       polish [label="仕上げ\n（アウトライン調整）"];
       export [label="書き出し・\n後処理"];
       plan -> silhouette -> line -> color -> shade -> polish -> export;
   }

一度で完成させる必要は無い。陰影を付けてから形を直したり、配色を変えたりするのは普通のことである。ただし、前の段階に戻るほど修正の手間が増えるため、シルエットと配色はなるべく早い段階で固めておくとよい。

サンプルコード
--------------

本書のサンプルコードは次の表のとおりである。各ファイルはリンクからダウンロードできる。すべてをまとめた :download:`examples.zip <_generated/examples.zip>` も用意した。

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - :download:`sprite_data.py <../examples/sprite_data.py>`
     - 本書で使うドット絵のデータ（他のサンプルから利用する）
     - 2、7、9
   * - :download:`scale_nearest.py <../examples/scale_nearest.py>`
     - 整数倍に拡大する
     - 2、10
   * - :download:`bresenham_line.py <../examples/bresenham_line.py>`
     - ブレゼンハムのアルゴリズムで直線を描く
     - 4
   * - :download:`make_palette.py <../examples/make_palette.py>`
     - 色相をずらしたカラーランプを作る
     - 5
   * - :download:`tile_preview.py <../examples/tile_preview.py>`
     - タイルを敷き詰めて継ぎ目を確認する
     - 8
   * - :download:`sprite_sheet.py <../examples/sprite_sheet.py>`
     - スプライトシートと GIF アニメーションを作る
     - 9
   * - :download:`pyxel_walk.py <../examples/pyxel_walk.py>`
     - Pyxel で歩行アニメーションを再生する
     - 9
   * - :download:`check_sprite.py <../examples/check_sprite.py>`
     - 色数や半透明のピクセルを検査する
     - 10
   * - :download:`reduce_colors.py <../examples/reduce_colors.py>`
     - 画像を縮小・減色して下書きを作る
     - 10
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定
     - －

サンプルコードは Pillow を使う。``pyxel_walk.py`` だけは Pyxel も使う。次のようにインストールする。

.. code-block:: console
   :linenos:

   python -m pip install pillow pyxel

サンプルコードは、すべてのファイルを同じフォルダに置き、そのフォルダをカレントディレクトリにして実行する。出力は ``output`` フォルダに保存される。

.. code-block:: console
   :linenos:

   cd examples
   python sprite_data.py
   python scale_nearest.py

サンプルコードには型ヒントを付けてあり、``examples`` フォルダで ``python -m flake8`` と ``python -m mypy .`` を実行すると、``setup.cfg`` の設定（行長 120 文字、mypy の ``strict`` モード）で検査できる。

動作確認環境
------------

本書のサンプルコードと図は、次の環境で動作を確認した。

.. list-table:: 動作確認環境
   :header-rows: 1
   :widths: 40 60

   * - ソフトウェア
     - バージョン
   * - Windows
     - 11
   * - Python
     - 3.14.6
   * - Pillow
     - 13.0.0
   * - Pyxel
     - 2.9.9
   * - matplotlib（図の作成のみ）
     - 3.11.2
   * - Sphinx（本書のビルドのみ）
     - 9.1.0

表記について
------------

本書では、画像を構成する最小の単位を「ピクセル」と呼ぶ。「ドット」は「ドット絵」や「ダブルドット」のような決まった言い方にだけ使う。また、図はすべて本書のために作成したもので、多くは拡大して表示している。図の説明で「8 倍」とある場合は、元のドット絵の 1 ピクセルを 8×8 ピクセルの正方形で表示していることを表す。
