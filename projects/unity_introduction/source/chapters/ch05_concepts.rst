第 5 章 Unity の基本概念
========================

この章では、Unity でゲームを作るうえで最も重要な概念である GameObject、Component、シーン、アセット、Prefab について説明します。

GameObject と Component
-----------------------

Unity のシーンに置かれるものは、キャラクター、地面、カメラ、ライトなど、すべて **GameObject** です。ただし、GameObject そのものは、名前などの基本的な情報と、位置を表す Transform コンポーネントを持つだけの「入れ物」です。GameObject に機能を与えるのが **Component**\ （コンポーネント）です。

例えば、前の章で作成した Cube を Inspector ウィンドウで確認すると、次のコンポーネントが付いています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コンポーネント
     - 機能
   * - Transform
     - 位置、回転、大きさを表します。すべての GameObject に必ず付いています。
   * - Mesh Filter
     - 表示する形状（メッシュ）を指定します。Cube の場合は立方体のメッシュです。
   * - Mesh Renderer
     - Mesh Filter で指定したメッシュを、指定したマテリアルで画面に描画します。
   * - Box Collider
     - 物理演算で使う、衝突判定用の箱形の形状です。

GameObject にどのようなコンポーネントを付けるかによって、その GameObject の役割が決まります。例えば、Mesh Renderer を取り除くと Cube は見えなくなり、Rigidbody コンポーネントを追加すると重力で落下するようになります。自分で書いた C# スクリプトもコンポーネントの一種で、GameObject に付けることで独自の動作を追加できます。

コンポーネントを追加するには、GameObject を選んで Inspector ウィンドウの下部にある :guilabel:`Add Component` をクリックし、追加したいコンポーネントを選びます。

このように、小さな機能の部品を組み合わせて GameObject を作る考え方を、コンポーネント指向と呼びます。

Transform と親子関係
--------------------

GameObject は、別の GameObject の子にできます。Hierarchy ウィンドウで GameObject を別の GameObject の上にドラッグすると、ドラッグした GameObject が子になります。

子の GameObject は、親の GameObject と一緒に移動、回転、拡大縮小します。例えば、車の GameObject の子として 4 つのタイヤを配置すれば、車を動かすとタイヤも一緒に動きます。

子の Transform コンポーネントに表示される値は、親から見た相対的な値です。これを **ローカル座標** と呼びます。一方、シーン全体の原点から見た値を **ワールド座標** と呼びます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 座標
     - 意味
   * - ワールド座標
     - シーンの原点 (0, 0, 0) を基準とした座標です。スクリプトでは ``transform.position`` で扱います。
   * - ローカル座標
     - 親の GameObject を基準とした座標です。スクリプトでは ``transform.localPosition`` で扱います。親がいない GameObject では、ワールド座標と同じ値になります。

回転（``rotation`` と ``localRotation``）や大きさ（``lossyScale`` と ``localScale``）にも、同じようにワールドとローカルの区別があります。

座標系
------

Unity の 3D 空間では、X 軸が右、Y 軸が上、Z 軸が前（画面の奥）を向いています。この座標系は **左手座標系** と呼ばれます。左手の親指を X 軸（右）、人差し指を Y 軸（上）に向けたとき、中指が Z 軸（前）を向くためです。

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 軸
     - 色
     - 向き
   * - X
     - 赤
     - 右
   * - Y
     - 緑
     - 上
   * - Z
     - 青
     - 前

Scene ビューの軸の矢印は、この色で表示されます。3D モデリングソフトウェアの中には、Z 軸が上を向く座標系や右手座標系を使うものがあります。そのようなソフトウェアで作ったモデルを読み込むと、向きが変わってしまうことがあるので注意してください。

Unity では、長さの単位を 1 = 1 m として扱うことが一般的です。物理演算の重力の初期値（9.81 m/s\ :sup:`2`）もこの前提で設定されているため、特別な理由がなければ、この単位に合わせて GameObject の大きさを決めてください。

