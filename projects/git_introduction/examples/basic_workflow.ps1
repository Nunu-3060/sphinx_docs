# ============================================================
# basic_workflow.ps1
#   Git の基本操作（init / add / commit / log / diff）を体験するスクリプト
#   （basic_workflow.sh の PowerShell 版）
#
# 使い方（PowerShell で実行します）:
#   powershell -ExecutionPolicy Bypass -File .\basic_workflow.ps1
#
# カレントディレクトリに practice-basic というディレクトリを作成し、
# その中で操作します。既に同名のディレクトリがある場合は中断します。
# ============================================================
$ErrorActionPreference = 'Stop'

# git コマンドを実行し、失敗したら処理を中断する
function Invoke-Git {
    git @args
    if ($LASTEXITCODE -ne 0) { throw "git $args が失敗しました（終了コード $LASTEXITCODE）。" }
}

# テキストファイルを BOM なしの UTF-8、改行コード LF で書き込む
function Write-TextFile([string]$Path, [string[]]$Lines) {
    $text = ($Lines -join "`n") + "`n"
    [System.IO.File]::WriteAllText((Join-Path $PWD.Path $Path), $text, (New-Object System.Text.UTF8Encoding $false))
}

function Show-Step([string]$Title) {
    Write-Host ""
    Write-Host "===== $Title ====="
}

$WorkDir = 'practice-basic'
if (Test-Path $WorkDir) {
    Write-Host "$WorkDir が既に存在します。削除してから再実行してください。"
    exit 1
}

$oldPager = $env:GIT_PAGER
$env:GIT_PAGER = 'cat'   # 出力をページャーで止めずに表示する
New-Item -ItemType Directory $WorkDir | Out-Null
Push-Location $WorkDir
try {
    Show-Step '1. リポジトリを作成する'
    Invoke-Git init -b main
    # このリポジトリだけで有効なユーザー設定（グローバル設定が未設定でも動くようにする）
    Invoke-Git config user.name 'Taro Yamada'
    Invoke-Git config user.email 'taro@example.com'

    Show-Step '2. ファイルを作成して状態を確認する'
    Write-TextFile 'hello.py' @(
        'def greet(name):'
        '    return f"Hello, {name}!"'
        ''
        ''
        'if __name__ == "__main__":'
        '    print(greet("Git"))'
    )
    Invoke-Git status

    Show-Step '3. ステージングエリアに追加する'
    Invoke-Git add hello.py
    Invoke-Git status --short

    Show-Step '4. コミットする'
    Invoke-Git commit -m 'Add greeting script'

    Show-Step '5. ファイルを変更して差分を確認する'
    $lines = [System.IO.File]::ReadAllLines((Join-Path $PWD.Path 'hello.py'))
    Write-TextFile 'hello.py' ($lines -replace 'Hello', 'Hi')
    Invoke-Git diff

    Show-Step '6. 変更をステージしてからコミットする'
    Invoke-Git add hello.py
    Invoke-Git diff --staged
    Invoke-Git commit -m 'Change greeting from Hello to Hi'

    Show-Step '7. 履歴を確認する'
    Invoke-Git log --oneline

    Write-Host ""
    Write-Host "完了しました。$WorkDir ディレクトリの中で自由に操作を試してください。"
}
finally {
    Pop-Location
    $env:GIT_PAGER = $oldPager
}
