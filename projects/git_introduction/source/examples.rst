サンプルファイル一覧
====================

本資料で使用しているサンプルファイルの一覧です。ファイル名のリンクからダウンロードできます。サンプルスクリプトは、拡張子が ``.sh`` の Git Bash 版と、``.ps1`` の PowerShell 版の 2 種類を用意しています。

.. list-table::
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - :download:`basic_workflow.sh <../examples/basic_workflow.sh>`

       :download:`basic_workflow.ps1 <../examples/basic_workflow.ps1>`
     - リポジトリの作成、ステージ、コミット、差分と履歴の確認を順に実行します。
     - :doc:`basic`
   * - :download:`undo_demo.sh <../examples/undo_demo.sh>`

       :download:`undo_demo.ps1 <../examples/undo_demo.ps1>`
     - ``git restore``、``git revert``、``git reset``、``git reflog`` を順に実行します。
     - :doc:`undo`
   * - :download:`branch_merge.sh <../examples/branch_merge.sh>`

       :download:`branch_merge.ps1 <../examples/branch_merge.ps1>`
     - ブランチを作成し、fast-forward マージと 3-way マージを実行します。
     - :doc:`branch`
   * - :download:`conflict_demo.sh <../examples/conflict_demo.sh>`

       :download:`conflict_demo.ps1 <../examples/conflict_demo.ps1>`
     - マージでコンフリクトを発生させ、解消するまでを実行します。
     - :doc:`branch`
   * - :download:`gitconfig.sample <../examples/gitconfig.sample>`
     - ホームディレクトリに置く ``.gitconfig`` の設定例です。
     - :doc:`setup`
   * - :download:`python.gitignore <../examples/python.gitignore>`
     - Python プロジェクト向けの ``.gitignore`` の例です。
     - :doc:`basic`、:doc:`python_project`
   * - :download:`pre-commit-config.yaml <../examples/pre-commit-config.yaml>`
     - pre-commit の設定ファイル ``.pre-commit-config.yaml`` の例です。
     - :doc:`python_project`
   * - :download:`python-test.yml <../examples/python-test.yml>`
     - GitHub Actions で Python のテストを自動で実行するワークフローの例です。
     - :doc:`github`

サンプルスクリプトの実行方法
----------------------------

拡張子が ``.sh`` のサンプルスクリプトは、Windows では Git Bash、macOS や Linux では端末で実行します。

.. code-block:: console

   $ bash basic_workflow.sh

拡張子が ``.ps1`` のサンプルスクリプトは、PowerShell で次のように実行します。``-ExecutionPolicy Bypass`` を付ける理由は、:doc:`powershell` を参照してください。

.. code-block:: ps1con

   PS> powershell -ExecutionPolicy Bypass -File .\basic_workflow.ps1

各スクリプトは、カレントディレクトリに ``practice-`` で始まる練習用のディレクトリを作成し、その中で Git を操作します。既存のリポジトリには影響を与えません。スクリプトの実行後は、作成されたディレクトリに移動して、``git log`` などで結果を確認したり、自由に操作を試したりしてください。同じスクリプトをもう一度実行する場合は、先に練習用のディレクトリを削除してください。

練習用のリポジトリでは、コミットの作成者として ``Taro Yamada`` という仮の名前を設定しています。この設定は練習用のリポジトリの中だけで有効であり、``--global`` の設定は変更しません。

設定ファイルの使い方
--------------------

``gitconfig.sample``、``python.gitignore``、``pre-commit-config.yaml``、``python-test.yml`` は、本来のファイル名や置き場所が決まっている設定ファイルです。このうち最初の 3 つは、本来のファイル名が「``.``」で始まります。先頭が「``.``」のファイルは OS によっては隠しファイルとして扱われ、ダウンロード後に見つけにくくなるため、異なる名前にしています。使うときは、次のようにファイル名を変更してください。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - ダウンロードしたファイル
     - 変更後のファイル名と置き場所
   * - ``gitconfig.sample``
     - ホームディレクトリの ``.gitconfig``\ （内容を既存のファイルに追記しても構いません）
   * - ``python.gitignore``
     - リポジトリの最上位ディレクトリの ``.gitignore``
   * - ``pre-commit-config.yaml``
     - リポジトリの最上位ディレクトリの ``.pre-commit-config.yaml``
   * - ``python-test.yml``
     - リポジトリの ``.github/workflows/`` ディレクトリの ``test.yml`` など（拡張子が ``.yml`` であれば、名前は自由です）
