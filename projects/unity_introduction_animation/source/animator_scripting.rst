スクリプトから Animator を制御する
==================================

第 5 章では、遷移の条件をパラメーターで指定した。この章では、スクリプトからパラメーターを変更してステートを切り替える方法と、Animator の状態をスクリプトで取得する方法を説明する。

パラメーターの設定
------------------

スクリプトから Animator を操作するには、まず ``GetComponent<Animator>()`` で Animator コンポーネントを取得する。取得は ``Awake`` や ``Start`` で一度だけ行い、フィールドに保存しておく。

パラメーターは、型に応じて次のメソッドで設定する。

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - 型
     - 設定するメソッド
     - 取得するメソッド
   * - Float
     - ``SetFloat``
     - ``GetFloat``
   * - Int
     - ``SetInteger``
     - ``GetInteger``
   * - Bool
     - ``SetBool``
     - ``GetBool``
   * - Trigger
     - ``SetTrigger``、``ResetTrigger``
     - なし

``SetFloat`` には、値を徐々に変化させるための引数 ``dampTime`` と ``deltaTime`` を指定できる。``animator.SetFloat("Speed", target, 0.1f, Time.deltaTime)`` と書くと、Speed はおよそ 0.1 秒かけて target に近づく。キーボードのように入力が 0 か 1 かで急に変わる場合でも、Blend Tree のブレンドが滑らかに変化する。

.. warning::

   Trigger は、遷移に使われるまで設定されたまま残る。攻撃できないステートにいる間に ``SetTrigger`` を呼ぶと、後で攻撃可能なステートに戻った瞬間に攻撃が始まることがある。不要になった Trigger は ``ResetTrigger`` で解除する。

パラメーターのハッシュ値
------------------------

パラメーターやステートは、名前の文字列の代わりにハッシュ値（名前から計算した整数）で指定できる。ハッシュ値は ``Animator.StringToHash`` で求める。

.. code-block:: csharp

   private static readonly int SpeedHash = Animator.StringToHash("Speed");

   // 文字列で指定する場合
   animator.SetFloat("Speed", 1f);

   // ハッシュ値で指定する場合
   animator.SetFloat(SpeedHash, 1f);

ハッシュ値で指定すると、呼び出しのたびに文字列からハッシュ値を計算する処理を省ける。また、パラメーター名の文字列がスクリプト中の 1 か所にまとまるため、名前を変更するときに修正漏れが起こりにくい。

次のサンプルは、キーボード入力から Speed を計算して設定する。第 5 章で作成した Locomotion の Blend Tree と組み合わせて使う。

.. literalinclude:: ../examples/PlayerAnimatorController.cs
   :language: csharp
   :caption: PlayerAnimatorController.cs

:download:`PlayerAnimatorController.cs をダウンロード <../examples/PlayerAnimatorController.cs>`

このサンプルはキャラクターの向きだけを変え、位置は動かさない。位置は、後述する Root Motion によってアニメーションから動かすか、スクリプトで別途動かす。

ステートを直接切り替える
------------------------

遷移を作成していないステートへも、スクリプトから直接切り替えられる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 内容
   * - ``Play``
     - 指定したステートへ即座に切り替える。ブレンドは行わない。
   * - ``CrossFade``
     - 指定したステートへブレンドしながら切り替える。ブレンドの時間は、遷移元の Animation Clip の長さを 1 とした割合で指定する。
   * - ``CrossFadeInFixedTime``
     - ``CrossFade`` と同じだが、ブレンドの時間を秒で指定する。

これらのメソッドは、被ダメージのようにどのステートからでも割り込ませたい動作に便利である。ただし、多用すると Animator ウィンドウを見ても実際の遷移が分からなくなる。通常の遷移は Animator Controller に定義し、直接の切り替えは例外的な場合に限るとよい。

現在のステートを取得する
------------------------

現在再生しているステートの情報は ``GetCurrentAnimatorStateInfo`` で取得する。引数にはレイヤーの番号を指定する（Base Layer は 0）。戻り値の ``AnimatorStateInfo`` には次の情報が含まれる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メンバー
     - 内容
   * - ``shortNameHash``
     - ステート名のハッシュ値。``Animator.StringToHash("Attack")`` と比較する。
   * - ``fullPathHash``
     - 「Base Layer.Attack」のように、レイヤー名を含むパスのハッシュ値。
   * - ``normalizedTime``
     - 再生位置。Animation Clip の長さを 1 とした割合で表す。ループするステートでは 1 を超えて増え続け、整数部がループした回数を表す。
   * - ``length``
     - ステートの長さ（秒）。
   * - ``IsName(名前)``
     - ステート名またはパスが一致する場合に true を返す。
   * - ``IsTag(タグ)``
     - ステートに設定したタグが一致する場合に true を返す。

