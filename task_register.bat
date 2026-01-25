@echo off

set BASE_DIR=%~dp0
cd /d %BASE_DIR%

set RUN_BAT=%BASE_DIR%\run.bat

if not exist "%RUN_BAT%" (
    echo [ERROR] run.bat not found
    pause
    exit /b 1
)

set TASK_NAME=VRCEventAutoRegister

schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "cmd.exe /c \"\"%RUN_BAT%\"\"" ^
  /sc DAILY ^
  /st 00:00 ^
  /ri 360 ^
  /du 24:00 ^
  /ru "%USERNAME%" ^
  /rl HIGHEST ^
  /f

schtasks /change ^
  /tn "%TASK_NAME%" ^
  /ri 360

if %ERRORLEVEL% neq 0 (
    echo [ERROR] failed to register task
    pause
    exit /b 1
)

echo [OK] task name "%TASK_NAME%" registered
echo execute time: 00:00 / 03:00 / 06:00 / 09:00 / 12:00 / 15:00 / 18:00 / 21:00
pause
