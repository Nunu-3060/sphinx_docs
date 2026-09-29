Animator Controller で状態を管理する
====================================

この章では、Animator Controller を使って、状況に応じて再生する Animation Clip を切り替える方法を説明する。例として、キャラクターの待機（Idle）、歩行（Walk）、走行（Run）、攻撃（Attack）を切り替える Animator Controller を作成する。

ステートとステートマシン
------------------------

Animator Controller は、ステートマシンによってアニメーションの状態を管理する。ステートマシンとは、あらかじめ決めた状態（ステート）の中から現在の状態を 1 つ選び、条件に応じて別の状態へ移る仕組みである。Animator Controller では、各ステートに再生する Animation Clip を割り当てる。

Animator Controller は Animator ウィンドウで編集する。Animator ウィンドウは、メニューの Window > Animation > Animator で開く。Project ウィンドウで Animator Controller をダブルクリックしても開ける。

Animator ウィンドウには、作成したステートのほかに、次の特別なノードが表示される。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ノード
     - 役割
   * - Entry
     - ステートマシンの入り口。ステートマシンに入ったとき、Entry からつながっているステート（既定のステート）へ移る。既定のステートはオレンジ色で表示される。
   * - Any State
     - 現在のステートに関係なく遷移させたい場合に使う。Any State から引いた遷移は、どのステートからでも発生する。
   * - Exit
     - ステートマシンの出口。後述する Sub-State Machine から親のステートマシンへ戻る場合に使う。

ステートを作成するには、Project ウィンドウから Animation Clip を Animator ウィンドウへドラッグする。Animation Clip が割り当てられたステートが作成される。空のステートを作成する場合は、Animator ウィンドウの空いている場所を右クリックし、Create State > Empty を選択する。空のステートを作成した場合は、Inspector ウィンドウの Motion に Animation Clip を指定する。

既定のステートを変更するには、ステートを右クリックして Set as Layer Default State を選択する。

パラメーター
------------

パラメーターは、スクリプトと Animator Controller の間で値を受け渡すための変数である。遷移の条件や、後述する Blend Tree のブレンドの割合に使う。パラメーターは Animator ウィンドウの左側の Parameters タブで、+ ボタンをクリックして追加する。

.. list-table::
   :header-rows: 1
   :widths: 15 40 45

   * - 型
     - 内容
     - 使用例
   * - Float
     - 小数の値
     - 移動の速さ、移動方向
   * - Int
     - 整数の値
     - 武器の種類、コンボの段数
   * - Bool
     - true または false
     - 接地しているか、しゃがんでいるか
   * - Trigger
     - 遷移に使われると自動的に false に戻る Bool
     - 攻撃、ジャンプ、被ダメージなど一度だけ起こる動作

この章の例では、次のパラメーターを追加する。

* Speed（Float）: 移動の速さ。0 で停止、0.5 で歩行、1 で走行を表す。
* Attack（Trigger）: 攻撃の開始を表す。

遷移
----

あるステートから別のステートへ移ることを遷移（Transition）という。遷移を作成するには、遷移元のステートを右クリックして Make Transition を選択し、遷移先のステートをクリックする。遷移は矢印で表示され、矢印をクリックすると Inspector ウィンドウで設定を変更できる。

遷移の条件
~~~~~~~~~~

遷移の条件は Inspector ウィンドウの Conditions で設定する。+ ボタンで条件を追加し、パラメーターと比較方法を選択する。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - パラメーターの型
     - 指定できる条件
   * - Float
     - Greater（より大きい）、Less（より小さい）
   * - Int
     - Greater、Less、Equals（等しい）、NotEqual（等しくない）
   * - Bool
     - true、false
   * - Trigger
     - Trigger が設定されていること

1 つの遷移に複数の条件を追加すると、すべての条件を満たしたときに遷移する。いずれかの条件を満たしたときに遷移させたい場合は、同じステート間に遷移を複数作成する。

