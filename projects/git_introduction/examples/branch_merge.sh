#!/usr/bin/env bash
# ============================================================
# branch_merge.sh
#   ブランチの作成とマージ（fast-forward マージと 3-way マージ）を体験するスクリプト
#
# 使い方:
#   bash branch_merge.sh
#
# カレントディレクトリに practice-branch というディレクトリを作成します。
# ============================================================
set -eu
export GIT_PAGER=cat

WORK_DIR="practice-branch"
if [ -e "$WORK_DIR" ]; then
    echo "$WORK_DIR が既に存在します。削除してから再実行してください。"
    exit 1
fi

step() { echo; echo "===== $1 ====="; }

step "準備: 最初のコミットを作成する"
mkdir "$WORK_DIR"
cd "$WORK_DIR"
git init -b main
git config user.name  "Taro Yamada"
git config user.email "taro@example.com"
echo "# Calculator" > README.md
git add README.md
git commit -m "Add README"

step "1. feature/add ブランチを作成して切り替える"
git switch -c feature/add
cat > calc.py <<'PY'
def add(a, b):
    return a + b
PY
git add calc.py
git commit -m "Add add function"

step "2. main に戻って fast-forward マージする"
git switch main
git merge feature/add
git log --oneline --graph --all

step "3. feature/sub ブランチで作業する"
git switch -c feature/sub
cat >> calc.py <<'PY'


def sub(a, b):
    return a - b
PY
git commit -am "Add sub function"

step "4. その間に main でも別の変更をコミットする"
git switch main
echo "Simple calculator module." >> README.md
git commit -am "Update README"

step "5. 3-way マージする（マージコミットが作成される）"
git merge --no-edit feature/sub
git log --oneline --graph --all

step "6. マージ済みのブランチを削除する"
git branch -d feature/add feature/sub
git branch

echo
echo "完了しました。"
