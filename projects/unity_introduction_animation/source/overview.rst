Unity のアニメーションの全体像
==============================

この章では、Unity でアニメーションを実現する方法を概観し、以降の章で扱う機能の関係を整理する。

アニメーションを実現する方法
----------------------------

Unity で GameObject を動かす方法は、大きく次の 3 つに分けられる。

スクリプト
   C# スクリプトの ``Update`` メソッドなどで、毎フレーム Transform の位置や回転を書き換える方法である。移動量をプログラムで計算するため、入力や物理演算の結果に応じて動きを変えやすい。第 3 章で扱う。

Animation Clip と Animator
   あらかじめ作成した動きのデータ（Animation Clip）を、Animator コンポーネントで再生する方法である。キャラクターの歩行や攻撃など、形の決まった動きに向いている。第 4 章から第 7 章で扱う。

Timeline
   複数の GameObject のアニメーション、音、表示の切り替えなどを 1 本の時間軸上に並べて再生する方法である。カットシーンや演出に向いている。第 8 章で扱う。

これらは排他的なものではなく、組み合わせて使うことが多い。たとえば、キャラクターの動作は Animator で再生し、移動方向はスクリプトで制御し、イベントシーンでは Timeline で制御するといった使い方をする。

Animator の構成要素
-------------------

Unity のアニメーションシステムは Mecanim とも呼ばれ、次の要素で構成される。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 要素
     - 役割
   * - Animation Clip
     - 時間の経過に伴うプロパティの変化を記録したアセット。拡張子は .anim である。FBX などのモデルファイルに含まれる場合もある。
   * - Animator Controller
     - どの Animation Clip をどの条件で再生するかを、ステートマシンとして定義したアセット。拡張子は .controller である。
   * - Animator コンポーネント
     - GameObject に追加して、Animator Controller に従って Animation Clip を再生するコンポーネント。
   * - Avatar
     - モデルの骨格（ボーン）の構造を Unity が理解できる形に対応付けたデータ。人型キャラクターのアニメーションを別のモデルに流用する場合に必要となる。

これらの関係を図で表すと次のようになる。

.. code-block:: text

   GameObject
    └─ Animator コンポーネント
         ├─ Controller : Animator Controller（.controller）
         │    └─ ステートマシン
         │         ├─ ステート「Idle」 → Animation Clip（Idle.anim）
         │         ├─ ステート「Walk」 → Animation Clip（Walk.anim）
         │         └─ ステート「Jump」 → Animation Clip（Jump.anim）
         └─ Avatar : Avatar（人型キャラクターの場合）

Animator コンポーネントは、Animator Controller に定義されたステートマシンに従って現在のステートを決め、そのステートに割り当てられた Animation Clip を再生する。スクリプトは Animator コンポーネントのパラメーターを変更することで、ステートの切り替えを指示する。

Legacy Animation との違い
-------------------------

Unity には、Animator より前から存在する Animation コンポーネントもある。これは Legacy Animation と呼ばれ、ステートマシンを持たず、スクリプトから Animation Clip を名前で指定して再生する仕組みである。

Legacy Animation は現在も使用できるが、Humanoid のリターゲットやレイヤーなどの機能を使えない。新しく作成するアニメーションには Animator を使うことを勧める。本書でも Legacy Animation は扱わない。

どの方法を選ぶべきか
--------------------

用途ごとの選び方の目安を次の表に示す。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 用途
     - 推奨する方法
     - 理由
   * - 回転し続けるアイテム、上下に揺れる床
     - スクリプト
     - 動きが単純で、数式で表せるため。
   * - 開閉する扉、点滅するランプ
     - Animation Clip と Animator
     - 動きをエディター上で見ながら調整できるため。
   * - キャラクターの待機・歩行・攻撃
     - Animation Clip と Animator
     - 状態に応じたモーションの切り替えを、ステートマシンで管理できるため。
   * - 入力に応じたキャラクターの移動
     - スクリプトと Animator の併用
     - 移動方向や速度はスクリプトで計算し、モーションの切り替えは Animator に任せるため。
   * - カメラワークを伴うイベントシーン
     - Timeline
     - 複数のオブジェクト、カメラ、音を同じ時間軸で同期させられるため。
