Return to Moria Server Manager (RTM Server Manager)
Version 1.0
Last Updated: March 2025

==========================================
INTRODUCTION
==========================================
The Return to Moria Server Manager (RTM Server Manager) is a standalone tool 
designed to simplify the setup and management of a dedicated Return to Moria server.

This application automatically sets up SteamCMD, installs the dedicated server, 
and provides a graphical user interface (GUI) to manage server settings.

==========================================
FEATURES
==========================================
- **Automatic Setup** - Extracts SteamCMD, installs the dedicated server, and applies default settings.
- **Graphical Interface** - No command-line needed; everything is handled via an easy-to-use UI.
- **Configuration Management** - Edit server settings through the app with tooltips explaining each option.
- **Live Terminal** - Start, stop, and send commands to the server from the GUI.
- **Auto Restart Scheduling** - Set hourly, daily, or weekly server restarts.
- **Notification System** - Enable **Discord webhooks** and **desktop notifications** for server events.
- **Crash Detection** - The app can detect when the server crashes and notify you.
- **SteamCMD Handling** - Automatically updates the dedicated server before every launch.
- **Log Viewer** - Keep track of server status, errors, and commands.

==========================================
INSTALLATION & FIRST-TIME SETUP
==========================================
1. **Extract the Folder**
   Once downloaded, extract the `RTM Server Manager` folder anywhere on your system.

   Important files inside:
RTM Server Manager/ ├── RTM_Server_Manager.exe # The executable ├── Default Files/ # Default server configuration files ├── steamcmd.zip # SteamCMD (extracted on first run) ├── settings.json # Stores user settings ├── RTMSM.ico # Application icon ├── logs/ # Server logs (once running)


2. **Running for the First Time**
The first time you run `RTM_Server_Manager.exe`, **it may appear to do nothing for several minutes**.
This is because it is:
- Extracting **SteamCMD**
- Downloading & Installing **the Dedicated Server**
- Copying **Default Configuration Files**

**This process can take between 2-10 minutes** depending on your internet speed.
Once completed, the application will launch automatically.

==========================================
USING THE APPLICATION
==========================================
When you launch **RTM Server Manager**, you'll see the following tabs:

1. **Configuration** - Edit server settings via GUI.
2. **Permissions** - Manage user/admin permissions.
3. **Rules** - Set server rules and display messages.
4. **Terminal** - Start/stop the server, send commands, and view real-time logs.
5. **Notifications** - Configure Discord & desktop alerts for server events.

==========================================
STARTING THE SERVER
==========================================
1. Click **Start Server** - This will check for updates and launch the server.
2. The **terminal will display logs** as the server initializes.
3. Once fully started, **players can connect**.

If the server crashes, **the manager will detect it and notify you**.

==========================================
SETTING UP AUTO RESTARTS
==========================================
To keep your server running smoothly, you can schedule automatic restarts:
1. Go to **Terminal Tab → Auto Restart**
2. Choose one of the following:
- **Hourly** – Restart every X hours.
- **Daily** – Restart at a set time.
- **Weekly** – Restart on a specific day & time.
3. Click **Save Restart Schedule**

The app will automatically restart the server based on your settings.

==========================================
ENABLING NOTIFICATIONS
==========================================
1. Go to **Notifications Tab**
2. Enter a **Discord Webhook URL** (if using Discord alerts)
3. Enable/Disable:
- Server Start Alerts
- Server Stop Alerts
- Crash Detection Alerts
4. Click **Test Notifications** to verify settings.

==========================================
🛠 TROUBLESHOOTING
==========================================

**The app doesn’t start or closes immediately**
- Run `RTM_Server_Manager.exe` **as Administrator**.
- Make sure your **antivirus is not blocking it**.
- If `settings.json` is missing, **reinstall the application**.

**The server doesn’t install or update**
- Check your **internet connection**.
- Make sure `steamcmd.zip` is inside the `RTM Server Manager` folder.
- If SteamCMD fails, **delete the `steamcmd/` folder** and restart the app.

⚠ **My settings don’t save!**
- Ensure `settings.json` is in the correct directory.
- Make sure you **click "Save Configuration"** after making changes.

