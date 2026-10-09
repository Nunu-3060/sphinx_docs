# ------------------------------------------------------------
# minimal.ks - 最小構成で Rocky Linux 10 をインストールする Kickstart ファイル
#
# 第 3 章「インストール」で使用します。
# インストーラーの起動時にカーネルパラメーターとして
#   inst.ks=http://<Web サーバー>/minimal.ks
# を指定すると、このファイルの内容に従って自動でインストールされます。
#
# 使用前に必ず変更する箇所:
#   - user 行の --password: 次のコマンドで作成したハッシュ値に置き換える
#       openssl passwd -6
#   - sshkey 行: 自分の公開鍵に置き換える
#
# 注意: clearpart --all はディスクの内容をすべて消去します。
# ------------------------------------------------------------

# インストール元 (インストールメディア)
cdrom

# テキストモードで実行し、完了後に再起動する
text
reboot

# 言語、キーボード、タイムゾーン
lang ja_JP.UTF-8
keyboard --vckeymap=jp --xlayouts='jp'
timezone Asia/Tokyo --utc

# ネットワーク (DHCP) とホスト名
network --bootproto=dhcp --device=link --activate --hostname=rocky01.example.com

# root アカウントはロックし、管理者ユーザーを作成する
rootpw --lock
user --name=admin --groups=wheel --password=REPLACE_WITH_HASH --iscrypted
sshkey --username=admin "ssh-ed25519 AAAA...REPLACE_WITH_YOUR_PUBLIC_KEY"

# セキュリティ
selinux --enforcing
firewall --enabled --service=ssh

# ディスク (全消去して自動パーティション、LVM を使用)
zerombr
clearpart --all --initlabel
autopart --type=lvm
bootloader

# 導入するパッケージ (最小構成)
%packages
@^minimal-environment
chrony
%end
