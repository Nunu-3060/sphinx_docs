便利な機能
==========

この章では、日常の開発で知っておくと便利な機能を紹介します。

作業の一時退避
--------------

作業の途中で別のブランチに切り替えて緊急の修正をしたいが、まだコミットできる状態ではない、という場合があります。このようなときは ``git stash`` で、コミットしていない変更を一時的に退避できます。

.. code-block:: console

   $ git stash push -m "WIP: login form"
   $ git status
   On branch feature/login
   nothing to commit, working tree clean

退避した変更は、次のコマンドで確認・復元・削除します。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 説明
   * - ``git stash list``
     - 退避した変更の一覧を表示します。
   * - ``git stash pop``
     - 最後に退避した変更をワーキングツリーに戻し、一覧から削除します。
   * - ``git stash apply``
     - 最後に退避した変更をワーキングツリーに戻します。一覧からは削除しません。
   * - ``git stash drop``
     - 最後に退避した変更を、ワーキングツリーに戻さずに一覧から削除します。

退避した変更は ``stash@{0}``\ （最新）、``stash@{1}`` のように番号で区別されます。``git stash pop stash@{1}`` のように番号を指定すると、最新以外の変更も戻せます。PowerShell では、``'stash@{1}'`` のように引用符で囲んでください。

標準では、未追跡のファイルは退避されません。未追跡のファイルも退避したい場合は、``-u`` オプションを付けます。

タグ
----

タグは、特定のコミットに付ける名前です。ブランチと異なり、タグは新しいコミットを作成しても移動しません。主に、リリースしたバージョンを記録するために使います。

.. code-block:: console

   $ git tag -a v1.0.0 -m "Release version 1.0.0"
   $ git tag
   v1.0.0

``-a`` オプションを付けると、作成者や日時、メッセージを含む注釈付きタグが作成されます。``-a`` を付けずに ``git tag v1.0.0`` とすると、名前だけの軽量タグが作成されます。リリースの記録には注釈付きタグを使いましょう。

タグは ``git push`` だけではリモートリポジトリに送信されません。タグを送信するには、次のように明示的に指定します。

.. code-block:: console

   $ git push origin v1.0.0

エイリアス
----------

よく使うコマンドには、短い別名（エイリアス）を付けられます。

.. code-block:: console

   $ git config --global alias.st "status --short --branch"
   $ git config --global alias.lg "log --oneline --graph --all"

上の設定をすると、``git st`` で ``git status --short --branch`` を、``git lg`` で ``git log --oneline --graph --all`` を実行できます。

変更した人の確認
----------------

``git blame`` は、ファイルの各行を最後に変更したコミットと作成者を表示します。ある行がいつ、なぜ変更されたのかを調べるときに使います。

.. code-block:: console

   $ git blame hello.py
   ^b71dd7d (Taro Yamada 2026-09-27 09:50:00 +0900 1) def greet(name):
   b1df4590 (Taro Yamada 2026-09-27 10:00:00 +0900 2)     return f"Hi, {name}!"

コミット ID の前の ``^`` は、そのコミットが履歴の起点となる最初のコミットであることを表します。表示されたコミット ID を ``git show`` に指定すると、そのコミットでの変更内容とコミットメッセージを確認できます。

履歴の検索
----------

``git log`` のオプションを使うと、条件に合うコミットだけを表示できます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 説明
   * - ``git log --author="Taro"``
     - 作成者の名前に ``Taro`` を含むコミットを表示します。
   * - ``git log --grep="login"``
     - コミットメッセージに ``login`` を含むコミットを表示します。
   * - ``git log -S "greet"``
     - ``greet`` という文字列が追加または削除されたコミットを表示します。
   * - ``git log --since="2 weeks ago"``
     - 2 週間前以降のコミットを表示します。

別のブランチのコミットの取り込み
--------------------------------

``git cherry-pick`` は、別のブランチにある特定のコミットの変更だけを、現在のブランチに取り込みます。たとえば、開発中のブランチで行ったバグの修正だけを、先に ``main`` ブランチに反映したい場合に使います。

.. code-block:: console

   $ git switch main
   $ git cherry-pick 3f5a1c9

取り込まれたコミットは、元のコミットと同じ変更内容を持つ、別のコミット ID の新しいコミットになります。

バグの原因となったコミットの特定
--------------------------------

``git bisect`` は、二分探索でバグの原因となったコミットを特定します。正常に動作していたコミットと、バグがあるコミットを指定すると、Git がその間のコミットを順に取り出すので、それぞれで動作を確認して結果を入力していきます。

.. code-block:: console

   $ git bisect start
   $ git bisect bad              # 現在のコミットにはバグがある
   $ git bisect good v1.0.0      # v1.0.0 は正常に動作していた
   （取り出されたコミットで動作を確認し、結果に応じて次のどちらかを実行する）
   $ git bisect good
   $ git bisect bad
   （原因となったコミットが特定されたら終了する）
   $ git bisect reset

二分探索なので、候補となるコミットが :math:`N` 個あっても、およそ :math:`\log_2 N` 回の確認で原因を特定できます。たとえば 1000 個のコミットがあっても、確認は 10 回程度で済みます。
