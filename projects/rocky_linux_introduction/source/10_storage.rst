.. _ch-storage:

ストレージ管理
==============

この章では、ディスクの追加、:term:`LVM` によるボリュームの管理、:term:`XFS` ファイルシステムの作成と拡張、バックアップとリストア、NFS のマウントを説明します。

ディスクとデバイス名
--------------------

Linux では、ディスクは ``/dev/`` 以下のデバイスファイルとして扱われます。デバイス名は接続方式によって異なります。

.. list-table:: 主なデバイス名
   :header-rows: 1
   :widths: 30 70

   * - デバイス名
     - 接続方式
   * - ``/dev/sda``、``/dev/sdb``
     - SATA、SAS、USB、Hyper-V の仮想ディスクなど
   * - ``/dev/vda``、``/dev/vdb``
     - KVM の virtio 形式の仮想ディスク
   * - ``/dev/nvme0n1``、``/dev/nvme1n1``
     - NVMe 接続の SSD

パーティションは、デバイス名の後に番号を付けて表します（``/dev/sda1``、``/dev/nvme0n1p1`` など）。

ディスクとパーティションの構成は ``lsblk`` で、ファイルシステムの使用量は ``df`` で確認します。

.. code-block:: console
   :linenos:

   $ lsblk
   NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
   sda           8:0    0   40G  0 disk
   ├─sda1        8:1    0  600M  0 part /boot/efi
   ├─sda2        8:2    0    1G  0 part /boot
   └─sda3        8:3    0 38.4G  0 part
     ├─rl-root 253:0    0 34.4G  0 lvm  /
     └─rl-swap 253:1    0    4G  0 lvm  [SWAP]
   sdb           8:16   0   20G  0 disk
   $ df -h
   $ sudo du -sh /var/log

この例では、``sda`` に OS がインストールされており、``sdb`` は追加したばかりの何も使われていないディスクです。インストール時に自動構成を選ぶと、``rl`` という名前の LVM のボリュームグループが作成され、その中に ``/`` とスワップ領域が作成されます。

LVM の仕組み
------------

LVM（Logical Volume Manager）は、複数のディスクをまとめて 1 つの大きな領域として扱い、そこから必要な大きさの領域を切り出して使う仕組みです。LVM を使うと、ファイルシステムを使ったまま容量を拡張したり、ディスクを追加したりできます。

.. list-table:: LVM の構成要素
   :header-rows: 1
   :widths: 30 70

   * - 構成要素
     - 説明
   * - 物理ボリューム（PV）
     - LVM で使うディスクやパーティション
   * - ボリュームグループ（VG）
     - 1 つ以上の PV をまとめた領域
   * - 論理ボリューム（LV）
     - VG から切り出した領域。ここにファイルシステムを作成する

ディスクを追加して使う
----------------------

追加したディスク ``/dev/sdb`` に LVM の領域を作成し、``/srv/data`` にマウントする手順を説明します。

1. パーティションを作成します。ここではディスク全体を 1 つのパーティションにします。

   .. code-block:: console
      :linenos:

      $ sudo parted /dev/sdb --script mklabel gpt mkpart data 1MiB 100% set 1 lvm on
      $ lsblk /dev/sdb

2. PV、VG、LV を順に作成します。

   .. code-block:: console
      :linenos:

      $ sudo pvcreate /dev/sdb1
      $ sudo vgcreate datavg /dev/sdb1
      $ sudo lvcreate -n datalv -L 10G datavg
      $ sudo lvs

   3 行目では、VG ``datavg`` から 10 GiB の LV ``datavg/datalv`` を作成しています。残りの領域は、後で拡張するために空けておきます。

3. XFS ファイルシステムを作成してマウントします。

   .. code-block:: console
      :linenos:

      $ sudo mkfs.xfs /dev/datavg/datalv
      $ sudo mkdir -p /srv/data
      $ sudo mount /dev/datavg/datalv /srv/data
      $ df -h /srv/data

XFS は、Rocky Linux の標準のファイルシステムです。大容量のファイルやディスクの扱いに優れていますが、容量を縮小できないという制約があります。

起動時の自動マウント
--------------------

``mount`` コマンドでのマウントは、再起動すると解除されます。起動時に自動でマウントするには、``/etc/fstab`` に記述します。デバイスの指定には、デバイス名の変化に影響されない UUID を使うのが安全です。

.. code-block:: console
   :linenos:

   $ sudo blkid /dev/datavg/datalv
   /dev/datavg/datalv: UUID="3f1c2b7a-8d4e-4c5f-9a6b-0e1d2c3b4a59" TYPE="xfs"

.. code-block:: text
   :linenos:
   :caption: /etc/fstab に追加する行

   UUID=3f1c2b7a-8d4e-4c5f-9a6b-0e1d2c3b4a59  /srv/data  xfs  defaults  0 0

``/etc/fstab`` を編集したら、再起動する前に必ず次のコマンドで誤りがないかを確認します。

.. code-block:: console
   :linenos:

   $ sudo systemctl daemon-reload
   $ sudo umount /srv/data
   $ sudo mount -a
   $ df -h /srv/data

.. warning::

   ``/etc/fstab`` に誤りがあると、起動時にマウントに失敗し、緊急モードで停止することがあります。起動に必須ではないディスクには、オプションに ``nofail`` を加えておくと、マウントに失敗しても起動を続けられます（例: ``defaults,nofail``）。

容量の拡張
----------

LVM と XFS を使っていれば、ファイルシステムを使ったまま容量を拡張できます。

