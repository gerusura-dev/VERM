@echo off
set TASK_NAME=VRCEventAutoRegister

schtasks /delete /tn "%TASK_NAME%" /f

if %ERRORLEVEL% neq 0 (
    echo [ERROR] failed to delete task
    pause
    exit /b 1
)

echo [OK] task name "%TASK_NAME%" deleted
pause
