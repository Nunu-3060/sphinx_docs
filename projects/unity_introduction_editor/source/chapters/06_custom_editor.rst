########################################################################
カスタムエディター
########################################################################

カスタムエディターを使うと、特定のコンポーネントの Inspector ウィンドウの表示を自由に組み立てられます。この章では、敵キャラクターを表す ``Enemy`` コンポーネントに、日本語のラベル、警告メッセージ、ボタンを追加します。

サンプルコード
========================================================================

表示の対象となるコンポーネントです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/Enemy.cs
   :caption: Runtime/Enemy.cs
   :linenos:

:download:`Enemy.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/Enemy.cs>`

カスタムエディターです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/EnemyEditor.cs
   :caption: Editor/EnemyEditor.cs
   :linenos:

:download:`EnemyEditor.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/EnemyEditor.cs>`

カスタムエディターの作り方
========================================================================

カスタムエディターは、次の手順で作成します。

#. ``UnityEditor.Editor`` クラスを継承したクラスを、エディター専用のアセンブリに作成します。
#. クラスに ``CustomEditor`` 属性を付け、対象のコンポーネントの型を指定します。
#. ``CreateInspectorGUI`` メソッドをオーバーライドし、表示する UI を作成して返します。

.. code-block:: csharp

   [CustomEditor(typeof(Enemy))]
   public class EnemyEditor : Editor
   {
       public override VisualElement CreateInspectorGUI()
       {
           var root = new VisualElement();
           // root に入力欄やボタンを追加します。
           return root;
       }
   }

``CreateInspectorGUI`` が返した ``VisualElement`` が、Inspector ウィンドウのコンポーネントの欄に表示されます。``VisualElement`` は UI Toolkit の UI を構成する要素の基底クラスで、ほかの要素を子として持てます。

``Editor`` クラスには、カスタムエディターで使う次のメンバーがあります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メンバー
     - 内容
   * - ``target``
     - 表示の対象となっているオブジェクト。複数選択時は、そのうちの 1 つ
   * - ``targets``
     - 表示の対象となっているすべてのオブジェクト
   * - ``serializedObject``
     - 対象のオブジェクトを扱う ``SerializedObject``。複数選択時は、すべての対象をまとめて扱う

PropertyField で入力欄を作る
========================================================================

``PropertyField`` は、``SerializedProperty`` の型に合わせて適切な入力欄を作成する要素です。int 型なら整数の入力欄、string 型なら文字列の入力欄が作成されます。第 4 章の ``Min`` 属性のような属性や、第 7 章で作成する PropertyDrawer も反映されます。

.. code-block:: csharp

   root.Add(new PropertyField(serializedObject.FindProperty("maxHp"), "最大 HP"));

第 2 引数を指定すると、ラベルの文字列を変更できます。省略した場合は、フィールド名から作られた表示名（``maxHp`` なら「Max Hp」）が使われます。

``CreateInspectorGUI`` が返した要素は、Inspector ウィンドウが自動で ``serializedObject`` にバインドします。バインドされた入力欄は、値の表示と変更の反映を自動で行うため、第 5 章で説明した ``Update`` や ``ApplyModifiedProperties`` を自分で呼ぶ必要はありません。

値の変化に応じて表示を変える
========================================================================

サンプルコードでは、HP が最大 HP を超えているときだけ警告を表示しています。

.. code-block:: csharp

   root.TrackPropertyValue(maxHpProperty, _ => UpdateHpWarning());
   root.TrackPropertyValue(hpProperty, _ => UpdateHpWarning());

``TrackPropertyValue`` は、指定した ``SerializedProperty`` の値が変わるたびにコールバックを呼ぶメソッドです。Inspector ウィンドウでの入力だけでなく、Undo やスクリプトによる変更でも呼ばれます。

要素の表示・非表示は、``style.display`` プロパティで切り替えます。``DisplayStyle.None`` にすると要素は非表示になり、レイアウト上の場所も占めなくなります。

ボタンを追加する
========================================================================

``Button`` のコンストラクターにメソッドを渡すと、ボタンをクリックしたときにそのメソッドが呼ばれます。

.. code-block:: csharp

   var healButton = new Button(HealAll) { text = "HP を全回復" };

