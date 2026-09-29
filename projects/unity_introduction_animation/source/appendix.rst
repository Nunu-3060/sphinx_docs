付録
====

用語集
------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 用語
     - 意味
   * - Animation Clip
     - 時間の経過に伴うプロパティの変化を記録したアセット。
   * - Animation Event
     - Animation Clip の指定した時刻にスクリプトのメソッドを呼び出す仕組み。
   * - Animator コンポーネント
     - Animator Controller に従って Animation Clip を再生するコンポーネント。
   * - Animator Controller
     - 再生する Animation Clip と、その切り替えの条件をステートマシンで定義したアセット。
   * - Avatar
     - モデルのボーンと Unity の標準的な人型の骨格との対応付け。
   * - Avatar Mask
     - アニメーションの影響を受ける部位を指定するアセット。
   * - Blend Tree
     - パラメーターの値に応じて複数の Animation Clip をブレンドするステート。
   * - IK（Inverse Kinematics）
     - 手先や足先の目標位置から、途中の関節の回転を計算する方法。
   * - Root Motion
     - アニメーションに含まれる、キャラクター全体の移動と回転。
   * - Timeline
     - トラックにクリップを並べ、複数のオブジェクトの演出を同じ時間軸で再生する機能。
   * - イージング
     - 補間の割合を関数で変換し、動きに緩急を付けること。
   * - キーフレーム
     - ある時刻におけるプロパティの値。キーフレームの間は補間される。
   * - ステート
     - ステートマシンにおける状態。Animator Controller では、再生する Animation Clip を割り当てる。
   * - 接線（Tangent）
     - キーフレームを通過するときのカーブの傾き。
   * - 遷移（Transition）
     - あるステートから別のステートへ移ること。
   * - パラメーター
     - スクリプトと Animator Controller の間で値を受け渡すための変数。
   * - 補間
     - 2 つの値の間の値を、割合を指定して求めること。
   * - リターゲット
     - あるモデル用に作られた Humanoid のアニメーションを、別のモデルで再生すること。

サンプルコード一覧
------------------

本書のサンプルコードの一覧を次に示す。ファイル名をクリックするとダウンロードできる。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - ファイル
     - 章
     - 内容
   * - :download:`MoveWithDeltaTime.cs <../examples/MoveWithDeltaTime.cs>`
     - 第 3 章
     - Time.deltaTime を使った等速の移動
   * - :download:`LerpMover.cs <../examples/LerpMover.cs>`
     - 第 3 章
     - 線形補間による移動と回転
   * - :download:`EasingMover.cs <../examples/EasingMover.cs>`
     - 第 3 章
     - イージング関数による往復の移動
   * - :download:`CurveMover.cs <../examples/CurveMover.cs>`
     - 第 3 章
     - AnimationCurve による上下の移動
   * - :download:`CoroutineBlink.cs <../examples/CoroutineBlink.cs>`
     - 第 3 章
     - コルーチンによる点滅
   * - :download:`FootstepEvent.cs <../examples/FootstepEvent.cs>`
     - 第 4 章
     - Animation Event による足音の再生
   * - :download:`PlayerAnimatorController.cs <../examples/PlayerAnimatorController.cs>`
     - 第 6 章
     - キーボード入力による Blend Tree のパラメーターの更新
   * - :download:`AttackTrigger.cs <../examples/AttackTrigger.cs>`
     - 第 6 章
     - Trigger による遷移と、CrossFadeInFixedTime による直接の切り替え
   * - :download:`StateLogger.cs <../examples/StateLogger.cs>`
     - 第 6 章
     - StateMachineBehaviour によるステートの出入りのログ出力
   * - :download:`RootMotionHandler.cs <../examples/RootMotionHandler.cs>`
     - 第 6 章
     - OnAnimatorMove による Root Motion の適用
   * - :download:`LookAtIK.cs <../examples/LookAtIK.cs>`
     - 第 7 章
     - IK による視線と右手の制御
   * - :download:`CutsceneController.cs <../examples/CutsceneController.cs>`
     - 第 8 章
     - Timeline の再生と Signal の受信

サンプルコードの書式は、次の EditorConfig の設定に従っている。

:download:`.editorconfig をダウンロード <../examples/.editorconfig>`

参考資料
--------

Unity の公式ドキュメントのうち、本書の内容に関係するページを次に示す。

* `Unity マニュアル: アニメーション <https://docs.unity3d.com/ja/6000.0/Manual/AnimationOverview.html>`_
* `Unity マニュアル: Animator Controller <https://docs.unity3d.com/ja/6000.0/Manual/class-AnimatorController.html>`_
* `Unity マニュアル: Root Motion <https://docs.unity3d.com/ja/6000.0/Manual/RootMotion.html>`_
* `Unity マニュアル: インバースキネマティクス <https://docs.unity3d.com/ja/6000.0/Manual/InverseKinematics.html>`_
* `スクリプトリファレンス: Animator <https://docs.unity3d.com/ja/6000.0/ScriptReference/Animator.html>`_
* `スクリプトリファレンス: StateMachineBehaviour <https://docs.unity3d.com/ja/6000.0/ScriptReference/StateMachineBehaviour.html>`_
* `スクリプトリファレンス: AnimationCurve <https://docs.unity3d.com/ja/6000.0/ScriptReference/AnimationCurve.html>`_
* `Timeline パッケージのマニュアル（英語） <https://docs.unity3d.com/Packages/com.unity.timeline@1.8/manual/index.html>`_
* `Animation Rigging パッケージのマニュアル（英語） <https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/index.html>`_
* `Input System パッケージのマニュアル（英語） <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/index.html>`_
