[Setup]
AppName=VEDA AI
AppVersion=1.0
DefaultDirName={autopf}\VEDA AI
DefaultGroupName=VEDA AI
OutputDir=installer
OutputBaseFilename=VEDA_AI-Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=veda-icon.ico
UninstallDisplayIcon={app}\VEDA_AI.exe
PrivilegesRequired=admin

[Files]
Source: "dist\VEDA_AI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "python_frontend\*"; DestDir: "{app}\python_frontend"; Flags: ignoreversion recursesubdirs
Source: "data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs
Source: "python_backend\*"; DestDir: "{app}\python_backend"; Flags: ignoreversion recursesubdirs
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion
Source: "veda-icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\VEDA AI"; Filename: "{app}\VEDA_AI.exe"; IconFilename: "{app}\veda-icon.ico"
Name: "{autodesktop}\VEDA AI"; Filename: "{app}\VEDA_AI.exe"; IconFilename: "{app}\veda-icon.ico"
Name: "{group}\Uninstall VEDA AI"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\VEDA_AI.exe"; Description: "Launch VEDA AI"; Flags: postinstall nowait skipifsilent
