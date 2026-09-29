第 10 章 物理演算
=================

Unity の物理演算を使うと、重力による落下、物体同士の衝突や跳ね返り、摩擦などを、自分で計算しなくても再現できます。

この章のサンプルコードは、``examples/chapter10`` フォルダーにあります。

Rigidbody と Collider
---------------------

物理演算に関わる主なコンポーネントは、Rigidbody と Collider の 2 つです。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - コンポーネント
     - 役割
   * - Rigidbody
     - GameObject を物理演算で動かす対象にします。質量を持ち、重力や力を受けて動くようになります。
   * - Collider
     - 衝突判定に使う形状を表します。見た目の形状（メッシュ）とは別に設定します。

Collider には、形状に応じて次のような種類があります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Collider
     - 特徴
   * - Box Collider
     - 直方体の形状です。
   * - Sphere Collider
     - 球の形状です。衝突判定の計算が最も軽い形状です。
   * - Capsule Collider
     - カプセル（円柱の両端に半球を付けた形）の形状です。人型のキャラクターによく使います。
   * - Mesh Collider
     - メッシュの形状をそのまま使います。複雑な形状を正確に表せますが、計算が重くなります。Rigidbody を付けた GameObject で使う場合は、:guilabel:`Convex` を有効にする必要があります。

複雑な形状の GameObject でも、Box Collider や Sphere Collider などの単純な Collider を複数組み合わせて近似すると、計算を軽くできます。

GameObject の種類と組み合わせ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rigidbody と Collider の組み合わせによって、GameObject の物理演算での扱いが変わります。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 構成
     - 扱い
     - 例
   * - Collider のみ
     - 静的な Collider。動かない物体として扱われます。
     - 地面、壁
   * - Collider と Rigidbody
     - 物理演算で動く物体として扱われます。
     - ボール、箱
   * - Collider と Rigidbody（:guilabel:`Is Kinematic` を有効）
     - 物理演算の力では動かず、スクリプトで動かす物体として扱われます。他の Rigidbody を押しのけることはできます。
     - 動く床、エレベーター

Rigidbody の主なプロパティ
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 意味
   * - :guilabel:`Mass`
     - 質量（kg）です。
   * - :guilabel:`Linear Damping`
     - 移動の減衰の強さです。大きいほど早く止まります。
   * - :guilabel:`Angular Damping`
     - 回転の減衰の強さです。
   * - :guilabel:`Use Gravity`
     - 重力の影響を受けるかどうかです。
   * - :guilabel:`Is Kinematic`
     - 物理演算の力で動かさず、スクリプトで動かすかどうかです。
   * - :guilabel:`Interpolate`
     - 物理演算の更新と描画のタイミングの差によって動きがかくつくのを、補間によって和らげます。プレイヤーなど、カメラが追いかける GameObject では :guilabel:`Interpolate` を選ぶとなめらかに表示されます。
   * - :guilabel:`Collision Detection`
     - 衝突判定の方式です。高速で動く GameObject が壁をすり抜けてしまう場合は、:guilabel:`Continuous` などに変更します。
   * - :guilabel:`Constraints`
     - 特定の軸の移動や回転を固定します。

.. note::

   Unity 6 では、``Rigidbody`` の一部のプロパティの名前が変わりました。``velocity`` は ``linearVelocity`` に、``drag`` は ``linearDamping`` に、``angularDrag`` は ``angularDamping`` になっています。古い資料のコードを使う場合は注意してください。

Rigidbody を動かす
------------------

Rigidbody を付けた GameObject を ``transform.position`` で直接動かすと、物理演算を無視した移動になり、衝突がうまく処理されません。Rigidbody を付けた GameObject は、次のような方法で動かします。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 方法
     - 用途
   * - ``AddForce(力, ForceMode.Force)``
     - 継続的に力を加えます。``FixedUpdate`` で毎回呼び出して使います。
   * - ``AddForce(力積, ForceMode.Impulse)``
     - 瞬間的に力を加えます。ジャンプや爆発などに使います。
   * - ``linearVelocity`` への代入
     - 速度を直接設定します。力の計算を介さないため、キャラクターの移動を細かく制御したい場合に使います。
   * - ``MovePosition(位置)``
     - :guilabel:`Is Kinematic` を有効にした Rigidbody を、物理演算の更新に合わせて移動させます。移動中に触れた他の Rigidbody を押しのけますが、壁などに当たっても止まりません。

衝突イベントとトリガーイベント
------------------------------

衝突が起きたことは、イベント関数で受け取れます。

.. literalinclude:: ../../examples/chapter10/CollisionReporter.cs
   :caption: CollisionReporter.cs
   :linenos:

