########################################################################
アセットの操作
########################################################################

この章では、スクリプトからアセットを作成・検索・変更する方法と、アセットのインポート時に処理を加える方法を説明します。

ScriptableObject
========================================================================

``ScriptableObject`` は、ゲームオブジェクトに追加しなくても、単独のアセットとしてデータを保存できるクラスです。アイテムや敵のパラメーターなど、複数の場所から参照する設定データを保存するのに向いています。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/ItemData.cs
   :caption: Runtime/ItemData.cs
   :linenos:

:download:`ItemData.cs をダウンロード <../../examples/Assets/EditorIntro/Runtime/ItemData.cs>`

``CreateAssetMenu`` 属性を付けると、Project ウィンドウの右クリックメニューから、:menuselection:`Create --> Editor Intro --> Item Data` を選択してアセットを作成できます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 引数
     - 意味
   * - ``fileName``
     - 作成されるアセットの既定のファイル名
   * - ``menuName``
     - :menuselection:`Create` メニューの下の、項目のパス
   * - ``order``
     - メニュー内での表示順（省略可）

``ScriptableObject`` は ``UnityEngine`` 名前空間のクラスであり、ビルドしたゲームからもアセットのデータを読み込めます。ただし、アセットの作成や変更の保存はエディターでだけ行えます。

AssetDatabase
========================================================================

``AssetDatabase`` は、プロジェクト内のアセットをスクリプトから操作するためのクラスです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/AssetUtility.cs
   :caption: Editor/AssetUtility.cs
   :linenos:

:download:`AssetUtility.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/AssetUtility.cs>`

このサンプルコードは、:menuselection:`Tools --> Editor Intro --> Assets` の下に 3 つのメニュー項目を追加します。

アセットのパス
------------------------------------------------------------------------

``AssetDatabase`` では、アセットの場所を「Assets/」から始まるパスで指定します。区切り文字は、Windows でも「/」を使います。

.. code-block:: text

   Assets/Data/Potion.asset

アセットを作成する
------------------------------------------------------------------------

``ScriptableObject`` のインスタンスは、``new`` ではなく ``ScriptableObject.CreateInstance`` で作成します。作成したインスタンスを ``AssetDatabase.CreateAsset`` に渡すと、指定したパスにアセットとして保存されます。

.. code-block:: csharp

   var item = ScriptableObject.CreateInstance<ItemData>();
   var path = AssetDatabase.GenerateUniqueAssetPath("Assets/NewItemData.asset");
   AssetDatabase.CreateAsset(item, path);
   AssetDatabase.SaveAssets();

``AssetDatabase.CreateAsset`` は、同じパスに既にアセットがあると上書きします。``AssetDatabase.GenerateUniqueAssetPath`` を使うと、同じ名前のファイルがある場合に「NewItemData 1.asset」のような重複しないパスが返されるため、誤って上書きするのを防げます。

アセットを検索する
------------------------------------------------------------------------

``AssetDatabase.FindAssets`` は、検索条件に合うアセットの GUID の配列を返します。GUID は、アセットごとに割り当てられる一意の識別子です。GUID は ``AssetDatabase.GUIDToAssetPath`` でパスに変換し、``AssetDatabase.LoadAssetAtPath`` でアセットを読み込みます。

.. code-block:: csharp

   var guids = AssetDatabase.FindAssets("t:ItemData");
   foreach (var guid in guids)
   {
       var path = AssetDatabase.GUIDToAssetPath(guid);
       var item = AssetDatabase.LoadAssetAtPath<ItemData>(path);
   }

検索条件には、次のような書き方ができます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 検索条件
     - 意味
   * - ``t:ItemData``
     - 型が ``ItemData`` のアセット
   * - ``Potion``
     - 名前に「Potion」を含むアセット
   * - ``Potion t:ItemData``
     - 名前に「Potion」を含み、型が ``ItemData`` のアセット
   * - ``l:Weapon``
     - ラベル「Weapon」が付いたアセット

