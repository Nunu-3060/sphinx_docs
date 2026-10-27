@echo off
rem Check the sample code and the figure scripts with flake8 and mypy.
rem Both use the settings in examples\setup.cfg.
setlocal
cd /d "%~dp0"

set RESULT=0

echo [flake8] examples
python -m flake8 --config examples\setup.cfg examples
if errorlevel 1 set RESULT=1

echo [flake8] source\_scripts
python -m flake8 --config examples\setup.cfg source\_scripts
if errorlevel 1 set RESULT=1

echo [mypy] examples
pushd examples
python -m mypy --config-file setup.cfg .
if errorlevel 1 set RESULT=1
popd

echo [mypy] source\_scripts
pushd source\_scripts
python -m mypy --config-file ..\..\examples\setup.cfg .
if errorlevel 1 set RESULT=1
popd

if %RESULT%==0 (
    echo.
    echo All checks passed.
) else (
    echo.
    echo Some checks failed.
)

endlocal & exit /b %RESULT%
