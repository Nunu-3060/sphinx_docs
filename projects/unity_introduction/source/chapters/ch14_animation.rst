第 14 章 アニメーション
=======================

この章では、GameObject の動きや、キャラクターのアニメーションを再生する方法を説明します。

この章のサンプルコードは、``examples/chapter14`` フォルダーにあります。

アニメーションのしくみ
----------------------

Unity のアニメーションは、次の 3 つの要素で構成されます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 要素
     - 役割
   * - Animation Clip
     - 1 つの動き（歩く、走る、ジャンプするなど）を記録したアセットです。時間とともに変化するプロパティの値を記録します。
   * - Animator Controller
     - どの Animation Clip を、どのような条件で切り替えて再生するかを定義したアセットです。
   * - Animator
     - Animator Controller に従ってアニメーションを再生するコンポーネントです。アニメーションさせたい GameObject に付けます。

Animation Clip の作成
---------------------

Unity Editor の Animation ウィンドウを使うと、GameObject の位置、回転、大きさ、色などのプロパティを、時間とともに変化させる Animation Clip を作れます。ここでは、上下に揺れ続ける立方体のアニメーションを作ります。

#. :menuselection:`GameObject --> 3D Object --> Cube` で立方体を作成し、選んだ状態にします。
#. :menuselection:`Window --> Animation --> Animation` で Animation ウィンドウを開きます。
#. :guilabel:`Create` ボタンをクリックし、Animation Clip の保存先と名前（例えば ``Float.anim``）を指定します。Animation Clip と Animator Controller が作成され、立方体に Animator コンポーネントが追加されます。
#. Animation ウィンドウの録画ボタン（赤い丸）をクリックして、録画モードにします。
#. タイムラインの 0:00 の位置で、立方体の :guilabel:`Position` の Y を 0 にします。録画モードでは値を変更したときにキーフレームが作成されるため、既に 0 の場合は、Inspector ウィンドウの :guilabel:`Position` を右クリックして :guilabel:`Add Key` を選びます。
#. タイムラインの 0:30 の位置をクリックし、:guilabel:`Position` の Y を 1 にします。
#. タイムラインの 1:00 の位置をクリックし、:guilabel:`Position` の Y を 0 にします。
#. 録画ボタンをもう一度クリックして、録画モードを終えます。

値を記録した時点を **キーフレーム** と呼びます。キーフレームの間の値は、Unity が自動的に補間します。再生すると、立方体が上下に揺れ続けます。Animation Clip は初期設定で繰り返し再生（:guilabel:`Loop Time` が有効）になっています。

.. note::

   Animation ウィンドウのタイムラインの目盛りは「秒:フレーム」の形式です。初期設定では 1 秒が 60 フレームなので、0:30 は 0.5 秒を表します。

キャラクターのアニメーションは、通常は Blender や Maya などの 3D モデリングソフトウェアで作成し、FBX 形式などのファイルで 3D モデルと一緒に読み込みます。読み込んだファイルに含まれるアニメーションは、Animation Clip として使えます。

Animator Controller とステートマシン
------------------------------------

Animator Controller をダブルクリックすると、Animator ウィンドウが開きます。Animator ウィンドウでは、アニメーションの切り替えを **ステートマシン** として設定します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 要素
     - 意味
   * - ステート
     - 1 つのアニメーションを再生している状態です。四角い箱で表示され、それぞれに Animation Clip を設定します。
   * - 遷移（Transition）
     - あるステートから別のステートに切り替わる経路です。矢印で表示されます。
   * - パラメーター
     - 遷移の条件に使う変数です。スクリプトから値を設定します。

例えば、「待機」「歩き」「ジャンプ」の 3 つのステートを持つキャラクターは、次のように設定します。

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - 遷移元
     - 遷移先
     - 条件
   * - 待機
     - 歩き
     - パラメーター ``Speed`` が 0.1 より大きい
   * - 歩き
     - 待機
     - パラメーター ``Speed`` が 0.1 より小さい
   * - 待機、歩き
     - ジャンプ
     - パラメーター ``Jump`` が設定された
   * - ジャンプ
     - 待機
     - 条件なし（:guilabel:`Has Exit Time` を有効にし、ジャンプのアニメーションが終わったら戻る）

設定の手順は次のとおりです。

#. Animator ウィンドウの左側の :guilabel:`Parameters` タブで :guilabel:`+` をクリックし、Float 型の ``Speed`` と、Trigger 型の ``Jump`` を追加します。
#. Project ウィンドウから Animation Clip を Animator ウィンドウにドラッグ＆ドロップして、ステートを作成します。最初に作成したステートはオレンジ色で表示され、最初に再生されるステート（既定のステート）になります。
#. 遷移元のステートを右クリックして :guilabel:`Make Transition` を選び、遷移先のステートをクリックすると、遷移が作成されます。
#. 遷移の矢印を選び、Inspector ウィンドウの :guilabel:`Conditions` で条件を設定します。

遷移の Inspector ウィンドウにある :guilabel:`Has Exit Time` が有効だと、条件を満たしても、遷移元のアニメーションが一定の位置まで再生されるまで遷移しません。入力にすぐ反応してほしい遷移では、:guilabel:`Has Exit Time` を無効にします。

パラメーターの型
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 型
     - 用途
   * - Float
     - 移動の速さなど、連続的に変化する値に使います。
   * - Int
     - 武器の種類など、整数で表す値に使います。
   * - Bool
     - 地面に立っているかどうかなど、オンとオフを切り替える値に使います。
   * - Trigger
     - ジャンプや攻撃など、1 回だけ実行する動作に使います。遷移に使われると、自動的にオフに戻ります。

スクリプトからの制御
--------------------

スクリプトから Animator のパラメーターを設定すると、アニメーションが切り替わります。

.. literalinclude:: ../../examples/chapter14/AnimatorParameterDriver.cs
   :caption: AnimatorParameterDriver.cs
   :linenos:

:download:`AnimatorParameterDriver.cs をダウンロード <../../examples/chapter14/AnimatorParameterDriver.cs>`

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 用途
   * - ``SetFloat(名前, 値)``
     - Float 型のパラメーターを設定します。
   * - ``SetInteger(名前, 値)``
     - Int 型のパラメーターを設定します。
   * - ``SetBool(名前, 値)``
     - Bool 型のパラメーターを設定します。
   * - ``SetTrigger(名前)``
     - Trigger 型のパラメーターを設定します。

パラメーターの名前は文字列でも指定できますが、この例のように ``Animator.StringToHash`` で事前にハッシュ値（整数）に変換しておくと、毎回の文字列の比較が不要になり、処理が効率的になります。パラメーターの名前を間違えると、エラーにはならず警告が表示されるだけなので、アニメーションが切り替わらない場合は Console ウィンドウを確認してください。
