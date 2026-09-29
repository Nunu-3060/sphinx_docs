"""各 Sphinx プロジェクトの build_html.bat を同じ内容に一括で書き換える。

カレントディレクトリの ``projects/*/source/conf.py`` を持つフォルダーを
Sphinx プロジェクトとみなし、そのフォルダーに build_html.bat を出力する。
バッチファイルは文字化けを避けるため ASCII のみ・CRLF 改行で出力する。

使い方::

    python unify_build_html.py            # 全プロジェクトを書き換える
    python unify_build_html.py --check    # 書き換えずに差分のあるものを表示する
    python unify_build_html.py color_introduction unity_introduction
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sphinx_projects import BAT_NAME, add_projects_argument, find_projects

# 環境変数 SPHINX_NO_OPEN が定義されているときはブラウザを開かない
# （run_build_html.py で一括ビルドするときに使う）。
BAT_TEMPLATE = """\
@echo off
rem Build the HTML documents and open index.html in the default browser.
setlocal
cd /d "%~dp0"

set SOURCEDIR=source
set BUILDDIR=build

rem Remove the previous build output.
if exist "%BUILDDIR%" (
    echo Removing the previous build output...
    rmdir /s /q "%BUILDDIR%"
)

rem Build the HTML documents.
python -m sphinx -b html -d %BUILDDIR%\\doctrees %SOURCEDIR% %BUILDDIR%\\html
if errorlevel 1 (
    echo.
    echo Build failed.
    endlocal
    exit /b 1
)

echo.
echo Build succeeded. The HTML pages are in %BUILDDIR%\\html.

rem Open index.html in the default browser.
rem Set SPHINX_NO_OPEN to skip this step.
if not defined SPHINX_NO_OPEN (
    start "" "%~dp0%BUILDDIR%\\html\\index.html"
)

endlocal
"""


def bat_bytes() -> bytes:
    """build_html.bat に書き込む内容を CRLF 改行・ASCII で返す。"""
    return BAT_TEMPLATE.replace("\n", "\r\n").encode("ascii")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_projects_argument(parser)
    parser.add_argument(
        "--check",
        action="store_true",
        help="書き換えずに、内容が異なる build_html.bat を表示する",
    )
    args = parser.parse_args()

    content = bat_bytes()
    differs: list[Path] = []
    for project in find_projects(Path.cwd(), args.projects):
        bat_path = project / BAT_NAME
        if bat_path.exists() and bat_path.read_bytes() == content:
            print(f"変更なし: {bat_path}")
            continue
        differs.append(bat_path)
        if args.check:
            print(f"差分あり: {bat_path}")
        else:
            bat_path.write_bytes(content)
            print(f"更新    : {bat_path}")

    print(f"{len(differs)} 件の build_html.bat が"
          f"{'統一されていません' if args.check else '更新されました'}。")
    return 1 if args.check and differs else 0


if __name__ == "__main__":
    sys.exit(main())
