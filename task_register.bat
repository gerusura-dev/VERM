@echo off
REM ============================
REM この bat のあるディレクトリ
REM ============================
set BASE_DIR=%~dp0
cd /d %BASE_DIR%

REM ============================
REM 仮想環境の Python を自動検出
REM ============================
set PYTHON_EXE=%BASE_DIR%\.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] 仮想環境の Python が見つかりません
    echo setup_env.bat を先に実行してください
    pause
    exit /b 1
)

REM ============================
REM 設定
REM ============================
set TASK_NAME=VRCEventAutoRegister
set SCRIPT=%BASE_DIR%\main.py

REM ============================
REM タスク登録
REM ============================
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "\"%PYTHON_EXE%\" \"%SCRIPT%\"" ^
  /sc DAILY ^
  /st 09:00 ^
  /ru "%USERNAME%" ^
  /rl HIGHEST ^
  /f

if %ERRORLEVEL% neq 0 (
    echo [ERROR] タスクの登録に失敗しました
    pause
    exit /b 1
)

echo [OK] タスク "%TASK_NAME%" を登録しました
pause