.. code-block:: console
   :linenos:

   $ sudo vgs
   $ sudo lvextend -r -L +5G /dev/datavg/datalv
   $ df -h /srv/data

1 行目で VG の空き容量（``VFree``）を確認し、2 行目で LV を 5 GiB 拡張しています。``-r`` を付けると、LV の拡張に続けてファイルシステムも拡張します。

VG に空き容量がない場合は、ディスクを追加して PV を作成し、``vgextend`` で VG に加えてから拡張します。

.. code-block:: console
   :linenos:

   $ sudo pvcreate /dev/sdc
   $ sudo vgextend datavg /dev/sdc

.. _sec-backup:

バックアップとリストア
----------------------

障害や操作ミスに備えて、定期的にバックアップを取得します。ここでは、標準のコマンドを使った基本的な方法を説明します。

tar によるバックアップ
~~~~~~~~~~~~~~~~~~~~~~

``tar`` を使うと、ディレクトリを 1 つのファイルにまとめて保存できます（「:ref:`ch-shell`」を参照）。Rocky Linux では SELinux のラベル（「:ref:`ch-security`」を参照）もファイルの属性として保存されているため、バックアップとリストアの際は ``--selinux`` と ``--xattrs`` を付けて、ラベルも含めて扱います。

.. code-block:: console
   :linenos:

   $ sudo tar --selinux --xattrs --acls -czpf /var/backup/etc.tar.gz /etc
   $ sudo tar --selinux --xattrs --acls -xzpf /var/backup/etc.tar.gz -C /tmp/restore

1 行目でバックアップを作成し、2 行目で ``/tmp/restore`` に展開しています。``tar`` は先頭の ``/`` を取り除いて保存するため、展開すると ``/tmp/restore/etc/`` に復元されます。必要なファイルを確認してから、元の場所にコピーしてください。

rsync による同期
~~~~~~~~~~~~~~~~

``rsync`` は、2 つのディレクトリの内容を同期するコマンドです。2 回目以降は変更のあったファイルだけを転送するため、大量のファイルを効率よくバックアップできます。SSH を使って別のサーバーへ転送することもできます（「:ref:`ch-network`」を参照）。

.. code-block:: console
   :linenos:

   $ sudo rsync -aAX --delete /srv/www/ /var/backup/www/

``-a`` はパーミッションや所有者などの属性を保持し、``-A`` は ACL、``-X`` は拡張属性（SELinux のラベルを含む）を保持します。``--delete`` は、コピー元で削除されたファイルをコピー先からも削除します。コピー元のディレクトリの末尾に ``/`` を付けると、ディレクトリそのものではなく、ディレクトリの中身を同期します。

バックアップのスクリプト
~~~~~~~~~~~~~~~~~~~~~~~~

``/etc`` と ``/srv/www`` を日付付きのファイル名でバックアップし、古いバックアップを削除するスクリプトの例を示します。「:ref:`sec-systemd-timer`」で示したタイマーと組み合わせると、毎日自動で実行できます。

.. literalinclude:: ../examples/shell/backup.sh
   :language: bash
   :linenos:
   :caption: backup.sh

:download:`backup.sh をダウンロード <../examples/shell/backup.sh>`

バックアップは、同じサーバーのディスクだけに置いておくと、ディスクの故障やサーバーの障害でバックアップも同時に失われます。``REMOTE_DEST`` を設定して別のサーバーにも転送してください。また、定期的にリストアの手順を試し、バックアップから実際に復元できることを確認してください。

LVM スナップショット
~~~~~~~~~~~~~~~~~~~~

LVM のスナップショットを使うと、ある時点の LV の状態を瞬時に保存できます。ソフトウェアの更新などの作業の前に取得しておくと、問題が起きたときに作業前の状態のファイルを取り出せます。スナップショットを作成するには、VG に空き容量が必要です。

.. code-block:: console
   :linenos:

   $ sudo lvcreate -s -n datasnap -L 2G /dev/datavg/datalv
   $ sudo mkdir -p /mnt/snap
   $ sudo mount -o ro,nouuid /dev/datavg/datasnap /mnt/snap
   $ ls /mnt/snap
   $ sudo umount /mnt/snap
   $ sudo lvremove /dev/datavg/datasnap

1 行目で、変更を記録する領域として 2 GiB を割り当ててスナップショットを作成しています。元の LV への変更量がこの容量を超えると、スナップショットは使えなくなります。3 行目の ``nouuid`` は、元の XFS ファイルシステムと同じ UUID を持つスナップショットをマウントするために必要なオプションです。スナップショットは長期間残すと性能が低下するため、作業が終わったら 6 行目のように削除します。

スナップショットは元の LV と同じディスク上にあるため、ディスクの故障には対応できません。バックアップの代わりにはならないことに注意してください。

NFS のマウント
--------------

NFS は、ネットワーク経由で別のサーバーのディレクトリを共有する仕組みです。NFS サーバーが公開しているディレクトリを、Rocky Linux にマウントして使う手順を説明します。

.. code-block:: console
   :linenos:

   $ sudo dnf install nfs-utils
   $ sudo mkdir -p /mnt/share
   $ sudo mount -t nfs nfs01.example.com:/export/share /mnt/share
   $ df -h /mnt/share

起動時に自動でマウントするには、``/etc/fstab`` に次のように記述します。``_netdev`` は、ネットワークが使えるようになってからマウントすることを表します。

.. code-block:: text
   :linenos:
   :caption: /etc/fstab に追加する行

   nfs01.example.com:/export/share  /mnt/share  nfs  defaults,_netdev,nofail  0 0
