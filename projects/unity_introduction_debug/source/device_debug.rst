.. _device-debug:

実機でのデバッグ
================

エディターでは正常に動作するのに、実機（スマートフォンやゲーム機など、実際にゲームを動かす端末）では不具合が発生することがあります。本章では、ビルドしたアプリケーションをデバッグする方法を紹介します。

Development Build と Script Debugging
-------------------------------------

実機でデバッグを行うには、ビルドの設定で Development Build を有効にします。ビルドの設定は、メニューの :menuselection:`File --> Build Profiles` で開く Build Profiles ウィンドウで行います。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 説明
   * - Development Build
     - 開発用のビルドを作成します。Profiler の接続やスクリプトのデバッグが可能になり、画面の右下に「Development Build」と表示されます。
   * - Autoconnect Profiler
     - アプリケーションの起動時に、エディターの Profiler へ自動的に接続します。
   * - Deep Profiling Support
     - ビルドしたアプリケーションで Deep Profile（:ref:`cpu-usage-module`）を使えるようにします。
   * - Script Debugging
     - ビルドしたアプリケーションに IDE のデバッガーを接続できるようにします。
   * - Wait For Managed Debugger
     - Script Debugging が有効な場合に、起動時にデバッガーの接続を待ちます。起動直後の処理をデバッグしたい場合に使います。

Development Build では ``DEVELOPMENT_BUILD`` シンボルが定義されるため、``#if DEVELOPMENT_BUILD`` を使って開発用のビルドでだけ動作するコードを書けます。

.. note::

   Development Build は、リリースビルドに比べて動作が遅くなることがあります。製品としての最終的な性能は、リリースビルドで確認してください。

.. _log-files:

ログファイルの場所
------------------

エディターとビルドしたアプリケーションは、ログをファイルに書き込みます。エラーが発生したのに画面では確認できない場合は、ログファイルを確認します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ログファイル
     - 場所
   * - エディター（Windows）
     - ``%LOCALAPPDATA%\Unity\Editor\Editor.log``
   * - エディター（macOS）
     - ``~/Library/Logs/Unity/Editor.log``
   * - アプリケーション（Windows）
     - ``%USERPROFILE%\AppData\LocalLow\<CompanyName>\<ProductName>\Player.log``
   * - アプリケーション（macOS）
     - ``~/Library/Logs/<CompanyName>/<ProductName>/Player.log``

``<CompanyName>`` と ``<ProductName>`` は、:menuselection:`Edit --> Project Settings --> Player` で設定した会社名と製品名です。エディターのログファイルは、Console ウィンドウの ⋮ メニューにある :guilabel:`Open Editor Log` からも開けます。

Android と iOS でのログの確認
-----------------------------

スマートフォンのアプリケーションが出力するログは、パソコンと接続して確認します。

Android
^^^^^^^

Android 端末を USB で接続し、Android SDK に含まれる adb コマンドで確認します。次のコマンドは、Unity が出力したログだけを表示します。

.. code-block:: text

   adb logcat -s Unity

Unity の Android Logcat パッケージを導入すると、エディターの :menuselection:`Window --> Analysis --> Android Logcat` で同様のログを確認できます。

iOS
^^^

Unity で書き出した Xcode プロジェクトを Xcode から実行すると、Xcode のコンソールにログが表示されます。macOS の「コンソール」アプリケーションで、接続した端末のログを確認することもできます。

実機への Profiler とデバッガーの接続
------------------------------------

Profiler の接続
^^^^^^^^^^^^^^^

Development Build で作成したアプリケーションを実機で起動し、Profiler ウィンドウのツールバーにある接続先のメニュー（既定では Play Mode と表示）から、実機を選択します。Autoconnect Profiler を有効にしてビルドした場合は、起動時に自動的に接続されます。実機での計測の注意点は、:ref:`editor-vs-device` で説明します。

デバッガーの接続
^^^^^^^^^^^^^^^^

Script Debugging を有効にしてビルドしたアプリケーションを実機で起動し、IDE から接続します。Visual Studio では、メニューの :menuselection:`デバッグ --> Unity デバッガーのアタッチ` を選び、表示された一覧から実機のアプリケーションを選択します。以降の操作は、エディターをデバッグする場合と同じです（:ref:`ide-debugger`）。

エディターと実機で挙動が異なる主な原因
--------------------------------------

エディターと実機で挙動が異なる場合は、次の原因が考えられます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 原因
     - 内容
   * - 性能の差
     - 開発用のパソコンに比べて、スマートフォンは CPU や GPU の性能が低く、メモリも少ないことが一般的です。エディターでは問題なくても、実機では処理が間に合わないことがあります。
   * - エディター専用のコード
     - ``UnityEditor`` 名前空間の API はビルドに含まれません。これらを使うコードは ``#if UNITY_EDITOR`` で囲む必要があります。
   * - ファイルのパス
     - ``Application.dataPath`` などのパスは、プラットフォームによって指す場所が異なります。セーブデータなどの保存には ``Application.persistentDataPath`` を使います。Android の StreamingAssets フォルダー内のファイルは圧縮ファイル（APK）の中にあるため、``System.IO.File`` では読み込めず、``UnityWebRequest`` を使う必要があります。
   * - コードの削除（ストリッピング）
     - IL2CPP でビルドすると、使われていないと判断されたコードが削除されます。リフレクションでしか参照していない型やメソッドが削除され、実行時にエラーになることがあります。``[Preserve]`` 属性や link.xml ファイルで、削除しないように指定します。
   * - グラフィックス API とシェーダー
     - プラットフォームによってグラフィックス API（Direct3D、Vulkan、Metal など）が異なるため、描画結果が変わることがあります。また、ビルド時に使われていないと判断されたシェーダーのバリアントが削除され、表示がおかしくなることがあります。
   * - 画面の解像度と形状
     - 画面の解像度や縦横比は端末によって異なります。また、ノッチ（画面上部の切り欠き）などがある端末では、``Screen.safeArea`` で UI を表示できる領域を確認する必要があります。
