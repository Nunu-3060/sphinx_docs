ゲームをシステムとして捉える
============================

ゲームは、状態と、状態を変える規則と、プレイヤーの入力からなるシステムである。この見方はエンジニアにはなじみやすく、ゲームの構造を図や数式やプログラムで表して検討できるという利点がある。この章では、コアループ、状態機械、資源の流れ、フィードバックループという 4 つの道具でゲームの構造を表す方法を学ぶ。

コアループ
----------

プレイヤーがゲームの中で何度も繰り返す一連の行動を、コアループと呼ぶ。コアループはゲームの遊びの中心であり、「このゲームは何をするゲームか」に対する最も短い答えである。

例えば、敵を倒して成長するアクション RPG のコアループは次のように表せる。

.. graphviz::
   :caption: アクション RPG のコアループ
   :align: center

   digraph core_loop {
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       explore [label="探索する"];
       fight [label="敵と戦う"];
       reward [label="経験値と\nアイテムを得る"];
       grow [label="キャラクターを\n強化する"];
       explore -> fight -> reward -> grow -> explore;
   }

コアループを図にすると、次の点を確認できる。

* ループの各段階に、プレイヤーが判断する余地や上達する余地があるか。
* 1 周にかかる時間は適切か。アクションゲームなら数秒から数十秒、ストラテジーゲームなら数分から数十分と、ジャンルによって大きく異なる。
* 1 周するたびに何かが変わるか。同じことの繰り返しに見えても、キャラクターが強くなる、新しい場所に行けるなどの変化があると、プレイヤーは繰り返しに飽きにくい。

入れ子になったループ
~~~~~~~~~~~~~~~~~~~~

多くのゲームは、時間の長さが異なる複数のループを入れ子にしている。

.. graphviz::
   :caption: 時間の長さが異なるループの入れ子
   :align: center

   digraph nested_loops {
       rankdir=LR;
       node [shape=box, style="rounded,filled"];
       subgraph cluster_meta {
           label="メタループ（数時間〜）";
           style="rounded"; color="#a0a0a0";
           subgraph cluster_session {
               label="二次ループ（数分〜数十分）";
               color="#7090c0";
               subgraph cluster_core {
                   label="コアループ（数秒〜数十秒）";
                   color="#c07070";
                   move [label="移動", fillcolor="#fbeeee"];
                   attack [label="攻撃", fillcolor="#fbeeee"];
                   move -> attack -> move;
               }
               clear [label="レベルを\nクリアする", fillcolor="#eef3fb"];
               equip [label="装備を\n整える", fillcolor="#eef3fb"];
               attack -> clear -> equip;
           }
           story [label="物語を\n進める", fillcolor="#f3f3f3"];
           unlock [label="新しい地域が\n開放される", fillcolor="#f3f3f3"];
           equip -> story -> unlock;
       }
   }

一番内側のコアループが面白くなければ、外側のループをどれだけ作り込んでもゲームは面白くならない。設計と試作は、まずコアループから始めるのが原則である。外側のループは、コアループに変化と目標を与え、長く遊び続ける理由を作る役割を持つ。

状態機械
--------

ゲームの多くの部分は、有限状態機械で表せる。有限状態機械は、状態遷移図として図に描ける。有限状態機械は、有限個の状態と、どのイベントでどの状態に移るかを表す遷移からなる。ゲームでは、画面の遷移やキャラクターの行動の管理によく使われる。

次の図は、ゲームの画面の遷移を表したものである。

.. graphviz::
   :caption: ゲーム画面の状態遷移
   :align: center

   digraph scenes {
       rankdir=LR;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       start [shape=point, width=0.15];
       TITLE [label="タイトル"];
       PLAYING [label="プレイ中"];
       PAUSED [label="ポーズ"];
       GAME_OVER [label="ゲームオーバー"];
       start -> TITLE;
       TITLE -> PLAYING [label="START"];
       PLAYING -> PAUSED [label="PAUSE"];
       PAUSED -> PLAYING [label="RESUME"];
       PLAYING -> GAME_OVER [label="PLAYER_DIED"];
       GAME_OVER -> TITLE [label="CONFIRM"];
   }

この状態遷移を Python で書いたものが :numref:`list-state-machine` である。遷移を辞書（遷移表）で表しているので、表に無い組み合わせのイベントは自動的に無視される。例えば、ポーズ中に「プレイヤーが倒された」というイベントが届いても、ゲームオーバーにはならない。

.. literalinclude:: ../examples/state_machine.py
   :language: python
   :linenos:
   :caption: state_machine.py（画面の状態遷移）
   :name: list-state-machine

実行すると次のように表示される。

