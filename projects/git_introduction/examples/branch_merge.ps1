# ============================================================
# branch_merge.ps1
#   ブランチの作成とマージ（fast-forward マージと 3-way マージ）を体験するスクリプト
#   （branch_merge.sh の PowerShell 版）
#
# 使い方（PowerShell で実行します）:
#   powershell -ExecutionPolicy Bypass -File .\branch_merge.ps1
#
# カレントディレクトリに practice-branch というディレクトリを作成します。
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

# テキストファイルの末尾に行を追加する
function Add-TextFile([string]$Path, [string[]]$Lines) {
    $text = ($Lines -join "`n") + "`n"
    [System.IO.File]::AppendAllText((Join-Path $PWD.Path $Path), $text, (New-Object System.Text.UTF8Encoding $false))
}

function Show-Step([string]$Title) {
    Write-Host ""
    Write-Host "===== $Title ====="
}

$WorkDir = 'practice-branch'
if (Test-Path $WorkDir) {
    Write-Host "$WorkDir が既に存在します。削除してから再実行してください。"
    exit 1
}

$oldPager = $env:GIT_PAGER
$env:GIT_PAGER = 'cat'
New-Item -ItemType Directory $WorkDir | Out-Null
Push-Location $WorkDir
try {
    Show-Step '準備: 最初のコミットを作成する'
    Invoke-Git init -b main
    Invoke-Git config user.name 'Taro Yamada'
    Invoke-Git config user.email 'taro@example.com'
    Write-TextFile 'README.md' @('# Calculator')
    Invoke-Git add README.md
    Invoke-Git commit -m 'Add README'

    Show-Step '1. feature/add ブランチを作成して切り替える'
    Invoke-Git switch -c feature/add
    Write-TextFile 'calc.py' @(
        'def add(a, b):'
        '    return a + b'
    )
    Invoke-Git add calc.py
    Invoke-Git commit -m 'Add add function'

    Show-Step '2. main に戻って fast-forward マージする'
    Invoke-Git switch main
    Invoke-Git merge feature/add
    Invoke-Git log --oneline --graph --all

    Show-Step '3. feature/sub ブランチで作業する'
    Invoke-Git switch -c feature/sub
    Add-TextFile 'calc.py' @(
        ''
        ''
        'def sub(a, b):'
        '    return a - b'
    )
    Invoke-Git commit -am 'Add sub function'

    Show-Step '4. その間に main でも別の変更をコミットする'
    Invoke-Git switch main
    Add-TextFile 'README.md' @('Simple calculator module.')
    Invoke-Git commit -am 'Update README'

    Show-Step '5. 3-way マージする（マージコミットが作成される）'
    Invoke-Git merge --no-edit feature/sub
    Invoke-Git log --oneline --graph --all

    Show-Step '6. マージ済みのブランチを削除する'
    Invoke-Git branch -d feature/add feature/sub
    Invoke-Git branch

    Write-Host ""
    Write-Host '完了しました。'
}
finally {
    Pop-Location
    $env:GIT_PAGER = $oldPager
}
