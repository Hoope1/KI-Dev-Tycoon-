# KI-Dev-Tycoon Client

Dieses Verzeichnis enthält den Godot-Prototypen für die Foundations-Phase. Der Fokus liegt aktuell darauf, ein lauffähiges Projektgerüst mit Mock-Szenen zu besitzen, das später mit den Daten des Simulations-Kernels verbunden wird.

## Projektstruktur

```
client/
  godot_project/
    project.godot          # Godot 4 Konfigurationsdatei
    scenes/
      dashboard.tscn       # UI-Mock des Dashboards
      project_list.tscn    # Wiederverwendbarer Projektslisten-Container
      resources/
        title_label.tres   # LabelSettings für den Screen-Titel
    scripts/
      project_list_preview.gd  # Renderlogik für Mock-Daten
  tools/
    build.py               # Build/Export-Orchestrierung
```

## Voraussetzungen

* Godot 4.2.x oder neuer muss lokal installiert und über den Befehl `godot4` verfügbar sein.
* Python 3.11+ für die Build-Hilfsskripte.

## Build Pipeline

Das Skript `tools/build.py` exportiert die Szenen in ein Distributionsverzeichnis (standardmäßig `build/web`). Es erzeugt eine minimale `index.html`, bindet die Godot-Exportdateien ein (sobald verfügbar) und schreibt Metadaten (z. B. Build-Timestamp).

```bash
cd client
python -m pip install -r tools/requirements.txt  # optional: linting utilities
python tools/build.py --export web --output build/web
```

Der Export nutzt den Godot-CLI-Aufruf

```bash
godot4 --headless --path godot_project --export-release "Web" build/web/KI-Dev-Tycoon.html
```

Falls der CLI-Befehl nicht gefunden wird oder `--mock-export` gesetzt ist, generiert das Skript einen Platzhalter-Build (HTML + Szenenliste) und erstellt trotzdem das ZIP-Artefakt (`build/KI-Dev-Tycoon-web.zip`). Dadurch bleibt die Pipeline auch ohne Godot-Binary ausführbar.

## Nächste Schritte

1. Szenen mit realen Daten aus der Simulation befüllen (Schritt 16 ff.).
2. UI-Komponenten modularisieren und gestylte Themes erstellen.
3. Automatisierte UI-Tests (Godot GUT) vorbereiten.
