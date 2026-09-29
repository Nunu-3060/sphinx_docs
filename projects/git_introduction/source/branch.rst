ブランチ
========

ブランチを使うと、メインの開発の流れに影響を与えずに、新機能の開発やバグの修正を別の流れとして進められます。作業が終わったら、その変更をメインの流れに合流（マージ）させます。

この章の操作を体験するサンプルスクリプトは、:ref:`branch-sample` にあります。

ブランチの仕組み
----------------

:doc:`concepts` で説明したとおり、ブランチは特定のコミットを指す目印です。新しいブランチを作成すると、現在のコミットを指す目印が 1 つ増えるだけで、ファイルがコピーされるわけではありません。

次の図は、``main`` ブランチから ``feature`` ブランチを作成し、``feature`` ブランチで 2 つのコミットを作成した状態を表しています。

.. code-block:: text

                   main
                    |
                    v
   [A] <-- [B] <-- [C]
                    ^
                    |
                    +---- [D] <-- [E]
                                   ^
                                   |
                            feature (HEAD)

ブランチの作成と切り替え
------------------------

ブランチの一覧は ``git branch`` で表示できます。先頭に ``*`` が付いているのが現在のブランチです。

.. code-block:: console

   $ git branch
   * main

新しいブランチを作成するには ``git branch <ブランチ名>`` を、ブランチを切り替えるには ``git switch <ブランチ名>`` を実行します。

.. code-block:: console

   $ git branch feature/login
   $ git switch feature/login
   Switched to branch 'feature/login'

``git switch -c`` を使うと、ブランチの作成と切り替えを 1 つのコマンドで行えます。

.. code-block:: console

   $ git switch -c feature/login

ブランチを切り替えると、ワーキングツリーのファイルは、切り替え先のブランチが指すコミットの状態に置き換わります。コミットしていない変更がある状態でブランチを切り替えると、変更が切り替え先に持ち越されたり、切り替えが拒否されたりします。ブランチを切り替える前に、変更をコミットするか、:doc:`useful` で説明する ``git stash`` で一時的に退避しておきましょう。

.. note::

   ``git switch`` は Git 2.23 で追加されたコマンドです。古い資料では、ブランチの切り替えに ``git checkout <ブランチ名>``、作成と切り替えに ``git checkout -b <ブランチ名>`` が使われています。

ブランチの名前は、作業の内容が分かるように付けます。``feature/login``\ （新機能）や ``fix/typo-in-readme``\ （バグの修正）のように、種類を表す接頭辞を付ける方法がよく使われます。

マージ
------

``git merge`` は、指定したブランチの変更を現在のブランチに取り込みます。``feature/login`` ブランチの変更を ``main`` ブランチに取り込む場合は、取り込む側の ``main`` ブランチに切り替えてから実行します。

.. code-block:: console

   $ git switch main
   $ git merge feature/login

マージの方法は、2 つのブランチの状態によって次の 2 種類に分かれます。

fast-forward マージ
^^^^^^^^^^^^^^^^^^^

``main`` ブランチでブランチの作成後に新しいコミットがない場合、Git は ``main`` ブランチの目印を ``feature/login`` ブランチの最新のコミットまで進めるだけでマージを完了します。これを fast-forward マージと呼びます。新しいコミットは作成されません。

.. code-block:: text

   Before:
          main
            |
            v
   [A] <-- [B] <-- [C] <-- [D]
                            ^
                            |
                      feature/login

   After:
                          main
                            |
                            v
   [A] <-- [B] <-- [C] <-- [D]
                            ^
                            |
                      feature/login

3-way マージ
^^^^^^^^^^^^

2 つのブランチの両方に新しいコミットがある場合、Git は 2 つのブランチの最新のコミットと、分岐元のコミットの 3 つを比較して変更を統合し、マージコミットを作成します。これを 3-way マージと呼びます。マージコミットは 2 つの親コミットを持ちます。

.. code-block:: text

                               main
                                 |
                                 v
   [A] <-- [B] <-- [C] <------- [M]
            ^                    |
            |                    |
            +---- [D] <-- [E] <--+
                           ^
                           |
                     feature/login

fast-forward マージが可能な場合でもマージコミットを作成したいときは、``--no-ff`` オプションを付けます。マージコミットが残ると、どのコミットがどのブランチで作成されたかが履歴から分かりやすくなります。

.. code-block:: console

   $ git merge --no-ff feature/login

