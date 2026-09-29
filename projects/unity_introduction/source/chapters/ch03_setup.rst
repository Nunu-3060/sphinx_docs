第 3 章 環境構築
================

Unity で開発を始めるには、Unity Hub、Unity Editor、コードエディターの 3 つを準備します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ソフトウェア
     - 役割
   * - Unity Hub
     - Unity Editor のインストールや、プロジェクトの作成と管理を行うアプリケーションです。
   * - Unity Editor
     - ゲームを制作するためのアプリケーションです。バージョンごとに別々にインストールします。
   * - コードエディター
     - C# スクリプトを編集するためのアプリケーションです。

Unity Hub のインストール
------------------------

#. `Unity のダウンロードページ <https://unity.com/download>`_ から Unity Hub のインストーラーをダウンロードします。
#. インストーラーを実行し、画面の指示に従ってインストールします。
#. Unity Hub を起動し、Unity ID でサインインします。Unity ID を持っていない場合は、サインイン画面から作成できます。
#. 初回起動時に、ライセンスの取得を求められます。個人で学習に使う場合は、Unity Personal のライセンスを取得します。

Unity Editor のインストール
---------------------------

#. Unity Hub の左側のメニューから :guilabel:`Installs` を選び、:guilabel:`Install Editor` をクリックします。
#. 表示された一覧から、:guilabel:`LTS` と表示されている Unity 6 系のバージョンを選びます。
#. モジュールの選択画面で、必要なモジュールにチェックを入れて、インストールを開始します。

LTS（Long Term Support）版は、長期間にわたって不具合の修正が提供されるバージョンです。新しい機能を試す目的でなければ、LTS 版を使うことをお勧めします。

モジュールは、特定のプラットフォーム向けのビルドやドキュメントなど、Unity Editor に追加する機能です。後から追加することもできるので、最初は次のものを選んでおけば十分です。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - モジュール
     - 用途
   * - Microsoft Visual Studio Community
     - Windows で Visual Studio をコードエディターとして使う場合に選びます。既にインストールしている場合は不要です。
   * - Windows Build Support (IL2CPP)
     - Windows 版の Unity Editor で、Windows 向けに IL2CPP でビルドする場合に選びます。Visual Studio の「C++ によるデスクトップ開発」ワークロードも必要です（:doc:`ch17_build` を参照）。
   * - Mac Build Support (IL2CPP)
     - macOS 版の Unity Editor で、macOS 向けに IL2CPP でビルドする場合に選びます。
   * - Web Build Support
     - Web ブラウザー向けにビルドする場合に選びます。
   * - Documentation
     - マニュアルとスクリプトリファレンスをローカルに保存し、オフラインでも参照できるようにします。

Unity Editor には、Unity Editor を動かしている OS 向けに Mono でビルドする機能が最初から含まれています。Mono と IL2CPP は、C# のコードをどのように実行するかの方式です。詳しくは :doc:`ch17_build` で説明します。

コードエディターの準備
----------------------

Unity で使える主なコードエディターは次の 3 つです。どれを使っても、本資料の内容を進めるうえで違いはありません。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コードエディター
     - 特徴
   * - Visual Studio
     - Windows 向けの統合開発環境です。Community エディションは個人や小規模な組織であれば無料で使えます。Unity Hub から一緒にインストールできます。
   * - Visual Studio Code
     - Windows、macOS、Linux で動く軽量なエディターです。Unity 拡張機能をインストールして使います。
   * - JetBrains Rider
     - Unity 向けの機能が充実した有料の統合開発環境です。学生や非商用利用向けの無料ライセンスもあります。

Visual Studio Code を使う場合は、次の手順で設定します。

#. Visual Studio Code の拡張機能ビューで、Microsoft が提供している :guilabel:`Unity` 拡張機能をインストールします。C# の開発に必要な拡張機能も一緒にインストールされます。
#. Unity Editor で :menuselection:`Window --> Package Manager` を開き、:guilabel:`Visual Studio Editor` パッケージがインストールされていることを確認します。
#. Unity Editor で :menuselection:`Edit --> Preferences`\ （macOS では :menuselection:`Unity --> Settings`）を開き、:guilabel:`External Tools` の :guilabel:`External Script Editor` で Visual Studio Code を選びます。