遷移のタイミングと長さ
~~~~~~~~~~~~~~~~~~~~~~

Inspector ウィンドウの Settings では、遷移のタイミングと長さを設定する。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 内容
   * - Has Exit Time
     - 有効にすると、遷移元の Animation Clip が Exit Time で指定した位置まで再生されてから遷移する。新しく作成した遷移では有効になっている。
   * - Exit Time
     - Has Exit Time が有効な場合に、遷移を開始する再生位置。Animation Clip の長さを 1 とした割合で指定する。
   * - Fixed Duration
     - 有効にすると、Transition Duration を秒で指定する。無効にすると、遷移元の Animation Clip の長さを 1 とした割合で指定する。
   * - Transition Duration
     - 遷移元と遷移先のアニメーションをブレンドする時間。
   * - Transition Offset
     - 遷移先の Animation Clip を再生し始める位置。Animation Clip の長さを 1 とした割合で指定する。
   * - Interruption Source
     - 遷移中に、別の遷移による割り込みを許可するかどうか。

Has Exit Time の設定は、遷移の目的に応じて次のように使い分ける。

* 入力に即座に反応させたい遷移（待機から攻撃など）では、Has Exit Time を無効にし、条件を設定する。
* モーションを最後まで再生してから戻したい遷移（攻撃から待機など）では、Has Exit Time を有効にし、Exit Time を 1 付近に設定する。条件は設定しなくてよい。

Has Exit Time が無効で条件も無い遷移は無効となり、遷移は発生しない。

Interruption Source は次の値から選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 値
     - 割り込みできる遷移
   * - None
     - 割り込みを許可しない（既定値）。
   * - Current State
     - 遷移元のステートから出る遷移。
   * - Next State
     - 遷移先のステートから出る遷移。
   * - Current State Then Next State
     - 遷移元のステートから出る遷移を優先し、次に遷移先のステートから出る遷移。
   * - Next State Then Current State
     - 遷移先のステートから出る遷移を優先し、次に遷移元のステートから出る遷移。

作成例
~~~~~~

この章の例では、Locomotion と Attack の 2 つのステートを使う。Locomotion は、Speed の値に応じて Idle、Walk、Run をブレンドするステートであり、次の節で説明する Blend Tree として作成する。Attack は、攻撃の Animation Clip を割り当てたステートである。Locomotion を既定のステートにし、次の遷移を作成する。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 遷移
     - Has Exit Time
     - 条件
   * - Locomotion → Attack
     - 無効
     - Attack
   * - Attack → Locomotion
     - 有効（Exit Time 0.9）
     - なし

Blend Tree
----------

Blend Tree は、パラメーターの値に応じて複数の Animation Clip を混ぜ合わせて再生するステートである。たとえば、Speed が 0.25 のときは待機と歩行の中間、0.75 のときは歩行と走行の中間の動きになるため、速さの変化に合わせてモーションが滑らかに変化する。

1D の Blend Tree
~~~~~~~~~~~~~~~~

1 つのパラメーターでブレンドする Blend Tree を作成する手順は次のとおりである。

#. Animator ウィンドウの空いている場所を右クリックし、Create State > From New Blend Tree を選択する。
#. 作成されたステートの名前を Locomotion に変更し、ダブルクリックして Blend Tree の編集画面を開く。
#. Blend Tree のノードを選択し、Inspector ウィンドウで Blend Type を 1D、Parameter を Speed に設定する。
#. Motion の一覧の + ボタンから Add Motion Field を 3 回選択し、Idle、Walk、Run の Animation Clip を指定する。
#. Automate Thresholds を無効にし、各 Animation Clip の Threshold を 0、0.5、1 に設定する。

Threshold は、その Animation Clip だけが再生されるパラメーターの値である。パラメーターが 2 つの Threshold の間にあるときは、2 つの Animation Clip が距離に応じた割合でブレンドされる。

