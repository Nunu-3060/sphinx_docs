#!/usr/bin/env bash
# ------------------------------------------------------------
# create_users.sh - ユーザーを一括作成するスクリプト
#
# 第 7 章「ユーザーとグループの管理」で使用します。
# CSV ファイルに書かれたユーザーを作成し、指定したグループに追加します。
# 初期パスワードは設定せず、初回ログイン前に管理者が
# 公開鍵を配置するか、passwd コマンドでパスワードを設定する運用を想定します。
#
# CSV の形式 (1 行 1 ユーザー、先頭行は見出し):
#   ユーザー名,補助グループ (複数ある場合は ; で区切る),コメント
#   例:
#     username,groups,comment
#     alice,wheel;developers,Alice Example
#     bob,developers,Bob Example
#
# 使い方:
#   sudo bash create_users.sh users.csv
# ------------------------------------------------------------
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "root 権限で実行してください" >&2
    exit 1
fi

if [[ $# -ne 1 || ! -f "$1" ]]; then
    echo "使い方: sudo bash $0 <CSV ファイル>" >&2
    exit 1
fi

CSV_FILE="$1"

# 先頭行 (見出し) を読み飛ばして 1 行ずつ処理する
tail -n +2 "${CSV_FILE}" | while IFS=, read -r username groups comment; do
    # 空行は読み飛ばす
    [[ -z "${username}" ]] && continue

    # 補助グループが存在しなければ作成する
    IFS=';' read -r -a group_list <<< "${groups}"
    for group in "${group_list[@]}"; do
        if ! getent group "${group}" > /dev/null; then
            groupadd "${group}"
            echo "グループ ${group} を作成しました"
        fi
    done

    # useradd と usermod の -G には、グループを , で区切って渡す
    group_option=()
    if [[ -n "${groups}" ]]; then
        group_option=(-G "${groups//;/,}")
    fi

    if id "${username}" &> /dev/null; then
        echo "ユーザー ${username} は既に存在するため、グループのみ追加します"
        if [[ ${#group_option[@]} -gt 0 ]]; then
            usermod -a "${group_option[@]}" "${username}"
        fi
    else
        useradd -m -c "${comment}" "${group_option[@]}" "${username}"
        echo "ユーザー ${username} を作成しました"
    fi
done

echo "完了しました。各ユーザーのパスワードまたは公開鍵を設定してください。"
