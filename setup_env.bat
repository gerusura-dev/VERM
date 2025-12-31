@echo off
REM =====================================
REM プロジェクトディレクトリへ移動
REM =====================================
cd /d %~dp0

echo [INFO] Checking Python...
py --version
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found
    pause
    exit /b 1
)

REM =====================================
REM uv インストール
REM =====================================
echo [INFO] Installing uv...
py -m pip install --upgrade pip
py -m pip install --upgrade uv

if %ERRORLEVEL% neq 0 (
    echo [ERROR] failed to install uv
    pause
    exit /b 1
)

REM =====================================
REM 仮想環境作成
REM =====================================
echo [INFO] Creating virtual environment (.venv)...
py -m uv venv .venv

REM =====================================
REM 依存関係インストール
REM =====================================
if exist pyproject.toml (
    echo [INFO] Installing dependencies into .venv...
    py -m uv run pip install -r pyproject.toml
) else (
    echo [WARN] pyproject.toml not found
)

REM =====================================
REM chrome_profile 初期化
REM =====================================
set CHROME_PROFILE=%CD%\chrome_profile
set FIRST_RUN_FLAG=%CHROME_PROFILE%\FirstRun.done

if not exist "%CHROME_PROFILE%" (
    mkdir "%CHROME_PROFILE%"
)

REM =====================================
REM 初回のみ Chrome 起動
REM =====================================
if not exist "%FIRST_RUN_FLAG%" (
    echo.
    echo === First time setup detected ===
    echo Chrome will be launched automatically.
    echo Please log in to Google and then close Chrome.
    echo.

    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
      --user-data-dir="%CHROME_PROFILE%"

    echo.
    echo After finishing login, close Chrome and press any key.
    pause

    echo done > "%FIRST_RUN_FLAG%"
)

echo.
echo === setup completed ===
echo chrome_profile: %CHROME_PROFILE%
pause

echo.
echo [OK] setup complete
echo.
echo venv: %CD%\.venv
pause