.. _ch-user:

ユーザーとグループの管理
========================

この章では、ユーザーとグループの作成・変更・削除、パスワードポリシー、``sudo`` の権限設定を説明します。

ユーザー情報を保存するファイル
------------------------------

Linux のユーザーとグループの情報は、次のテキストファイルに保存されています。

.. list-table:: ユーザー情報を保存するファイル
   :header-rows: 1
   :widths: 25 75

   * - ファイル
     - 内容
   * - ``/etc/passwd``
     - ユーザー名、ユーザー ID（UID）、主グループの ID（GID）、ホームディレクトリ、ログインシェルなど。全ユーザーが読める
   * - ``/etc/shadow``
     - パスワードのハッシュ値と有効期限。root のみが読める
   * - ``/etc/group``
     - グループ名、グループ ID、所属するユーザー

``/etc/passwd`` は、1 行が 1 ユーザーに対応し、項目を ``:`` で区切って記述します。

.. code-block:: text
   :linenos:

   admin:x:1000:1000:Administrator:/home/admin:/bin/bash

左から、ユーザー名、パスワード（``x`` は ``/etc/shadow`` に保存されていることを表す）、UID、GID、コメント、ホームディレクトリ、ログインシェルです。

UID が 1000 未満のユーザーは、サービスを動かすためのシステムユーザーです。人が使う一般ユーザーには、1000 以上の UID が割り当てられます。

これらのファイルは直接編集せず、次の節で説明するコマンドを使って変更してください。

ユーザーとグループの操作
------------------------

ユーザーとグループを操作する主なコマンドを次に示します。いずれも管理者権限が必要です。

.. list-table:: ユーザーとグループを操作するコマンド
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 動作
   * - ``useradd -m -c "<コメント>" <ユーザー>``
     - ユーザーを作成する。``-m`` でホームディレクトリも作成する
   * - ``passwd <ユーザー>``
     - パスワードを設定する
   * - ``usermod -aG <グループ> <ユーザー>``
     - ユーザーを補助グループに追加する。``-a`` を忘れると、他の補助グループから外れるので注意する
   * - ``usermod -L <ユーザー>``
     - ユーザーをロックする（パスワードでログインできなくする）
   * - ``userdel -r <ユーザー>``
     - ユーザーを削除する。``-r`` でホームディレクトリも削除する
   * - ``groupadd <グループ>``
     - グループを作成する
   * - ``groupdel <グループ>``
     - グループを削除する
   * - ``id <ユーザー>``
     - ユーザーの UID と所属するグループを表示する

次の例では、開発者用のグループ ``developers`` を作成し、ユーザー ``alice`` を作成してそのグループに追加しています。

.. code-block:: console
   :linenos:

   $ sudo groupadd developers
   $ sudo useradd -m -c "Alice Example" -G developers alice
   $ sudo passwd alice
   $ id alice
   uid=1001(alice) gid=1001(alice) groups=1001(alice),1002(developers)

ユーザーを作成すると、同じ名前の主グループも自動で作成されます。グループへの追加は、そのユーザーが次にログインしたときから有効になります。

多数のユーザーを作成する場合は、CSV ファイルから一括で作成するスクリプトを使うと便利です。

.. literalinclude:: ../examples/shell/create_users.sh
   :language: bash
   :linenos:
   :caption: create_users.sh

:download:`create_users.sh をダウンロード <../examples/shell/create_users.sh>`

パスワードポリシー
------------------

パスワードの有効期限は ``chage`` コマンドで確認・設定します。

.. code-block:: console
   :linenos:

   $ sudo chage -l alice
   $ sudo chage -M 90 -W 14 alice

2 行目では、パスワードの有効期間を 90 日、期限切れの警告を 14 日前から表示するように設定しています。新しく作成するユーザーの既定値は ``/etc/login.defs`` の ``PASS_MAX_DAYS`` などで設定します。

パスワードの長さや複雑さの条件は、``/etc/security/pwquality.conf`` で設定します。

.. code-block:: ini
   :linenos:
   :caption: /etc/security/pwquality.conf の設定例

   # パスワードの最小の長さ
   minlen = 12
   # 必要な文字の種類の数 (大文字、小文字、数字、記号のうち)
   minclass = 3

この条件は、一般ユーザーが ``passwd`` で自分のパスワードを変更するときに適用されます。管理者が ``sudo passwd`` で設定する場合は、警告が表示されるだけで設定はできてしまうため注意してください。

.. _sec-faillock:

ログイン失敗時のアカウントロック
--------------------------------

パスワードを何度も試す攻撃への対策として、ログインに一定回数失敗したユーザーを一時的にロックする仕組み（faillock）があります。認証の設定は ``authselect`` コマンドで管理されており、次のように faillock を有効にします。

.. code-block:: console
   :linenos:

   $ authselect current
   $ sudo authselect enable-feature with-faillock

ロックの条件は ``/etc/security/faillock.conf`` で設定します。

.. code-block:: ini
   :linenos:
   :caption: /etc/security/faillock.conf の設定例

   # 5 回失敗したらロックする
   deny = 5
   # 15 分 (900 秒) 経過したらロックを解除する
   unlock_time = 900

ロックされたユーザーの状態の確認と、ロックの解除は次のように行います。

.. code-block:: console
   :linenos:

   $ sudo faillock --user alice
   $ sudo faillock --user alice --reset

公開鍵認証で SSH 接続する場合は、パスワードを使わないため faillock の対象になりません。SSH への攻撃への対策は「:ref:`ch-security`」で説明します。

.. _sec-sudoers:

sudo の権限設定
---------------

``sudo`` で誰がどのコマンドを実行できるかは、``/etc/sudoers`` と ``/etc/sudoers.d/`` 内のファイルで設定します。Rocky Linux の既定の設定では、``wheel`` グループに所属するユーザーがすべてのコマンドを実行できます。

.. code-block:: text
   :linenos:
   :caption: /etc/sudoers の既定の設定（抜粋）

   %wheel  ALL=(ALL)       ALL

管理者として扱うユーザーは ``wheel`` グループに追加します。

.. code-block:: console
   :linenos:

   $ sudo usermod -aG wheel alice

特定のコマンドだけを許可する場合は、``/etc/sudoers.d/`` にファイルを作成します。次の例では、``webadmin`` グループのユーザーに、nginx の再起動と設定の検査だけを許可しています。

.. code-block:: text
   :linenos:
   :caption: /etc/sudoers.d/webadmin

   %webadmin ALL=(root) /usr/bin/systemctl restart nginx, /usr/sbin/nginx -t

sudoers のファイルは、必ず ``visudo`` コマンドで編集してください。``visudo`` は保存時に文法を検査するため、記述の誤りによって ``sudo`` が使えなくなる事態を防げます。

.. code-block:: console
   :linenos:

   $ sudo visudo -f /etc/sudoers.d/webadmin