ブランチの削除
--------------

マージが終わって不要になったブランチは、``git branch -d`` で削除します。

.. code-block:: console

   $ git branch -d feature/login
   Deleted branch feature/login (was 0fc0315).

まだマージしていないブランチを ``-d`` で削除しようとすると、変更が失われないようにエラーになります。マージしていない変更を破棄してでも削除したい場合は、``-D`` を使います。

コンフリクトの解消
------------------

2 つのブランチで同じファイルの同じ箇所を変更していると、Git はどちらの変更を採用すべきかを判断できず、マージを中断します。この状態をコンフリクト（競合）と呼びます。

.. code-block:: console

   $ git merge feature
   Auto-merging greeting.py
   CONFLICT (content): Merge conflict in greeting.py
   Automatic merge failed; fix conflicts and then commit the result.

コンフリクトが発生したファイルには、次のような記号が書き込まれます。

.. code-block:: text

   <<<<<<< HEAD
   MESSAGE = "Good morning"
   =======
   MESSAGE = "Hi"
   >>>>>>> feature

``<<<<<<< HEAD`` から ``=======`` までが現在のブランチの内容、``=======`` から ``>>>>>>> feature`` までが取り込もうとしたブランチの内容です。コンフリクトは次の手順で解消します。

1. ``git status`` で、コンフリクトが発生しているファイルを確認します。
2. ファイルを開き、最終的に残したい内容に編集します。``<<<<<<<``、``=======``、``>>>>>>>`` の行は必ず削除します。
3. 編集したファイルを ``git add`` でステージします。
4. ``git commit`` を実行して、マージを完了します。

.. code-block:: console

   $ git add greeting.py
   $ git commit

VS Code などのエディターには、コンフリクトした箇所を強調表示し、どちらの変更を採用するかをボタンで選べる機能があります。

コンフリクトの解消を諦めてマージを始める前の状態に戻したい場合は、``git merge --abort`` を実行します。

.. code-block:: console

   $ git merge --abort

リベース
--------

``git rebase`` は、現在のブランチのコミットを、指定したブランチの先端の後ろに付け替えます。``feature`` ブランチで作業している間に ``main`` ブランチが進んだ場合、次のように実行すると、``feature`` ブランチのコミットを最新の ``main`` ブランチの後ろに並べ直せます。

.. code-block:: console

   $ git switch feature
   $ git rebase main

.. code-block:: text

   Before:
   [A] <-- [B] <-- [C]                  main
            ^
            |
            +---- [D] <-- [E]           feature

   After:
   [A] <-- [B] <-- [C]                  main
                    ^
                    |
                    +---- [D'] <-- [E'] feature

リベースの後で ``main`` ブランチに ``feature`` ブランチをマージすると fast-forward マージになるため、履歴が 1 本の直線になり読みやすくなります。一方、付け替えられたコミット D' と E' は、元の D と E とは異なるコミット ID を持つ新しいコミットです。

リベースの途中でコンフリクトが発生した場合は、マージと同様にファイルを編集して ``git add`` した後、``git rebase --continue`` を実行します。リベースを中止する場合は ``git rebase --abort`` を実行します。

.. warning::

   既にリモートリポジトリにプッシュし、他の人が使っている可能性のあるコミットはリベースしないでください。リベースはコミットを作り直すため、他の人が持っている履歴と食い違います。リベースは、まだプッシュしていない自分だけのコミットを整理する目的で使いましょう。

.. _branch-sample:

サンプルスクリプト
------------------

この章の操作を体験するサンプルスクリプトです。PowerShell 版の内容は :ref:`powershell-samples` で確認できます。

ブランチの作成と、fast-forward マージおよび 3-way マージを体験するサンプルスクリプトです。

* :download:`branch_merge.sh をダウンロード <../examples/branch_merge.sh>`
* :download:`branch_merge.ps1（PowerShell 版）をダウンロード <../examples/branch_merge.ps1>`

.. literalinclude:: ../examples/branch_merge.sh
   :language: bash
   :caption: branch_merge.sh

コンフリクトを発生させ、解消するまでを体験するサンプルスクリプトです。

* :download:`conflict_demo.sh をダウンロード <../examples/conflict_demo.sh>`
* :download:`conflict_demo.ps1（PowerShell 版）をダウンロード <../examples/conflict_demo.ps1>`

.. literalinclude:: ../examples/conflict_demo.sh
   :language: bash
   :caption: conflict_demo.sh
