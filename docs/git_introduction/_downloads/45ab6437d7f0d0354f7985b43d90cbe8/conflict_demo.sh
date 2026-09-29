#!/usr/bin/env bash
# ============================================================
# conflict_demo.sh
#   マージ時のコンフリクト（競合）を発生させ、解消するまでを体験するスクリプト
#
# 使い方:
#   bash conflict_demo.sh
#
# カレントディレクトリに practice-conflict というディレクトリを作成します。
# ============================================================
set -eu
export GIT_PAGER=cat

WORK_DIR="practice-conflict"
if [ -e "$WORK_DIR" ]; then
    echo "$WORK_DIR が既に存在します。削除してから再実行してください。"
    exit 1
fi

step() { echo; echo "===== $1 ====="; }

step "準備: 共通のファイルをコミットする"
mkdir "$WORK_DIR"
cd "$WORK_DIR"
git init -b main
git config user.name  "Taro Yamada"
git config user.email "taro@example.com"
echo 'MESSAGE = "Hello"' > greeting.py
git add greeting.py
git commit -m "Add greeting message"

step "1. feature ブランチで同じ行を変更する"
git switch -c feature
echo 'MESSAGE = "Hi"' > greeting.py
git commit -am "Change message to Hi"

step "2. main ブランチでも同じ行を変更する"
git switch main
echo 'MESSAGE = "Good morning"' > greeting.py
git commit -am "Change message to Good morning"

step "3. マージするとコンフリクトが発生する"
# コンフリクト時は git merge が失敗（終了コード 1）するため、|| true で処理を続ける
git merge feature || true
git status --short
echo "--- greeting.py の内容 ---"
cat greeting.py

step "4. ファイルを編集してコンフリクトを解消する"
# 本来はエディターで編集します。ここでは解消後の内容を直接書き込みます。
echo 'MESSAGE = "Hi, good morning"' > greeting.py
cat greeting.py

step "5. 解消したファイルをステージしてマージを完了する"
git add greeting.py
git commit --no-edit
git log --oneline --graph --all

echo
echo "完了しました。"
