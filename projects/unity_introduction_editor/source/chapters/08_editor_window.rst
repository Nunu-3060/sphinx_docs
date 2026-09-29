########################################################################
EditorWindow
########################################################################

``EditorWindow`` を継承すると、Inspector ウィンドウや Console ウィンドウと同じように、ドッキングやタブ化ができる独自のウィンドウを作成できます。この章では、選択中のオブジェクトの一覧を表示するウィンドウを作成します。

また、この章では UI の構造を UXML、見た目を USS という別のファイルに記述する方法も説明します。

サンプルコード
========================================================================

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/SampleWindow.cs
   :caption: Editor/SampleWindow.cs
   :linenos:

:download:`SampleWindow.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/SampleWindow.cs>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/UI/SampleWindow.uxml
   :language: xml
   :caption: Editor/UI/SampleWindow.uxml
   :linenos:

:download:`SampleWindow.uxml をダウンロード <../../examples/Assets/EditorIntro/Editor/UI/SampleWindow.uxml>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/UI/SampleWindow.uss
   :language: css
   :caption: Editor/UI/SampleWindow.uss
   :linenos:

:download:`SampleWindow.uss をダウンロード <../../examples/Assets/EditorIntro/Editor/UI/SampleWindow.uss>`

:menuselection:`Tools --> Editor Intro --> Sample Window` を選択するとウィンドウが開きます。Hierarchy ウィンドウや Project ウィンドウでオブジェクトを選択すると、その名前が一覧に表示されます。

ウィンドウを開く
========================================================================

ウィンドウを開くメソッドは、第 3 章の ``MenuItem`` 属性を使ってメニューに登録します。

.. code-block:: csharp

   [MenuItem("Tools/Editor Intro/Sample Window")]
   public static void Open()
   {
       var window = GetWindow<SampleWindow>();
       window.titleContent = new GUIContent("Sample Window");
   }

``GetWindow<T>`` は、指定した型のウィンドウが既に開いていればそのウィンドウを、開いていなければ新しく作成して返します。そのため、メニューを何度選択しても、同じウィンドウが複数開くことはありません。``titleContent`` には、ウィンドウのタブに表示するタイトルを設定します。

ウィンドウの UI を作成する
========================================================================

ウィンドウの UI は ``CreateGUI`` メソッドで作成します。``CreateGUI`` は、ウィンドウが開かれたときや、ドメインリロードの後に UI を作り直すときに呼ばれます。

作成した要素は、``rootVisualElement`` プロパティが返す要素に子として追加します。カスタムエディターの ``CreateInspectorGUI`` では作成した要素を戻り値として返しましたが、``EditorWindow`` では ``rootVisualElement`` に追加する点が異なります。

UI は C# のコードだけでも作成できます。第 12 章の一括リネームツールは、C# のコードだけで UI を作成しています。この章では、UXML と USS を使う方法を説明します。

UXML で UI の構造を記述する
========================================================================

UXML は、UI の構造を XML 形式で記述するファイルです。HTML に似た書き方で、要素の入れ子関係を記述します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 記述
     - 意味
   * - ``<ui:Label text="..." />``
     - ``Label`` 要素を作成し、``text`` プロパティを設定します。
   * - ``name="count-label"``
     - 要素に名前を付けます。C# のコードから要素を探すときに使います。
   * - ``class="heading"``
     - 要素に USS クラスを付けます。USS でスタイルを指定するときに使います。
   * - ``<ui:Style src="..." />``
     - USS ファイルを読み込みます。``src`` には UXML ファイルからの相対パスを指定します。

C# のコードでは、``AssetDatabase.LoadAssetAtPath<VisualTreeAsset>`` で UXML ファイルを読み込み、``CloneTree`` で内容を ``rootVisualElement`` に複製します。

.. code-block:: csharp

   var visualTree = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>(UxmlPath);
   visualTree.CloneTree(rootVisualElement);

複製した要素は、``Q`` メソッドに型と名前を指定して取得します。

