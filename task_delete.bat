@echo off
set TASK_NAME=VRCEventAutoRegister

schtasks /delete /tn "%TASK_NAME%" /f

if %ERRORLEVEL% neq 0 (
    echo [ERROR] タスクの削除に失敗しました
    pause
    exit /b 1
)

echo [OK] タスク "%TASK_NAME%" を削除しました
pause
