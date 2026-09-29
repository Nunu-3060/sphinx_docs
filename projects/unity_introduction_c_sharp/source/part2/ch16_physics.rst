################################################################
第 16 章 物理演算と衝突判定
################################################################

Unity には、重力、力、衝突などを計算する物理演算の機能があります。この章では、Rigidbody と Collider を使って物体を物理的に動かす方法と、衝突を検出する方法を学びます。

Rigidbody と Collider
================================================================

物理演算には、主に次の 2 つのコンポーネントを使います。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - コンポーネント
     - 役割
   * - Rigidbody
     - 質量を持ち、重力や力によって動く物体にします。
   * - Collider
     - 衝突判定に使う形状です。Box Collider（直方体）、Sphere Collider（球）、Capsule Collider（カプセル）、Mesh Collider（メッシュの形状）などがあります。

Rigidbody の主なプロパティは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 説明
   * - ``mass``
     - 質量（kg）です。
   * - ``linearDamping``
     - 移動の減衰（空気抵抗のようなもの）です。値が大きいほど、早く止まります。
   * - ``useGravity``
     - 重力の影響を受けるかどうかです。
   * - ``isKinematic``
     - ``true`` にすると、物理演算では動かず、スクリプトで Transform を操作して動かす物体（キネマティック）になります。
   * - ``linearVelocity``
     - 現在の速度（m/s）です。

.. note::

   Unity 6 では、``Rigidbody`` の一部のプロパティの名前が変わりました。以前の ``velocity`` は ``linearVelocity`` に、``drag`` は ``linearDamping`` に、``angularDrag`` は ``angularDamping`` になっています。古い解説を参考にするときは注意してください。

物理演算で動かす
================================================================

AddForce
----------------------------------------------------------------

Rigidbody を持つ物体は、``AddForce`` で力を加えて動かします。第 2 引数の ``ForceMode`` で、力の加え方を指定します。

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - ForceMode
     - 意味
     - 質量の影響
   * - ``Force``\ （既定）
     - 継続的な力です。毎回の ``FixedUpdate`` で加え続ける場合に使います。
     - 受ける
   * - ``Impulse``
     - 瞬間的な力（撃力）です。ジャンプや爆発などに使います。
     - 受ける
   * - ``Acceleration``
     - 継続的な加速度です。
     - 受けない
   * - ``VelocityChange``
     - 瞬間的な速度の変化です。
     - 受けない

質量を :math:`m`、加えた力を :math:`F` とすると、``Force`` では物体に :math:`a = F / m` の加速度が生じます。``Impulse`` では、速度が一度に :math:`\Delta v = F / m` だけ変わります。

物理演算の処理は FixedUpdate で行う
----------------------------------------------------------------

物理演算は、``FixedUpdate`` と同じ一定の時間間隔で計算されます。そのため、Rigidbody に力を加える処理は ``FixedUpdate`` に書きます。一方、入力は ``Update`` で読み取ります（第 14 章）。そこで、``Update`` で読み取った入力をフィールドに保存しておき、``FixedUpdate`` でその値を使って力を加えます。

.. warning::

   物理演算で動かしている（``isKinematic`` が ``false`` の）Rigidbody の ``transform.position`` を直接書き換えると、物理演算の結果と食い違い、壁をすり抜けるなどの不自然な動きになります。物理演算で動かす物体は、``AddForce`` などの Rigidbody のメソッドで動かしてください。

ジャンプのサンプルコード
----------------------------------------------------------------

.. literalinclude:: ../../examples/ch16/JumpBall.cs
   :language: csharp
   :caption: JumpBall.cs

:download:`JumpBall.cs をダウンロード <../../examples/ch16/JumpBall.cs>`

床の上にいるかどうかは、``OnCollisionStay`` で受け取った接触点の法線（面に垂直な向き）で判定しています。法線の ``y`` が大きい（上向きに近い）接触点があれば、ボールは床の上に乗っていると判断できます。このサンプルコードでは説明を簡単にするため、何かから離れたら床から離れたとみなしています。

