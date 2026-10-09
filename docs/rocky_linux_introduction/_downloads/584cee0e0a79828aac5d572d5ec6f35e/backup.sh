#!/usr/bin/env bash
# ------------------------------------------------------------
# backup.sh - 設定ファイルと Web コンテンツを日次でバックアップするスクリプト
#
# 第 10 章「ストレージ管理」で使用します。
#   1. /etc と /srv/www を tar.gz 形式で 1 つのファイルにまとめる
#   2. 保存期間 (既定値: 7 日) を過ぎた古いバックアップを削除する
#   3. (任意) rsync で別のサーバーへ転送する
#
# 使い方:
#   sudo bash backup.sh
#   systemd タイマーから定期実行する場合は、examples/systemd/backup.service と
#   examples/systemd/backup.timer を参照してください。
#
# 環境変数で動作を変更できます。
#   BACKUP_DIR      保存先ディレクトリ   (既定値: /var/backup)
#   RETENTION_DAYS  保存日数             (既定値: 7)
#   REMOTE_DEST     rsync の転送先       (例: backup@backup01:/data/web01/)
#                   未設定の場合は転送しません。
# ------------------------------------------------------------
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/var/backup}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
REMOTE_DEST="${REMOTE_DEST:-}"

# バックアップ対象 (存在しないものは除外する)
TARGETS=()
for path in /etc /srv/www; do
    [[ -e "${path}" ]] && TARGETS+=("${path}")
done

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="${BACKUP_DIR}/$(hostname -s)-${TIMESTAMP}.tar.gz"

mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

echo "バックアップを作成します: ${ARCHIVE}"
# --selinux と --xattrs で SELinux のラベルと拡張属性も保存する
tar --selinux --xattrs --acls -czpf "${ARCHIVE}" "${TARGETS[@]}"

echo "${RETENTION_DAYS} 日より古いバックアップを削除します"
find "${BACKUP_DIR}" -maxdepth 1 -name '*.tar.gz' -mtime "+${RETENTION_DAYS}" \
    -print -delete

if [[ -n "${REMOTE_DEST}" ]]; then
    echo "${REMOTE_DEST} へ転送します"
    rsync -av "${BACKUP_DIR}/" "${REMOTE_DEST}"
fi

echo "完了しました"
