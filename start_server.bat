@echo off

:: Customize these paths if necessary
set "STEAMCMD_PATH=C:\SteamCmd"
set "SERVER_PATH=C:\Return to Moria"
set "SERVER_EXE=MoriaServer.exe"
set "APP_ID=3349480"

echo [1/2] Updating Return to Moria via SteamCMD...
cd /d "%STEAMCMD_PATH%"
steamcmd +login anonymous +app_update %APP_ID% validate +quit

echo.
echo [2/2] Launching the server...
cd /d "%SERVER_PATH%"
start "" "%SERVER_EXE%" -log -port=7777

REM Wait a few seconds for the server to start (adjust as necessary)
timeout /t 5 /nobreak >nul

REM Set your Discord webhook URL (update it with your actual webhook URL)
set "discordWebhookUrl=PUT URL HER"
set "message=Return to Moria server has started."

REM Send the Discord notification using curl
curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"%message%\"}" %discordWebhookUrl%

echo.
echo Done! Press any key to close this window...
