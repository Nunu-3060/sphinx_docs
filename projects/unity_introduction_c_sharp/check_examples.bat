@echo off
rem Check the sample code in the examples folder.
rem   1. Coding conventions in .editorconfig (dotnet format)
rem   2. Compilation together with the UnityEngine stubs (dotnet build)
rem   3. Output of the Part 1 samples (dotnet run)
setlocal
cd /d "%~dp0"

rem Use the user-local .NET SDK if it exists; otherwise use dotnet on PATH.
set "DOTNET=dotnet"
if exist "%LOCALAPPDATA%\Microsoft\dotnet\dotnet.exe" set "DOTNET=%LOCALAPPDATA%\Microsoft\dotnet\dotnet.exe"

set "PROJECT=tools\UnityCheck\UnityCheck.csproj"

echo [1/3] dotnet format
"%DOTNET%" format "%PROJECT%" --verify-no-changes
if errorlevel 1 (
    echo Coding convention violations were found.
    exit /b 1
)

echo [2/3] dotnet build
"%DOTNET%" build "%PROJECT%" -nologo -v q
if errorlevel 1 (
    echo Compilation failed.
    exit /b 1
)

echo [3/3] dotnet run
"%DOTNET%" run --project "%PROJECT%" --no-build
endlocal
