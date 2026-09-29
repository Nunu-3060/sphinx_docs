########################################################################
SerializedObject と Undo
########################################################################

エディター拡張では、スクリプトからコンポーネントやアセットの値を変更する場面が多くあります。このとき、単にフィールドへ値を代入するだけでは、次のような問題が起きます。

* Ctrl + Z で元に戻せない
* シーンやアセットが「変更あり」にならず、変更が保存されないことがある
* プレハブのインスタンスで、変更がオーバーライドとして記録されない

この章では、これらの問題を避けるための 2 つの方法を説明します。第 6 章以降のサンプルコードは、すべてこの章の方法に従っています。

方法 1：SerializedObject を使う
========================================================================

``SerializedObject`` は、Unity がシリアライズしたデータを通してオブジェクトを読み書きするためのクラスです。Inspector ウィンドウも、内部ではこの仕組みで値を表示・変更しています。

``SerializedObject`` を使って値を変更する手順は次のとおりです。

.. code-block:: csharp

   // 1. 変更したいオブジェクトから SerializedObject を作成します。
   var serializedEnemy = new SerializedObject(enemy);

   // 2. フィールド名を指定して SerializedProperty を取得します。
   var hpProperty = serializedEnemy.FindProperty("hp");

   // 3. 型に応じたプロパティ（intValue、floatValue、stringValue など）で値を変更します。
   hpProperty.intValue = 100;

   // 4. 変更をオブジェクトに反映します。
   serializedEnemy.ApplyModifiedProperties();

``ApplyModifiedProperties`` を呼ぶと、次の処理がまとめて行われます。

* 変更を Undo に記録する
* オブジェクト（シーン上のオブジェクトならシーン）を変更ありにする
* プレハブのインスタンスなら、変更をオーバーライドとして記録する

``SerializedObject`` を使う利点は、ほかにもあります。

* private フィールドでも、シリアライズされていればフィールド名で読み書きできる
* 複数のオブジェクトをまとめて編集できる（第 6 章で説明します）
* UI Toolkit の入力欄と結び付ける（バインドする）ことができる

一方で、フィールド名を文字列で指定するため、フィールド名を変更したときにコンパイルエラーにならず、実行時に ``FindProperty`` が ``null`` を返すようになる点に注意が必要です。フィールド名は定数にまとめておくと、変更漏れを防ぎやすくなります。

Update と ApplyModifiedProperties
------------------------------------------------------------------------

``SerializedObject`` は、作成した時点のオブジェクトの値を保持しています。作成した後にほかの処理でオブジェクトの値が変わった場合は、``Update`` メソッドを呼んで最新の値を読み込み直します。

.. code-block:: csharp

   serializedEnemy.Update();                    // 最新の値を読み込む
   hpProperty.intValue += 10;                   // 値を変更する
   serializedEnemy.ApplyModifiedProperties();   // 変更を反映する

UI Toolkit で作成した Inspector ウィンドウやウィンドウでは、入力欄をバインドしておけば、読み込みと反映は自動で行われます。``Update`` と ``ApplyModifiedProperties`` を自分で呼ぶ必要があるのは、ボタンをクリックしたときの処理などで、スクリプトから直接値を変更する場合です。

方法 2：Undo.RecordObject を使う
========================================================================

オブジェクトのフィールドやプロパティを直接変更する場合は、変更する前に ``Undo.RecordObject`` を呼びます。

.. code-block:: csharp

   // 変更前の状態を記録します。第 2 引数は Undo の履歴に表示される名前です。
   Undo.RecordObject(transform, "Reset Y Position");

   var position = transform.localPosition;
   position.y = 0f;
   transform.localPosition = position;

``Undo.RecordObject`` は、呼んだ時点のオブジェクトの状態を記録し、後で変更後の状態と比べて差分を Undo に登録します。同時に、オブジェクトを変更ありにします。そのため、シーン上のオブジェクトであれば ``EditorUtility.SetDirty`` を別に呼ぶ必要はありません。

ただし、次の場合は追加の処理が必要です。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 変更するオブジェクト
     - 追加で必要な処理
   * - プレハブのインスタンス
     - 変更後に ``PrefabUtility.RecordPrefabInstancePropertyModifications`` を呼び、変更をオーバーライドとして記録します。
   * - ScriptableObject などのアセット
     - Unity のスクリプトリファレンスでは、``Undo.RecordObject`` に加えて ``EditorUtility.SetDirty`` も呼ぶことが推奨されています。

複数のオブジェクトをまとめて変更する場合は、``Undo.RecordObjects`` を使うと、1 回の Ctrl + Z でまとめて元に戻せます。

作成・削除・親子関係の変更
------------------------------------------------------------------------

``Undo.RecordObject`` で記録できるのは、既存のオブジェクトの値の変更だけです。オブジェクトの作成や削除、親子関係の変更には、それぞれ専用のメソッドを使います。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 操作
     - 使うメソッド
   * - ゲームオブジェクトの作成
     - 作成後に ``Undo.RegisterCreatedObjectUndo`` を呼ぶ
   * - コンポーネントの追加
     - ``AddComponent`` の代わりに ``Undo.AddComponent`` を使う
   * - オブジェクトの削除
     - ``Object.DestroyImmediate`` の代わりに ``Undo.DestroyObjectImmediate`` を使う
   * - 親子関係の変更
     - ``Transform.SetParent`` の代わりに ``Undo.SetTransformParent`` を使う

どちらの方法を使うか
========================================================================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 観点
     - SerializedObject
     - Undo.RecordObject
   * - Undo・変更あり・オーバーライドの記録
     - すべて自動
     - プレハブのインスタンスなどでは追加の処理が必要
   * - private フィールドの変更
     - できる（フィールド名を文字列で指定）
     - できない（public なメンバーが必要）
   * - UI Toolkit とのバインド
     - できる
     - できない
   * - 書きやすさ
     - 手順が多い
     - 通常の C# のコードと同じように書ける

Inspector ウィンドウのカスタマイズや、シリアライズされたフィールドの変更には ``SerializedObject`` を使うのが基本です。``Transform`` の位置のようにプロパティとして公開されている値を変更する場合や、Scene ビューのハンドルで値を変更する場合は、``Undo.RecordObject`` を使うと簡潔に書けます。

参考資料
========================================================================

* :unity-api:`SerializedObject`
* :unity-api:`SerializedProperty`
* :unity-api:`Undo`
* :unity-api:`Undo.RecordObject`
* :unity-api:`EditorUtility.SetDirty`
* :unity-api:`PrefabUtility.RecordPrefabInstancePropertyModifications`
