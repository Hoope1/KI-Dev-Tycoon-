# KI-Dev-Tycoon Monorepo

Dieses Repository bündelt alle Assets für die Solo-MVP-Umsetzung von **KI-Dev-Tycoon** auf Steam (Windows x64, offline). Quelle aller verbindlichen Entscheidungen ist [`Zusatz.md`](./Zusatz.md); sämtliche weiteren Dokumente erweitern oder konkretisieren diesen Anhang.

## Strukturüberblick

```
/README.md              # Diese Übersicht
/Zusatz.md              # Source of truth (Steam-MVP, Solo-Dev, ≤ €500)
/100_schritte_plan.md   # Umsetzungsschritte, nach Zusatz.md strukturiert
/Gameplan.md            # Ergänzende Ableitungen & Referenzen
/client/                # Unity 6 Client-Grundgerüst
  README.md             # Setup- und Build-Anweisungen für Unity
/sim/                   # Python-Simulationskernel (Prototyping & Tests)
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

Der Unity-Client bildet das UI- und Plattform-Frontend. Folge den Anweisungen in [`client/README.md`](client/README.md), um Unity 6 LTS zu installieren, das Projekt zu öffnen und Builds zu erzeugen. Die Implementierung orientiert sich strikt an den Architekturvorgaben aus `Zusatz.md` (deterministischer Kernel, 0,5 s Tick, Steamworks.NET für Achievements).

## Weiterführende Dokumente

- `Zusatz.md` – Primäre Produktspezifikation (Steam-MVP, Solo-Dev, ≤ €500).
- `AGENT.md` – Arbeitsanweisungen & Coding-Guidelines für alle Agent:innen.
- `Gameplan.md` – Ergänzende Ableitungen (Loops, Referenzen, Visual Style) zum Zusatz.
- `100_schritte_plan.md` – Schrittplan entlang der in `Zusatz.md` definierten Milestones.
- `sim/docs/vision_kpis.md` – Legacy-Vision; dient als Inspirationsquelle für KPIs.
- `docs/contributing.md` – Commit- und Branch-Richtlinien (Conventional Commits).
