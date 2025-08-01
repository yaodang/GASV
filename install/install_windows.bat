@echo off
setlocal enabledelayedexpansion

set "CONDA_ENV=gasv"
set "CONDA_PATH=D:\software\conda"

if not exist "%CONDA_PATH%\Scripts\conda.exe" (
    echo Error: can't find conda，please modify CONDA_PATH.
    pause
    exit /b 1
)

echo Activate the conda environment %CONDA_ENV%...
call "%CONDA_PATH%\Scripts\activate.bat" %CONDA_ENV%

if "!CONDA_DEFAULT_ENV!" neq "%CONDA_ENV%" (
    echo Error：activate conda environment failed，please check if the environment name is correct。
    pause
    exit /b 1
)


echo ============= Start Install =============

set "SCRIPT_PATH=%~dp0"
if "%SCRIPT_PATH:~-1%"=="\" set "SCRIPT_PATH=%SCRIPT_PATH:~0,-1%"
set "PARENT_DIR=%SCRIPT_PATH%"
:loop
if not "%PARENT_DIR:~-1%"=="\" (
    set "PARENT_DIR=%PARENT_DIR:~0,-1%"
    goto loop
)
set "PARENT_DIR=%PARENT_DIR:~0,-1%"

rem echo %PARENT_DIR%

rem pyinstaller -n GASVGUI -i %PARENT_DIR%\source\GUI\icons\swallow.png %PARENT_DIR%\source\GASV_GUI.py
rem copy "%PARENT_DIR%\source\directory.ini" "dist\GASVGUI\"

pyinstaller -n GASVR %PARENT_DIR%\source\run.py

echo Install over.

pause
endlocal
