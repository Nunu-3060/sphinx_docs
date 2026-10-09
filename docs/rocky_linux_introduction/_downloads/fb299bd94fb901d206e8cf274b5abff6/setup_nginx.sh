#!/usr/bin/env bash
# ------------------------------------------------------------
# setup_nginx.sh - nginx による Web サーバーを構築するスクリプト
#
# 第 17 章「総合演習: nginx による Web サーバーの構築」の手順
# (HTTPS 化を除く) をまとめて実行します。
#   1. nginx を導入して自動起動を有効にする
#   2. firewalld で HTTP と HTTPS を許可する
#   3. /srv/www/example にコンテンツを配置し、SELinux のラベルを設定する
#   4. examples/nginx/example.conf を /etc/nginx/conf.d/ に配置する
#   5. 設定を検査して nginx を再読み込みする
#
# 使い方:
#   本スクリプトと example.conf を同じディレクトリに置き、次を実行します。
#   sudo bash setup_nginx.sh
# ------------------------------------------------------------
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "root 権限で実行してください" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF_SOURCE="${SCRIPT_DIR}/example.conf"
DOC_ROOT="/srv/www/example"

if [[ ! -f "${CONF_SOURCE}" ]]; then
    echo "${CONF_SOURCE} が見つかりません" >&2
    exit 1
fi

echo "=== 1. nginx を導入します ==="
dnf -y install nginx policycoreutils-python-utils
systemctl enable --now nginx

echo "=== 2. ファイアウォールで HTTP と HTTPS を許可します ==="
firewall-cmd --permanent --add-service=http --add-service=https
firewall-cmd --reload

echo "=== 3. コンテンツを配置します ==="
mkdir -p "${DOC_ROOT}"
cat > "${DOC_ROOT}/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="ja">
<head><meta charset="utf-8"><title>Rocky Linux 入門</title></head>
<body><h1>nginx on Rocky Linux 10</h1></body>
</html>
EOF
# /srv 配下は既定で Web サーバーから読めないラベルのため、ラベルを設定する
semanage fcontext -a -t httpd_sys_content_t "/srv/www(/.*)?" \
    || semanage fcontext -m -t httpd_sys_content_t "/srv/www(/.*)?"
restorecon -Rv /srv/www

echo "=== 4. 設定ファイルを配置します ==="
install -m 644 "${CONF_SOURCE}" /etc/nginx/conf.d/example.conf

echo "=== 5. 設定を検査して再読み込みします ==="
nginx -t
systemctl reload nginx

echo "完了しました。curl -I http://localhost/ で動作を確認してください。"