第 2 引数にフォルダーのパスの配列を渡すと、検索範囲をそのフォルダーの中に限定できます。

アセットを変更して保存する
------------------------------------------------------------------------

アセットの値を変更する方法は、第 5 章で説明したシーン上のオブジェクトの場合と同じです。サンプルコードでは、``SerializedObject`` を使って価格を 2 倍にしています。

変更したアセットは、メモリー上では変更済みになりますが、ファイルにはすぐには書き込まれません。プロジェクトを保存したとき（:menuselection:`File --> Save Project` を選択したときなど）に書き込まれます。すぐに書き込みたい場合は、``AssetDatabase.SaveAssetIfDirty``\ （指定したアセットだけ）または ``AssetDatabase.SaveAssets``\ （変更済みのすべてのアセット）を呼びます。

.. warning::

   アセットのファイルを移動・削除・名前変更するときは、``System.IO`` のクラスではなく、``AssetDatabase.MoveAsset``、``AssetDatabase.DeleteAsset``、``AssetDatabase.RenameAsset`` を使ってください。``System.IO`` で操作すると、.meta ファイルが一緒に処理されず、アセットの参照が切れる原因になります。

AssetPostprocessor
========================================================================

``AssetPostprocessor`` を継承したクラスを作成すると、アセットのインポートの前後に処理を加えられます。例えば、特定のフォルダーに追加された画像のインポート設定を、自動的に変更できます。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/TextureImportProcessor.cs
   :caption: Editor/TextureImportProcessor.cs
   :linenos:

:download:`TextureImportProcessor.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/TextureImportProcessor.cs>`

このサンプルコードは、パスに「/Sprites/」を含むフォルダーに画像を追加したとき、その画像の「Texture Type」を「Sprite (2D and UI)」にします。

``AssetPostprocessor`` では、決まった名前のメソッドを定義すると、対応するタイミングで呼ばれます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 呼ばれるタイミング
   * - ``OnPreprocessTexture``
     - テクスチャーのインポートの直前
   * - ``OnPostprocessTexture``
     - テクスチャーのインポートの直後
   * - ``OnPreprocessModel``
     - 3D モデルのインポートの直前
   * - ``OnPreprocessAudio``
     - オーディオのインポートの直前
   * - ``OnPostprocessAllAssets``
     - 任意のアセットのインポート・削除・移動の後（static メソッドとして定義する）

インポート対象のアセットのパスは ``assetPath`` プロパティで、インポートの設定を持つ ``AssetImporter`` は ``assetImporter`` プロパティで取得できます。テクスチャーの場合、``assetImporter`` は ``TextureImporter`` 型なので、キャストして設定を変更します。

インポートの処理は、画像を追加したときだけでなく、再インポートしたときや、インポートの設定を変更したときにも実行されます。何も考えずに設定を変更すると、ユーザーが Inspector ウィンドウで変更した設定が、次のインポートで元に戻ってしまいます。サンプルコードでは、``assetImporter.importSettingsMissing`` で .meta ファイルが無い（初めてインポートされる）ことを確認し、このときだけ設定を変更しています。

.. note::

   ``AssetPostprocessor`` のコードを変更しても、既にインポート済みのアセットには反映されません。反映するには、対象のアセットを右クリックして :menuselection:`Reimport` を選択します。``GetVersion`` メソッドをオーバーライドしてバージョン番号を返すようにしておくと、番号を変えたときに、対象のアセットが自動で再インポートされます。

参考資料
========================================================================

* :unity-api:`ScriptableObject`
* :unity-api:`CreateAssetMenuAttribute`
* :unity-api:`AssetDatabase`
* :unity-api:`AssetDatabase.FindAssets`
* :unity-api:`AssetPostprocessor`
* :unity-api:`AssetImporter-importSettingsMissing`