ボタンの処理でスクリプトから値を変更する場合は、第 5 章の方法に従います。サンプルコードでは、``SerializedObject`` を使って変更しています。

複数選択への対応
========================================================================

カスタムエディターは、既定では複数のオブジェクトを同時に編集できません。複数選択に対応するには、クラスに ``CanEditMultipleObjects`` 属性を付けます。

``CanEditMultipleObjects`` 属性を付けると、``serializedObject`` がすべての対象をまとめて扱うようになります。``PropertyField`` で値を変更すると、選択中のすべてのオブジェクトに同じ値が設定されます。対象ごとに値が異なる入力欄には「—」が表示されます。

ボタンの処理のように、対象ごとに異なる値を設定したい場合は注意が必要です。例えば「HP を最大 HP と同じ値にする」処理で ``serializedObject`` を使うと、``maxHp`` プロパティの ``intValue`` は 1 つ目の対象の値しか返さないため、すべての対象の HP が 1 つ目の対象の最大 HP になってしまいます。サンプルコードでは、``targets`` の要素ごとに ``SerializedObject`` を作成して、この問題を避けています。

.. code-block:: csharp

   foreach (var t in targets)
   {
       var enemyObject = new SerializedObject(t);
       var maxHp = enemyObject.FindProperty(MaxHpField).intValue;
       enemyObject.FindProperty(HpField).intValue = maxHp;
       enemyObject.ApplyModifiedProperties();
   }

既定の表示に要素を追加する
========================================================================

すべてのフィールドを自分で並べるのではなく、既定の表示に要素を少し追加したいだけの場合は、``InspectorElement.FillDefaultInspector`` を使います。

.. code-block:: csharp

   public override VisualElement CreateInspectorGUI()
   {
       var root = new VisualElement();

       // 既定の Inspector ウィンドウと同じ入力欄を root に追加します。
       InspectorElement.FillDefaultInspector(root, serializedObject, this);

       root.Add(new Button(HealAll) { text = "HP を全回復" });
       return root;
   }

この方法なら、コンポーネントにフィールドを追加したときに、カスタムエディターを修正する必要がありません。

参考：IMGUI による書き方
========================================================================

UI Toolkit が導入される前は、``OnInspectorGUI`` メソッドをオーバーライドし、IMGUI で表示を記述していました。既存のコードや資料の多くはこの書き方なので、読めるようにしておくと役に立ちます。

.. code-block:: csharp

   public override void OnInspectorGUI()
   {
       // 最新の値を読み込みます。
       serializedObject.Update();

       EditorGUILayout.PropertyField(serializedObject.FindProperty("enemyName"), new GUIContent("名前"));
       EditorGUILayout.PropertyField(serializedObject.FindProperty("maxHp"), new GUIContent("最大 HP"));
       EditorGUILayout.PropertyField(serializedObject.FindProperty("hp"), new GUIContent("HP"));

       // 変更を反映します。
       serializedObject.ApplyModifiedProperties();

       if (GUILayout.Button("HP を全回復"))
       {
           HealAll();
       }
   }

IMGUI の ``OnInspectorGUI`` は、再描画のたびに毎回呼ばれ、UI を毎回作り直します。そのため、``Update`` と ``ApplyModifiedProperties`` を毎回自分で呼ぶ必要があります。UI Toolkit の ``CreateInspectorGUI`` は最初に 1 回だけ呼ばれ、作成した UI はそのまま使い続けられます。

``CreateInspectorGUI`` が要素を返した場合、``OnInspectorGUI`` は使われません。両者の違いは「:doc:`13_appendix`」にもまとめています。

参考資料
========================================================================

* :unity-api:`Editor`
* :unity-api:`CustomEditor`
* :unity-api:`CanEditMultipleObjects`
* :unity-api:`UIElements.PropertyField`
* :unity-api:`UIElements.BindingExtensions.TrackPropertyValue`
* :unity-api:`UIElements.InspectorElement.FillDefaultInspector`
* `カスタムインスペクターの作成 <https://docs.unity3d.com/ja/6000.0/Manual/UIE-HowTo-CreateCustomInspector.html>`_\ （Unity マニュアル）
