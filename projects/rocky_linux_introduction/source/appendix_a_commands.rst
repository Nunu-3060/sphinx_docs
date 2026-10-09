.. _appendix-commands:

付録 A コマンド早見表
=====================

本書で扱った主なコマンドを、分類ごとにまとめます。詳しい説明は、各項目に示した章を参照してください。

ファイルとテキスト
------------------

詳しくは「:ref:`ch-shell`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``ls -la``、``cd``、``pwd``
     - ファイルの一覧表示、ディレクトリの移動、現在のディレクトリの表示
   * - ``cp -a``、``mv``、``rm -r``、``mkdir -p``
     - コピー、移動、削除、ディレクトリの作成
   * - ``less``、``head``、``tail -f``
     - ファイルの内容の表示
   * - ``grep``、``sed``、``awk``、``sort``、``uniq -c``、``wc -l``
     - テキストの検索と加工
   * - ``chmod``、``chown``
     - パーミッションと所有者の変更
   * - ``tar -czf``、``tar -xzf``
     - アーカイブの作成と展開
   * - ``find <ディレクトリ> -name <名前>``
     - ファイルの検索

パッケージ
----------

詳しくは「:ref:`ch-package`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``dnf search``、``dnf info``
     - パッケージの検索と詳細表示
   * - ``sudo dnf install``、``sudo dnf remove``
     - パッケージの導入と削除
   * - ``sudo dnf upgrade``
     - パッケージの更新
   * - ``dnf updateinfo list --security``
     - 未適用のセキュリティの修正の一覧
   * - ``dnf history``、``sudo dnf history undo <番号>``
     - 操作の履歴と取り消し
   * - ``dnf provides <ファイル>``
     - ファイルを含むパッケージの検索
   * - ``rpm -qa``、``rpm -qf <ファイル>``、``rpm -V <パッケージ>``
     - 導入済みのパッケージの一覧、ファイルの所属の確認、ファイルの検証

ユーザーと権限
--------------

詳しくは「:ref:`ch-user`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``useradd -m``、``usermod -aG``、``userdel -r``
     - ユーザーの作成、グループへの追加、削除
   * - ``passwd``、``chage``
     - パスワードの設定と有効期限の設定
   * - ``id``
     - UID と所属するグループの表示
   * - ``visudo``
     - sudoers の安全な編集
   * - ``faillock --user <ユーザー> --reset``
     - アカウントのロックの解除

プロセスとサービス
------------------

詳しくは「:ref:`ch-process-service`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``ps aux``、``pgrep -a``、``top``
     - プロセスの確認
   * - ``kill``、``pkill``
     - プロセスへのシグナルの送信
   * - ``systemctl status|start|stop|restart|reload``
     - サービスの状態確認と操作
   * - ``systemctl enable --now``、``systemctl disable``
     - 自動起動の設定
   * - ``systemctl daemon-reload``
     - ユニットファイルの再読み込み
   * - ``systemctl list-timers``
     - タイマーの一覧
   * - ``systemctl --failed``
     - 失敗したユニットの一覧

起動とカーネル
--------------

詳しくは「:ref:`ch-boot-kernel`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``systemctl get-default``、``systemctl set-default``
     - 既定のターゲットの確認と変更
   * - ``grubby --default-kernel``、``grubby --set-default``
     - 既定のカーネルの確認と変更
   * - ``grubby --update-kernel=ALL --args=<パラメーター>``
     - カーネルパラメーターの追加
   * - ``uname -r``、``rpm -q kernel``
     - 動作中のカーネルと、導入済みのカーネルの確認
   * - ``systemd-analyze blame``
     - 起動に時間のかかったサービスの確認

ストレージ
----------

