人型キャラクターのアニメーション
================================

この章では、人型キャラクターのモデルとモーションを扱う方法を説明する。人型キャラクターでは、Humanoid という仕組みを使うと、あるモデル用に作られたモーションを別のモデルで再生できる。

Generic と Humanoid
-------------------

FBX などのモデルファイルを Project ウィンドウで選択すると、Inspector ウィンドウにインポート設定が表示される。Rig タブの Animation Type で、アニメーションの扱い方を選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Animation Type
     - 内容
   * - None
     - アニメーションを使用しない。
   * - Legacy
     - Legacy Animation（Animation コンポーネント）で使用する。
   * - Generic
     - ボーンの構造をそのまま使用する。人型以外のモデル（動物、機械など）に使う。
   * - Humanoid
     - ボーンを Unity の標準的な人型の骨格に対応付けて使用する。人型のモデルに使う。

Generic では、Animation Clip はボーンの名前と階層で記録されるため、同じボーン構造を持つモデルでしか再生できない。Humanoid では、Animation Clip は標準的な人型の骨格に対する動きとして記録されるため、ボーンの名前や比率が異なるモデルでも再生できる。

Avatar の設定とリターゲット
---------------------------

Animation Type を Humanoid にして Apply ボタンをクリックすると、モデルのボーンと人型の骨格の対応付け（Avatar）が自動的に作成される。Avatar Definition を Create From This Model にすると、このモデルから Avatar を作成する。同じボーン構造を持つ別のモデルの Avatar を使う場合は、Copy From Other Avatar を選ぶ。

Configure ボタンをクリックすると Avatar の設定画面が開き、ボーンの対応付けを確認・修正できる。人型の図で緑色の部位は正しく対応付けられており、赤色の部位は対応付けに問題がある。Humanoid として扱うには、腰、脊椎、頭、両腕、両脚など、最低 15 本の必須ボーンが対応付けられている必要がある。

ボーンが正しく対応付けられていれば、あるモデル用に作られた Humanoid の Animation Clip を、別の Humanoid のモデルでそのまま再生できる。この仕組みをリターゲットという。モーションをまとめて作成し、複数のキャラクターで共有できるため、制作の手間を大きく減らせる。

.. note::

   リターゲットでは、モデルの体形の違いによって、手が体に食い込んだり足が地面から浮いたりすることがある。その場合は、Avatar の設定画面の Muscles & Settings タブで関節の可動範囲を調整するか、後述する IK で手足の位置を補正する。

モーションの取り込み
--------------------

外部のツールで作成したモーションは、FBX ファイルとして取り込むことが多い。モデルファイルのインポート設定の Animation タブでは、ファイルに含まれるモーションを Animation Clip として取り出す設定を行う。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - Import Animation
     - 有効にすると、ファイルに含まれるアニメーションを取り込む。
   * - Clips
     - 取り出す Animation Clip の一覧。1 つのモーションを開始フレームと終了フレームで区切り、複数の Animation Clip に分割できる。
   * - Loop Time、Loop Pose
     - ループの設定。第 4 章で説明した設定と同じである。
   * - Root Transform の各項目
     - Root Motion として取り出す成分の設定。第 6 章で説明した設定と同じである。
   * - Mask
     - 取り込む部位を Avatar Mask で制限する。
   * - Events
     - Animation Event を追加する。

Loop Time を有効にすると、先頭と末尾の姿勢がどの程度一致しているかが、各項目の横に色付きの丸で表示される。緑色であれば、ループさせても継ぎ目が目立ちにくい。

モデルファイルに含まれる Animation Clip は読み取り専用であり、Animation ウィンドウで編集できない。編集したい場合は、Project ウィンドウでモデルファイル内の Animation Clip を選択し、Edit > Duplicate（Ctrl + D）で複製する。複製した Animation Clip は、独立した .anim ファイルとして編集できる。

IK による手足と視線の制御
-------------------------

通常のアニメーションは、腰から肩、肘、手首というように、親のボーンから順に回転を指定して手先の位置を決める。これを FK（Forward Kinematics）という。反対に、手先の目標位置を指定し、そこに届くように途中の関節の回転を計算する方法を IK（Inverse Kinematics）という。

IK を使うと、次のような処理をアニメーションに加えられる。

* 近くの物体の方へ顔や視線を向ける。
* ドアノブや手すりに手を合わせる。
* 段差や坂で、足を地面の高さに合わせる。

Humanoid のモデルでは、Animator の IK 機能を使える。IK の処理は ``OnAnimatorIK`` メソッドに書く。このメソッドは、Animator Controller のレイヤーの設定で IK Pass を有効にしたレイヤーでのみ呼び出される。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 内容
   * - ``SetLookAtWeight``
     - 視線の IK の影響度を設定する。体、頭、目それぞれの影響度も指定できる。
   * - ``SetLookAtPosition``
     - 視線を向ける位置を設定する。
   * - ``SetIKPositionWeight``、``SetIKRotationWeight``
     - 手足の IK の位置と回転の影響度を設定する。対象は ``AvatarIKGoal`` の LeftHand、RightHand、LeftFoot、RightFoot のいずれかで指定する。
   * - ``SetIKPosition``、``SetIKRotation``
     - 手足の目標の位置と回転を設定する。

影響度は 0 から 1 の値で指定し、0 ではアニメーションのまま、1 では目標の位置に完全に合わせる。影響度を 0 のままにすると、目標の位置を設定しても IK は働かない。

.. literalinclude:: ../examples/LookAtIK.cs
   :language: csharp
   :caption: LookAtIK.cs

:download:`LookAtIK.cs をダウンロード <../examples/LookAtIK.cs>`

発展: Animation Rigging パッケージ
----------------------------------

Animator の IK 機能は Humanoid のモデルでしか使えず、手足と視線以外は制御できない。より柔軟な制御が必要な場合は、Animation Rigging パッケージを使う。Package Manager ウィンドウから Animation Rigging をインストールすると使用できる。

Animation Rigging では、Rig Builder と Rig コンポーネントをキャラクターに追加し、その下に制約（Constraint）のコンポーネントを配置する。代表的な制約は次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 制約
     - 内容
   * - Two Bone IK Constraint
     - 腕や脚のような 2 本のボーンの先端を、目標の位置に合わせる。
   * - Multi-Aim Constraint
     - ボーンを目標の方向へ向ける。頭や武器の向きの制御に使う。
   * - Damped Transform
     - 親のボーンの動きに遅れて追従させる。しっぽや髪の揺れに使う。

Animation Rigging は Generic のモデルでも使用でき、制約の設定をエディター上で確認しながら調整できる。詳しい使い方は :doc:`appendix` の参考資料を参照すること。