Blend Tree は、ブレンドする Animation Clip の再生位置を割合で同期させる。そのため、長さの異なる歩行と走行のモーションでも、足の運びがそろった状態でブレンドされる。ただし、各 Animation Clip の先頭で同じ側の足を踏み出しているなど、動きの周期がそろっている必要がある。

2D の Blend Tree
~~~~~~~~~~~~~~~~

2 つのパラメーター（例: 左右方向の移動量と前後方向の移動量）でブレンドする場合は、Blend Type に 2D の種類を選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Blend Type
     - 用途
   * - 2D Simple Directional
     - 前・後・左・右のように、方向ごとに Animation Clip が 1 つずつある場合。
   * - 2D Freeform Directional
     - 同じ方向に速さの異なる Animation Clip（歩行と走行など）がある場合。
   * - 2D Freeform Cartesian
     - 2 つのパラメーターが方向を表さない場合（前進の速さと旋回の速さなど）。
   * - Direct
     - Animation Clip ごとに用意したパラメーターで、それぞれの重みを直接指定する場合。表情のブレンドなどに使う。

レイヤーと Avatar Mask
----------------------

「走りながら手を振る」のように、体の部位ごとに別のアニメーションを再生したい場合は、レイヤーを使う。レイヤーは Animator ウィンドウの左側の Layers タブで追加する。上にあるレイヤーから順に処理され、下にあるレイヤーほど後から適用される。

レイヤー名の右にある歯車のアイコンをクリックすると、次の設定を変更できる。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 項目
     - 内容
   * - Weight
     - レイヤーの影響度。0 で無効、1 で最大となる。最初のレイヤー（Base Layer）の Weight は常に 1 である。
   * - Mask
     - レイヤーの影響を受ける部位を指定する Avatar Mask。
   * - Blending
     - Override は下のレイヤーのアニメーションを置き換える。Additive は下のレイヤーのアニメーションに加算する。
   * - Sync
     - ほかのレイヤーと同じステートマシンの構造を使い、Animation Clip だけを差し替える。負傷時の歩き方のように、構造が同じで動きだけが異なる場合に使う。
   * - IK Pass
     - 有効にすると、このレイヤーで OnAnimatorIK が呼び出される。第 7 章で使用する。

Avatar Mask は、Project ウィンドウの右クリックメニューの Create > Avatar Mask で作成する。Humanoid の項目では、人型の図の部位をクリックして、影響を受ける部位（緑色）と受けない部位（赤色）を切り替える。Humanoid 以外のモデルでは、Transform の項目でボーンごとに指定する。

上半身だけに手を振るアニメーションを適用する場合は、次のように設定する。

#. 下半身（脚と足元の IK）を赤色にした Avatar Mask を作成する。
#. Animator Controller にレイヤーを追加し、Weight を 1、Mask に作成した Avatar Mask、Blending を Override に設定する。
#. 追加したレイヤーに、手を振る Animation Clip のステートを作成する。

レイヤーの Weight はスクリプトから ``Animator.SetLayerWeight`` で変更できる。手を振り始めるときに 0 から 1 へ徐々に変化させると、自然に動作を重ねられる。

Sub-State Machine
-----------------

ステートが増えると Animator ウィンドウが見づらくなる。関連するステートをまとめるには Sub-State Machine を使う。Animator ウィンドウの空いている場所を右クリックし、Create Sub-State Machine を選択すると作成できる。

Sub-State Machine をダブルクリックすると、その中のステートを編集できる。Sub-State Machine の中から親のステートマシンへ戻るには、Exit ノードへ遷移させる。Exit ノードへ遷移すると、親のステートマシンで Sub-State Machine から出る遷移が評価される。

たとえば、ジャンプの開始・上昇・落下・着地の 4 つのステートを Jump という Sub-State Machine にまとめると、親のステートマシンには Locomotion、Attack、Jump の 3 つだけが表示され、全体の構造を把握しやすくなる。
