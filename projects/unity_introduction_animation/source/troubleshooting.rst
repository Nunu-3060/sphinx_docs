パフォーマンスとトラブルシューティング
======================================

この章では、アニメーションの処理負荷を抑えるための設定と、アニメーションを扱う際によく起こる問題の原因と対処を説明する。

処理負荷を抑える設定
--------------------

Animator は、キャラクターの数が多いほど処理負荷が大きくなる。次の設定で負荷を抑えられる。

Culling Mode
~~~~~~~~~~~~

Animator コンポーネントの Culling Mode は、キャラクターが画面に映っていないときの動作を決める。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 画面外にあるときの動作
   * - Always Animate
     - 画面外でも常にアニメーションを更新する。既定値。
   * - Cull Update Transforms
     - ステートマシンの処理は続けるが、ボーンの Transform の更新、リターゲット、IK を省略する。
   * - Cull Completely
     - アニメーションの処理をすべて停止する。

Root Motion で移動するキャラクターに Cull Completely を設定すると、画面外にいる間は移動も止まる。画面外でも移動を続ける必要がある場合は、Cull Update Transforms を使う。

Update Mode
~~~~~~~~~~~

Animator コンポーネントの Update Mode は、アニメーションを更新するタイミングを決める。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 内容
   * - Normal
     - ``Update`` と同じタイミングで更新する。``Time.timeScale`` の影響を受ける。
   * - Fixed
     - 物理演算と同じタイミングで更新する。Rigidbody で動くキャラクターなど、物理演算と連動させる場合に使う。以前のバージョンでは Animate Physics という名前だった。
   * - Unscaled Time
     - ``Update`` と同じタイミングで更新するが、``Time.timeScale`` の影響を受けない。一時停止中に動かしたいメニュー画面の UI などに使う。

Optimize Game Objects
~~~~~~~~~~~~~~~~~~~~~

モデルファイルのインポート設定の Rig タブで Optimize Game Objects を有効にすると、ボーンの GameObject が Hierarchy ウィンドウから取り除かれ、ボーンの Transform を更新する負荷が減る。武器を持たせる手のボーンなど、スクリプトから参照したいボーンは Extra Transforms to Expose で個別に残せる。

その他の工夫
~~~~~~~~~~~~

* パラメーターやステートは、ハッシュ値で指定する（第 6 章を参照）。
* 使っていないレイヤーは Weight を 0 にする。レイヤーは数が多いほど処理負荷が増える。
* 動かす必要がなくなったキャラクターは、Animator コンポーネントを無効にする。

よくある問題と対処
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 症状
     - 主な原因
     - 対処
   * - アニメーションが再生されない。
     - Animator コンポーネントの Controller が未設定である。またはステートの Motion が未設定である。
     - Controller と、各ステートの Motion に Animation Clip が設定されているか確認する。
   * - 一部のプロパティだけ再生されない。
     - アニメーションさせている GameObject の名前や階層が変わった。
     - Animation ウィンドウで「(Missing!)」と表示されているプロパティを確認し、名前や階層を元に戻す。
   * - 入力してから動作が始まるまでに遅れがある。
     - 遷移の Has Exit Time が有効になっている。または Transition Duration が長い。
     - Has Exit Time を無効にし、Transition Duration を短くする。
   * - 攻撃ボタンを押していないのに攻撃が始まる。
     - 以前に設定した Trigger が、遷移に使われないまま残っている。
     - 不要になった時点で ``ResetTrigger`` を呼ぶ。
   * - Any State からの遷移で、同じモーションが先頭から繰り返し再生される。
     - 遷移の Can Transition To Self が有効になっている。
     - Can Transition To Self を無効にする。
   * - 移動するモーションがループのたびに元の位置へ戻る。
     - Apply Root Motion が無効で、Animation Clip の移動がそのまま姿勢として再生されている。
     - Apply Root Motion を有効にするか、Root Transform Position (XZ) の Bake Into Pose を有効にしてその場で再生し、移動はスクリプトで行う。
   * - 移動中に足が地面を滑って見える。
     - スクリプトによる移動の速さと、モーションの歩幅が一致していない。
     - Root Motion を使う。またはモーションの再生速度（ステートの Speed）を移動の速さに合わせる。
   * - あるステートで変更したプロパティが、別のステートに移っても元に戻らない。または予期せず元に戻る。
     - ステートの Write Defaults の設定が混在している。
     - Animator Controller 内のステートの Write Defaults を、すべて有効またはすべて無効にそろえる。
   * - ``OnAnimatorIK`` が呼び出されない。
     - レイヤーの IK Pass が無効である。またはモデルが Humanoid ではない。
     - IK Pass を有効にし、Animation Type が Humanoid であることを確認する。
   * - Animation Event で「has no receiver」というエラーが表示される。
     - 指定したメソッドを持つスクリプトが、Animator と同じ GameObject に追加されていない。
     - Animator と同じ GameObject にスクリプトを追加し、メソッド名が一致しているか確認する。
   * - キー入力の処理で InvalidOperationException が発生する。
     - Input System のみが有効なプロジェクトで、旧来の ``Input`` クラスを使用している。
     - Input System の API（``Keyboard.current`` など）を使用する。

Write Defaults は、ステートの Inspector ウィンドウにある設定である。有効な場合、そのステートでアニメーションしていないプロパティは既定値（Animator が初期化されたときの値）に戻される。無効な場合は、直前の値がそのまま残る。どちらが正しいということはないが、1 つの Animator Controller の中で混在させると動作を予測しにくくなる。
