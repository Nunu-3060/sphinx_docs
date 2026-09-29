GitHub との連携
===============

:doc:`remote` と :doc:`workflow` では、Git のコマンドを使ってリモートリポジトリとやり取りする方法と、プルリクエストを使った開発の流れを説明しました。この章では、GitHub が提供する機能を Git と組み合わせて使う方法を説明します。

GitHub でのリポジトリの作成
---------------------------

GitHub にサインインし、画面右上の「+」メニューから「New repository」を選ぶと、リポジトリの作成画面が表示されます。主な設定項目は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 説明
   * - Repository name
     - リポジトリの名前です。URL の一部になります。
   * - Public / Private
     - Public はだれでも閲覧でき、Private は招待した人だけが閲覧できます。
   * - Add a README file
     - リポジトリの説明を書く ``README.md`` を作成します。
   * - Add .gitignore
     - 言語に合わせた ``.gitignore`` を作成します。Python のプロジェクトでは「Python」を選びます。
   * - Choose a license
     - ライセンスファイル（``LICENSE``）を作成します。公開するリポジトリでは、利用条件を明確にするために設定しておきましょう。

手元に既にあるローカルリポジトリを GitHub に登録する場合は、README、``.gitignore``、ライセンスのいずれも作成せず、空のリポジトリを作成してください。これらを作成すると、リモートリポジトリにローカルリポジトリとは無関係なコミットができるため、最初のプッシュが拒否されます。

空のリポジトリを作成すると、ローカルリポジトリを登録するためのコマンドが画面に表示されます。内容は :doc:`remote` で説明した ``git remote add`` と ``git push -u`` です。

.. code-block:: console

   $ git remote add origin https://github.com/taro/hello-git.git
   $ git push -u origin main

GitHub CLI
----------

GitHub CLI（``gh`` コマンド）を使うと、リポジトリやプルリクエストの作成など、通常はブラウザーで行う GitHub の操作をターミナルから実行できます。

インストールと認証
^^^^^^^^^^^^^^^^^^

使用している OS に応じて、次の方法でインストールします。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - OS
     - インストール方法
   * - Windows
     - ``winget install --id GitHub.cli`` を実行します。
   * - macOS
     - Homebrew を使って ``brew install gh`` を実行します。
   * - Linux
     - `GitHub CLI の公式サイト <https://cli.github.com/>`_ の手順に従って、ディストリビューションのパッケージマネージャーでインストールします。

インストールが終わったら、``gh auth login`` を実行して GitHub にログインします。質問に答えていくとブラウザーが開き、認証が完了します。接続方法に HTTPS を選び、Git の認証にも GitHub の認証情報を使うかどうかの質問に「Yes」と答えると、``git push`` などでも同じ認証情報が使われるようになります。

.. code-block:: console

   $ gh auth login
   $ gh auth status

主なコマンド
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``gh repo create hello-git --private --source=. --remote=origin --push``
     - カレントディレクトリのローカルリポジトリをもとに、GitHub に非公開のリポジトリを作成し、``origin`` として登録してプッシュします。
   * - ``gh repo clone taro/hello-git``
     - GitHub のリポジトリを複製します。
   * - ``gh pr create --fill``
     - 現在のブランチからプルリクエストを作成します。``--fill`` を付けると、コミットメッセージからタイトルと説明が自動で入力されます。
   * - ``gh pr list``
     - プルリクエストの一覧を表示します。
   * - ``gh pr checkout 12``
     - 12 番のプルリクエストのブランチを取得して、そのブランチに切り替えます。レビューの際に、手元で動作を確認するときに使います。
   * - ``gh pr merge 12 --squash --delete-branch``
     - 12 番のプルリクエストを「Squash and merge」でマージし、作業用のブランチを削除します。
   * - ``gh issue create``
     - イシューを作成します。
   * - ``gh issue list``
     - イシューの一覧を表示します。
   * - ``gh browse``
     - 現在のリポジトリの GitHub のページをブラウザーで開きます。

``gh`` コマンドは、Git Bash でも PowerShell でも同じように入力できます。

イシューとプルリクエストの連携
------------------------------

イシューは、バグの報告や機能の要望、作業の予定などを記録する、GitHub の課題管理の機能です。各イシューには ``#12`` のような番号が付けられます。

コミットメッセージやプルリクエストの説明に ``#12`` と書くと、そのイシューへのリンクになり、イシューの画面にも関連するコミットやプルリクエストが表示されます。

さらに、プルリクエストの説明に次のようなキーワードとイシューの番号を書いておくと、プルリクエストが既定のブランチ（通常は ``main``）にマージされたときに、そのイシューが自動的にクローズされます。

.. code-block:: text

   Add login form

   Closes #12

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - キーワード
     - 使用例
   * - close、closes、closed
     - ``Closes #12``
   * - fix、fixes、fixed
     - ``Fixes #12``
   * - resolve、resolves、resolved
     - ``Resolves #12``

コミットメッセージに書いた場合も、そのコミットが既定のブランチに取り込まれるとイシューがクローズされます。

フォークによる貢献
------------------

