第 15 章 シーン管理とデータの保存
=================================

この章では、シーンを切り替える方法と、ゲームのデータを保存する方法を説明します。

この章のサンプルコードは、``examples/chapter15`` フォルダーにあります。

シーンの切り替え
----------------

Scene List への登録
~~~~~~~~~~~~~~~~~~~

スクリプトからシーンを読み込むには、そのシーンを **Scene List** に登録しておく必要があります。

#. :menuselection:`File --> Build Profiles` で Build Profiles ウィンドウを開きます。
#. 左側の一覧から :guilabel:`Scene List` を選びます。
#. Project ウィンドウからシーンアセットをドラッグ＆ドロップして追加します。

Scene List の各シーンには、上から順に 0、1、2 と番号（ビルドインデックス）が付きます。ビルドしたアプリケーションを起動すると、番号が 0 のシーンが最初に読み込まれます。

シーンを読み込む
~~~~~~~~~~~~~~~~

シーンの読み込みには、``UnityEngine.SceneManagement`` 名前空間の ``SceneManager`` クラスを使います。

.. literalinclude:: ../../examples/chapter15/SceneLoader.cs
   :caption: SceneLoader.cs
   :linenos:

:download:`SceneLoader.cs をダウンロード <../../examples/chapter15/SceneLoader.cs>`

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 特徴
   * - ``SceneManager.LoadScene``
     - シーンを読み込みます。読み込みが終わるまでゲームの処理が止まるため、大きなシーンでは画面が一瞬止まったように見えます。
   * - ``SceneManager.LoadSceneAsync``
     - シーンを非同期で読み込みます。読み込みの間もゲームが動き続けるため、読み込み中の画面や進み具合を表示できます。

どちらのメソッドも、シーンの名前またはビルドインデックスで読み込むシーンを指定できます。``SceneLoader`` の ``LoadScene`` をボタンの :guilabel:`On Click ()` に設定し、引数の欄にシーンの名前を入力すると、ボタンでシーンを切り替えられます。

新しいシーンを読み込むと、それまでのシーンにあった GameObject はすべて破棄されます。

シーンをまたいだデータの受け渡し
--------------------------------

スコアや選んだキャラクターのように、次のシーンに引き継ぎたいデータがある場合は、次のような方法を使います。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 方法
     - 特徴
   * - static なフィールド
     - クラスの ``static`` なフィールドはシーンを読み込んでも失われません。最も簡単な方法ですが、どこからでも変更できてしまうため、使いすぎに注意してください。
   * - ``DontDestroyOnLoad``
     - ``DontDestroyOnLoad(gameObject)`` を呼んだ GameObject は、シーンを読み込んでも破棄されません。対象は、親を持たない（Hierarchy ウィンドウの最上位にある）GameObject である必要があります。BGM を再生し続ける GameObject などに使います。ただし、この GameObject を配置したシーンを再び読み込むと、GameObject が重複してしまうので、重複を防ぐ処理が必要です。
   * - ScriptableObject
     - :doc:`ch08_scripting_advanced` で説明した ScriptableObject のアセットを、複数のシーンの GameObject から参照します。
   * - ファイルへの保存
     - 後述する方法でデータを保存し、次のシーンで読み込みます。ゲームを終了した後もデータを残せます。

データの保存
------------

ゲームを終了した後もデータを残すには、データをファイルなどに保存します。

PlayerPrefs
~~~~~~~~~~~

**PlayerPrefs** は、キー（名前）と値の組を保存するしくみです。音量やグラフィックスの品質などの、簡単な設定の保存に向いています。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - メソッド
     - 機能
   * - ``SetInt``、``SetFloat``、``SetString``
     - 値を保存します。
   * - ``GetInt``、``GetFloat``、``GetString``
     - 値を読み込みます。第 2 引数には、キーが存在しない場合の値を指定します。
   * - ``HasKey``
     - キーが存在するかどうかを調べます。
   * - ``DeleteKey``、``DeleteAll``
     - 値を削除します。
   * - ``Save``
     - 値をディスクに書き込みます。

PlayerPrefs の値は、アプリケーションを正常に終了したときにも自動的に書き込まれます。ただし、強制終了などに備えて、重要な値を変更したときは ``Save`` を呼んでおくと安全です。

PlayerPrefs は、保存できる型が整数、小数、文字列に限られます。また、Windows ではレジストリに保存されるなど、ユーザーが簡単に中身を見たり書き換えたりできる場所に保存されます。多くのデータや、改ざんされると困るデータの保存には向いていません。

JSON ファイル
~~~~~~~~~~~~~

多くのデータをまとめて保存する場合は、データを JSON 形式の文字列に変換して、ファイルに保存する方法が便利です。Unity には、オブジェクトと JSON を相互に変換する ``JsonUtility`` クラスが用意されています。

まず、保存するデータをクラスとして定義します。

.. literalinclude:: ../../examples/chapter15/SaveData.cs
   :caption: SaveData.cs
   :linenos:

:download:`SaveData.cs をダウンロード <../../examples/chapter15/SaveData.cs>`

次に、データをファイルに保存し、読み込むクラスを作ります。

.. literalinclude:: ../../examples/chapter15/SaveSystem.cs
   :caption: SaveSystem.cs
   :linenos:

:download:`SaveSystem.cs をダウンロード <../../examples/chapter15/SaveSystem.cs>`

保存先には、``Application.persistentDataPath`` で取得できるフォルダーを使います。このフォルダーは、アプリケーションが自由に読み書きできる場所として、OS ごとに用意されています。例えば、Windows では ``C:\Users\ユーザー名\AppData\LocalLow\会社名\製品名`` のようなフォルダーになります。会社名と製品名は、:menuselection:`Edit --> Project Settings` の :guilabel:`Player` で設定した値です。

``SaveSystem`` と PlayerPrefs の使い方の例は次のとおりです。

.. literalinclude:: ../../examples/chapter15/SaveExample.cs
   :caption: SaveExample.cs
   :linenos:

:download:`SaveExample.cs をダウンロード <../../examples/chapter15/SaveExample.cs>`

このスクリプトを GameObject に付けて再生し、Inspector ウィンドウのコンポーネントのメニュー（⋮）から各項目を選ぶと、保存と読み込みを試せます。保存したファイルの場所は Console ウィンドウに表示されます。

.. note::

   ``JsonUtility`` は動作が速い反面、変換できる型に制限があります。``Dictionary`` や、プロパティ、多次元配列は変換できません。これらを扱いたい場合は、``Newtonsoft Json`` パッケージ（``com.unity.nuget.newtonsoft-json``）などのライブラリを使います。
