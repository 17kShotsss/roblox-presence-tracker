# Roblox Presence Tracker

A Python desktop app that tracks your Roblox presence, showing if you're in-game, the place ID, and the job ID.

---

## Features

- Display your Roblox **display name** and **@username**
- Shows **in-game** or **offline** status
- Retrieves **Place ID** and **Job ID**
- Copy buttons for:
  - Job ID
  - Place ID
  - Join Script
  - Join Link
- Auto-refresh every 5 seconds
- Dark-themed, responsive **Tkinter GUI**

---

## Installation

1. Install Python 3.8+ and pip
2. Install dependencies:

```bash
pip install customtkinter>=5.2.0 requests>=2.31.0 pyperclip>=1.8.2 pywin32>=306 Pillow>=10.0.0
```

3. Run the app:

```bash
python main.py
```

---

## Usage

- The window shows your Roblox name, username, and presence.
- Copy buttons allow quick access to Job ID, Place ID, join scripts, or links.
- The app automatically refreshes presence data every 5 seconds.

### Buttons

| Button           | Function |
|-----------------|----------|
| Copy Job ID      | Copies the current Job ID |
| Copy Place ID    | Copies the current Place ID |
| Copy Join Script | Copies a Lua join script for TeleportService |
| Copy Join Link   | Copies the Roblox game URL with job ID |
| Refresh          | Refreshes presence data |

---

## Notes

- Works on **Windows**.
- Automatically reads `.ROBLOSECURITY` cookie from Chrome, Edge, or Firefox.
- Firefox support may be limited.

---

## Built With

- Python 3
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for GUI
- Requests for API requests
- Pyperclip for clipboard operations
- PyWin32 for Windows cookie decryption
- Pillow for image support (if needed)