.. code-block:: text
   :linenos:

   開始: TITLE
   PLAYER_DIED : TITLE のまま（無視）
   START       : TITLE -> PLAYING
   PAUSE       : PLAYING -> PAUSED
   PLAYER_DIED : PAUSED のまま（無視）
   RESUME      : PAUSED -> PLAYING
   PLAYER_DIED : PLAYING -> GAME_OVER
   CONFIRM     : GAME_OVER -> TITLE

状態機械で設計を表すと、「この状態でこのイベントが起きたらどうなるか」をすべての組み合わせについて検討できる。仕様の抜けや矛盾を早い段階で見つけられるので、デザイナーとプログラマーの間で仕様を確認する道具としても有効である。

キャラクターの状態
~~~~~~~~~~~~~~~~~~

キャラクターの行動も状態機械で表せる。次の図は、横スクロールのアクションゲームのキャラクターの例である。

.. graphviz::
   :caption: キャラクターの状態遷移
   :align: center

   digraph character {
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb"];
       idle [label="立ち"];
       run [label="走り"];
       jump [label="上昇"];
       fall [label="落下"];
       damage [label="やられ"];
       idle -> run [label="左右キー"];
       run -> idle [label="キーを離す"];
       idle -> jump [label="ジャンプ"];
       run -> jump [label="ジャンプ"];
       run -> fall [label="足場から出る"];
       jump -> fall [label="速度が下向き"];
       fall -> idle [label="着地"];
       idle -> damage [label="敵に触れる"];
       run -> damage;
       jump -> damage;
       fall -> damage;
   }

図にすると「落下中にジャンプボタンを押したらどうなるか」「やられ状態から戻るのはどの状態か」といった、仕様で決めるべき点が見えてくる。落下中のジャンプは、第 7 章で扱うコヨーテタイムや先行入力の設計に関わる。

資源の流れ
----------

多くのゲームには、金貨、体力、弾薬、木材のように、増えたり減ったりする量（資源）がある。資源の増減を流れとして図に表すと、ゲームの経済を設計しやすくなる。ゲームデザイナーのヨリス・ドルマンスは、こうした図を描いてシミュレーションするための記法「Machinations」を提案した。ここでは、その考え方を借りて、資源の流れを次の 4 つの要素で表す。

.. list-table:: 資源の流れを表す要素
   :header-rows: 1
   :widths: 20 45 35

   * - 要素
     - 意味
     - 例
   * - ソース（湧き出し口）
     - 資源を生み出す
     - 敵を倒すと金貨が出る。時間とともに体力が回復する
   * - プール（貯まる場所）
     - 資源を貯めておく
     - 所持金、所持アイテム、体力の残量
   * - シンク（吸い込み口）
     - 資源を消す
     - 店での買い物、修理費、ダメージ
   * - 変換器
     - ある資源を別の資源に変える
     - 鉱石を武器に加工する。経験値でスキルを習得する

.. graphviz::
   :caption: RPG の金貨の流れ
   :align: center

   digraph economy {
       rankdir=LR;
       node [style=filled];
       enemy [label="敵を倒す\n（ソース）", shape=triangle, fillcolor="#d8f0d8"];
       quest [label="依頼の報酬\n（ソース）", shape=triangle, fillcolor="#d8f0d8"];
       wallet [label="所持金\n（プール）", shape=circle, fillcolor="#fff4c8"];
       shop [label="武器を買う\n（変換器）", shape=box, fillcolor="#eef3fb"];
       inn [label="宿代・修理費\n（シンク）", shape=invtriangle, fillcolor="#f8dada"];
       power [label="攻撃力\n（プール）", shape=circle, fillcolor="#fff4c8"];
       enemy -> wallet;
       quest -> wallet;
       wallet -> shop;
       shop -> power;
       wallet -> inn;
       power -> enemy [style=dashed, label="倒す速さが上がる"];
   }

ソースとシンクのつり合いが崩れると、ゲームの経済は破綻する。ソースが強すぎると資源が余り、買い物で悩むという選択の面白さが失われる。オンラインゲームでは、プレイヤー全体の通貨が増え続けて物価が上がるインフレーションがよく問題になる。逆にシンクが強すぎると、プレイヤーは常に資源不足に悩まされ、窮屈に感じる。

フィードバックループ
--------------------

上の図で、攻撃力から「敵を倒す」へ戻る点線の矢印に注目してほしい。金貨で強い武器を買うと敵を速く倒せるようになり、さらに金貨が貯まりやすくなる。このように、ある量の変化が巡り巡って同じ量をさらに変化させる構造を、フィードバックループと呼ぶ。

