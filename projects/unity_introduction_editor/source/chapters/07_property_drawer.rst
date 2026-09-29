########################################################################
PropertyDrawer と DecoratorDrawer
########################################################################

第 6 章のカスタムエディターは、コンポーネント単位で表示をカスタマイズする仕組みでした。これに対して PropertyDrawer は、フィールド単位で表示をカスタマイズする仕組みです。一度作成すれば、どのコンポーネントのフィールドにも適用されます。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 仕組み
     - カスタマイズの単位
     - 適用される場所
   * - カスタムエディター
     - コンポーネント（またはアセット）の型
     - 指定した型の Inspector ウィンドウ全体
   * - PropertyDrawer
     - フィールドの型、または属性
     - その型のフィールド、またはその属性を付けたフィールド
   * - DecoratorDrawer
     - 属性
     - その属性を付けたフィールドの上

サンプルコード
========================================================================

PropertyDrawer と DecoratorDrawer が適用されるフィールドを持つコンポーネントです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/DrawerExample.cs
   :caption: Runtime/DrawerExample.cs
   :linenos:

:download:`DrawerExample.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/DrawerExample.cs>`

このコンポーネントをゲームオブジェクトに追加すると、Inspector ウィンドウは次のように表示されます。

* 「Spawn Interval」の上に、補足説明が表示される
* 「Spawn Interval」の最小値と最大値が 1 行に並び、最小値が最大値を超えると警告が表示される
* 「Target Tag」が、タグを選択するドロップダウンになる

型に対する PropertyDrawer
========================================================================

最小値と最大値の組を表す ``MinMaxRange`` 構造体を例に、独自の型の表示をカスタマイズします。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/MinMaxRange.cs
   :caption: Runtime/MinMaxRange.cs
   :linenos:

:download:`MinMaxRange.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/MinMaxRange.cs>`

独自の型をシリアライズするには、型に ``Serializable`` 属性を付けます。PropertyDrawer を作成しない場合、この型のフィールドは、折りたたみ可能な見出しの下に「Min」と「Max」が縦に並んで表示されます。

この表示を 1 行にまとめる PropertyDrawer が次のコードです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/MinMaxRangeDrawer.cs
   :caption: Editor/MinMaxRangeDrawer.cs
   :linenos:

:download:`MinMaxRangeDrawer.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/MinMaxRangeDrawer.cs>`

PropertyDrawer は、次の手順で作成します。

#. ``PropertyDrawer`` クラスを継承したクラスを、エディター専用のアセンブリに作成します。
#. クラスに ``CustomPropertyDrawer`` 属性を付け、対象の型を指定します。
#. ``CreatePropertyGUI`` メソッドをオーバーライドし、表示する UI を作成して返します。

``CreatePropertyGUI`` の引数には、表示の対象となるフィールドの ``SerializedProperty`` が渡されます。構造体やクラスの中のフィールドは、``FindPropertyRelative`` にフィールド名を指定して取得します。

入力欄と ``SerializedProperty`` を結び付けるには、``BindProperty`` メソッドを使います。

.. code-block:: csharp

   var field = new FloatField(label);
   field.BindProperty(property);

最小値が最大値を超えたときの警告は、第 6 章と同じく ``TrackPropertyValue`` を使って表示を切り替えています。

属性に対する PropertyDrawer
========================================================================

PropertyDrawer は、型ではなく属性に対しても作成できます。属性に対する PropertyDrawer を使うと、同じ string 型のフィールドでも、属性を付けたものだけ表示を変えられます。

まず、``PropertyAttribute`` を継承した属性クラスを作成します。属性はゲーム本体側のスクリプトで使うため、ゲーム本体側のアセンブリに置きます。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/TagSelectorAttribute.cs
   :caption: Runtime/TagSelectorAttribute.cs
   :linenos:

:download:`TagSelectorAttribute.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/TagSelectorAttribute.cs>`

