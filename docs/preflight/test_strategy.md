# Test- & QA-Strategie — KI-Dev-Tycoon (Preflight Schritt 9)

Diese Strategie deckt Unit-, Property- und Integrationstests für den deterministischen Sim-Kernel sowie Textual-/CLI-spezifische Prüfungen ab. Grundlage sind die Vorgaben aus `Zusatz.md` (Coverage ≥ 90 %, deterministische Seeds).

## Testebenen
1. **Unit-Tests (Python)**
   - Ziel: Einzelne Systeme (`core.time`, `core.rng`, `core.economy`, `core.research`).
   - Framework: pytest (`tests/unit/...`).
   - Seeds: `SEED_CORE = 1337` (Global), Sub-Seeds pro Modul (`rng`, `hiring`, `events`).
2. **Property-Tests**
   - Ziel: Invarianten wie `quality ∈ [0,1]`, `cash ≥ 0`, `adoption ≤ tam`, `reputation ∈ [0,100]`.
   - Framework: Hypothesis; Seeds über `PY_SEED = 20251006`.
3. **Integrationstests / Headless Runner**
   - CLI: `poetry run ki-sim run --ticks 17280 --seed 424242 --profile default` (30 Tage) exportiert KPI-CSV.
   - Validierung: KPI-Snapshots mit Toleranzen (±2 %).
4. **Textual UI Tests**
   - `textual.testing` für Screens/Widgets (Snapshot- und Interaktionstests).
   - Fokus: Navigation, Accessibility (Themes), Save/Load-Flow.
5. **API/CLI Contract Tests**
   - FastAPI TestClient (`ki_dev_tycoon.api`) → Response-Schemas, deterministische Seeds.
   - Typer CLI Tests via `CliRunner` (Click/Typer) mit Fixtures.

## Seed-Plan
- **Global Simulation Seed:** `424242` (Production default) – referenziert in Savegames.
- **Testing Seeds:**
  - Unit/Core: `1337` (Tick, RNG, Economy), `7331` (Team/Hiring), `9001` (Events).
  - Property Tests: `20251006` per `PY_SEED` Environment.
  - Integration/Headless: `424242` (baseline) + `424243` (regression alt).
  - UI Snapshots: `TEXTUAL_SEED = 5150` (eingebettet im Test-Fixture).
- Seeds werden in `docs/testing/seeds.md` (später) versioniert.

## Tooling
- **Python:** `poetry run pytest`, `poetry run pytest --maxfail=1 --disable-warnings`, `poetry run mypy`, `poetry run ruff check`.
- **Textual:** `textual-devtools` für manuelle QA, Snapshot-Recorder.
- **CI:** GitHub Actions Matrix (Python 3.11/3.12) mit nox-Sessions (`lint`, `typecheck`, `tests`, `build`).

## Reporting
- KPI-CSV in `artifacts/tests/<date>/kpi_<seed>.csv`.
- Coverage-Reports via `pytest --cov=ki_dev_tycoon --cov-report=term-missing`.
- Textual-Snapshots unter `app/tests/snapshots/` versionieren.
- Fehlgeschlagene Tests erstellen Issues mit Seed + Repro-Schritten.

> **Next Steps:** Einrichtung der Testpakete in Woche 1 (Schritte 15–24) und Anlegen eines `docs/testing`-Ordners zur Seed-Versionierung.