シーン
------

**シーン** は、GameObject を配置する空間であり、ゲームの 1 つの場面を表します。タイトル画面、ステージ 1、ステージ 2 のように、場面ごとにシーンを分けて作るのが一般的です。シーンは、拡張子が ``.unity`` のファイル（シーンアセット）として Assets フォルダーに保存されます。

新しいプロジェクトには、``Assets/Scenes`` フォルダーに ``SampleScene`` というシーンが用意されています。新しいシーンは、:menuselection:`File --> New Scene` で作成できます。シーンの切り替えについては :doc:`ch15_scenes_and_data` で説明します。

アセットとパッケージ
--------------------

**アセット** は、ゲームで使う素材の総称です。3D モデル、テクスチャ（画像）、音声、スクリプト、マテリアル、シーンなど、Assets フォルダーに置かれたファイルはすべてアセットとして扱われます。

外部で作成したファイルをプロジェクトで使うには、ファイルを Project ウィンドウにドラッグ＆ドロップします。Unity は、ファイルの種類に応じて自動的に読み込み（インポート）を行います。読み込みの設定は、Project ウィンドウでアセットを選ぶと Inspector ウィンドウに表示されます。

**パッケージ** は、Unity の機能やツールを追加するための単位です。Input System、Cinemachine、TextMeshPro など、Unity の多くの機能はパッケージとして提供されています。パッケージは、:menuselection:`Window --> Package Manager` で開く Package Manager ウィンドウで、追加、更新、削除します。

Prefab
------

同じ敵キャラクターを何体も配置したい場合、GameObject を複製して並べることもできます。しかし、この方法では、後で敵の設定を変えたくなったときに、すべての複製を 1 つずつ修正しなければなりません。

**Prefab**\ （プレハブ）は、GameObject をコンポーネントや子の GameObject ごとアセットとして保存したものです。Prefab をシーンに配置したものを **Prefab インスタンス** と呼びます。Prefab を修正すると、その変更はすべての Prefab インスタンスに反映されます。

Prefab の作成と編集
~~~~~~~~~~~~~~~~~~~

#. Hierarchy ウィンドウの GameObject を、Project ウィンドウにドラッグ＆ドロップします。Prefab アセットが作成され、Hierarchy ウィンドウの GameObject の名前が青色で表示されます。これは、その GameObject が Prefab インスタンスになったことを表します。
#. Project ウィンドウの Prefab アセットをシーンにドラッグ＆ドロップすると、Prefab インスタンスを追加できます。
#. Prefab アセットをダブルクリックすると、Prefab を単独で編集する画面（Prefab モード）になります。ここで行った変更は、すべての Prefab インスタンスに反映されます。Hierarchy ウィンドウの左上にある :guilabel:`<` をクリックすると、Prefab モードが終わります。

オーバーライド
~~~~~~~~~~~~~~

Prefab インスタンスごとに、一部の値だけを変えることもできます。これを **オーバーライド** と呼びます。オーバーライドした値は Inspector ウィンドウで太字になり、左端に青い線が表示されます。オーバーライドした値は、Prefab アセットを変更しても上書きされません。

Inspector ウィンドウの上部にある :guilabel:`Overrides` メニューから、オーバーライドした値を Prefab アセットに反映する（:guilabel:`Apply All`）ことや、Prefab アセットの値に戻す（:guilabel:`Revert All`）ことができます。

Prefab Variant
~~~~~~~~~~~~~~

**Prefab Variant** は、既存の Prefab を元にして、一部の値を変えた別の Prefab です。例えば、「敵」の Prefab を元に、色と体力だけを変えた「強い敵」の Prefab Variant を作れます。元の Prefab を変更すると、その変更は Prefab Variant にも反映されます（Prefab Variant で変えた値を除きます）。

Prefab Variant を作成するには、Project ウィンドウで元の Prefab を右クリックし、:menuselection:`Create --> Prefab Variant` を選びます。
