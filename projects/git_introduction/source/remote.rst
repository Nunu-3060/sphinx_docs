リモートリポジトリ
==================

これまでの章では、手元のコンピューターにあるリポジトリ（ローカルリポジトリ）だけを操作してきました。この章では、GitHub などのサーバー上にあるリポジトリ（リモートリポジトリ）を使って、変更を共有する方法を説明します。

リモートリポジトリとは
----------------------

リモートリポジトリは、ネットワーク上に置かれたリポジトリです。各開発者は、リモートリポジトリの内容をローカルリポジトリに取り込み（フェッチ）、ローカルリポジトリで作成したコミットをリモートリポジトリに送信（プッシュ）することで、変更を共有します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コマンド
     - 説明
   * - ``git clone``
     - リモートリポジトリを複製して、ローカルリポジトリを作成します。
   * - ``git fetch``
     - リモートリポジトリの新しいコミットを、ローカルリポジトリに取り込みます。ワーキングツリーは変更しません。
   * - ``git pull``
     - ``git fetch`` を実行した後、取り込んだ変更を現在のブランチに統合します。
   * - ``git push``
     - ローカルリポジトリのコミットを、リモートリポジトリに送信します。

リポジトリの複製
----------------

既存のリモートリポジトリを手元に複製するには、``git clone`` に URL を指定します。

.. code-block:: console

   $ git clone https://github.com/octocat/Hello-World.git
   $ cd Hello-World

``git clone`` を実行すると、リモートリポジトリと同じ名前のディレクトリが作成され、すべての履歴がダウンロードされます。複製元のリモートリポジトリは、``origin`` という名前で自動的に登録されます。

リモートリポジトリの登録
------------------------

``git init`` で作成したローカルリポジトリを、後からリモートリポジトリと結び付けるには ``git remote add`` を使います。一般に、主となるリモートリポジトリには ``origin`` という名前を付けます。

.. code-block:: console

   $ git remote add origin https://github.com/taro/hello-git.git
   $ git remote -v
   origin  https://github.com/taro/hello-git.git (fetch)
   origin  https://github.com/taro/hello-git.git (push)

``git remote -v`` で、登録されているリモートリポジトリの名前と URL を確認できます。

GitHub でリモートリポジトリを作成する手順は、:doc:`github` で説明します。

プッシュ
--------

``git push`` で、ローカルリポジトリのコミットをリモートリポジトリに送信します。初めてプッシュするブランチでは、``-u`` オプションを付けます。

.. code-block:: console

   $ git push -u origin main

``-u`` オプションを付けると、ローカルの ``main`` ブランチとリモートの ``main`` ブランチが対応付けられます。これを上流ブランチ（upstream）の設定と呼びます。一度設定すれば、以降は ``git push`` や ``git pull`` だけで、対応するブランチとやり取りできます。

他の人が先にプッシュしていて、リモートリポジトリにローカルリポジトリにないコミットがある場合、プッシュは拒否されます。

.. code-block:: console

   $ git push
    ! [rejected]        main -> main (fetch first)
   error: failed to push some refs to 'https://github.com/taro/hello-git.git'

この場合は、``git pull`` でリモートリポジトリの変更を取り込んでから、もう一度プッシュします。

フェッチとリモート追跡ブランチ
------------------------------

``git fetch`` を実行すると、リモートリポジトリの新しいコミットがダウンロードされ、``origin/main`` のようなリモート追跡ブランチが更新されます。リモート追跡ブランチは、最後にフェッチした時点でのリモートリポジトリのブランチの位置を記録したものです。

.. code-block:: console

   $ git fetch
   $ git log --oneline main..origin/main

``main..origin/main`` は、「``origin/main`` にあって ``main`` にないコミット」を表します。上の例では、リモートリポジトリで追加されたコミットのうち、まだ手元の ``main`` ブランチに取り込んでいないものを確認しています。

``git fetch`` はローカルのブランチやワーキングツリーを変更しないため、いつ実行しても安全です。

プル
----

``git pull`` は、``git fetch`` と、取り込んだ変更の統合をまとめて行います。

.. code-block:: console

   $ git pull

ローカルの ``main`` ブランチに新しいコミットがなければ、fast-forward マージで統合されます。ローカルとリモートの両方に新しいコミットがある場合の統合方法は、次の設定で選べます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定
     - 両方に新しいコミットがある場合の動作
   * - ``git config --global pull.ff only``
     - 統合せずにエラーにします。利用者が統合方法を判断してから、改めて操作します。
   * - ``git config --global pull.rebase false``
     - マージで統合します（マージコミットが作成されます）。
   * - ``git config --global pull.rebase true``
     - リベースで統合します（ローカルのコミットがリモートのコミットの後ろに付け替えられます）。

統合方法を設定していない状態で両方に新しいコミットがある場合、Git は統合方法を指定するよう求めるエラーを表示して、プルを中断します。どの方法を選ぶかはチームで統一しておきましょう。迷う場合は、意図しないマージコミットが作成されない ``pull.ff only`` をお勧めします。

認証
----

GitHub にプッシュするには、認証が必要です。認証の方法には HTTPS と SSH の 2 種類があります。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 方法
     - 説明
   * - HTTPS
     - ``https://github.com/...`` 形式の URL を使います。GitHub ではパスワードによる認証は使えないため、Git for Windows に付属する Git Credential Manager によるブラウザーでの認証や、個人用アクセストークンを使います。
   * - SSH
     - ``git@github.com:...`` 形式の URL を使います。SSH の鍵ペアを作成し、公開鍵を GitHub に登録して認証します。

SSH の鍵ペアは、次のコマンドで作成できます。作成された公開鍵（``~/.ssh/id_ed25519.pub``）の内容を、GitHub の「Settings」の「SSH and GPG keys」に登録します。秘密鍵（``~/.ssh/id_ed25519``）は、他の人に渡したり、リポジトリにコミットしたりしないでください。

.. code-block:: console

   $ ssh-keygen -t ed25519 -C "taro@example.com"
   $ ssh -T git@github.com

公開鍵の内容は、次のコマンドでクリップボードにコピーできます。コピーした内容を GitHub の登録画面に貼り付けます。

.. code-block:: console

   $ cat ~/.ssh/id_ed25519.pub | clip

.. code-block:: ps1con

   PS> Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard

``clip`` は Windows のコマンドです。macOS では ``clip`` の代わりに ``pbcopy`` を使います。``ssh-keygen`` と ``ssh`` は、Git Bash と PowerShell のどちらでも同じように入力できます。

``ssh -T git@github.com`` を実行して、GitHub のユーザー名を含むメッセージが表示されれば、SSH の設定は完了しています。

詳しい手順は、GitHub の公式ドキュメント `SSH を使用した GitHub への接続 <https://docs.github.com/ja/authentication/connecting-to-github-with-ssh>`_ を参照してください。
