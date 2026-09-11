; ==============================================================================
; Inno Setup Script for Jankalyan Blood Bank Digital System (QF/JKRP/18)
; ==============================================================================
; Requires: Inno Setup 6.x (https://jrsoftware.org/isdl.php)
; 
; Instructions:
; 1. First, build the executable package using:
;    python build_exe.py
; 2. Open this file (inno_setup.iss) in Inno Setup Compiler and click "Compile" (or press Ctrl+F9).
;    Or run from command line:
;    iscc inno_setup.iss
; ==============================================================================

#define MyAppName "Jankalyan Blood Bank Digital System"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Jankalyan Blood Centre & Hospital"
#define MyAppExeName "JankalyanBloodBank.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".db"

[Setup]
; App Identity
AppId={{C8E29910-3492-41FA-83DF-8F32C0D41BA2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Jankalyan Blood Bank
DefaultGroupName=Jankalyan Blood Bank
AllowNoIcons=yes
OutputDir=dist_installer
OutputBaseFilename=JankalyanBloodBank_Setup_v1.0
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Visual Branding
DisableProgramGroupPage=auto
DisableReadyPage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "Create a Quick Launch shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; All files compiled by PyInstaller into dist\JankalyanBloodBank
Source: "dist\JankalyanBloodBank\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu Shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Launch Jankalyan Blood Bank Digital System"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop Shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Launch Jankalyan Blood Bank Digital System"

[Run]
; Option to launch the application immediately after setup finishes
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Note: User data is stored in %APPDATA%\JankalyanBloodBank and is intentionally preserved on uninstall.
Type: files; Name: "{app}\*.log"

[Code]
// Helper message indicating user data preservation
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    // User database is preserved in %APPDATA%\JankalyanBloodBank\data\
  end;
end;
