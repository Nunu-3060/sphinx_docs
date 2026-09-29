#!/usr/bin/env bash
# ============================================================
# basic_workflow.sh
#   Git の基本操作（init / add / commit / log / diff）を体験するスクリプト
#
# 使い方（Git Bash、macOS や Linux の端末で実行します）:
#   bash basic_workflow.sh
#
# カレントディレクトリに practice-basic というディレクトリを作成し、
# その中で操作します。既に同名のディレクトリがある場合は中断します。
# ============================================================
set -eu
export GIT_PAGER=cat   # 出力をページャーで止めずに表示する

WORK_DIR="practice-basic"
if [ -e "$WORK_DIR" ]; then
    echo "$WORK_DIR が既に存在します。削除してから再実行してください。"
    exit 1
fi

step() { echo; echo "===== $1 ====="; }

step "1. リポジトリを作成する"
mkdir "$WORK_DIR"
cd "$WORK_DIR"
git init -b main
# このリポジトリだけで有効なユーザー設定（グローバル設定が未設定でも動くようにする）
git config user.name  "Taro Yamada"
git config user.email "taro@example.com"

step "2. ファイルを作成して状態を確認する"
cat > hello.py <<'PY'
def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Git"))
PY
git status

step "3. ステージングエリアに追加する"
git add hello.py
git status --short

step "4. コミットする"
git commit -m "Add greeting script"

step "5. ファイルを変更して差分を確認する"
sed -i.bak 's/Hello/Hi/' hello.py && rm hello.py.bak
git diff

step "6. 変更をステージしてからコミットする"
git add hello.py
git diff --staged
git commit -m "Change greeting from Hello to Hi"

step "7. 履歴を確認する"
git log --oneline

echo
echo "完了しました。$WORK_DIR ディレクトリの中で自由に操作を試してください。"
