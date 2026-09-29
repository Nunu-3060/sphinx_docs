########################################################################
Scene ビューの拡張
########################################################################

Scene ビューに線や図形、操作用のハンドルを表示すると、位置や範囲などの値を目で見ながら編集できるようになります。この章では、経路を表す ``Waypoint`` コンポーネントを例に、Scene ビューの拡張方法を説明します。

Scene ビューに表示する方法には、ギズモとハンドルの 2 種類があります。

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - 種類
     - クラス
     - 名前空間
     - 主な用途
   * - ギズモ
     - ``Gizmos``
     - ``UnityEngine``
     - 位置や範囲の表示（表示のみ）
   * - ハンドル
     - ``Handles``
     - ``UnityEditor``
     - 表示に加えて、マウスによる値の編集

サンプルコード
========================================================================

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/Waypoint.cs
   :caption: Runtime/Waypoint.cs
   :linenos:

:download:`Waypoint.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/Waypoint.cs>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/WaypointEditor.cs
   :caption: Editor/WaypointEditor.cs
   :linenos:

:download:`WaypointEditor.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/WaypointEditor.cs>`

空のゲームオブジェクトに ``Waypoint`` コンポーネントを追加すると、Scene ビューに経路の点が水色の球で表示されます。ゲームオブジェクトを選択すると、点を結ぶ線と、各点を移動するためのハンドルが表示されます。

ギズモで表示する
========================================================================

ギズモは、コンポーネントの ``OnDrawGizmos`` メソッドまたは ``OnDrawGizmosSelected`` メソッドの中で、``Gizmos`` クラスのメソッドを呼んで描画します。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 呼ばれるタイミング
   * - ``OnDrawGizmos``
     - Scene ビューを描画するたび。ゲームオブジェクトを選択しているかどうかに関係なく呼ばれる
   * - ``OnDrawGizmosSelected``
     - ゲームオブジェクトを選択しているときだけ呼ばれる

``Gizmos`` クラスには、``DrawSphere``\ （球）、``DrawWireCube``\ （立方体の枠）、``DrawLine``\ （線）などのメソッドがあります。描画の色は、描画の前に ``Gizmos.color`` で指定します。

``Gizmos`` クラスは ``UnityEngine`` 名前空間にあるため、ゲーム本体側のスクリプトに書けます。``OnDrawGizmos`` はエディターでだけ呼ばれ、ビルドしたゲームでは呼ばれません。

ハンドルで編集する
========================================================================

ハンドルは、カスタムエディターの ``OnSceneGUI`` メソッドの中で描画します。``OnSceneGUI`` は、対象のゲームオブジェクトを選択している間、Scene ビューを描画するたびに呼ばれます。

線や文字を描画する
------------------------------------------------------------------------

``Handles`` クラスは、ハンドルのほかに、線や文字を描画するメソッドも持っています。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 内容
   * - ``Handles.DrawAAPolyLine``
     - 指定した太さで、点を順に結ぶ線を描画する
   * - ``Handles.DrawLine``
     - 2 点を結ぶ線を描画する
   * - ``Handles.Label``
     - 指定した位置に文字を描画する
   * - ``Handles.DrawWireDisc``
     - 円を描画する

描画の色は、描画の前に ``Handles.color`` で指定します。

ハンドルで値を変更する
------------------------------------------------------------------------

``Handles.PositionHandle`` は、移動ツールと同じ 3 軸の矢印を表示し、ドラッグ後の位置を返します。ハンドルが操作されたかどうかは、``EditorGUI.BeginChangeCheck`` と ``EditorGUI.EndChangeCheck`` で調べます。

.. code-block:: csharp

   EditorGUI.BeginChangeCheck();
   var newWorldPoint = Handles.PositionHandle(worldPoints[i], handleRotation);
   if (EditorGUI.EndChangeCheck())
   {
       Undo.RecordObject(waypoint, "Move Waypoint");
       points[i] = transform.InverseTransformPoint(newWorldPoint);
       // ...
   }

``EndChangeCheck`` は、``BeginChangeCheck`` を呼んでから値が変更された場合に ``true`` を返します。値が変わったときだけ ``Undo.RecordObject`` を呼び、新しい値を保存します。

ハンドルの操作による変更では、``SerializedObject`` ではなく ``Undo.RecordObject`` を使うと簡潔に書けます（第 5 章を参照）。サンプルコードでは、プレハブのインスタンスにも対応するため、変更後に ``PrefabUtility.RecordPrefabInstancePropertyModifications`` を呼んでいます。

``Handles.PositionHandle`` のほかにも、次のようなハンドルがあります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 内容
   * - ``Handles.RotationHandle``
     - 回転ツールと同じハンドルを表示し、回転後の向きを返す
   * - ``Handles.ScaleHandle``
     - 拡大縮小ツールと同じハンドルを表示し、変更後の倍率を返す
   * - ``Handles.RadiusHandle``
     - 球の半径を変更するハンドルを表示し、変更後の半径を返す
   * - ``Handles.FreeMoveHandle``
     - 画面上で自由にドラッグできるハンドルを表示し、移動後の位置を返す

ハンドルの向きは、Scene ビューのツールバーの設定に合わせています。``Tools.pivotRotation`` が ``PivotRotation.Local`` のときはゲームオブジェクトの向きに、``PivotRotation.Global`` のときはワールド座標の軸に合わせます。

ローカル座標とワールド座標
========================================================================

サンプルコードの ``Waypoint`` コンポーネントは、経路の点をゲームオブジェクトから見たローカル座標で保存しています。こうしておくと、ゲームオブジェクトを移動・回転したときに、経路全体が一緒に移動・回転します。

一方、Scene ビューへの描画やハンドルの位置は、ワールド座標で指定します。そのため、ローカル座標とワールド座標を相互に変換する必要があります。

ローカル座標 :math:`\mathbf{p}_\mathrm{local}` からワールド座標 :math:`\mathbf{p}_\mathrm{world}` への変換は、ゲームオブジェクトの位置・回転・拡大縮小を表す 4 行 4 列の行列 :math:`M` を使って、次のように表せます。

.. math::

   \begin{pmatrix} \mathbf{p}_\mathrm{world} \\ 1 \end{pmatrix} = M \begin{pmatrix} \mathbf{p}_\mathrm{local} \\ 1 \end{pmatrix}

逆に、ワールド座標からローカル座標への変換には、逆行列 :math:`M^{-1}` を使います。

.. math::

   \begin{pmatrix} \mathbf{p}_\mathrm{local} \\ 1 \end{pmatrix} = M^{-1} \begin{pmatrix} \mathbf{p}_\mathrm{world} \\ 1 \end{pmatrix}

Unity では、行列 :math:`M` は ``Transform.localToWorldMatrix``、逆行列 :math:`M^{-1}` は ``Transform.worldToLocalMatrix`` で取得できます。ただし、点の変換だけであれば、行列を直接扱う必要はありません。次のメソッドを使います。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 変換
   * - ``Transform.TransformPoint``
     - ローカル座標 → ワールド座標
   * - ``Transform.InverseTransformPoint``
     - ワールド座標 → ローカル座標

サンプルコードでは、描画の前に ``TransformPoint`` でワールド座標に変換し、ハンドルで移動した後に ``InverseTransformPoint`` でローカル座標に戻して保存しています。

EditorTool
========================================================================

Unity には、移動ツールや回転ツールのように、ツールバーで切り替えて使う「ツール」を独自に追加する ``EditorTool`` という仕組みもあります。``EditorTool`` を継承したクラスを作成すると、特定のコンポーネントを選択したときだけツールバーに表示されるツールを作成できます。

``OnSceneGUI`` によるハンドルは、ゲームオブジェクトを選択している間は常に表示されます。ほかのツールと表示が重なって操作しにくい場合や、専用の操作モードを用意したい場合は、``EditorTool`` の利用を検討してください。

参考資料
========================================================================

* :unity-api:`Gizmos`
* :unity-api:`Handles`
* :unity-api:`Handles.PositionHandle`
* :unity-api:`Editor.OnSceneGUI`
* :unity-api:`Transform.TransformPoint`
* :unity-api:`EditorTools.EditorTool`
