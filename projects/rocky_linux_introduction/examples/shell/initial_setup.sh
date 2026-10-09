#!/usr/bin/env bash
# ------------------------------------------------------------
# initial_setup.sh - Rocky Linux 10 の初期設定をまとめて行うスクリプト
#
# 第 4 章「初期設定」で説明した手順を順番に実行します。
#   1. システムを最新の状態に更新する
#   2. ホスト名を設定する
#   3. 日本語ロケールとタイムゾーンを設定する
#   4. 時刻同期 (chronyd) を有効にする
#
# 使い方:
#   sudo bash initial_setup.sh <ホスト名>
#   例: sudo bash initial_setup.sh web01.example.com
#
# 実行後は、カーネルが更新されている場合に備えて再起動してください。
# ------------------------------------------------------------
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "root 権限で実行してください (例: sudo bash $0 <ホスト名>)" >&2
    exit 1
fi

if [[ $# -ne 1 ]]; then
    echo "使い方: sudo bash $0 <ホスト名>" >&2
    exit 1
fi

NEW_HOSTNAME="$1"

echo "=== 1. システムを更新します ==="
dnf -y upgrade --refresh

echo "=== 2. ホスト名を ${NEW_HOSTNAME} に設定します ==="
hostnamectl set-hostname "${NEW_HOSTNAME}"

echo "=== 3. 日本語ロケールとタイムゾーンを設定します ==="
dnf -y install langpacks-ja
localectl set-locale LANG=ja_JP.UTF-8
timedatectl set-timezone Asia/Tokyo

echo "=== 4. 時刻同期を有効にします ==="
dnf -y install chrony
systemctl enable --now chronyd

echo "=== 設定結果 ==="
hostnamectl status
localectl status
timedatectl status

echo "完了しました。必要に応じて再起動してください (sudo systemctl reboot)。"
