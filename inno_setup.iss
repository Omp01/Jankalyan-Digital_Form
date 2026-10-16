; ==============================================================================
; Inno Setup Script for Jankalyan Blood Bank Digital System (QF/JKRP/18)
; ==============================================================================
; Version: 1.1.0 (Wi-Fi LAN Multi-Device Access & Automated Firewall Support)
; Requires: Inno Setup 6.x (Download free from: https://jrsoftware.org/isdl.php)
;
; Build Steps:
; 1. Build PyInstaller standalone folder:
;    python build_exe.py   (or run build.bat)
; 2. Open this script in Inno Setup Compiler and click Compile (Ctrl+F9), or run:
;    iscc inno_setup.iss
; ==============================================================================

#define MyAppName "Jankalyan Blood Bank Digital System"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "Jankalyan Blood Centre & Hospital"
#define MyAppExeName "JankalyanBloodBank.exe"
#define MyAppURL "http://127.0.0.1:8000"

[Setup]
; Unique Application Identifier (GUID)
AppId={{C8E29910-3492-41FA-83DF-8F32C0D41BA2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Jankalyan Blood Bank
DefaultGroupName=Jankalyan Blood Bank
AllowNoIcons=yes
OutputDir=dist_installer
OutputBaseFilename=JankalyanBloodBank_Setup_v1.1.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Branding & Wizard Behavior
DisableProgramGroupPage=auto
DisableReadyPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "firewallrule"; Description: "Configure Windows Firewall rule for Wi-Fi / LAN multi-device access (Port 8000)"; GroupDescription: "Network Options:"; Flags: checkedonce

[Files]
; Include all PyInstaller bundled dependencies from dist\JankalyanBloodBank
Source: "dist\JankalyanBloodBank\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu Shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Launch Jankalyan Blood Bank Digital System (Port 8000 - Wi-Fi / LAN Enabled)"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop Shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Launch Jankalyan Blood Bank Digital System (Port 8000 - Wi-Fi / LAN Enabled)"

[Run]
; 1. Add Windows Firewall Inbound Rule for Port 8000 (Allows tablets/other PCs on Wi-Fi to access server)
Filename: "netsh.exe"; Parameters: "advfirewall firewall add rule name=""Jankalyan Blood Bank Server (Port 8000)"" dir=in action=allow protocol=TCP localport=8000 profile=any"; Tasks: firewallrule; Flags: runhidden; StatusMsg: "Configuring Windows Firewall for Wi-Fi network access..."

; 2. Launch application post-installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Remove Windows Firewall Rule on uninstallation
Filename: "netsh.exe"; Parameters: "advfirewall firewall delete rule name=""Jankalyan Blood Bank Server (Port 8000)"""; Flags: runhidden

[UninstallDelete]
; Clean up runtime logs in application directory
Type: files; Name: "{app}\*.log"

[Code]
// Note: User SQLite database and audit logs stored in %APPDATA%\JankalyanBloodBank\data\
// are permanently preserved across setup upgrades and uninstallations.
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // Database safely preserved in %APPDATA%\JankalyanBloodBank\data\
  end;
end;