次に、この属性に対する PropertyDrawer を、エディター専用のアセンブリに作成します。``CustomPropertyDrawer`` 属性には、属性クラスの型を指定します。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/TagSelectorDrawer.cs
   :caption: Editor/TagSelectorDrawer.cs
   :linenos:

:download:`TagSelectorDrawer.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/TagSelectorDrawer.cs>`

属性は、どの型のフィールドにも付けられてしまいます。サンプルコードでは、``propertyType`` でフィールドの型を調べ、string 型以外に付けられた場合はエラーメッセージを表示しています。

``TagField`` は、プロジェクトに登録されているタグを選択肢に持つドロップダウンです。UI Toolkit には、このほかにもエディター用の入力欄が用意されています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 要素
     - 内容
   * - ``TagField``
     - タグを選択するドロップダウン
   * - ``LayerField``
     - レイヤーを選択するドロップダウン
   * - ``ObjectField``
     - オブジェクトの参照を指定する入力欄
   * - ``ColorField``
     - 色を指定する入力欄

``BaseField<string>.alignedFieldUssClassName`` は、Inspector ウィンドウでほかのフィールドとラベルの幅をそろえるための USS クラス名です。``PropertyField`` が作成する入力欄には自動で付きますが、自分で作成した入力欄には付かないため、明示的に追加しています。

DecoratorDrawer
========================================================================

DecoratorDrawer は、フィールドの上に装飾を加えるための仕組みです。第 4 章の ``Header`` 属性や ``Space`` 属性も、DecoratorDrawer で実現されています。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/NoteAttribute.cs
   :caption: Runtime/NoteAttribute.cs
   :linenos:

:download:`NoteAttribute.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/NoteAttribute.cs>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/NoteDrawer.cs
   :caption: Editor/NoteDrawer.cs
   :linenos:

:download:`NoteDrawer.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/NoteDrawer.cs>`

DecoratorDrawer はフィールドの値を扱わないため、``CreatePropertyGUI`` に引数がありません。属性に渡した値は、``attribute`` プロパティから取得します。

PropertyDrawer と違い、DecoratorDrawer は 1 つのフィールドに複数適用できます。サンプルコードの ``spawnInterval`` フィールドでは、``Note`` 属性による DecoratorDrawer と、``MinMaxRange`` 型に対する PropertyDrawer が同時に適用されています。

PropertyDrawer を作るときの注意点
========================================================================

PropertyDrawer の中で、同じフィールドの ``PropertyField`` を作らない
------------------------------------------------------------------------

属性に対する PropertyDrawer の中で、引数の ``property`` をそのまま ``PropertyField`` に渡すと、その ``PropertyField`` にも同じ PropertyDrawer が適用される可能性があります。サンプルコードの ``TagSelectorDrawer`` のように、``TagField`` などの具体的な入力欄を作成してください。

一方、``FindPropertyRelative`` で取得した子のフィールドを ``PropertyField`` で表示するのは問題ありません。

IMGUI の Inspector ウィンドウでは表示されない
------------------------------------------------------------------------

``CreatePropertyGUI`` は UI Toolkit 用のメソッドです。Unity 6 の既定の Inspector ウィンドウは UI Toolkit で表示されるため、通常は問題ありません。ただし、IMGUI の ``OnInspectorGUI`` で作られたカスタムエディターの中では ``CreatePropertyGUI`` は使われず、代わりに IMGUI 用の ``OnGUI`` メソッドが呼ばれます。``OnGUI`` を実装していない場合は、「No GUI Implemented」と表示されます。

参考資料
========================================================================

* :unity-api:`PropertyDrawer`
* :unity-api:`PropertyDrawer.CreatePropertyGUI`
* :unity-api:`DecoratorDrawer`
* :unity-api:`PropertyAttribute`
* :unity-api:`UIElements.TagField`
* :unity-api:`UIElements.BaseField_1-alignedFieldUssClassName`
