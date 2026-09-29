# ============================================================
# conflict_demo.ps1
#   マージ時のコンフリクト（競合）を発生させ、解消するまでを体験するスクリプト
#   （conflict_demo.sh の PowerShell 版）
#
# 使い方（PowerShell で実行します）:
#   powershell -ExecutionPolicy Bypass -File .\conflict_demo.ps1
#
# カレントディレクトリに practice-conflict というディレクトリを作成します。
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

$WorkDir = 'practice-conflict'
if (Test-Path $WorkDir) {
    Write-Host "$WorkDir が既に存在します。削除してから再実行してください。"
    exit 1
}

$oldPager = $env:GIT_PAGER
$env:GIT_PAGER = 'cat'
New-Item -ItemType Directory $WorkDir | Out-Null
Push-Location $WorkDir
try {
    Show-Step '準備: 共通のファイルをコミットする'
    Invoke-Git init -b main
    Invoke-Git config user.name 'Taro Yamada'
    Invoke-Git config user.email 'taro@example.com'
    Write-TextFile 'greeting.py' @('MESSAGE = "Hello"')
    Invoke-Git add greeting.py
    Invoke-Git commit -m 'Add greeting message'

    Show-Step '1. feature ブランチで同じ行を変更する'
    Invoke-Git switch -c feature
    Write-TextFile 'greeting.py' @('MESSAGE = "Hi"')
    Invoke-Git commit -am 'Change message to Hi'

    Show-Step '2. main ブランチでも同じ行を変更する'
    Invoke-Git switch main
    Write-TextFile 'greeting.py' @('MESSAGE = "Good morning"')
    Invoke-Git commit -am 'Change message to Good morning'

    Show-Step '3. マージするとコンフリクトが発生する'
    # コンフリクト時は git merge が失敗（終了コード 1）するため、Invoke-Git を使わずに実行する
    git merge feature
    if ($LASTEXITCODE -ne 1) { throw '想定したコンフリクトが発生しませんでした。' }
    Invoke-Git status --short
    Write-Host '--- greeting.py の内容 ---'
    Get-Content greeting.py

    Show-Step '4. ファイルを編集してコンフリクトを解消する'
    # 本来はエディターで編集します。ここでは解消後の内容を直接書き込みます。
    Write-TextFile 'greeting.py' @('MESSAGE = "Hi, good morning"')
    Get-Content greeting.py

    Show-Step '5. 解消したファイルをステージしてマージを完了する'
    Invoke-Git add greeting.py
    Invoke-Git commit --no-edit
    Invoke-Git log --oneline --graph --all

    Write-Host ""
    Write-Host '完了しました。'
}
finally {
    Pop-Location
    $env:GIT_PAGER = $oldPager
}