.. list-table:: 2 種類のフィードバックループ
   :header-rows: 1
   :widths: 20 40 40

   * - 種類
     - 働き
     - 例
   * - 正のフィードバック
     - 差を広げる。勝っている側がさらに有利になる
     - モノポリーで土地を多く持つ人ほど収入が増え、さらに土地を買える
   * - 負のフィードバック
     - 差を縮める。負けている側が追いつきやすくなる
     - レースゲームで後ろを走るほど強いアイテムが出る

正のフィードバックは、ゲームを決着に向かわせる力になる。序盤の小さな有利が拡大していく感覚は気持ちがよく、ゲームが際限なく長引くことも防ぐ。しかし強すぎると、序盤で勝負が決まり、負けている側は残りの時間を消化試合として過ごすことになる。

負のフィードバックは、ゲームを接戦に保つ力になる。最後まで逆転の可能性が残るので、全員が最後まで真剣に遊べる。しかし強すぎると、序盤にどれだけ頑張っても結果に影響しなくなり、努力が報われないと感じさせる。負けている側を助ける仕組みは、輪ゴムで引き戻すような働きにたとえてラバーバンドとも呼ばれる。

シミュレーションで確かめる
~~~~~~~~~~~~~~~~~~~~~~~~~~

フィードバックの効果は、シミュレーションで確かめるとよく分かる。:numref:`list-resource-flow` は、2 人のプレイヤーが毎ターンさいころを振って金貨を得るという単純な経済で、次の 3 つのルールを比べるプログラムである。

* **fixed**：収入はさいころの目だけ（フィードバックなし）
* **positive**：所持金の 10 % が利子として増える（正のフィードバック）
* **rubber**：positive に加え、負けている側が差の 20 % を補助として受け取る（負のフィードバック）

.. literalinclude:: ../examples/resource_flow.py
   :language: python
   :lineno-match:
   :lines: 23-70
   :caption: resource_flow.py（ルールとシミュレーションの部分）
   :name: list-resource-flow

各ルールで 2000 回ずつゲームを行い、ターンごとの所持金の差を平均した結果が次の図である。

.. figure:: /_generated/resource_flow.png
   :alt: フィードバックループと所持金の差
   :align: center

   フィードバックループと所持金の差

フィードバックの無いルールでは、差はさいころの運によって少しずつ広がる程度である。正のフィードバックを加えると、運によって生じた小さな差が利子によって拡大し、30 ターン後には 7 倍近い差になる。負のフィードバックを組み合わせると、差はほとんど広がらなくなる。

どれが正しいということはなく、作りたい体験によって選ぶ。運よりも戦略で決着してほしいなら正のフィードバックを抑えめにし、接戦を楽しんでほしいなら負のフィードバックを加える。重要なのは、こうした効果を「なんとなく」ではなく、シミュレーションで数値として確かめられることである。

創発
----

少数の単純なルールが組み合わさって、ルールからは直接予想できない複雑な振る舞いが生じることを、創発と呼ぶ。囲碁のルールは数行で説明できるが、そこから生まれる戦略は何千年もの間研究されても尽きない。

研究者のユールは、ゲームの構造を 2 つの型に分けた。

.. list-table:: 創発型と進行型
   :header-rows: 1
   :widths: 20 45 35

   * - 型
     - 特徴
     - 例
   * - 創発型
     - 少数のルールの組み合わせから多様な状況が生まれる。遊ぶたびに展開が変わる
     - 囲碁、将棋、テトリス、多くの対戦ゲーム
   * - 進行型
     - デザイナーが用意した出来事を順番に体験していく。展開はほぼ決まっている
     - 物語を重視したアドベンチャーゲーム

多くのビデオゲームは両方の要素を持つ。アクションゲームのレベルは、デザイナーが用意した順番で進む（進行型）が、敵とプレイヤーの動きの組み合わせはその場で生まれる（創発型）。

創発は、デザイナーが予想しなかった面白い遊びを生む源泉である。一方で、予想しなかった攻略法（バランスを壊す必勝法や、レベルの一部を飛ばす近道）も生む。ルールを組み合わせたときにどのような振る舞いが起きうるかを、実際に遊んだりシミュレーションしたりして確かめることが欠かせない。

演習
----

#. 好きなゲームのコアループを図に描け。入れ子になった外側のループがあれば、それも描け。
#. 同じゲームの資源を 1 つ選び、ソース、プール、シンク、変換器を書き出せ。
#. :numref:`list-resource-flow` の ``INTEREST_RATE`` と ``CATCH_UP_RATE`` を変えて実行し、所持金の差がどう変わるかを確かめよ。差がほとんど広がらず、それでいて先行した側がわずかに有利であり続けるような値を探せ。
#. 正のフィードバックが強すぎて、序盤で勝負が決まってしまうゲームの例を挙げ、負のフィードバックを加える方法を提案せよ。
