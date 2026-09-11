# Standalone Windows Setup (.exe) Packaging Guide

This guide explains how to package the **Jankalyan Blood Bank Digital System** into a standalone Windows desktop installer using **PyInstaller** and **Inno Setup**.

---

## 1. Problem Solved: SQLite Database Persistence in Packaged Apps

### Why Standard PyInstaller Packaging Fails with SQLite:
1. **PyInstaller Temp Extraction (`sys._MEIPASS`)**:
   - If SQLite `.db` files are bundled inside the executable, PyInstaller unpacks them into a temporary folder (`%TEMP%\_MEIxxxxxx`).
   - When the user closes the application, Windows purges the temp folder, wiping all saved patient records, audit logs, and user credentials.
2. **Program Files Permission Denied**:
   - When installed to `C:\Program Files\Jankalyan Blood Bank`, standard Windows user accounts lack write permissions to that directory.
   - Attempting to write to `C:\Program Files\...\bloodbank.db` causes SQLite `OperationalError: unable to open database file` crashes.

### How It Is Resolved:
We implemented [`services/path_service.py`](file:///d:/Jankalyaan_Digitalized_Form/services/path_service.py):
- **Read-Only Bundled Assets** (`templates/`, `static/`, `schema.sql`) are loaded from `sys._MEIPASS` or the application installation folder.
- **Writable SQLite Database** (`bloodbank.db`) is automatically created and stored in the user's permanent application data directory:
  ```
  %APPDATA%\JankalyanBloodBank\data\bloodbank.db
  (e.g., C:\Users\<Username>\AppData\Roaming\JankalyanBloodBank\data\bloodbank.db)
  ```
- **Automatic Initialization**: On the very first run, if no database exists in `%APPDATA%`, the application automatically executes `database/schema.sql` and seeds the initial default users and configuration.
- **Upgrades & Uninstallation Safety**: Updating or uninstalling the application binary in `Program Files` will **never delete** donor records or hospital database files.

---

## 2. Prerequisites

1. **Python 3.10+** (with virtual environment or system Python).
2. **Inno Setup 6.x** (Download free from: [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)).

---

## 3. Step-by-Step Build Instructions

### Step 1: Install Build Dependencies
Open PowerShell or Command Prompt in the project root:
```powershell
pip install -r requirements.txt
```

### Step 2: Build the Executable with PyInstaller
You can build using any of the following methods:

**Method 1 (Double-Click Batch File - Recommended):**
Double-click [`build.bat`](build.bat) in the project folder.

**Method 2 (Python Command):**
```powershell
python build_exe.py
```

**Method 3 (Direct PyInstaller CLI):**
```powershell
pyinstaller --noconfirm bloodbank.spec
```

This generates the compiled standalone folder at:
```
dist\JankalyanBloodBank\
├── JankalyanBloodBank.exe   <-- Main Launcher
├── templates\
├── static\
├── database\schema.sql
└── ... (Python runtime DLLs)
```

### Step 3: Test the Executable Locally
Double-click `dist\JankalyanBloodBank\JankalyanBloodBank.exe`.
- The application will verify/initialize `%APPDATA%\JankalyanBloodBank\data\bloodbank.db`.
- Waitress server will start on `http://127.0.0.1:8000`.
- Your default web browser will automatically open to the login screen.

---

## 4. Building the Windows Installer with Inno Setup

### Method A: Using Inno Setup Compiler GUI
1. Open **Inno Setup Compiler**.
2. Click **File -> Open** and select [`inno_setup.iss`](file:///d:/Jankalyaan_Digitalized_Form/inno_setup.iss).
3. Click **Build -> Compile** (or press `Ctrl+F9`).
4. The generated setup wizard will be saved in `dist_installer/JankalyanBloodBank_Setup_v1.0.exe`.

### Method B: Using Inno Setup Command Line (`iscc`)
If Inno Setup is added to your system PATH:
```powershell
iscc inno_setup.iss
```

---

## 5. Summary of Key Files

| File | Purpose |
|---|---|
| [`services/path_service.py`](file:///d:/Jankalyaan_Digitalized_Form/services/path_service.py) | Dynamic path resolver for writable `%APPDATA%` SQLite DB and read-only bundled assets |
| [`desktop_launcher.py`](file:///d:/Jankalyaan_Digitalized_Form/desktop_launcher.py) | Standalone launcher: auto-inits DB, runs Waitress WSGI, opens browser |
| [`bloodbank.spec`](file:///d:/Jankalyaan_Digitalized_Form/bloodbank.spec) | PyInstaller spec packaging templates, static, schema.sql, and dependencies |
| [`build_exe.py`](file:///d:/Jankalyaan_Digitalized_Form/build_exe.py) | One-command PyInstaller build runner |
| [`inno_setup.iss`](file:///d:/Jankalyaan_Digitalized_Form/inno_setup.iss) | Inno Setup script generating professional Windows Setup `.exe` |

---

## 6. Default Admin & Staff Credentials
- **Admin**: `admin` / `Admin@123`
- **Medical Officer**: `doctor` / `Doctor@123`
- **Staff**: `staff` / `Staff@123`
