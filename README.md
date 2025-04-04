# Return to Moria Server Manager (RTM Server Manager)

- [Download the latest application at:](https://github.com/Baghdaddy27/RTM-Dedicated-Server-Manager/releases)

---

## INTRODUCTION

The **Return to Moria Server Manager** is a standalone tool designed to simplify the setup and management of a dedicated Return to Moria server.

This application automatically sets up SteamCMD, installs the dedicated server, and provides a modern **graphical user interface (GUI)** to manage configuration, restarts, notifications, and more.

---

## FEATURES

- **Automatic Setup** – Extracts SteamCMD, installs the server, and applies default settings.  
- **GUI-Based Management** – No command line needed. Configure and manage everything through an intuitive interface.  
- **Configuration Editing** – Modify server config, permissions, and rules with tooltips and field validation.  
- **Integrated Terminal** – Start, stop, and send commands directly to the server from the built-in terminal.  
- **Auto Restart Scheduler** – Set scheduled restarts every 1–4 hours with optional pre-warning notifications.  
- **Notification System** – Enable Discord webhooks and desktop toasts for server start/stop/crash events.  
- **Crash Detection** – Detects server crashes and alerts you via your selected notification methods.  
- **SteamCMD Auto-Update** – Ensures the dedicated server is always up to date.  
- **Log Viewer** – Tracks server events, command output, and warnings in real time.

---

## INSTALLATION & FIRST-TIME SETUP

### 1. Extract the Folder

Download and extract the **RTM Server Manager** folder anywhere on your system.  
The folder should contain:

```
RTM Server Manager/
├── main.exe                  # The executable
├── steamcmd.zip              # SteamCMD (auto-extracted on first run)
├── settings.json             # Stores saved paths and notification settings
├── .wm                       # (Optional) Welcome message, hidden file
├── assets/
│   └── RTMSM.png             # App branding image
├── Default Files/
│   ├── MoriaServerConfig.ini
│   ├── MoriaServerPermissions.txt
│   └── MoriaServerRules.txt
├── logs/                     # Populated automatically during runtime
```

---

### 2. First Launch

Double-click `main.exe`. It may appear to “hang” for several minutes the first time — this is normal. It is:

- Extracting SteamCMD
- Downloading and installing the Return to Moria Dedicated Server
- Setting up default config files

This process can take 2–10 minutes depending on your internet speed.  
Once setup is complete, the application will launch automatically.

---

## USING THE APPLICATION

When you launch RTM Server Manager, the main panel is split into sections:

### Setup Section

- **Verify SteamCMD** – Installs or extracts SteamCMD.
- **Verify RTM Files** – Installs or updates the server files.
- **Setup Notifications** – Opens a dialog to configure Discord/webhook and desktop notifications.

### Server Control Section

- **Start Server** – Updates and launches the server.
- **Stop Server** – Sends a graceful shutdown command.
- **Auto Restart** – Opens the restart scheduling window.

### Server Settings Section

- **Edit Config** – Modify `MoriaServerConfig.ini`
- **Edit Permissions** – Modify `MoriaServerPermissions.txt`
- **Edit Rules** – Modify `MoriaServerRules.txt`

---

## STARTING THE SERVER

1. Click **Start Server**  
2. The terminal pane will begin logging as the server boots  
3. Once it finishes loading, players can connect via direct IP  

If the server crashes, the app will notify you (if notifications are enabled).

---

## SETTING UP AUTO RESTARTS

1. Click **Auto Restart**  
2. Configure:
   - Frequency (1–4 hours)
   - Start Time (HH:MM)
   - Enable Restart Warnings
3. Click **Save**  
The app will run a background watchdog that gracefully restarts the server at the scheduled time.

---

## ENABLING NOTIFICATIONS

1. Click **Setup Notifications**  
2. Choose:
   - Enable/Disable Desktop Notifications
   - Enable/Disable Discord Webhook Notifications
3. Enter your Discord Webhook URL  
4. Click **Test Notification** to verify everything works  

You’ll be notified on:
- Server Start
- Server Stop
- Crash Detection
- Scheduled Restarts (if enabled)

---

## TROUBLESHOOTING

### The app doesn’t start or closes immediately

- Run as Administrator
- Make sure your antivirus isn’t blocking it
- If `settings.json` is missing or corrupted, delete it and re-launch

### The server won’t install/update

- Confirm `steamcmd.zip` is in the same folder as `main.exe`
- Check internet access
- Delete the `steamcmd/` folder and re-run **Verify SteamCMD**

### My settings aren’t saving

- Make sure `settings.json` is present in the same folder as `main.exe`
- Always click **Save Configuration** after making changes

---

## FEEDBACK & UPDATES

Have feedback, questions, or ideas? Post them on the official GitHub:

- [GitHub Discussions](https://github.com/Baghdaddy27/RTM-Dedicated-Server-Manager/discussions/1)  
- [GitHub Releases](https://github.com/Baghdaddy27/RTM-Dedicated-Server-Manager/releases)
