# ============================================================
# undo_demo.ps1
#   変更の取り消し（restore / revert / reset / reflog）を体験するスクリプト
#   （undo_demo.sh の PowerShell 版）
#
# 使い方（PowerShell で実行します）:
#   powershell -ExecutionPolicy Bypass -File .\undo_demo.ps1
#
# カレントディレクトリに practice-undo というディレクトリを作成します。
# ============================================================
$ErrorActionPreference = 'Stop'

# git コマンドを実行し、失敗したら処理を中断する
function Invoke-Git {
    git @args
    if ($LASTEXITCODE -ne 0) { throw "git $args が失敗しました（終了コード $LASTEXITCODE）。" }
}

# テキストファイルの末尾に行を追加する（BOM なしの UTF-8、改行コード LF）
function Add-TextFile([string]$Path, [string[]]$Lines) {
    $text = ($Lines -join "`n") + "`n"
    [System.IO.File]::AppendAllText((Join-Path $PWD.Path $Path), $text, (New-Object System.Text.UTF8Encoding $false))
}

function Show-Step([string]$Title) {
    Write-Host ""
    Write-Host "===== $Title ====="
}

$WorkDir = 'practice-undo'
if (Test-Path $WorkDir) {
    Write-Host "$WorkDir が既に存在します。削除してから再実行してください。"
    exit 1
}

$oldPager = $env:GIT_PAGER
$env:GIT_PAGER = 'cat'
New-Item -ItemType Directory $WorkDir | Out-Null
Push-Location $WorkDir
try {
    Show-Step '準備: コミットを 3 つ作成する'
    Invoke-Git init -b main
    Invoke-Git config user.name 'Taro Yamada'
    Invoke-Git config user.email 'taro@example.com'
    foreach ($i in 1..3) {
        Add-TextFile 'notes.txt' @("line $i")
        Invoke-Git add notes.txt
        Invoke-Git commit -m "Add line $i"
    }
    Invoke-Git log --oneline

    Show-Step '1. git restore: ワーキングツリーの変更を破棄する'
    Add-TextFile 'notes.txt' @('unwanted change')
    Invoke-Git status --short
    Invoke-Git restore notes.txt
    Invoke-Git status --short
    Write-Host '（何も表示されなければ変更は破棄されています）'

    Show-Step '2. git restore --staged: ステージを取り消す'
    Add-TextFile 'notes.txt' @('staged change')
    Invoke-Git add notes.txt
    Invoke-Git status --short
    Invoke-Git restore --staged notes.txt
    Invoke-Git status --short
    Invoke-Git restore notes.txt   # 次の手順のためにワーキングツリーも元に戻す

    Show-Step '3. git revert: 直前のコミットを打ち消すコミットを作成する'
    Invoke-Git revert --no-edit HEAD
    Invoke-Git log --oneline
    Get-Content notes.txt

    Show-Step '4. git reset --hard: revert のコミットを履歴から取り除く'
    Invoke-Git reset --hard HEAD~1
    Invoke-Git log --oneline

    Show-Step '5. git reflog: HEAD の移動履歴を確認する'
    Invoke-Git reflog

    Write-Host ""
    Write-Host '完了しました。'
}
finally {
    Pop-Location
    $env:GIT_PAGER = $oldPager
}