:download:`CollisionReporter.cs をダウンロード <../../examples/chapter10/CollisionReporter.cs>`

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - イベント関数
     - 呼ばれるタイミング
   * - ``OnCollisionEnter``
     - 他の Collider と衝突した瞬間
   * - ``OnCollisionStay``
     - 他の Collider と接触している間
   * - ``OnCollisionExit``
     - 他の Collider から離れた瞬間
   * - ``OnTriggerEnter``
     - トリガーの範囲に入った瞬間
   * - ``OnTriggerStay``
     - トリガーの範囲に入っている間
   * - ``OnTriggerExit``
     - トリガーの範囲から出た瞬間

Collider の :guilabel:`Is Trigger` を有効にすると、その Collider は物体を押し返さず、他の Collider が範囲に入ったことを検出するだけの **トリガー** になります。アイテムの取得、ゴールの判定、敵の索敵範囲などに使います。

.. important::

   衝突イベントやトリガーイベントが呼ばれるには、次の条件を満たす必要があります。

   * 両方の GameObject に Collider が付いている。
   * 少なくとも一方の GameObject に Rigidbody が付いている。
   * 衝突イベントの場合は、少なくとも一方の Rigidbody の :guilabel:`Is Kinematic` が無効になっている（トリガーイベントは、:guilabel:`Is Kinematic` が有効でも呼ばれます）。

   イベントが呼ばれない場合は、まずこの条件を確認してください。また、2D 用の Collider（Box Collider 2D など）と 3D 用の Collider は互いに衝突しません。

レイキャスト
------------

**レイキャスト** は、ある点から指定した方向に光線（レイ）を飛ばし、最初に当たった Collider を調べる機能です。射撃の当たり判定、足元に地面があるかの判定、マウスでクリックした物体の特定などに使います。

.. literalinclude:: ../../examples/chapter10/ClickPusher.cs
   :caption: ClickPusher.cs
   :linenos:

:download:`ClickPusher.cs をダウンロード <../../examples/chapter10/ClickPusher.cs>`

このスクリプトをシーン内の任意の GameObject に付けます。地面として Plane を配置し、その上に Rigidbody を付けた Cube を置いて再生します。Cube をクリックすると、クリックした位置からカメラの奥の方向へ押し出されます。

``Camera.ScreenPointToRay`` は、画面上の位置から、カメラの奥へ向かうレイを作ります。``Physics.Raycast`` はレイが Collider に当たると ``true`` を返し、当たった位置や Collider などの情報を ``RaycastHit`` に格納します。

レイヤーと衝突マトリクス
------------------------

GameObject には **レイヤー** を 1 つ設定できます。レイヤーは、Inspector ウィンドウの右上にある :guilabel:`Layer` で設定します。新しいレイヤーは、:guilabel:`Layer` の一覧の :guilabel:`Add Layer...` から追加できます。

レイヤーを使うと、次のような設定ができます。

* **衝突マトリクス**：:menuselection:`Edit --> Project Settings` の :guilabel:`Physics` にある :guilabel:`Layer Collision Matrix` で、レイヤー同士が衝突するかどうかを設定できます。例えば、味方の弾が味方に当たらないようにできます。
* **レイキャストの対象の限定**：``Physics.Raycast`` の引数に ``LayerMask`` を渡すと、特定のレイヤーの Collider だけにレイを当てられます。``ClickPusher`` の :guilabel:`Target Layers` がその例です。
* **カメラの描画対象の限定**：Camera コンポーネントの :guilabel:`Culling Mask` で、描画するレイヤーを選べます。

2D の物理演算
-------------

2D ゲームでは、2D 用の物理演算を使います。コンポーネントの名前の末尾に ``2D`` が付いている（Rigidbody 2D、Box Collider 2D など）ほかは、基本的な考え方は 3D と同じです。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 項目
     - 3D
     - 2D
   * - Rigidbody
     - Rigidbody
     - Rigidbody 2D
   * - Collider
     - Box Collider など
     - Box Collider 2D など
   * - 衝突イベント
     - ``OnCollisionEnter(Collision)``
     - ``OnCollisionEnter2D(Collision2D)``
   * - トリガーイベント
     - ``OnTriggerEnter(Collider)``
     - ``OnTriggerEnter2D(Collider2D)``
   * - レイキャスト
     - ``Physics.Raycast``
     - ``Physics2D.Raycast``

3D と 2D の物理演算は完全に別のしくみとして動いているため、3D のコンポーネントと 2D のコンポーネントを混在させても、互いに作用しません。
