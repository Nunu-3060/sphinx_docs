.. _ch-boot-kernel:

起動の仕組みとカーネル
======================

この章では、電源を入れてからログインできるようになるまでの流れと、ブートローダーやカーネルの管理方法を説明します。この章の内容は、「:ref:`ch-troubleshooting`」で起動しないシステムを復旧する際の前提知識になります。

起動の流れ
----------

Rocky Linux は、次の順序で起動します。

.. list-table:: 起動の流れ
   :header-rows: 1
   :widths: 10 25 65

   * - 順序
     - 段階
     - 処理の内容
   * - 1
     - ファームウェア（UEFI / BIOS）
     - ハードウェアを初期化し、ディスク上のブートローダーを読み込んで実行する
   * - 2
     - ブートローダー（:term:`GRUB 2`）
     - 起動メニューを表示し、選ばれたカーネルと :term:`initramfs` をメモリに読み込んで、カーネルに制御を渡す
   * - 3
     - :term:`カーネル`
     - ハードウェアを認識し、initramfs を一時的なルートファイルシステムとして使って起動処理を進める
   * - 4
     - initramfs
     - 本来のルートファイルシステム（LVM 上の ``/`` など）を使うために必要なドライバーを読み込み、ルートファイルシステムをマウントする
   * - 5
     - systemd
     - PID 1 として起動し、既定のターゲットに必要なサービスを順に起動する
   * - 6
     - ログイン画面
     - コンソールのログインプロンプト、または GUI のログイン画面が表示される

起動にかかった時間と、時間のかかったサービスは次のコマンドで確認できます。

.. code-block:: console
   :linenos:

   $ systemd-analyze
   $ systemd-analyze blame | head

起動時のメッセージは ``journalctl -b`` で確認できます（「:ref:`ch-log-monitoring`」を参照）。

.. _sec-boot-target:

ブートターゲット
----------------

systemd は、起動時に「どの状態まで起動するか」をターゲットで指定します。主なターゲットは次のとおりです。

.. list-table:: 主なターゲット
   :header-rows: 1
   :widths: 30 70

   * - ターゲット
     - 状態
   * - ``multi-user.target``
     - ネットワークを含むすべてのサービスが起動した、CUI での通常の状態。サーバーの既定値
   * - ``graphical.target``
     - ``multi-user.target`` に加えて、GUI のログイン画面が起動した状態
   * - ``rescue.target``
     - 最小限のサービスだけを起動した、保守用の状態（レスキューモード）。root のパスワードが必要
   * - ``emergency.target``
     - ルートファイルシステムを読み取り専用でマウントしただけの、最も限られた状態（緊急モード）。root のパスワードが必要

既定のターゲットの確認と変更は、次のように行います。

.. code-block:: console
   :linenos:

   $ systemctl get-default
   multi-user.target
   $ sudo systemctl set-default graphical.target

``set-default`` の変更は次回の起動時から有効になります。

.. note::

   Rocky Linux 10 では root アカウントが既定で無効なため、``rescue.target`` と ``emergency.target`` では root のパスワードを求められてもログインできません。この場合の対処方法は「:ref:`ch-troubleshooting`」で説明します。

GRUB 2 の設定
-------------

Rocky Linux は、ブートローダーとして GRUB 2 を使います。起動メニューの項目は、カーネルごとに ``/boot/loader/entries/`` に作成されるファイル（BLS 形式）で管理されています。これらのファイルを直接編集するのではなく、``grubby`` コマンドで操作します。

.. code-block:: console
   :linenos:

   $ sudo grubby --default-kernel
   /boot/vmlinuz-6.12.0-211.16.1.el10_2.x86_64
   $ sudo grubby --info=ALL
   $ sudo grubby --set-default=/boot/vmlinuz-6.12.0-211.13.1.el10_2.x86_64

上から順に、既定で起動するカーネルの確認、すべての起動項目の表示、既定で起動するカーネルの変更です。カーネルのバージョンは例です。

起動メニューの表示時間などの全体的な設定は ``/etc/default/grub`` に記述します。このファイルを変更した場合は、次のコマンドで GRUB 2 の設定ファイルを再生成します。

