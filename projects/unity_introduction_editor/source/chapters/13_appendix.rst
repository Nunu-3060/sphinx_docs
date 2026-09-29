########################################################################
付録
########################################################################

よくあるトラブルと対処
========================================================================

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - 症状
     - 主な原因
     - 対処
   * - ゲームのビルド時に「The type or namespace name 'UnityEditor' could not be found」と表示される
     - ``UnityEditor`` を使うスクリプトが、ゲーム本体のアセンブリに含まれている
     - スクリプトを Editor フォルダーまたはエディター専用のアセンブリに移すか、``#if UNITY_EDITOR`` で囲む（第 2 章）
   * - 「'Editor' is a namespace but is used like a type」と表示される
     - 名前空間の一部に「Editor」という名前を使っている
     - 名前空間の名前を変更するか、``UnityEditor.Editor`` と完全な名前で書く（第 1 章）
   * - メニュー項目が表示されない
     - メソッドが static ではない、またはコンパイルエラーがある
     - メソッドを static にする。Console ウィンドウでコンパイルエラーを確認する
   * - カスタムエディターが使われない
     - ``CustomEditor`` 属性の型の指定が誤っている、またはコンパイルエラーがある
     - ``CustomEditor`` 属性の引数を確認する。Console ウィンドウでコンパイルエラーを確認する
   * - 変更した値が保存されない、Ctrl + Z で元に戻せない
     - フィールドに値を直接代入している
     - ``SerializedObject`` または ``Undo.RecordObject`` を使う（第 5 章）
   * - プレハブのインスタンスで変更が元に戻る
     - 変更がオーバーライドとして記録されていない
     - ``SerializedObject`` を使うか、``PrefabUtility.RecordPrefabInstancePropertyModifications`` を呼ぶ（第 5 章）
   * - ``FindProperty`` が ``null`` を返す
     - フィールド名の誤り、またはフィールドがシリアライズされていない
     - フィールド名の綴りを確認する。private フィールドなら ``SerializeField`` 属性が付いているか確認する
   * - PropertyDrawer の位置に「No GUI Implemented」と表示される
     - IMGUI で作られたカスタムエディターの中で表示されている
     - PropertyDrawer に IMGUI 用の ``OnGUI`` も実装するか、カスタムエディターを UI Toolkit で作り直す（第 7 章）
   * - EditorWindow に UXML の内容が表示されない
     - UXML ファイルのパスが誤っている
     - UXML ファイルの場所と、コードで指定したパスが一致しているか確認する（第 8 章）
   * - エディター拡張で保持していた値が消える
     - static フィールドの値がドメインリロードで初期化された
     - ``EditorPrefs`` や ``ScriptableSingleton`` で保存する（第 11 章）

UI Toolkit と IMGUI の対応表
========================================================================

既存のコードや資料を読むときの参考に、UI Toolkit と IMGUI で同じことをする場合の書き方を示します。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 用途
     - UI Toolkit
     - IMGUI
   * - カスタムエディターの UI を作るメソッド
     - ``Editor.CreateInspectorGUI``
     - ``Editor.OnInspectorGUI``
   * - PropertyDrawer の UI を作るメソッド
     - ``PropertyDrawer.CreatePropertyGUI``
     - ``PropertyDrawer.OnGUI``、``PropertyDrawer.GetPropertyHeight``
   * - EditorWindow の UI を作るメソッド
     - ``EditorWindow.CreateGUI``
     - ``EditorWindow.OnGUI``
   * - UI を作るタイミング
     - 最初に 1 回だけ
     - 再描画のたびに毎回
   * - シリアライズされたフィールドの入力欄
     - ``PropertyField``
     - ``EditorGUILayout.PropertyField``
   * - 文字列の入力欄
     - ``TextField``
     - ``EditorGUILayout.TextField``
   * - 整数の入力欄
     - ``IntegerField``
     - ``EditorGUILayout.IntField``
   * - ボタン
     - ``Button``\ （``clicked`` イベントで処理を実行）
     - ``GUILayout.Button``\ （クリックされたフレームで ``true`` を返す）
   * - メッセージの表示
     - ``HelpBox``
     - ``EditorGUILayout.HelpBox``
   * - 横に並べる
     - ``style.flexDirection = FlexDirection.Row``
     - ``EditorGUILayout.BeginHorizontal`` と ``EditorGUILayout.EndHorizontal``
   * - SerializedObject との同期
     - バインドにより自動
     - ``serializedObject.Update`` と ``serializedObject.ApplyModifiedProperties`` を自分で呼ぶ
   * - 見た目の指定
     - USS
     - ``GUIStyle``

Scene ビューの ``OnSceneGUI`` と ``Handles`` は、UI Toolkit を使う場合でも IMGUI と同じ仕組みで描画します。第 9 章の ``EditorGUI.BeginChangeCheck`` も IMGUI の機能です。

用語集
========================================================================

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 用語
     - 意味
   * - アセンブリ
     - スクリプトをコンパイルした結果の単位（DLL ファイル）。アセンブリ定義ファイルで分割できる
   * - シリアライズ
     - オブジェクトの状態を、保存できる形式に変換すること。Unity では、シーンやアセットにフィールドの値を保存する仕組みを指す
   * - ドメインリロード
     - スクリプトの再コンパイル後などに、読み込まれているスクリプトをすべて破棄して読み込み直す処理
   * - バインド
     - UI Toolkit の入力欄と ``SerializedProperty`` を結び付け、値を自動で同期させること
   * - オーバーライド（プレハブ）
     - プレハブのインスタンスで、元のプレハブと異なる値に変更された部分
   * - ダーティ（変更あり）
     - オブジェクトやシーンに、保存されていない変更がある状態

参考資料
========================================================================

Unity マニュアル
------------------------------------------------------------------------

* `Unity 6 ユーザーマニュアル <https://docs.unity3d.com/ja/6000.0/Manual/index.html>`_
* `C# スクリプトを使用したカスタムエディターウィンドウの作成 <https://docs.unity3d.com/ja/6000.0/Manual/UIE-HowTo-CreateEditorWindow.html>`_
* `カスタムインスペクターの作成 <https://docs.unity3d.com/ja/6000.0/Manual/UIE-HowTo-CreateCustomInspector.html>`_
* `UI Toolkit <https://docs.unity3d.com/ja/6000.0/Manual/UIElements.html>`_
* `Unity の UI システムの比較 <https://docs.unity3d.com/ja/6000.0/Manual/UI-system-compare.html>`_

スクリプトリファレンス
------------------------------------------------------------------------

* `スクリプトリファレンス（Unity 6） <https://docs.unity3d.com/6000.0/Documentation/ScriptReference/index.html>`_
* :unity-api:`Editor`
* :unity-api:`EditorWindow`
* :unity-api:`PropertyDrawer`
* :unity-api:`AssetDatabase`
