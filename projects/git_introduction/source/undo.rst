変更の取り消し
==============

Git では、ほとんどの操作を後から取り消せます。この章では、取り消したい対象ごとに使うコマンドを説明します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 取り消したいもの
     - 使うコマンド
   * - ワーキングツリーの変更（まだステージしていない変更）
     - ``git restore <file>``
   * - ステージした変更（ステージだけを取り消す）
     - ``git restore --staged <file>``
   * - 直前のコミットの内容やメッセージ
     - ``git commit --amend``
   * - 過去のコミット（履歴を残したまま打ち消す）
     - ``git revert <commit>``
   * - 過去のコミット（履歴から取り除く）
     - ``git reset <commit>``

この章の操作を体験するサンプルスクリプトは、:ref:`undo-sample` にあります。

ワーキングツリーの変更を取り消す
--------------------------------

ファイルを編集したものの、編集前の状態に戻したい場合は ``git restore`` を使います。

.. code-block:: console

   $ git restore hello.py

``git restore <file>`` は、ワーキングツリーのファイルをステージングエリアの状態に戻します。そのファイルの変更をステージしていなければ、最後のコミットの状態に戻ります。ステージした変更も含めて最後のコミットの状態に戻したい場合は、``git restore --staged --worktree <file>`` を実行します。

.. warning::

   ``git restore`` で取り消した変更は、Git に記録されていないため元に戻せません。実行する前に、本当に不要な変更かを ``git diff`` で確認してください。

ステージを取り消す
------------------

``git add`` でステージした変更をステージングエリアから外すには、``--staged`` オプションを付けて ``git restore`` を実行します。ワーキングツリーの変更はそのまま残ります。

.. code-block:: console

   $ git restore --staged hello.py

.. note::

   ``git restore`` は Git 2.23 で追加されたコマンドです。古い資料では、同じ操作に ``git checkout -- <file>`` や ``git reset HEAD <file>`` が使われています。これらのコマンドも引き続き使えますが、本資料では役割が明確な ``git restore`` を使います。

直前のコミットを修正する
------------------------

コミットした直後に、コミットメッセージの誤りやファイルの追加漏れに気付いた場合は、``git commit --amend`` で直前のコミットを修正できます。

.. code-block:: console

   $ git add forgotten.py
   $ git commit --amend -m "Add greeting script and helper"

``--amend`` は、直前のコミットを修正後の内容で作り直します。作り直されたコミットは、元のコミットとは異なるコミット ID になります。

.. warning::

   既にリモートリポジトリにプッシュしたコミットは、``--amend`` で修正しないでください。他の人が持っている履歴と食い違い、混乱の原因になります。プッシュ済みのコミットを取り消したい場合は、次に説明する ``git revert`` を使います。

コミットを打ち消す
------------------

``git revert`` は、指定したコミットの変更を打ち消す新しいコミットを作成します。元のコミットは履歴に残るため、既にプッシュしたコミットに対しても安全に使えます。

.. code-block:: console

   $ git revert HEAD
   [main 9ba290e] Revert "Add line 3"
    1 file changed, 1 deletion(-)

``HEAD`` は最新のコミットを表します。``HEAD~1`` は 1 つ前、``HEAD~2`` は 2 つ前のコミットを表し、コミット ID の代わりに使えます。

コミットを取り消す
------------------

``git reset`` は、現在のブランチが指すコミットを指定したコミットに移動し、それより後のコミットを履歴から取り除きます。オプションによって、ステージングエリアとワーキングツリーをどう扱うかが変わります。

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - オプション
     - ステージングエリア
     - ワーキングツリー
     - 主な用途
   * - ``--soft``
     - 変更しない
     - 変更しない
     - 複数のコミットを 1 つにまとめ直します。
   * - ``--mixed``\ （既定）
     - 指定したコミットの状態に戻す
     - 変更しない
     - コミットを取り消し、変更をステージし直します。
   * - ``--hard``
     - 指定したコミットの状態に戻す
     - 指定したコミットの状態に戻す
     - コミットも変更もすべて破棄します。

たとえば、直前のコミットを取り消し、その変更をワーキングツリーに残したまま作業をやり直すには、次のように実行します。

.. code-block:: console

   $ git reset HEAD~1

.. warning::

   ``git reset --hard`` は、まだコミットしていないワーキングツリーの変更も破棄します。破棄した変更は元に戻せないため、実行する前に ``git status`` で状態を確認してください。また、``git commit --amend`` と同じ理由で、プッシュ済みのコミットに対して ``git reset`` を使わないでください。

reflog で失ったコミットを取り戻す
---------------------------------

``git reset`` で取り除いたコミットも、すぐに消えるわけではありません。``git reflog`` を使うと、HEAD が過去にどのコミットを指していたかの履歴を確認できます。

.. code-block:: console

   $ git reflog
   efc7b06 HEAD@{0}: reset: moving to HEAD~1
   9ba290e HEAD@{1}: revert: Revert "Add line 3"
   efc7b06 HEAD@{2}: commit: Add line 3

取り除いたコミットの ID が分かれば、``git reset --hard 9ba290e`` のように実行して、その状態に戻せます。コミット ID の代わりに、``HEAD@{1}`` のような reflog の表記で指定することもできます。PowerShell では、``{}`` を含む引数を引用符で囲む必要があります（:doc:`powershell` を参照）。

.. code-block:: console

   $ git reset --hard HEAD@{1}

.. code-block:: ps1con

   PS> git reset --hard 'HEAD@{1}'

reflog はローカルリポジトリにだけ記録され、一定期間が過ぎると古い記録から削除されます。標準では、どのブランチからもたどれなくなったコミットの記録は 30 日、それ以外の記録は 90 日で削除されます。

.. _undo-sample:

サンプルスクリプト
------------------

この章で説明した ``git restore``、``git revert``、``git reset``、``git reflog`` を順に実行するサンプルスクリプトです。

PowerShell 版の内容は :ref:`powershell-samples` で確認できます。

* :download:`undo_demo.sh をダウンロード <../examples/undo_demo.sh>`
* :download:`undo_demo.ps1（PowerShell 版）をダウンロード <../examples/undo_demo.ps1>`

.. literalinclude:: ../examples/undo_demo.sh
   :language: bash
   :caption: undo_demo.sh