詳しくは「:ref:`ch-storage`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``lsblk``、``blkid``、``df -h``、``du -sh``
     - ディスクと使用量の確認
   * - ``pvcreate``、``vgcreate``、``lvcreate``
     - LVM の領域の作成
   * - ``lvextend -r -L +<サイズ>``
     - 論理ボリュームとファイルシステムの拡張
   * - ``mkfs.xfs``
     - XFS ファイルシステムの作成
   * - ``mount -a``
     - ``/etc/fstab`` の内容でのマウント（設定の確認）
   * - ``rsync -aAX``
     - 属性を保ったディレクトリの同期

ネットワーク
------------

詳しくは「:ref:`ch-network`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``nmcli device status``、``nmcli connection show``
     - デバイスと接続の確認
   * - ``nmcli connection modify``、``nmcli connection up``
     - 接続の設定の変更と反映
   * - ``ip -br address``、``ip route``
     - IP アドレスと経路の確認
   * - ``ss -tlnp``
     - 待ち受けているポートの確認
   * - ``ping``、``tracepath``、``curl -I``
     - 疎通の確認
   * - ``getent hosts``、``dig``
     - 名前解決の確認
   * - ``scp``、``sftp``、``rsync -avz``
     - ファイルの転送

セキュリティ
------------

詳しくは「:ref:`ch-security`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``firewall-cmd --list-all``
     - ファイアウォールの設定の確認
   * - ``firewall-cmd --permanent --add-service=<サービス>``、``firewall-cmd --reload``
     - サービスの許可と反映
   * - ``getenforce``、``setenforce``
     - SELinux の動作モードの確認と一時的な変更
   * - ``ls -Z``、``ps -eZ``
     - SELinux のコンテキストの確認
   * - ``semanage fcontext -a``、``restorecon -Rv``
     - SELinux のラベルの登録と適用
   * - ``setsebool -P``
     - SELinux のブール値の変更
   * - ``ausearch -m AVC -ts recent``、``sealert -a``
     - SELinux による拒否の調査
   * - ``update-crypto-policies --show|--set``
     - 暗号化ポリシーの確認と変更

ログと監視
----------

詳しくは「:ref:`ch-log-monitoring`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``journalctl -u <サービス>``、``journalctl -f``、``journalctl -b``、``journalctl -p err``
     - ログの確認
   * - ``free -h``、``uptime``、``vmstat``、``sar``
     - リソースの確認
   * - ``tuned-adm active``、``tuned-adm profile``
     - tuned のプロファイルの確認と変更
   * - ``sysctl``、``sysctl --system``
     - カーネルパラメーターの確認と反映
   * - ``sos report``
     - 障害調査用の情報の収集

GPU
---

詳しくは「:ref:`ch-gpu`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``lspci -nnk``
     - GPU と、使用中のカーネルモジュールの確認
   * - ``mokutil --sb-state``
     - Secure Boot の状態の確認
   * - ``mokutil --import /var/lib/dkms/mok.pub``
     - DKMS の署名鍵の登録の予約
   * - ``sudo dnf install nvidia-open``
     - NVIDIA のドライバーの導入
   * - ``nvidia-smi``、``nvidia-smi -L``
     - GPU の状態と一覧の表示
   * - ``dkms status``
     - DKMS で管理しているカーネルモジュールのビルドの状態
   * - ``dnf versionlock add '*nvidia*<ブランチ>*'``
     - ドライバーのブランチの固定
   * - ``nvidia-ctk cdi list``
     - コンテナに渡せる GPU（CDI デバイス）の一覧
   * - ``podman run --device nvidia.com/gpu=all``
     - GPU を使うコンテナの起動

コンテナ
--------

詳しくは「:ref:`ch-container`」を参照してください。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - コマンド
     - 用途
   * - ``podman pull``、``podman images``
     - イメージの取得と一覧
   * - ``podman run -d --name <名前> -p <ホスト側>:<コンテナ側>``
     - コンテナの起動
   * - ``podman ps -a``、``podman logs``、``podman exec -it``
     - コンテナの確認と操作
   * - ``podman stop``、``podman rm``、``podman rmi``
     - コンテナとイメージの停止・削除
   * - ``systemctl --user daemon-reload``、``systemctl --user start``
     - Quadlet で定義したコンテナの起動
