########################################################################
メニューの追加
########################################################################

エディター拡張の第一歩として、メニューに項目を追加し、選択したときに処理を実行できるようにします。

サンプルコード
========================================================================

この章では、次の 2 つのファイルを使います。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/MenuItemExample.cs
   :caption: Editor/MenuItemExample.cs
   :linenos:

:download:`MenuItemExample.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/MenuItemExample.cs>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/ContextMenuExample.cs
   :caption: Runtime/ContextMenuExample.cs
   :linenos:

:download:`ContextMenuExample.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/ContextMenuExample.cs>`

MenuItem 属性
========================================================================

static メソッドに ``MenuItem`` 属性を付けると、そのメソッドがメニューの項目になります。引数には、メニュー上の位置を「/」区切りのパスで指定します。

.. code-block:: csharp

   [MenuItem("Tools/Editor Intro/Hello")]
   private static void Hello()
   {
       Debug.Log("Hello, Editor!");
   }

サンプルコードを追加すると、メニューバーに :menuselection:`Tools --> Editor Intro --> Hello` が表示されます。選択すると、Console ウィンドウに「Hello, Editor!」と表示されます。

パスの先頭には、既存のメニュー名（``Assets``、``GameObject``、``Window`` など）も新しいメニュー名も指定できます。独自のツールは、``Tools`` の下にまとめるのが一般的です。

ショートカットキー
------------------------------------------------------------------------

パスの末尾に半角空白と特殊な文字を続けると、ショートカットキーを割り当てられます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 文字
     - 意味
   * - ``%``
     - Ctrl キー（macOS では Cmd キー）
   * - ``#``
     - Shift キー
   * - ``&``
     - Alt キー（macOS では Option キー）
   * - ``_``
     - 修飾キーなし（``_g`` なら G キーだけで実行）

サンプルコードの ``"Tools/Editor Intro/Hello With Shortcut %&h"`` は、Ctrl + Alt + H で実行できます。割り当てたショートカットキーは、:menuselection:`Edit --> Shortcuts` で開く Shortcuts ウィンドウで確認・変更できます。

検証関数
------------------------------------------------------------------------

``MenuItem`` 属性の第 2 引数に ``true`` を指定したメソッドは「検証関数」になります。検証関数は、同じパスのメニュー項目を表示する前に呼ばれ、``false`` を返すとその項目はグレーアウトして選択できなくなります。

.. code-block:: csharp

   [MenuItem("Tools/Editor Intro/Log Selected Name", true)]
   private static bool ValidateLogSelectedName()
   {
       return Selection.activeGameObject != null;
   }

この例では、ゲームオブジェクトを選択していないときに :menuselection:`Tools --> Editor Intro --> Log Selected Name` を選択できないようにしています。これにより、本体のメソッドで ``Selection.activeGameObject`` が ``null`` になる心配がなくなります。

表示順と区切り線
------------------------------------------------------------------------

``MenuItem`` 属性の第 3 引数は、表示順を決める値（priority）です。値が小さい項目ほど上に表示されます。省略した場合は 1000 として扱われます。

直前の項目と priority が大きく離れていると（目安として 11 以上）、間に区切り線が入ります。サンプルコードでは、:menuselection:`Tools --> Editor Intro --> About` の priority を 2000 にして、ほかの項目と区切り線で分けています。

コンテキストメニューへの追加
========================================================================

コンポーネントのコンテキストメニュー
------------------------------------------------------------------------

パスを「CONTEXT/コンポーネントの型名/」で始めると、そのコンポーネントのコンテキストメニューに項目を追加できます。コンテキストメニューは、Inspector ウィンドウでコンポーネントのヘッダーを右クリックするか、ヘッダー右端の「⋮」ボタンをクリックすると表示されます。

.. code-block:: csharp

   [MenuItem("CONTEXT/Transform/Reset Y Position")]
   private static void ResetYPosition(MenuCommand command)
   {
       var transform = (Transform)command.context;
       // ...
   }

メソッドの引数を ``MenuCommand`` 型にすると、``context`` プロパティから操作対象のコンポーネントを取得できます。

このメソッドでは、値を変更する前に ``Undo.RecordObject`` を呼んでいます。これにより、変更を Ctrl + Z で元に戻せます。``Undo`` の詳細は「:doc:`05_serialized_object`」で説明します。

ゲームオブジェクトの作成メニュー
------------------------------------------------------------------------

パスを「GameObject/」で始め、priority を 10 にすると、ほかのゲームオブジェクト作成メニューと同じグループになり、Hierarchy ウィンドウの「+」ボタンのメニューと右クリックメニューにも表示されます。

.. code-block:: csharp

   [MenuItem("GameObject/Editor Intro/Marker", false, 10)]
   private static void CreateMarker(MenuCommand command)
   {
       var marker = new GameObject("Marker");
       GameObjectUtility.SetParentAndAlign(marker, command.context as GameObject);
       Undo.RegisterCreatedObjectUndo(marker, "Create Marker");
       Selection.activeObject = marker;
   }

Hierarchy ウィンドウでゲームオブジェクトを右クリックして実行した場合、``command.context`` には右クリックしたゲームオブジェクトが入ります。``GameObjectUtility.SetParentAndAlign`` は、作成したゲームオブジェクトをその子にし、位置を親に合わせます。メニューバーから実行した場合は ``command.context`` が ``null`` になり、シーンの直下に作成されます。

作成したゲームオブジェクトは ``Undo.RegisterCreatedObjectUndo`` で Undo に登録します。登録しておくと、Ctrl + Z で作成を取り消せます。

ContextMenu 属性と ContextMenuItem 属性
========================================================================

ゲーム本体側のスクリプトにメニューを追加したいときは、``UnityEngine`` 名前空間の ``ContextMenu`` 属性と ``ContextMenuItem`` 属性を使えます。どちらも ``UnityEngine`` 名前空間にあるため、Editor フォルダーに分ける必要はありません。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 属性
     - 付ける場所
     - メニューが表示される場所
   * - ``ContextMenu``
     - インスタンスメソッド
     - コンポーネントのコンテキストメニュー
   * - ``ContextMenuItem``
     - フィールド
     - Inspector ウィンドウでフィールド名を右クリックしたときのメニュー

``ContextMenu`` 属性は、``MenuItem`` 属性の「CONTEXT/」と違い、static ではないメソッドに付けます。メソッドの中では、そのコンポーネントのフィールドを直接操作できます。

``ContextMenuItem`` 属性の第 2 引数には、実行するメソッドの名前を文字列で指定します。サンプルコードのように ``nameof`` 演算子を使うと、メソッド名を変更したときの書き換え漏れを防げます。

参考資料
========================================================================

* :unity-api:`MenuItem`
* :unity-api:`MenuCommand`
* :unity-api:`GameObjectUtility.SetParentAndAlign`
* :unity-api:`ContextMenu`
* :unity-api:`ContextMenuItemAttribute`
