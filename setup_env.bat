@echo off
REM =====================================
REM プロジェクトディレクトリへ移動
REM =====================================
cd /d %~dp0

echo [INFO] Checking Python...
py --version
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python が見つかりません
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
    echo [ERROR] uv のインストールに失敗しました
    pause
    exit /b 1
)

REM =====================================
REM 仮想環境作成
REM =====================================
echo [INFO] Creating virtual environment (.venv)...
py -m uv venv .venv

if %ERRORLEVEL% neq 0 (
    echo [ERROR] 仮想環境の作成に失敗しました
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
    echo [WARN] pyproject.toml が見つかりません（依存関係は未インストール）
)

echo.
echo [OK] セットアップ完了
echo.
echo 仮想環境: %CD%\.venv
pause