.. code-block:: console
   :linenos:

   $ sudo grub2-mkconfig -o /boot/grub2/grub.cfg

UEFI と BIOS のどちらで起動している場合も、出力先は ``/boot/grub2/grub.cfg`` です。

.. _sec-kernel-param:

カーネルパラメーター
--------------------

カーネルパラメーターは、起動時にカーネルに渡す設定です。永続的に変更するには ``grubby`` を使います。

.. code-block:: console
   :linenos:

   $ cat /proc/cmdline
   $ sudo grubby --update-kernel=ALL --args="console=ttyS0,115200"
   $ sudo grubby --update-kernel=ALL --remove-args="console=ttyS0,115200"

1 行目で現在のカーネルパラメーターを確認し、2 行目ですべてのカーネルにパラメーターを追加し、3 行目で削除しています。変更は次回の起動時から有効になります。

1 回の起動だけ一時的に変更するには、起動メニューで次のように操作します。トラブルシューティングで、レスキューモードで起動する場合などに使います。

1. 起動メニューが表示されたら、:kbd:`↑` / :kbd:`↓` で起動するカーネルを選び、:kbd:`e` を押します。
2. 編集画面で ``linux`` から始まる行を探し、行末にパラメーターを追加します。
3. :kbd:`Ctrl+X` を押して起動します。

起動時によく使うカーネルパラメーターを次に示します。

.. list-table:: よく使うカーネルパラメーター
   :header-rows: 1
   :widths: 35 65

   * - パラメーター
     - 意味
   * - ``systemd.unit=rescue.target``
     - レスキューモードで起動する
   * - ``systemd.unit=emergency.target``
     - 緊急モードで起動する
   * - ``rd.break``
     - initramfs の段階で起動を中断し、シェルを起動する（「:ref:`ch-troubleshooting`」を参照）
   * - ``inst.ks=<URL>``
     - インストーラーに Kickstart ファイルを読み込ませる（「:ref:`ch-installation`」を参照）

カーネルの更新
--------------

カーネルのパッケージは、他のパッケージとは異なり、更新しても古いバージョンが削除されず、新しいバージョンが追加で導入されます。新しいカーネルで問題が起きた場合に、起動メニューから古いカーネルを選んで起動できるようにするためです。

.. code-block:: console
   :linenos:

   $ uname -r
   6.12.0-211.16.1.el10_2.x86_64
   $ rpm -q kernel
   kernel-6.12.0-211.13.1.el10_2.x86_64
   kernel-6.12.0-211.16.1.el10_2.x86_64

``uname -r`` は現在動作しているカーネルのバージョンを、``rpm -q kernel`` は導入されているカーネルの一覧を表示します。新しいカーネルは、再起動するまで使われません。

保持するカーネルの数は、``/etc/dnf/dnf.conf`` の ``installonly_limit`` で決まります（既定値は 3）。これを超えると、古いカーネルから自動で削除されます。手動で古いカーネルを削除するには、次のようにします。

.. code-block:: console
   :linenos:

   $ sudo dnf remove --oldinstallonly

カーネルモジュール
------------------

デバイスドライバーなどのカーネルの機能の多くは、必要なときに読み込まれるカーネルモジュールとして提供されています。

.. code-block:: console
   :linenos:

   $ lsmod | head
   $ modinfo xfs
   $ sudo modprobe <モジュール名>

上から順に、読み込まれているモジュールの一覧、モジュールの情報の表示、モジュールの読み込みです。通常は、ハードウェアの認識に合わせて自動で読み込まれるため、手動で操作する機会はあまりありません。

Rocky Linux に含まれていない外部のカーネルモジュール（NVIDIA の GPU のドライバーなど）は、:term:`DKMS` という仕組みで管理するのが一般的です。DKMS は、外部のカーネルモジュールをソースコードからビルドし、カーネルが更新されるたびに自動でビルドし直します。カーネルの更新のたびに対応が必要になる点に注意が必要です。詳しくは「:ref:`ch-gpu`」で説明します。

カーネルの動作を調整するパラメーター（sysctl）については、「:ref:`ch-log-monitoring`」で説明します。
