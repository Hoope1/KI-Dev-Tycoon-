# KI-Dev-Tycoon Python-Frontend (Textual)

Dieses Verzeichnis enthält den Python-Client für den Steam-MVP von **KI-Dev-Tycoon**. Der Client implementiert UI, Launcher, lokale API-Integration sowie die Tick-Schleife ausschließlich mit Python-Komponenten. Alle Vorgaben stammen aus [`Zusatz.md`](../Zusatz.md) und dem aktualisierten [`100_schritte_plan.md`](../100_schritte_plan.md).

## Projektstruktur (Soll)

```text
app/
  pyproject.toml             # Poetry-Extras (`ui`, `build`)
  src/
    ki_dev_tycoon/
      ui/
        __init__.py
        app.py              # Textual.App Einstiegspunkt
        screens/
          dashboard.py
          team.py
          research.py
          products.py
          market.py
        widgets/
          kpi_panel.py
          timeline.py
      cli/
        __init__.py
        ui_commands.py      # Typer-Befehle (`ki-ui dev`, `ki-ui play`)
      api_client/
        __init__.py
        adapters.py         # Zugriff auf `sim` via FastAPI oder direkter Import
  tests/
    test_ui_smoke.py        # Textual Snapshot-Tests
  tools/
    build_app.py            # PyInstaller/Briefcase-Build-Skript
    steam_upload.py         # SteamCMD-Automatisierung (Python only)
```

> **Hinweis:** Die Ordnerstruktur wird im Laufe der Wochen W1–W4 gemäß `100_schritte_plan.md` aufgebaut. Placeholder-Dateien sind erlaubt, solange sie klar als solche markiert sind.

## Voraussetzungen

- Python 3.11 (kompatibel zu Poetry-Umgebung im Repo)
- Poetry ≥ 1.8 (verwendet für Workspace-Setup)
- Textual ≥ 0.58, Rich, Typer, FastAPI, Uvicorn (lokale API), SQLModel/SQLite
- PyInstaller ≥ 6.0 für Windows-Builds; optional Briefcase/Inno Setup
- OBS oder ScreenToGif für Marketing-Captures

## Projekt einrichten

1. Poetry-Umgebung auf Root-Ebene einrichten (`poetry install --with dev,ui`).
2. Textual-Entwicklungstools installieren (`poetry run textual devtools`).
3. Beispiel-Assets bauen (`poetry run python scripts/generate_assets.py`).

## Frontend starten

- **Entwicklungsmodus:** `poetry run ki-ui dev` → startet Textual-App mit Hot-Reload.
- **Spielmodus:** `poetry run ki-ui play --save-slot 1` → lädt Savegame und startet den Sim-Loop.
- **Headless-Autoplay:** `poetry run ki-ui autoplay --ticks 365 --seed 42` → nutzt Textual Dummy-Driver für automatisierte Tests.

### Navigationsstruktur & Dialoge

Die Textual-App stellt sechs Hauptbereiche bereit, die über eine horizontale Navigationsleiste (oder via Tastenkürzel `1`–`6`) erreichbar sind:

1. **Dashboard** – KPI-Panel, Zeitreihenübersicht und Eventlog.
2. **Team** – Rollenübersicht, Skill-Level sowie Recruiting-Events.
3. **Forschung** – Aktiver Forschungsknoten, Fortschritt und Backlog.
4. **Produkte** – Portfolio-Metriken, Durchschnittsqualität und Ereignisse.
5. **Markt** – Segment-Adoption, TAM und Nachfragekennzahlen.
6. **Events** – Chronologisches Log der Simulation.

Mit `Ctrl+P` öffnet sich der Theme-Dialog. Hier können Light/Dark-Mode und ein farbenblindenfreundlicher Akzentmodus umgeschaltet werden. Änderungen werden sofort auf alle Screens angewendet.

## Build Pipeline

PyInstaller-Builds werden vollständig über Python-Skripte orchestriert:

```bash
poetry run python app/tools/build_app.py \
  --onefile \
  --dist dist/windows \
  --icon assets/icons/app.ico
```

Das Skript kapselt alle Schritte (Assets bündeln, virtuelle Env einbetten, Steam-spezifische Dateien kopieren). Für Steam-Uploads steht `app/tools/steam_upload.py` bereit (`steamcmd` via `subprocess`).

## Tests & QA

- **Unit-/Widget-Tests:** `poetry run pytest app/tests -q`
- **Textual Snapshot Tests:** `poetry run pytest app/tests --snapshot-update`
- **mypy:** `poetry run mypy app/src`
- **Linting:** `poetry run ruff check app/src app/tests`
- **UI-Recording:** `poetry run ki-ui record --script scripts/demo_script.yaml`

Die Snapshot-Tests verwenden `textual.testing` und vergleichen das KPI-Panel mit einem gespeicherten Referenz-Rendering (`app/tests/__snapshots__/dashboard_kpis.txt`). Bei UI-Änderungen kann der Snapshot über `poetry run pytest app/tests --snapshot-update` aktualisiert werden.

## Lokale API (optional)

Für Modding und externe Tools kann eine lokale FastAPI-Instanz (`ki_dev_tycoon.api`) gestartet werden:

```bash
poetry run ki-api serve --host 127.0.0.1 --port 8765
```

Die Textual-App verbindet sich automatisch, sobald der Server läuft; andernfalls nutzt sie den eingebetteten Simulationskern.

## Steam-Integration (optional)

- `steamworks`-Python-Binding (MIT) zum Auslösen von Achievements.
- Integration erfolgt über `ki_dev_tycoon.platform.steam` Modul (reine Python-Wrapper).
- Fallback: internes Achievement-Log, falls Steam-SDK nicht verfügbar ist.

## Offene Aufgaben

Die detaillierten Aufgaben befinden sich im [`100_schritte_plan.md`](../100_schritte_plan.md) unter den Abschnitten W1–W6. Das Frontend gilt als funktionsfähig, wenn alle W3- und W4-Schritte abgeschlossen, automatisiert getestet und PyInstaller-Builds ohne manuelle Nacharbeit erstellt werden können.
