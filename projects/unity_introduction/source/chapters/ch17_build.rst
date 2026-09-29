第 17 章 ビルドと配布
=====================

作ったゲームを Unity Editor の外で動かすには、対象のプラットフォーム向けにビルドします。この章では、:doc:`ch16_tutorial` で作ったゲームを例に、ビルドの方法を説明します。

Build Profiles ウィンドウ
-------------------------

ビルドの設定は、:menuselection:`File --> Build Profiles` で開く Build Profiles ウィンドウで行います。主な項目は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - :guilabel:`Scene List`
     - ビルドに含めるシーンの一覧です（:doc:`ch15_scenes_and_data` を参照）。
   * - :guilabel:`Platforms`
     - ビルドの対象にできるプラットフォームの一覧です。プラットフォームを選ぶと、右側にそのプラットフォームの設定が表示されます。
   * - :guilabel:`Build Profiles`
     - プラットフォームと設定の組み合わせを、ビルドプロファイルとして保存したものの一覧です。例えば、同じ Windows 向けでも、開発用と配布用で設定を分けて保存できます。

ビルドの対象のプラットフォームを変えるには、一覧からプラットフォームを選び、:guilabel:`Switch Platform` をクリックします。切り替えると、アセットがそのプラットフォーム向けに変換されるため、プロジェクトの規模によっては時間がかかります。一覧に目的のプラットフォームがない場合や、:guilabel:`Install with Unity Hub` と表示される場合は、Unity Hub からモジュールを追加します（:doc:`ch03_setup` を参照）。

Windows 向けのビルド
--------------------

#. Build Profiles ウィンドウの :guilabel:`Scene List` に、ビルドに含めるシーンがすべて登録されていることを確認します。
#. :guilabel:`Platforms` から :guilabel:`Windows` を選びます。現在の対象でない場合は、:guilabel:`Switch Platform` をクリックします。
#. :guilabel:`Build` をクリックし、ビルドの結果を保存するフォルダーを選びます。
#. ビルドが終わると、選んだフォルダーに実行ファイル（``製品名.exe``）などが作成されます。実行ファイルをダブルクリックすると、ゲームが起動します。

:guilabel:`Build And Run` をクリックすると、ビルドが終わった後にすぐにゲームが起動します。

.. important::

   ビルドの結果を保存するフォルダーには、プロジェクトの Assets フォルダーの中を選ばないでください。Unity がビルドの結果をアセットとして読み込もうとして、問題が起きることがあります。プロジェクトのフォルダーの中に ``Builds`` などのフォルダーを作り、そこに保存するのが一般的です。

ゲームを配布するときは、実行ファイルだけでなく、ビルドの結果のフォルダー全体（``製品名_Data`` フォルダーや ``UnityPlayer.dll`` など）を zip ファイルなどにまとめて配布します。ただし、``製品名_BurstDebugInformation_DoNotShip`` フォルダーはデバッグ用の情報なので、配布物に含めないでください。IL2CPP でビルドした場合に作成される ``製品名_BackUpThisFolder_ButDontShipItWithYourGame`` フォルダーも、配布物に含めません。

Development Build
~~~~~~~~~~~~~~~~~

Build Profiles ウィンドウの :guilabel:`Development Build` を有効にしてビルドすると、開発用のビルドになります。開発用のビルドでは、エラーが発生したときに画面にログが表示されるほか、Profiler による性能の計測（:doc:`ch18_debug_and_optimization` を参照）やデバッガーの接続ができるようになります。配布するときは、:guilabel:`Development Build` を無効にしてビルドします。

Web ブラウザー向けのビルド
--------------------------

Web ブラウザー向けにビルドするには、:guilabel:`Platforms` から :guilabel:`Web` を選んでビルドします。ビルドの結果は、``index.html`` と、``Build`` フォルダーなどで構成されます。

Web ブラウザー向けのビルドの結果は、``index.html`` をダブルクリックしてファイルとして開いても動きません。Web サーバーに配置して、Web サーバー経由で開く必要があります。:guilabel:`Build And Run` を使うと、Unity が一時的な Web サーバーを起動して、ブラウザーでゲームを開きます。

Web サーバーに配置するときは、ビルドの圧縮形式（Brotli や gzip）に合わせて、Web サーバーの設定が必要になる場合があります。詳しくは、`Unity マニュアルの Web 向けの配置のページ <https://docs.unity3d.com/Manual/webgl-deploying.html>`_ を参照してください。

Player Settings
---------------

アプリケーションの名前やアイコン、画面の設定などは、**Player Settings** で設定します。Player Settings は、:menuselection:`Edit --> Project Settings` の :guilabel:`Player` か、Build Profiles ウィンドウの :guilabel:`Player Settings` ボタンから開けます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 項目
     - 内容
   * - :guilabel:`Company Name`
     - 会社名です。保存先のフォルダーの名前などに使われます。
   * - :guilabel:`Product Name`
     - 製品名です。ウィンドウのタイトルや、実行ファイルの名前に使われます。
   * - :guilabel:`Version`
     - アプリケーションのバージョンです。
   * - :guilabel:`Default Icon`
     - アプリケーションのアイコンです。
   * - :guilabel:`Resolution and Presentation`
     - 起動時の画面のモード（フルスクリーンかウィンドウか）や、ウィンドウの大きさです。
   * - :guilabel:`Splash Image`
     - 起動時に表示するスプラッシュ画面の設定です。
   * - :guilabel:`Other Settings`
     - スクリプトの実行方式（:guilabel:`Scripting Backend`）など、詳細な設定です。

スクリプトの実行方式
~~~~~~~~~~~~~~~~~~~~

:guilabel:`Other Settings` の :guilabel:`Scripting Backend` では、C# のスクリプトをどのような方式で実行するかを選びます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 方式
     - 特徴
   * - Mono
     - C# のコードを中間言語にコンパイルし、実行時に機械語に変換しながら実行します。ビルドが速いため、開発中の確認に向いています。
   * - IL2CPP
     - C# のコードを C++ のコードに変換してから、機械語にコンパイルします。ビルドには時間がかかりますが、実行速度が速くなる傾向があり、コードの解析もされにくくなります。iOS や家庭用ゲーム機など、IL2CPP だけに対応しているプラットフォームもあります。

IL2CPP でビルドするには、対象のプラットフォームの IL2CPP 用のモジュールと、C++ のコンパイラーが必要です。Windows 向けの場合は、Visual Studio の「C++ によるデスクトップ開発」ワークロードをインストールしておきます。また、多くのプラットフォームでは、ビルド先と同じ OS で Unity Editor を動かす必要があります。