.. code-block:: csharp

   countLabel = rootVisualElement.Q<Label>("count-label");
   rootVisualElement.Q<Button>("ping-button").clicked += PingActiveObject;

UXML ファイルのパスについて
------------------------------------------------------------------------

サンプルコードでは、UXML ファイルのパスを定数で指定しています。サンプルコードを ``Assets/EditorIntro`` 以外の場所に置いた場合は、``UxmlPath`` を変更してください。

パスの指定を避けたい場合は、``VisualTreeAsset`` 型のシリアライズされるフィールド（``SerializeField`` 属性を付けた private フィールドなど）を用意し、スクリプトの「既定の参照（Default References）」に UXML ファイルを設定する方法もあります。スクリプトファイルを Project ウィンドウで選択すると、Inspector ウィンドウで既定の参照を設定できます。

UI Builder
------------------------------------------------------------------------

UXML ファイルは、:menuselection:`Window --> UI Toolkit --> UI Builder` で開く UI Builder を使うと、画面上で要素を配置しながら作成できます。UI Builder で作成した UXML ファイルも、C# のコードからは同じ方法で読み込めます。

USS で見た目を指定する
========================================================================

USS（Unity Style Sheet）は、要素の見た目を指定するファイルです。Web ページの CSS に似た書き方で、セレクターとプロパティを記述します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - セレクター
     - 対象
   * - ``.heading``
     - USS クラス ``heading`` が付いた要素
   * - ``#count-label``
     - 名前が ``count-label`` の要素
   * - ``Button``
     - ``Button`` 型の要素
   * - ``.button-row > Button``
     - USS クラス ``button-row`` が付いた要素の、直下の子である ``Button`` 型の要素

USS のプロパティの多くは CSS と同じ名前ですが、``-unity-font-style`` のように「-unity-」で始まる Unity 独自のプロパティもあります。

UI Toolkit のレイアウトは、Flexbox という仕組みに基づいています。既定では子の要素は縦に並び、``flex-direction: row`` を指定すると横に並びます。``flex-grow: 1`` を指定した要素は、余った幅（または高さ）いっぱいに広がります。

選択の変更に反応する
========================================================================

``EditorWindow`` には、エディターの状態が変わったときに呼ばれるメソッドがいくつか用意されています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 呼ばれるタイミング
   * - ``OnSelectionChange``
     - Hierarchy ウィンドウや Project ウィンドウでの選択が変わったとき
   * - ``OnHierarchyChange``
     - シーン上のゲームオブジェクトが追加・削除・変更されたとき
   * - ``OnProjectChange``
     - プロジェクト内のアセットが追加・削除・変更されたとき
   * - ``OnFocus``、``OnLostFocus``
     - ウィンドウがフォーカスを得たとき、失ったとき

サンプルコードでは、``OnSelectionChange`` で表示を更新しています。``OnSelectionChange`` は ``CreateGUI`` より前に呼ばれることもあるため、``Refresh`` メソッドの先頭で、要素が作成済みかどうかを確認しています。

選択中のオブジェクトは、``Selection`` クラスで取得・変更できます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メンバー
     - 内容
   * - ``Selection.activeObject``
     - 選択中のオブジェクトのうち、アクティブな（最後に選択した）もの
   * - ``Selection.activeGameObject``
     - アクティブなオブジェクトがゲームオブジェクトの場合はそのゲームオブジェクト、それ以外は ``null``
   * - ``Selection.objects``
     - 選択中のすべてのオブジェクト。代入すると選択を変更できる
   * - ``Selection.gameObjects``
     - 選択中のすべてのゲームオブジェクト

参考資料
========================================================================

* :unity-api:`EditorWindow`
* :unity-api:`EditorWindow.GetWindow`
* :unity-api:`Selection`
* :unity-api:`UIElements.VisualTreeAsset`
* `UI Toolkit <https://docs.unity3d.com/ja/6000.0/Manual/UIElements.html>`_\ （Unity マニュアル）
* `USS プロパティリファレンス <https://docs.unity3d.com/ja/6000.0/Manual/UIE-USS-Properties-Reference.html>`_\ （Unity マニュアル）
