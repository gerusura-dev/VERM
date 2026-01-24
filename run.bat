@echo off
setlocal enabledelayedexpansion

set BASE_DIR=%~dp0
cd /d %BASE_DIR%

echo [INFO] Check VERM Version ...
git pull
if errorlevel 1 (
  echo [WARNING] Failed to check VERM version
  exit /b 1
)

set CHROME_PROFILE=%BASE_DIR%chrome_profile

echo [INFO] Launching Chrome with debug port...

for /f %%i in ('
  powershell -NoProfile -Command ^
    "(Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -PassThru -ArgumentList '--remote-debugging-port=9222','--user-data-dir=%CHROME_PROFILE%','--profile-directory=Default').Id"
') do set CHROME_PID=%%i

timeout /t 5 > nul

echo [INFO] Running Python script...
.venv\Scripts\python.exe main.py

echo [INFO] Closing Chrome (PID=%CHROME_PID%) ...
taskkill /PID %CHROME_PID% /T /F > nul 2>&1

endlocal
