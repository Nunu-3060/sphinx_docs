.. _physics-ui:

物理演算と UI の最適化
======================

本章では、CPU の負荷の原因になりやすい物理演算と UI（uGUI）について、代表的な改善手法を紹介します。それぞれの負荷は、Profiler の Physics モジュールと UI モジュール、および CPU Usage モジュールで確認できます（:ref:`profiling`）。

物理演算
--------

Fixed Timestep
^^^^^^^^^^^^^^

物理演算は、:menuselection:`Edit --> Project Settings --> Time` の :guilabel:`Fixed Timestep` で設定した間隔（既定では 0.02 秒）ごとに実行されます（:ref:`update-fixedupdate`）。この値を大きくすると物理演算の回数が減り、負荷が下がります。ただし、衝突の判定の精度が下がり、速く動く物体がすり抜けやすくなります。

処理が重くなってフレーム時間が長くなると、遅れを取り戻すために 1 フレームの中で物理演算が何回も実行されます。すると、さらにフレーム時間が長くなるという悪循環に陥ることがあります。同じ画面の :guilabel:`Maximum Allowed Timestep` は、1 フレームの中で物理演算に使う時間の上限を設定し、この悪循環を防ぎます。

Layer Collision Matrix
^^^^^^^^^^^^^^^^^^^^^^

:menuselection:`Edit --> Project Settings --> Physics` の :guilabel:`Layer Collision Matrix` では、どのレイヤー同士で衝突を判定するかを設定できます。衝突する必要のないレイヤーの組み合わせ（敵の弾同士など）の判定を無効にすると、判定の処理が減ります。

Raycast でも、引数に最大距離とレイヤーマスクを指定して、判定の対象を必要な範囲に絞り込みます。

コライダーの選び方
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 手法
     - 説明
   * - プリミティブなコライダーを使う
     - Sphere Collider、Capsule Collider、Box Collider は、判定の計算が軽量です。Mesh Collider は形状が複雑なほど計算が重くなるため、プリミティブなコライダーの組み合わせで代用できないかを検討します。
   * - Mesh Collider には Convex を使う
     - Rigidbody を付けて動かす Mesh Collider は、:guilabel:`Convex` を有効にする必要があります。Convex を有効にすると凸形状に近似され、判定の計算も軽くなります。
   * - 動かすコライダーには Rigidbody を付ける
     - Rigidbody のない静的なコライダーは、動かないことを前提に最適化されています。スクリプトで動かすコライダーには Rigidbody を付け、物理演算の力で動かさない場合は :guilabel:`Is Kinematic` を有効にします。

UI（uGUI）
----------

Canvas の分割
^^^^^^^^^^^^^

uGUI では、Canvas に含まれる UI 要素のメッシュがまとめて生成されます。Canvas 内の UI 要素が 1 つでも変化すると、その Canvas 全体のメッシュが再構築されます。毎フレーム変化する UI 要素（タイマーの表示など）と、ほとんど変化しない UI 要素（背景の画像など）が同じ Canvas にあると、変化しない UI 要素も毎回再構築の対象になってしまいます。

頻繁に変化する UI 要素は、別の Canvas に分けて配置してください。Canvas の中に Canvas を配置すると、内側の Canvas は外側の Canvas とは別に再構築されます。

Raycast Target
^^^^^^^^^^^^^^

Image や Text などの UI 要素は、:guilabel:`Raycast Target` が有効な場合、タップやクリックの判定の対象になります。判定の対象が多いと、入力の処理の負荷が増えます。ボタンなど操作を受け付ける要素以外では、:guilabel:`Raycast Target` を無効にしてください。

Layout Group
^^^^^^^^^^^^

Horizontal Layout Group や Grid Layout Group などの Layout Group は、子要素の配置を自動的に計算する便利なコンポーネントです。しかし、子要素が変化するたびに配置の再計算が行われ、Layout Group を入れ子にしていると計算量が大きく増えます。頻繁に内容が変わる UI や要素の多いリストでは、Layout Group の使用を避けるか、配置を決めた後で Layout Group を無効にすることを検討します。

UI の表示・非表示
^^^^^^^^^^^^^^^^^

UI 全体を一時的に隠す場合は、GameObject を ``SetActive(false)`` で無効にするのではなく、Canvas コンポーネントの ``enabled`` を false にする方法も有効です。GameObject を無効にすると、再び有効にしたときに Canvas の再構築などの処理が発生しますが、Canvas コンポーネントを無効にする方法では、生成済みのメッシュが保持されるため、表示し直す際の負荷が小さくなります。
