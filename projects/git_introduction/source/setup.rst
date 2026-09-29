インストールと初期設定
======================

インストール
------------

使用している OS に応じて、次の方法で Git をインストールします。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - OS
     - インストール方法
   * - Windows
     - `Git for Windows <https://gitforwindows.org/>`_ のインストーラーを実行します。Git 本体に加えて、本資料で使用する Git Bash もインストールされます。
   * - macOS
     - ターミナルで ``xcode-select --install`` を実行して Xcode Command Line Tools をインストールします。Homebrew を使っている場合は ``brew install git`` でもインストールできます。
   * - Linux
     - ディストリビューションのパッケージマネージャーでインストールします。たとえば Ubuntu では ``sudo apt install git``、Fedora では ``sudo dnf install git`` を実行します。

インストールが終わったら、次のコマンドでバージョンを確認します。バージョン番号が表示されれば、インストールは完了しています。

.. code-block:: console

   $ git --version
   git version 2.40.0.windows.1

ユーザー情報の設定
------------------

Git はコミットのたびに、作成者の名前とメールアドレスを記録します。最初に次のコマンドでユーザー情報を設定します。名前とメールアドレスは自分のものに置き換えてください。

.. code-block:: console

   $ git config --global user.name "Taro Yamada"
   $ git config --global user.email "taro@example.com"

ここで設定したメールアドレスは、コミットの履歴として公開されます。GitHub で公開するリポジトリに個人のメールアドレスを載せたくない場合は、GitHub が提供する ``noreply`` のメールアドレスを使ってください。

その他の推奨設定
----------------

ユーザー情報のほかに、次の設定をしておくと便利です。

.. code-block:: console

   $ git config --global init.defaultBranch main
   $ git config --global core.editor "code --wait"
   $ git config --global core.quotepath false

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 説明
   * - ``init.defaultBranch``
     - ``git init`` で作成される最初のブランチの名前です。GitHub の既定に合わせて ``main`` にしておきます。
   * - ``core.editor``
     - コミットメッセージの入力などで起動するエディターです。上の例は VS Code を使う場合の設定です。設定しない場合は Vim などが起動します。
   * - ``core.quotepath``
     - ``false`` にすると、``git status`` などで日本語のファイル名がエスケープされずにそのまま表示されます。

改行コードの設定
----------------

Windows と macOS や Linux では、テキストファイルの改行コードが異なります（Windows は CRLF、macOS や Linux は LF）。異なる OS の開発者が同じリポジトリを使うと、改行コードの違いだけで差分が発生することがあります。

Git for Windows の標準のインストール設定では ``core.autocrlf`` が ``true`` になり、リポジトリには LF で保存し、ワーキングツリーには CRLF で取り出すように自動で変換されます。このとき、次のような警告が表示されることがありますが、変換が行われることを知らせているだけなので問題はありません。

.. code-block:: text

   warning: in the working copy of 'hello.py', LF will be replaced by CRLF the next time Git touches it

チームで改行コードを統一したい場合は、リポジトリに ``.gitattributes`` ファイルを置いて改行コードを指定する方法もあります。

設定の確認と設定の範囲
----------------------

現在の設定は次のコマンドで確認できます。``--show-origin`` を付けると、各設定がどのファイルに書かれているかも表示されます。

.. code-block:: console

   $ git config --list --show-origin

Git の設定には 3 つの範囲があり、同じ項目が複数の範囲で設定されている場合は、より狭い範囲の設定が優先されます。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - オプション
     - 適用範囲
     - 保存先
   * - ``--system``
     - コンピューターのすべてのユーザー
     - システム全体の設定ファイル（Linux では ``/etc/gitconfig``、Git for Windows ではインストール先の ``etc\gitconfig``）
   * - ``--global``
     - ログインしているユーザー
     - ホームディレクトリの ``.gitconfig``
   * - ``--local``
     - 特定のリポジトリ
     - リポジトリ内の ``.git/config``

``git config`` でオプションを省略した場合は ``--local`` として扱われます。仕事用のリポジトリだけメールアドレスを変えたい場合は、そのリポジトリの中で ``--global`` を付けずに ``git config user.email`` を実行します。

設定ファイルの例は :download:`gitconfig.sample <../examples/gitconfig.sample>` からダウンロードできます。

ヘルプの表示
------------

各コマンドの詳しい説明は、次のコマンドで表示できます。

.. code-block:: console

   $ git help commit
   $ git commit -h

``git help`` は詳しいマニュアルを表示し、``-h`` オプションは主なオプションの一覧を簡潔に表示します。
