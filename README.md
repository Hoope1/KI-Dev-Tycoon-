# KI-Dev-Tycoon Monorepo

Dieses Repository bündelt den Simulations-Kernel (`/sim`) und den zukünftigen Spiel-Client (`/client`) des Projekts **KI-Dev-Tycoon**.

## Strukturüberblick

```
/README.md              # Diese Übersicht
/100_schritte_plan.md   # Schrittweiser Ausführungsplan (verbindlich)
/Gameplan.md            # GDD/PRD mit Vision, Systemdesign & KPIs
/client/                # Placeholder für Unity-/Godot-Client
  README.md             # Aktueller Stand & nächste Schritte für den Client
/sim/                   # Python-Simulationskernel
  README.md             # Technische Details & Nutzungshinweise
  pyproject.toml        # Poetry-Konfiguration
  src/                  # Python-Quellcode (Paket `ki_dev_tycoon`)
  tests/                # Test-Suites (pytest/hypothesis)
  docs/                 # Simulationsspezifische Dokumentation & Artefakte
```

## Erste Schritte (Simulation)

1. Wechsle in den Ordner `sim/`.
2. Installiere die Python-Abhängigkeiten mit Poetry (`poetry install --with dev`).
3. Führe Tests und Lints via `poetry run pytest`, `poetry run mypy`, `poetry run ruff check` aus.

## Erste Schritte (Client)

*Der Client ist noch nicht initialisiert.* Sobald die Engine gewählt wurde, werden hier Setup-Anweisungen ergänzt.

## Weiterführende Dokumente

* `AGENT.md` – Arbeitsanweisungen & Coding-Guidelines für alle Agent:innen.
* `Gameplan.md` – Vollständiger Produktions- und Game-Design-Plan.
* `100_schritte_plan.md` – Priorisierte Arbeitsliste mit Abnahmekriterien.
* `sim/docs/vision_kpis.md` – Vision & KPI-Rahmen für das Projekt.
* `docs/contributing.md` – Commit- und Branch-Richtlinien (Conventional Commits).
