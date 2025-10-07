# KI-Dev-Tycoon Monorepo

Dieses Repository bündelt alle Assets für die Solo-MVP-Umsetzung von **KI-Dev-Tycoon** auf Steam (Windows x64, offline). Quelle aller verbindlichen Entscheidungen ist [`Zusatz.md`](./Zusatz.md); sämtliche weiteren Dokumente erweitern oder konkretisieren diesen Anhang. Alle Laufzeitkomponenten werden vollständig in Python umgesetzt.

## Strukturüberblick

```text
/README.md              # Diese Übersicht
/Zusatz.md              # Source of truth (Steam-MVP, Solo-Dev, ≤ €500, Python-only)
/100_schritte_plan.md   # Umsetzungsschritte, nach Zusatz.md strukturiert
/Gameplan.md            # Ergänzende Ableitungen & Referenzen
/app/                   # Textual-Frontend & Launcher (Python)
  README.md             # Setup- und Build-Anweisungen für das Python-Frontend
/sim/                   # Python-Simulationskernel (Deterministischer Core)
  README.md             # Technische Details & Nutzungshinweise
  pyproject.toml        # Poetry-Konfiguration
  src/                  # Python-Quellcode (Paket `ki_dev_tycoon`)
  tests/                # Test-Suites (pytest/hypothesis)
  docs/                 # Simulationsspezifische Dokumentation & Artefakte
/client/                # Legacy-Prototypen (Godot/Unity) – nicht mehr aktiv weiterentwickeln
/docs/                  # Projektdokumentation, ADRs, Playtests
```

## Erste Schritte (Simulation & Tools)

1. Wechsle in den Ordner `sim/`.
2. Installiere die Python-Abhängigkeiten mit Poetry (`poetry install --with dev`).
3. Führe Tests und Lints via `poetry run pytest`, `poetry run mypy`, `poetry run ruff check` aus.
4. Starte die Headless-Simulation über `poetry run ki-sim run --ticks 365 --seed 42`.

## Erste Schritte (Python-Frontend)

1. Lies [`app/README.md`](app/README.md) für den Aufbau des Textual-Frontends.
2. Installiere zusätzliche Frontend-Abhängigkeiten mit `poetry install --with ui` (siehe `app/pyproject.toml`).
3. Starte den Prototypen mit `poetry run ki-ui dev`.
4. Für gebündelte Builds: `poetry run python tools/build_app.py` erzeugt einen PyInstaller-Output (`dist/windows/`).

## Weiterführende Dokumente

- `Zusatz.md` – Primäre Produktspezifikation (Steam-MVP, Solo-Dev, ≤ €500, Python-only).
- `AGENT.md` – Arbeitsanweisungen & Coding-Guidelines für alle Agent:innen.
- `Gameplan.md` – Ergänzende Ableitungen (Loops, Referenzen, Visual Style) zum Zusatz.
- `100_schritte_plan.md` – Schrittplan entlang der in `Zusatz.md` definierten Milestones.
- `app/README.md` – UI-/Launcher-Details für das Textual-Frontend.
- `sim/docs/vision_kpis.md` – Legacy-Vision; dient als Inspirationsquelle für KPIs.
- `docs/contributing.md` – Commit- und Branch-Richtlinien (Conventional Commits).

> Hinweis: Der Ordner `client/` enthält historische Prototypen (Godot/Unity) und dient ausschließlich der Referenz. Neue Arbeit findet in `app/` (Python) und `sim/` statt.
