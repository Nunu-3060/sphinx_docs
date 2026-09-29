########################################################################
エディター拡張の基本
########################################################################

この章では、エディター拡張のスクリプトをどこに置き、どのようにゲーム本体と分けるかを説明します。ここを誤ると、エディター上では動くのにゲームのビルドだけが失敗する、という問題が起きます。

UnityEngine と UnityEditor
========================================================================

Unity の API は、大きく 2 つの名前空間に分かれています。

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - 名前空間
     - 内容
     - ビルドしたゲームでの利用
   * - ``UnityEngine``
     - ``MonoBehaviour``、``GameObject``、``Transform`` など、ゲームの実行に必要な機能
     - 利用できる
   * - ``UnityEditor``
     - ``MenuItem``、``Editor``、``EditorWindow``、``AssetDatabase`` など、エディターの機能
     - 利用できない

``UnityEditor`` 名前空間の機能は Unity エディターの中にしか存在せず、ビルドしたゲームには含まれません。そのため、``UnityEditor`` を使うスクリプトがゲーム本体と同じアセンブリに含まれていると、ビルド時に次のようなコンパイルエラーになります。

.. code-block:: text

   error CS0246: The type or namespace name 'UnityEditor' could not be found

スクリプトを分ける方法
========================================================================

エディター拡張のスクリプトは、エディター専用のアセンブリに分ける必要があります。分ける方法は次の 3 つです。

Editor フォルダーに置く
------------------------------------------------------------------------

``Assets`` フォルダーの下にある「Editor」という名前のフォルダーは、特別なフォルダーとして扱われます。Editor フォルダーに置いたスクリプトは ``Assembly-CSharp-Editor`` というエディター専用のアセンブリにコンパイルされ、ビルドには含まれません。

Editor フォルダーは ``Assets/Editor`` だけでなく、``Assets/MyTool/Editor`` のように、どの階層にいくつ作ってもかまいません。

最も手軽な方法ですが、後述するアセンブリ定義ファイルを使っているフォルダーの下では、Editor フォルダーの特別な扱いは無効になる点に注意してください。

アセンブリ定義ファイルを使う
------------------------------------------------------------------------

アセンブリ定義ファイル（拡張子 .asmdef）を置くと、そのフォルダー以下のスクリプトを独立したアセンブリとしてコンパイルできます。アセンブリを分けると、変更したアセンブリとそれに依存するアセンブリだけが再コンパイルされるため、プロジェクトが大きくなってもコンパイル時間を短く保てます。

アセンブリ定義ファイルは、Project ウィンドウで右クリックし、:menuselection:`Create --> Scripting --> Assembly Definition` を選択して作成します。作成したファイルを選択すると、Inspector ウィンドウで設定を変更できます。

エディター専用のアセンブリにするには、「Platforms」の一覧で「Editor」だけにチェックを入れます。本書のサンプルコードでは、ゲーム本体側とエディター拡張側で、それぞれ次のアセンブリ定義ファイルを使っています。

.. literalinclude:: ../../examples/Assets/EditorIntro/Runtime/EditorIntro.Runtime.asmdef
   :language: json
   :caption: Runtime/EditorIntro.Runtime.asmdef

:download:`EditorIntro.Runtime.asmdef をダウンロード <../../examples/Assets/EditorIntro/Runtime/EditorIntro.Runtime.asmdef>`

.. literalinclude:: ../../examples/Assets/EditorIntro/Editor/EditorIntro.Editor.asmdef
   :language: json
   :caption: Editor/EditorIntro.Editor.asmdef

:download:`EditorIntro.Editor.asmdef をダウンロード <../../examples/Assets/EditorIntro/Editor/EditorIntro.Editor.asmdef>`

エディター拡張側の設定のうち、重要な項目は次の 2 つです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 意味
   * - ``includePlatforms``
     - ``Editor`` だけを指定しているため、このアセンブリはエディターでだけ使われ、ビルドには含まれません。
   * - ``references``
     - ゲーム本体側のアセンブリ ``EditorIntro.Runtime`` を参照しています。これにより、エディター拡張から ``Enemy`` などのクラスを使えます。

参照の向きは「エディター拡張側 → ゲーム本体側」の一方向にします。ゲーム本体側からエディター拡張側を参照すると、ビルドしたゲームに存在しないアセンブリを参照することになるためです。

条件付きコンパイルを使う
------------------------------------------------------------------------

ゲーム本体側のスクリプトの中で、一部だけエディターの機能を使いたい場合は、``#if UNITY_EDITOR`` で囲みます。``UNITY_EDITOR`` はエディターでコンパイルするときだけ定義されるシンボルなので、囲んだ部分はビルド時にコンパイルされません。

.. code-block:: csharp

   using UnityEngine;
   #if UNITY_EDITOR
   using UnityEditor;
   #endif

   public class Spawner : MonoBehaviour
   {
       // 選択中のとき、Scene ビューにゲームオブジェクトの名前を表示します。
       private void OnDrawGizmosSelected()
       {
   #if UNITY_EDITOR
           // Handles は UnityEditor 名前空間のクラスなので、#if UNITY_EDITOR で囲みます。
           Handles.Label(transform.position, name);
   #endif
       }
   }

この方法は手軽ですが、多用するとゲーム本体のコードとエディター用のコードが混ざって読みにくくなります。まとまった量のエディター拡張は、Editor フォルダーまたはアセンブリ定義ファイルで分けるようにしてください。

3 つの方法の比較
------------------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 方法
     - 向いている場面
     - 注意点
   * - Editor フォルダー
     - 小規模なプロジェクト、手軽に試したいとき
     - アセンブリ定義ファイルがあるフォルダーの下では使えない
   * - アセンブリ定義ファイル
     - 中規模以上のプロジェクト、配布するツール
     - ゲーム本体側とエディター拡張側の両方にファイルが必要
   * - ``#if UNITY_EDITOR``
     - ゲーム本体のスクリプトに少しだけエディター用の処理を加えるとき
     - 多用するとコードが読みにくくなる

スクリプトの再読み込み
========================================================================

スクリプトを変更して Unity エディターに戻ると、スクリプトが再コンパイルされ、続いて「ドメインリロード」が行われます。ドメインリロードでは、読み込まれているスクリプトがすべて破棄されて読み込み直されるため、static フィールドの値は初期値に戻ります。

エディター拡張で状態を保持したい場合は、static フィールドに頼らず、第 11 章で説明する方法で保存してください。

エディターの起動時やドメインリロードの直後に処理を実行したい場合は、クラスに ``InitializeOnLoad`` 属性を付け、static コンストラクターに処理を書きます。

.. code-block:: csharp

   using UnityEditor;
   using UnityEngine;

   [InitializeOnLoad]
   public static class StartupLogger
   {
       // エディターの起動時と、ドメインリロードの直後に呼ばれます。
       static StartupLogger()
       {
           Debug.Log("スクリプトが読み込まれました。");
       }
   }

参考資料
========================================================================

* `特殊なフォルダー名 <https://docs.unity3d.com/ja/6000.0/Manual/SpecialFolders.html>`_\ （Unity マニュアル）
* `Unity のアセンブリの概要 <https://docs.unity3d.com/ja/6000.0/Manual/assembly-definitions-intro.html>`_\ （Unity マニュアル）
* `Unity での条件付きコンパイル <https://docs.unity3d.com/ja/6000.0/Manual/platform-dependent-compilation.html>`_\ （Unity マニュアル）
* :unity-api:`InitializeOnLoadAttribute`
