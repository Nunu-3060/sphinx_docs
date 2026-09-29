@echo off
rem Build the Sphinx documentation as HTML and open it in the default browser.

setlocal
cd /d "%~dp0"

rem Remove the previous build results.
if exist build rmdir /s /q build

rem Build HTML into build\html.
python -m sphinx -b html source build\html
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

rem Open the top page in the default browser.
start "" "%~dp0build\html\index.html"

endlocal
