コマンド早見表
==============

本資料で説明した主なコマンドを、用途ごとにまとめます。

設定
----

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git config --global user.name "<名前>"``
     - コミットに記録する名前を設定します。
   * - ``git config --global user.email "<メールアドレス>"``
     - コミットに記録するメールアドレスを設定します。
   * - ``git config --list --show-origin``
     - 現在の設定と、設定が書かれているファイルを表示します。

リポジトリの作成
----------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git init``
     - カレントディレクトリに新しいリポジトリを作成します。
   * - ``git clone <URL>``
     - リモートリポジトリを複製します。

変更の記録
----------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git status``
     - ワーキングツリーとステージングエリアの状態を表示します。
   * - ``git add <file>``
     - 変更をステージします。
   * - ``git commit -m "<メッセージ>"``
     - ステージした変更をコミットします。
   * - ``git rm <file>``
     - ファイルを削除し、その削除をステージします。
   * - ``git mv <old> <new>``
     - ファイルの名前を変更し、その変更をステージします。

履歴と差分の確認
----------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git log --oneline --graph --all``
     - すべてのブランチの履歴をグラフで表示します。
   * - ``git show <commit>``
     - コミットの詳細を表示します。
   * - ``git diff``
     - まだステージしていない変更を表示します。
   * - ``git diff --staged``
     - ステージした変更を表示します。
   * - ``git blame <file>``
     - 各行を最後に変更したコミットを表示します。

変更の取り消し
--------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git restore <file>``
     - ワーキングツリーの変更を破棄します。
   * - ``git restore --staged <file>``
     - ステージを取り消します。
   * - ``git commit --amend``
     - 直前のコミットを修正します。
   * - ``git revert <commit>``
     - コミットを打ち消す新しいコミットを作成します。
   * - ``git reset <commit>``
     - 現在のブランチを指定したコミットに戻します。
   * - ``git reflog``
     - HEAD の移動履歴を表示します。

ブランチ
--------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git branch``
     - ブランチの一覧を表示します。
   * - ``git switch <branch>``
     - ブランチを切り替えます。
   * - ``git switch -c <branch>``
     - ブランチを作成して切り替えます。
   * - ``git merge <branch>``
     - 指定したブランチを現在のブランチにマージします。
   * - ``git rebase <branch>``
     - 現在のブランチのコミットを、指定したブランチの先端の後ろに付け替えます。
   * - ``git branch -d <branch>``
     - マージ済みのブランチを削除します。

リモートリポジトリ
------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git remote -v``
     - 登録されているリモートリポジトリを表示します。
   * - ``git remote add origin <URL>``
     - リモートリポジトリを ``origin`` という名前で登録します。
   * - ``git fetch``
     - リモートリポジトリの変更を取り込みます。
   * - ``git pull``
     - リモートリポジトリの変更を取り込み、現在のブランチに統合します。
   * - ``git push -u origin <branch>``
     - ブランチをプッシュし、上流ブランチを設定します。
   * - ``git push``
     - 上流ブランチにプッシュします。

その他
------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``git stash push -m "<メッセージ>"``
     - コミットしていない変更を一時的に退避します。
   * - ``git stash pop``
     - 退避した変更を戻します。
   * - ``git tag -a <tag> -m "<メッセージ>"``
     - 注釈付きタグを作成します。
   * - ``git cherry-pick <commit>``
     - 指定したコミットの変更を現在のブランチに取り込みます。
   * - ``git bisect start``
     - 二分探索によるバグの原因の特定を開始します。

GitHub CLI
----------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 説明
   * - ``gh auth login``
     - GitHub にログインします。
   * - ``gh repo clone <owner>/<repo>``
     - GitHub のリポジトリを複製します。
   * - ``gh pr create --fill``
     - 現在のブランチからプルリクエストを作成します。
   * - ``gh pr checkout <number>``
     - プルリクエストのブランチを取得して切り替えます。