Visual Studio や Rider を使う場合も、:guilabel:`External Script Editor` で使用するコードエディターを選びます。正しく設定できていれば、Unity Editor でスクリプトをダブルクリックしたときに、選んだコードエディターでスクリプトが開き、コード補完が働きます。

プロジェクトの作成
------------------

#. Unity Hub の左側のメニューから :guilabel:`Projects` を選び、:guilabel:`New project` をクリックします。
#. 使用する Unity Editor のバージョンを選びます。
#. テンプレートの一覧から :guilabel:`Universal 3D` を選びます。
#. :guilabel:`Project name` にプロジェクト名を、:guilabel:`Location` に保存先のフォルダーを入力します。
#. :guilabel:`Create project` をクリックします。

しばらく待つと、Unity Editor が起動し、作成したプロジェクトが開きます。

テンプレートは、プロジェクトの初期設定の組み合わせです。主なテンプレートには次のものがあります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - テンプレート
     - 用途
   * - Universal 3D
     - URP（Universal Render Pipeline）を使う 3D プロジェクトです。PC からスマートフォンまで幅広いプラットフォームに対応しています。本資料ではこのテンプレートを使います。
   * - Universal 2D
     - URP を使う 2D プロジェクトです。
   * - High Definition 3D
     - HDRP（High Definition Render Pipeline）を使う 3D プロジェクトです。高性能な PC や家庭用ゲーム機向けに、高品質なグラフィックスを実現します。
   * - 3D (Built-In Render Pipeline)
     - 従来のレンダーパイプラインを使う 3D プロジェクトです。古い資料やアセットを使う場合に選びます。

レンダーパイプラインについては :doc:`ch11_graphics` で説明します。

.. note::

   プロジェクトの保存先のパスには、なるべく日本語や空白を含めないでください。一部のツールやパッケージが正しく動作しない場合があります。

プロジェクトのフォルダー構成
----------------------------

作成したプロジェクトのフォルダーには、次のようなフォルダーがあります。

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - フォルダー
     - 内容
     - バージョン管理
   * - Assets
     - スクリプト、3D モデル、テクスチャ、シーンなど、プロジェクトで使うアセットを保存します。
     - 対象にする
   * - Packages
     - プロジェクトで使うパッケージの一覧（``manifest.json``）などを保存します。
     - 対象にする
   * - ProjectSettings
     - プロジェクトの設定を保存します。
     - 対象にする
   * - Library
     - Unity がアセットを読み込むために生成するキャッシュです。削除しても Unity が再生成します。
     - 対象外にする
   * - Temp
     - Unity Editor の実行中に使う一時ファイルです。
     - 対象外にする
   * - Logs
     - ログファイルです。
     - 対象外にする
   * - UserSettings
     - ユーザーごとのエディターの設定です。
     - 対象外にする

Git などでプロジェクトをバージョン管理する場合は、Library、Temp、Logs、UserSettings の各フォルダーを管理の対象から外します。Git の場合は、GitHub が公開している `Unity 用の .gitignore <https://github.com/github/gitignore/blob/main/Unity.gitignore>`_ を利用すると便利です。

Unity は、Assets フォルダー内の各ファイルに対して、同じ名前に ``.meta`` を付けたファイルを作成します。``.meta`` ファイルには、アセットを識別する ID や読み込みの設定が記録されています。``.meta`` ファイルもバージョン管理の対象に含めてください。``.meta`` ファイルが失われると、アセット間の参照が切れてしまいます。また、Assets フォルダー内のファイルを移動したり名前を変えたりするときは、エクスプローラーや Finder ではなく、Unity Editor の Project ウィンドウで操作してください。Project ウィンドウで操作すれば、``.meta`` ファイルも一緒に移動されます。