遷移中かどうかは ``IsInTransition`` で確認し、遷移先のステートの情報は ``GetNextAnimatorStateInfo`` で取得する。

次のサンプルは、攻撃中は攻撃の入力を受け付けず、H キーで被ダメージのステートへ直接切り替える。

.. literalinclude:: ../examples/AttackTrigger.cs
   :language: csharp
   :caption: AttackTrigger.cs

:download:`AttackTrigger.cs をダウンロード <../examples/AttackTrigger.cs>`

.. note::

   Animator は、すべてのスクリプトの ``Update`` が呼ばれた後に更新される。そのため、``SetTrigger`` を呼んだ直後に同じ ``Update`` の中で ``GetCurrentAnimatorStateInfo`` を呼んでも、ステートはまだ切り替わっていない。

StateMachineBehaviour
---------------------

StateMachineBehaviour は、ステートに追加するスクリプトである。ステートに入ったとき、再生中、出たときにメソッドが呼び出されるため、「攻撃ステートの間だけ移動を禁止する」のように、ステートに連動した処理を書くのに向いている。

StateMachineBehaviour を継承したクラスを作成し、Animator ウィンドウでステートを選択して、Inspector ウィンドウの Add Behaviour から追加する。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 呼び出されるタイミング
   * - ``OnStateEnter``
     - ステートに入ったとき（遷移を開始したとき）
   * - ``OnStateUpdate``
     - ステートにいる間、毎フレーム
   * - ``OnStateExit``
     - ステートから出たとき（遷移が完了したとき）
   * - ``OnStateMove``
     - Root Motion の処理の直後
   * - ``OnStateIK``
     - IK の処理の直後

.. literalinclude:: ../examples/StateLogger.cs
   :language: csharp
   :caption: StateLogger.cs

:download:`StateLogger.cs をダウンロード <../examples/StateLogger.cs>`

.. note::

   StateMachineBehaviour は Animator Controller というアセットの一部として保存される。そのため、Inspector ウィンドウでシーン上の GameObject をフィールドに指定することはできない。シーン上のオブジェクトが必要な場合は、メソッドの引数で渡される ``animator`` から ``GetComponent`` などで取得する。

Root Motion
-----------

歩行や走行のモーションには、キャラクター全体が前へ進む動きが含まれていることが多い。この「キャラクター全体の移動と回転」を Root Motion という。Root Motion を使うと、足の動きと実際の移動量が一致するため、足が地面を滑るように見える現象を防げる。

Animator コンポーネントの Apply Root Motion を有効にすると、Animation Clip に含まれる移動と回転が GameObject の Transform に適用される。無効にすると、アニメーションはその場で再生され、移動はスクリプトで行う必要がある。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 項目
     - Root Motion で移動する
     - スクリプトで移動する
   * - 足の滑り
     - 起こりにくい
     - 移動速度とモーションが合わないと起こる
   * - 操作の反応
     - モーションに従うため遅れることがある
     - 入力に即座に反応させやすい
   * - 向いている場面
     - 移動量が重要なアクション（攻撃の踏み込み、回避など）
     - 操作性を重視するアクションゲームの移動

スクリプトで ``OnAnimatorMove`` メソッドを定義すると、Root Motion を自動で適用する代わりに、このメソッドが呼び出される。Animator の ``deltaPosition`` と ``deltaRotation`` には、そのフレームでアニメーションが動かそうとした移動量と回転量が入っているため、これを加工して適用できる。次のサンプルは、水平方向の移動は Root Motion に任せ、垂直方向は重力で計算して CharacterController で移動させる。

.. literalinclude:: ../examples/RootMotionHandler.cs
   :language: csharp
   :caption: RootMotionHandler.cs

:download:`RootMotionHandler.cs をダウンロード <../examples/RootMotionHandler.cs>`

Root Motion のうち、どの成分を移動として取り出すかは、Animation Clip のインポート設定の Root Transform Rotation、Root Transform Position (Y)、Root Transform Position (XZ) で指定する。各項目の Bake Into Pose を有効にすると、その成分は移動として取り出されず、姿勢の一部として再生される。たとえば、その場での足踏みのような上下の揺れは Position (Y) の Bake Into Pose を有効にして姿勢に含め、前進する動きは Position (XZ) の Bake Into Pose を無効にして移動として取り出す。
