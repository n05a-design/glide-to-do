; SPDX-License-Identifier: MPL-2.0
; Inno Setup 6 Skript für Glide (Windows x64)
; Erzeugt einen unprivilegierten Benutzer-Installer nach %LOCALAPPDATA%\Programs\Glide.
; Startmenüeintrag mit fester AppUserModelID: Shaye.Glide (docs/10_VEROEFFENTLICHUNG.md).

#ifndef MyAppVersion
#define MyAppVersion "1.0.1"
#endif

#define MyAppName "Glide"
#define MyAppPublisher "Tim von Trostorff"
#define MyAppURL "https://github.com/n05a-design/glide-to-do"
#define MyAppExeName "Glide.exe"
#define MyAppId "Shaye.Glide"

#ifndef SourceDir
#define SourceDir "..\paket\bau\dist\Glide"
#endif

#ifndef OutputFileName
#define OutputFileName "Glide-" + MyAppVersion + "-windows-x64-setup"
#endif

[Setup]
; Einmalig festgelegte AppId aus docs/10_VEROEFFENTLICHUNG.md
AppId={{0A756FC5-5DDB-4B0F-9EC8-B4AA85753597}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Unprivilegierte Installation je Benutzer ohne UAC-Adminabfrage
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=.
OutputBaseFilename={#OutputFileName}
SetupIconFile=..\..\assets\icons\glide.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; AppUserModelID: "{#MyAppId}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; AppUserModelID: "{#MyAppId}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
