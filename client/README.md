# KI-Dev-Tycoon Client (Unity 6 LTS)

Dieses Verzeichnis enthält den Unity-Client für den Steam-MVP von **KI-Dev-Tycoon**. Der Client implementiert UI, Steam-Integration und die Tick-Schleife, während der deterministische Simulationskern (`Core.Sim`) strikt ohne Unity-Abhängigkeiten bleibt. Alle Vorgaben stammen aus [`Zusatz.md`](../Zusatz.md).

## Projektstruktur (Soll)

```
client/
  ai-dev-tycoon/                # Unity-Projekt
    Assets/
      Scripts/
        Core.Sim/
        Core.Data/
        Game.UI/
        Game.App/
        Platform.Steam/
      Data/
        RoleDefs/
        Research/
        Products/
        Markets/
        Events/
      Resources/
      Addressables/
    Packages/
    ProjectSettings/
  tools/
    build.ps1                   # Headless Build-Script (Windows)
    capture_plan.md             # Shot-Liste für Trailer/Screenshots
```

> **Hinweis:** Die Ordnerstruktur wird im Laufe von W1–W4 gemäß `100_schritte_plan.md` aufgebaut. Placeholder-Dateien sind erlaubt, solange sie klar als solche markiert sind.

## Voraussetzungen

- Unity Hub mit Unity 6000.x LTS (Windows Build Support, IL2CPP, Visual Studio Integration optional).
- Steamworks.NET (via Git-URL `https://github.com/rlabrecque/Steamworks.NET.git#upm`).
- Optional: PowerShell ≥ 5.1 bzw. PowerShell Core für Build-Skripte.

## Projekt öffnen

1. Unity Hub starten und auf **Add** → `client/ai-dev-tycoon` zeigen.
2. Beim ersten Import werden benötigte Pakete (TextMeshPro, Input System, Localization, Addressables) nachinstalliert.
3. Nach erfolgreichem Import die Szene `Assets/Scenes/Bootstrap.unity` öffnen und im Play Mode prüfen.

## Build Pipeline

Der Build-Prozess folgt den Vorgaben aus `Zusatz.md` (Windows x64, IL2CPP, Offline). Ein minimales PowerShell-Skript kann wie folgt aussehen:

```powershell
param(
  [string]$ProjectPath = "$(Resolve-Path ../ai-dev-tycoon)",
  [string]$OutputPath = "$(Resolve-Path ../build)"
)

$unity = "C:\\Program Files\\Unity\\Hub\\Editor\\6000.0.XXf1\\Editor\\Unity.exe"
$buildTarget = "StandaloneWindows64"
$buildMethod = "Game.App.Builds.Cmd.BuildWindows"  # statische Methode im Projekt

& $unity -batchmode -quit -projectPath $ProjectPath -executeMethod $buildMethod -buildTarget $buildTarget -logFile build.log -CustomBuildPath "$OutputPath/KI-Dev-Tycoon.exe"
```

Vor dem Build sicherstellen:

- `steam_appid.txt` liegt im Projektroot.
- Release-Konfiguration nutzt IL2CPP, Managed Stripping Level „Low“, Debug-Symbole deaktiviert.
- Addressables/Localization wurden gebuildet (`Addressables Build Player Content`).

## Tests & QA

- **Play Mode Tests:** Tick-Schleife (0,5 s), Save/Load Rotation, Offline-Prozess mit simuliertem `dt`.
- **Edit Mode Tests:** PCG32-RNG, Sim-Invarianten (`Core.Sim`), Daten-Loader.
- **Headless Runner:** CLI-Tool (C#) führt 30 Ingame-Tage aus und exportiert KPI-CSV (siehe `tools/`-Ordner).

## Steam-Integration Checkliste

1. `SteamAPI.Init()` / `SteamAPI.Shutdown()` werden sicher aufgerufen (inkl. Fallback ohne Steam).
2. Achievements über `Platform.Steam.Ach.Unlock` an Domain-Events gebunden.
3. Rich Presence Strings (z. B. „Day 12 • 1 Product • 5 Staff“) aktualisieren sich im Tick.
4. `steam_appid.txt` wird für Nicht-Steam-Starts entfernt (Build-Skript sorgt dafür).

## Offene Aufgaben

Die detaillierten Aufgaben befinden sich im [`100_schritte_plan.md`](../100_schritte_plan.md) unter den Abschnitten W1–W6. Der Client gilt erst als funktionsfähig, wenn alle W3- und W4-Schritte abgeschlossen und getestet wurden.

