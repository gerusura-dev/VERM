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

if %ERRORLEVEL% neq 0 (
    echo [ERROR] failed to create venv
    pause
    exit /b 1
)

REM =====================================
REM 依存関係インストール
REM =====================================
if exist pyproject.toml (
    echo [INFO] Installing dependencies from pyproject.toml...
    py -m uv pip install -r pyproject.toml
) else (
    echo [WARN] pyproject.toml not found
)

echo.
echo [OK] setup complete
echo.
echo venv: %CD%\.venv
pause