書き込み権限のない他の人のリポジトリ（オープンソースのプロジェクトなど）に変更を提案するには、フォークを使います。フォークとは、他の人のリポジトリを自分の GitHub アカウントに複製したものです。フォークには自由にプッシュできるため、フォークで作業し、元のリポジトリにプルリクエストを送ります。

作業の流れは次のとおりです。

1. 元のリポジトリの GitHub のページで「Fork」ボタンを押し、自分のアカウントにフォークを作成します。
2. フォークを手元に複製し、元のリポジトリを ``upstream`` という名前で登録します。

   .. code-block:: console

      $ git clone https://github.com/taro/awesome-project.git
      $ cd awesome-project
      $ git remote add upstream https://github.com/original-owner/awesome-project.git

3. 作業用のブランチを作成してコミットし、フォーク（``origin``）にプッシュします。

   .. code-block:: console

      $ git switch -c fix/typo
      $ git commit -am "Fix typo in README"
      $ git push -u origin fix/typo

4. GitHub でフォークのページを開き、元のリポジトリに対してプルリクエストを作成します。

作業している間に元のリポジトリが更新された場合は、次のようにして、その変更をフォークに取り込みます。GitHub のフォークのページにある「Sync fork」ボタンでも、同じことができます。

.. code-block:: console

   $ git fetch upstream
   $ git switch main
   $ git merge upstream/main
   $ git push origin main

GitHub Actions による自動テスト
-------------------------------

GitHub Actions は、プッシュやプルリクエストの作成などをきっかけに、テストやビルドなどの処理を GitHub のサーバー上で自動的に実行する機能です。コードの変更のたびにテストを自動で実行する仕組みは、CI（継続的インテグレーション）と呼ばれます。

GitHub Actions で実行する処理は、リポジトリの ``.github/workflows/`` ディレクトリに置いた YAML 形式のファイル（ワークフロー）に記述します。次の例は、``main`` ブランチへのプッシュと、プルリクエストの作成・更新のたびに、Python の 2 つのバージョンで ``pytest`` を実行するワークフローです。

.. literalinclude:: ../examples/python-test.yml
   :language: yaml
   :caption: .github/workflows/test.yml の例

:download:`python-test.yml をダウンロード <../examples/python-test.yml>`

ワークフローのファイルをコミットして GitHub にプッシュすると、リポジトリの「Actions」タブで実行結果を確認できるようになります。プルリクエストの画面にもテストの結果が表示されるため、レビューする人は、テストが成功していることを確認してからマージできます。

ブランチの保護
--------------

``main`` ブランチへの誤ったプッシュや、レビューを経ていない変更のマージを防ぐために、ブランチに保護ルールを設定できます。リポジトリの「Settings」の「Branches」（または「Rules」の「Rulesets」）から、対象のブランチ名と次のようなルールを設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ルール
     - 効果
   * - プルリクエストを必須にする
     - ブランチへの直接のプッシュを禁止し、プルリクエストを経由した変更だけを受け付けます。
   * - 承認を必須にする
     - 指定した人数のレビューで承認されるまで、マージできないようにします。
   * - ステータスチェックの成功を必須にする
     - GitHub Actions のテストなどが成功するまで、マージできないようにします。
   * - 強制プッシュを禁止する
     - :doc:`workflow` で説明した強制プッシュを禁止します。

GitHub の無料プランでは、ブランチの保護ルールを設定できるのは公開リポジトリだけです。非公開のリポジトリで使うには、有料プランが必要です。

GitHub Pages による公開
-----------------------

GitHub Pages は、リポジトリに置いた HTML ファイルなどを、Web サイトとして無料で公開する機能です。Sphinx で作成した文書も、ビルドした HTML を GitHub Pages で公開できます。

GitHub Pages は、標準では Jekyll という静的サイトジェネレーターでファイルを処理します。Jekyll は名前が ``_`` で始まるディレクトリを公開しないため、そのままでは Sphinx が出力する ``_static`` ディレクトリ（CSS や JavaScript が入っている）が公開されず、表示が崩れます。公開するディレクトリの最上位に ``.nojekyll`` という空のファイルを置くと、Jekyll による処理が行われなくなります。Sphinx では、``conf.py`` の ``extensions`` に ``sphinx.ext.githubpages`` を追加すると、ビルド時に ``.nojekyll`` が自動で出力されます。

公開の設定は、リポジトリの「Settings」の「Pages」で行います。公開するブランチとディレクトリを指定する方法と、GitHub Actions でビルドして公開する方法があります。

エディターやツールとの連携
--------------------------

コマンドを使わずに、エディターやアプリケーションから Git と GitHub を操作することもできます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ツール
     - 説明
   * - VS Code
     - 「ソース管理」ビューで、差分の確認、ステージ、コミット、プッシュなどを行えます。拡張機能「GitHub Pull Requests」を追加すると、プルリクエストの作成やレビューも VS Code の中で行えます。
   * - GitHub Desktop
     - GitHub が提供する Git のアプリケーションです。コミットやブランチの操作、プルリクエストの作成を画面上で行えます。

これらのツールも、内部では本資料で説明した Git の操作を行っています。コマンドで仕組みを理解しておくと、ツールで問題が起きたときにも原因を判断しやすくなります。
