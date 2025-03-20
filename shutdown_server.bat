@echo off
setlocal

REM Log the start time of the shutdown process
echo [%date% %time%] Starting shutdown process for Return to Moria... >> "C:\Scripts\ServerUpdateLog.txt"

REM Attempt to kill the process and log the output
echo [%date% %time%] Attempting to kill MoriaServer-Win64-Shipping.exe... >> "C:\Scripts\ServerUpdateLog.txt"
taskkill /F /IM MoriaServer-Win64-Shipping.exe >> "C:\Scripts\ServerUpdateLog.txt" 2>&1

timeout /t 5 /nobreak >nul

REM Log the running processes to verify if it's still active
echo [%date% %time%] Checking running processes... >> "C:\Scripts\ServerUpdateLog.txt"
tasklist /FI "IMAGENAME eq MoriaServer-Win64-Shipping.exe" >> "C:\Scripts\ServerUpdateLog.txt" 2>&1

REM Set your Discord webhook URL (update it below)
set "discordWebhookUrl=PUT URL HERE"
set "message=Return to Moria has been shut down."

REM Send the Discord notification using curl
curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"%message%\"}" %discordWebhookUrl%

echo [%date% %time%] Discord notification sent. >> "C:\Scripts\ServerUpdateLog.txt"

endlocal
