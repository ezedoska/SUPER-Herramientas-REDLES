; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Super Herramientas REDLES"
#define MyAppVersion "2.20210208"
#define MyAppPublisher "Doskapps"
#define MyAppURL "https://registroefectores.desarrollosocial.gob.ar"
#define MyAppExeName "run.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7DF9CC54-9B04-4619-A59C-4F595C8263A4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userdocs}\{#MyAppName}
DisableDirPage=yes
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=C:\Users\moree\Desktop
OutputBaseFilename=SuperHerramientasREDLES
SetupIconFile=C:\Users\moree\Desktop\super-herramientas-redles\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\moree\Desktop\super-herramientas-redles\dist\run\run.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\moree\Desktop\super-herramientas-redles\dist\run\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\asignacion"; Filename: "{app}\asignacion.xlsx"; Tasks: desktopicon
Name: "{autodesktop}\cruceDNI"; Filename: "{app}\cruceDNI.xlsx"; Tasks: desktopicon
Name: "{autodesktop}\cruceFORM"; Filename: "{app}\cruceFORM.xlsx"; Tasks: desktopicon
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

