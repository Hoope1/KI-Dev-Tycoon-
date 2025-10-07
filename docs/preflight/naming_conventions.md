# Naming- & Namespace-Konventionen — KI-Dev-Tycoon (Preflight Schritt 6)

Die folgenden Konventionen leiten sich aus `Zusatz.md` ab und gelten für das Unity-Projekt (`client/`) sowie ergänzende Tools/Skripte. Sie stellen sicher, dass der deterministische Sim-Kernel klar von der UI/Plattform-Schicht getrennt bleibt.

## C# Namespaces
- **Core.Sim** — Deterministischer Simulationskernel (keine Unity-Abhängigkeiten). Unterräume:
  - `Core.Sim.Time`, `Core.Sim.Rng`, `Core.Sim.Economy`, `Core.Sim.Research`, `Core.Sim.Team`, `Core.Sim.Market`, `Core.Sim.Persistence`.
- **Core.Data** — ScriptableObjects & Datenkataloge (nur Unity Editor-spezifische Klassen zum Laden/Validieren).
- **Game.App** — Bootstrap, Dependency Injection, Tick-Loop, Save-System.
- **Game.UI** — UI-Präsentationslogik, Views, Presenter, Input-Handling.
- **Platform.Steam** — Steamworks.NET Adapter (Achievements, Rich Presence, Initialisierung).
- **Game.Tests** — EditMode-/PlayMode-Tests (strukturieren nach Feature: `Game.Tests.Core`, `Game.Tests.UI`).

## Dateien & Ordner
- Unity-Ordner unter `Assets/` spiegeln Namespace-Struktur (`Assets/Scripts/Core/Sim`, `Assets/Scripts/Game/UI`).
- ScriptableObjects liegen in `Assets/Data/` mit Präfix `SO_` (z. B. `SO_RoleDef.asset`).
- Editor-spezifische Utilities (`Custom Editors`, `Importers`) in `Assets/Editor/`.
- Prefabs folgen Schema `Pf_<Kategorie>_<Name>` (z. B. `Pf_UI_Tab_HQ`).
- Addressables-Gruppen: `ui/*`, `sim/*`, `audio/*`.

## Coding-Standards (Kurzfassung)
- C#-Dateien im `Core.Sim`-Namespace nutzen `readonly` Felder und Konstruktor-Injektion (kein `MonoBehaviour`).
- Öffentlich sichtbare Klassen/Methoden mit XML-Dokumentation (für Schritt 24 vorbereiten).
- Keine Abkürzungen in öffentlichen APIs; PascalCase für Typen, camelCase für Variablen/Felder, UPPER_SNAKE_CASE für Konstanten.
- Events/Delegates benennen als `SomethingChangedEventArgs`, Handler `OnSomethingChanged`.

## Python / Tools
- Python-Module im `sim/`-Pfad behalten das existierende Paket `ki_dev_tycoon.*`.
- Skripte im Repo folgen Snake Case (`export_kpis.py`), Klassen CamelCase.

> **Wartung:** Neue Systeme müssen die Namenskonventionen in Pull Requests dokumentieren. Abweichungen nur mit expliziter ADR.
