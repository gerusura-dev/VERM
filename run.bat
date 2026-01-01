@echo off
set BASE_DIR=%~dp0
cd /d %BASE_DIR%

set CHROME_PROFILE=%BASE_DIR%chrome_profile

echo [INFO] Launching Chrome with debug port...

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="%CHROME_PROFILE%" ^
  --profile-directory=Default

timeout /t 5 > nul

echo [INFO] Running Python script...
.venv\Scripts\python.exe main.py