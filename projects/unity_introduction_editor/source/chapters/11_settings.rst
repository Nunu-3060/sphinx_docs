########################################################################
設定の保存
########################################################################

エディター拡張では、ツールのオン・オフや、入力欄の初期値などの設定を保存したい場面があります。第 2 章で説明したとおり、static フィールドの値はドメインリロードで失われるため、設定はファイルなどに保存する必要があります。

この章では、設定を保存する 2 つの方法と、設定を編集する画面を Project Settings ウィンドウに追加する方法を説明します。

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 方法
     - 保存先
     - 共有される範囲
   * - ``EditorPrefs``
     - Windows ではレジストリ、macOS では plist ファイル
     - 同じコンピューターのすべてのプロジェクト
   * - ``ScriptableSingleton``
     - 指定したファイル
     - 保存先による（後述）

EditorPrefs
========================================================================

``EditorPrefs`` は、キーと値の組を保存するクラスです。bool 型、int 型、float 型、string 型の値を保存できます。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/EditorPrefsExample.cs
   :caption: Editor/EditorPrefsExample.cs
   :linenos:

:download:`EditorPrefsExample.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/EditorPrefsExample.cs>`

:menuselection:`Tools --> Editor Intro --> Verbose Log` を選択するたびに設定が切り替わり、メニュー項目にチェックマークが付いたり外れたりします。Unity エディターを再起動しても、設定は保持されます。

値の保存には ``SetBool`` などの Set で始まるメソッドを、読み込みには ``GetBool`` などの Get で始まるメソッドを使います。Get で始まるメソッドの第 2 引数には、キーが保存されていないときに返す既定値を指定します。

``EditorPrefs`` の値は、同じコンピューターで開くすべてのプロジェクトで共有されます。ほかのツールと同じキーを使うと値を上書きし合ってしまうため、サンプルコードの ``"EditorIntro.VerboseLog"`` のように、ツール名などを先頭に付けたキーにしてください。

メニュー項目のチェックマークは、``Menu.SetChecked`` で設定します。検証関数はメニューを開くたびに呼ばれるため、サンプルコードでは検証関数の中でチェックマークの状態を更新しています。

``EditorPrefs`` は手軽ですが、プロジェクトごとに異なる設定や、チームで共有したい設定には向きません。そのような設定には、次の ``ScriptableSingleton`` を使います。

ScriptableSingleton
========================================================================

``ScriptableSingleton<T>`` は、インスタンスが 1 つだけ存在する ``ScriptableObject`` を作成するためのクラスです。``FilePath`` 属性で指定したファイルに、シリアライズされたフィールドの値を保存できます。

第 12 章で作成する一括リネームツールの初期値を保存する設定クラスが、次のコードです。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/BatchRenameSettings.cs
   :caption: Editor/BatchRenameSettings.cs
   :linenos:

:download:`BatchRenameSettings.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/BatchRenameSettings.cs>`

設定の読み書きは、``instance`` プロパティで取得したインスタンスを通して行います。``instance`` プロパティに初めてアクセスしたときに、保存されたファイルから値が読み込まれます。ファイルが無い場合は、フィールドの初期値が使われます。

値を変更しただけではファイルに保存されません。保存するには ``Save`` メソッドを呼びます。``Save`` メソッドは protected なので、サンプルコードでは public な ``SaveSettings`` メソッドを用意しています。

保存先
------------------------------------------------------------------------

``FilePath`` 属性の第 2 引数で、保存先の基準となるフォルダーを指定します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 基準となるフォルダー
   * - ``FilePathAttribute.Location.ProjectFolder``
     - プロジェクトのルートフォルダー（``Assets`` フォルダーがあるフォルダー）
   * - ``FilePathAttribute.Location.PreferencesFolder``
     - Unity エディターの設定フォルダー（すべてのプロジェクトで共有される）

``ProjectFolder`` を基準にする場合、保存先として一般的なフォルダーは次の 2 つです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フォルダー
     - 用途
   * - ``ProjectSettings``
     - チーム全員で共有する設定。通常はバージョン管理の対象にする
   * - ``UserSettings``
     - 個人ごとの設定。通常はバージョン管理の対象外にする

サンプルコードでは、リネームの初期値をチームで共有する想定で、``ProjectSettings`` フォルダーに保存しています。

SettingsProvider
========================================================================

``SettingsProvider`` を使うと、Project Settings ウィンドウまたは Preferences ウィンドウに、独自の設定ページを追加できます。

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/BatchRenameSettingsProvider.cs
   :caption: Editor/BatchRenameSettingsProvider.cs
   :linenos:

:download:`BatchRenameSettingsProvider.cs をダウンロード <../../examples/Assets/EditorIntro/Editor/BatchRenameSettingsProvider.cs>`

:menuselection:`Edit --> Project Settings` を選択して Project Settings ウィンドウを開くと、左側の一覧に「Editor Intro」が追加され、その下に「Batch Rename」ページが表示されます。

設定ページは、``SettingsProvider`` 属性を付けた static メソッドで ``SettingsProvider`` のインスタンスを返すことで登録します。コンストラクターの引数と、主なプロパティは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 引数・プロパティ
     - 意味
   * - 第 1 引数（パス）
     - ページの場所。``SettingsScope.Project`` の場合は「Project/」、``SettingsScope.User`` の場合は「Preferences/」で始める
   * - 第 2 引数（``SettingsScope``）
     - ``Project`` なら Project Settings ウィンドウ、``User`` なら Preferences ウィンドウに表示する
   * - ``label``
     - 左側の一覧に表示する名前
   * - ``activateHandler``
     - ページが表示されるときに呼ばれる処理。第 2 引数の要素に UI を追加する
   * - ``keywords``
     - 設定ウィンドウの検索欄で、このページを候補として表示するためのキーワード

サンプルコードでは、各入力欄の ``RegisterValueChangedCallback`` で値の変更を受け取り、設定クラスに値を設定してから保存しています。開始番号と桁数は、設定クラスのプロパティで範囲内の値に補正されるため、補正後の値を ``SetValueWithoutNotify`` で入力欄に表示し直しています。``SetValueWithoutNotify`` は、値の変更を通知せずに入力欄の値を変更するメソッドで、コールバックが繰り返し呼ばれるのを防げます。

参考資料
========================================================================

* :unity-api:`EditorPrefs`
* :unity-api:`Menu.SetChecked`
* :unity-api:`ScriptableSingleton_1`
* :unity-api:`FilePathAttribute`
* :unity-api:`SettingsProvider`
