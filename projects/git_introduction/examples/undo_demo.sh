#!/usr/bin/env bash
# ============================================================
# undo_demo.sh
#   変更の取り消し（restore / revert / reset / reflog）を体験するスクリプト
#
# 使い方:
#   bash undo_demo.sh
#
# カレントディレクトリに practice-undo というディレクトリを作成します。
# ============================================================
set -eu
export GIT_PAGER=cat

WORK_DIR="practice-undo"
if [ -e "$WORK_DIR" ]; then
    echo "$WORK_DIR が既に存在します。削除してから再実行してください。"
    exit 1
fi

step() { echo; echo "===== $1 ====="; }

step "準備: コミットを 3 つ作成する"
mkdir "$WORK_DIR"
cd "$WORK_DIR"
git init -b main
git config user.name  "Taro Yamada"
git config user.email "taro@example.com"
for i in 1 2 3; do
    echo "line $i" >> notes.txt
    git add notes.txt
    git commit -m "Add line $i"
done
git log --oneline

step "1. git restore: ワーキングツリーの変更を破棄する"
echo "unwanted change" >> notes.txt
git status --short
git restore notes.txt
git status --short
echo "（何も表示されなければ変更は破棄されています）"

step "2. git restore --staged: ステージを取り消す"
echo "staged change" >> notes.txt
git add notes.txt
git status --short
git restore --staged notes.txt
git status --short
git restore notes.txt   # 次の手順のためにワーキングツリーも元に戻す

step "3. git revert: 直前のコミットを打ち消すコミットを作成する"
git revert --no-edit HEAD
git log --oneline
cat notes.txt

step "4. git reset --hard: revert のコミットを履歴から取り除く"
git reset --hard HEAD~1
git log --oneline

step "5. git reflog: HEAD の移動履歴を確認する"
git reflog

echo
echo "完了しました。"
