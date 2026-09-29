################################################################
付録 A コーディング規約
################################################################

コードの書き方の決まりを、コーディング規約と呼びます。書き方が揃っていると、自分が書いたコードも他人が書いたコードも読みやすくなります。本書のサンプルコードは、Microsoft の C# のコーディング規約をもとに、次の規約に従って書いています。

命名規則
================================================================

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - 対象
     - 書き方
     - 例
   * - クラス、構造体、列挙型
     - PascalCase
     - ``PlayerController``、``GameState``
   * - インターフェイス
     - ``I`` で始まる PascalCase
     - ``IDamageable``
   * - メソッド、プロパティ、イベント
     - PascalCase
     - ``TakeDamage``、``MaxHp``、``ScoreChanged``
   * - 列挙型の値、定数
     - PascalCase
     - ``GameState.Playing``、``MaxLevel``
   * - ``public`` なフィールド
     - PascalCase
     - ``PublicValue``
   * - ``private`` なフィールド
     - ``_`` で始まる camelCase
     - ``_moveSpeed``、``_rigidbody``
   * - ローカル変数、引数
     - camelCase
     - ``playerName``、``amount``

.. note::

   Unity の API には、``transform.position`` のように、プロパティ名が camelCase のものがあります。これは Unity の歴史的な事情によるもので、自分のコードでは上の規則に従ってかまいません。

書式
================================================================

* インデントは空白 4 文字にします。
* ``{`` は、クラス、メソッド、``if`` 文などの次の行に単独で書きます。
* ``if`` 文や ``for`` 文の本体が 1 行だけでも、``{`` と ``}`` を省略しません。
* アクセス修飾子は省略しません。Unity のイベント関数にも ``private`` を付けます。
* ``int`` や ``string`` などは、``Int32`` や ``String`` ではなく C# のキーワードで書きます。
* ``using`` ディレクティブは、ファイルの先頭に書き、``System`` で始まるものを先に並べます。
* ファイルの文字コードは UTF-8、改行コードは CRLF にします。

Unity 6 の C# は 9.0 なので、C# 10 以降で追加された書き方（ファイルスコープの名前空間など）は使えません。

.editorconfig
================================================================

.editorconfig は、コーディング規約をコードエディターに伝えるための設定ファイルです。Visual Studio や Visual Studio Code（C# Dev Kit）は、.editorconfig の内容に従ってコードを整形し、規約に違反している箇所を警告します。

本書で使っている .editorconfig は次のとおりです。Unity のプロジェクトのフォルダー（Assets フォルダーと同じ階層）に置くと、プロジェクト内のすべてのスクリプトに適用されます。この .editorconfig は、:doc:`../introduction` のサンプルコード一式の zip ファイルにも含まれています。

.. literalinclude:: ../../.editorconfig
   :language: ini
   :caption: .editorconfig

:download:`.editorconfig をダウンロード <../../.editorconfig>`

サンプルコードの検査
================================================================

本書のサンプルコードは、.NET SDK に含まれる dotnet format コマンドを使って、この .editorconfig の規約に従っていることを検査しています。dotnet format は、.editorconfig の規約に違反している箇所を検出し、自動で修正することもできます。

.. code-block:: text

   dotnet format プロジェクトファイル.csproj --verify-no-changes

``--verify-no-changes`` を付けると、ファイルを修正せずに、違反している箇所だけを表示します。付けずに実行すると、修正できる箇所が自動で修正されます。

Unity のプロジェクトでは、コードエディターの設定（第 1 章）をすると、Unity がプロジェクトのフォルダーに .csproj ファイルを作成します。このファイルを指定して dotnet format を実行すると、スクリプトを検査できます。ただし、Unity のバージョンや環境によっては、dotnet format がプロジェクトを読み込めないことがあります。その場合は、.editorconfig をプロジェクトのフォルダーに置いたうえで、コードエディターに表示される警告を確認してください。