衝突判定
================================================================

衝突とトリガー
----------------------------------------------------------------

Collider には、次の 2 つの使い方があります。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 種類
     - 動作
     - 例
   * - 衝突（Collision）
     - 物体どうしがぶつかり、跳ね返ったり止まったりします。
     - 壁、床、ボール
   * - トリガー（Trigger）
     - 物体はすり抜けますが、重なったことを検出できます。
     - アイテム、ゴール地点、ダメージを受ける範囲

Collider をトリガーにするには、Inspector ウィンドウで Collider の Is Trigger にチェックを入れます。

衝突とトリガーのイベント関数
----------------------------------------------------------------

衝突やトリガーが起きると、次のイベント関数が呼ばれます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - イベント関数
     - 呼ばれるタイミング
   * - ``OnCollisionEnter(Collision collision)``
     - 衝突が始まったとき
   * - ``OnCollisionStay(Collision collision)``
     - 衝突が続いている間、物理演算の更新ごと
   * - ``OnCollisionExit(Collision collision)``
     - 衝突が終わったとき
   * - ``OnTriggerEnter(Collider other)``
     - トリガーに重なり始めたとき
   * - ``OnTriggerStay(Collider other)``
     - トリガーに重なっている間、物理演算の更新ごと
   * - ``OnTriggerExit(Collider other)``
     - トリガーから離れたとき

これらのイベント関数が呼ばれるには、次の条件を満たす必要があります。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 種類
     - 条件
   * - 衝突
     - 両方の物体が Collider を持ち、少なくとも一方が ``isKinematic`` が ``false`` の Rigidbody を持つこと
   * - トリガー
     - 両方の物体が Collider を持ち、少なくとも一方の Collider がトリガーで、少なくとも一方が Rigidbody を持つこと

.. note::

   2D のゲームでは、Rigidbody2D や BoxCollider2D などの 2D 用のコンポーネントを使い、イベント関数も ``OnCollisionEnter2D`` や ``OnTriggerEnter2D`` のように名前の最後に 2D が付いたものを使います。3D 用と 2D 用のコンポーネントどうしは衝突しません。

タグ
----------------------------------------------------------------

ぶつかった相手が何かを見分けるには、タグを使うと便利です。タグは、GameObject に付けられるラベルです。Inspector ウィンドウの上部にある Tag で設定します。Player などのタグは最初から用意されており、Add Tag を選ぶと新しいタグを追加できます。

タグを比べるときは、``other.CompareTag("Player")`` のように ``CompareTag`` を使います。``other.tag == "Player"`` と書くこともできますが、``CompareTag`` の方が効率的です。

衝突判定のサンプルコード
----------------------------------------------------------------

.. literalinclude:: ../../examples/ch16/CollisionReporter.cs
   :language: csharp
   :caption: CollisionReporter.cs

:download:`CollisionReporter.cs をダウンロード <../../examples/ch16/CollisionReporter.cs>`

``{collision.relativeVelocity.magnitude:F2}`` の ``:F2`` は、小数点以下 2 桁で表示するための書式の指定です。

.. note::

   速く動く小さな物体は、1 回の物理演算の更新の間に薄い壁を通り抜けてしまうことがあります。その場合は、Rigidbody の Collision Detection を Continuous に変更します。

まとめ
================================================================

* Rigidbody を付けると物理演算で動き、Collider を付けると衝突判定ができます。
* Rigidbody に力を加える処理は ``FixedUpdate`` に、入力の読み取りは ``Update`` に書きます。
* Is Trigger にチェックを入れた Collider は、すり抜けながら重なりを検出できます。
* 衝突は ``OnCollisionEnter`` など、トリガーは ``OnTriggerEnter`` などで検出します。
* 相手を見分けるにはタグを使い、``CompareTag`` で比べます。
