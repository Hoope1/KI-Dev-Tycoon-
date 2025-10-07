# Test- & QA-Strategie — KI-Dev-Tycoon (Preflight Schritt 9)

Diese Strategie deckt Unit-, Property- und Integrationstests für den deterministischen Sim-Kernel sowie Client-spezifische Prüfungen ab. Grundlage sind die Vorgaben aus `Zusatz.md` (Coverage ≥ 90 %, deterministische Seeds).

## Testebenen
1. **Unit-Tests (C#)**
   - Ziel: Einzelne Systeme (`Core.Sim.Time`, `Core.Sim.Rng`, `Core.Sim.Economy`).
   - Framework: NUnit (Unity Test Framework) im EditMode.
   - Seeds: `SeedCore = 1337` (Global), Sub-Seeds pro Modul (`rng`, `hiring`, `events`).
2. **Property-Tests (Python-Prototyp)**
   - Ziel: Invarianten wie `Quality ∈ [0,1]`, `Cash ≥ 0`, `Adoption ≤ TAM`.
   - Framework: Hypothesis über `sim/`-Paket; Seeds `PY_SEED = 20251006`.
3. **Integrationstests / Headless Runner**
   - Unity Batchmode (`-runTests`) simuliert 30 Ingame-Tage, exportiert KPI-CSV.
   - CLI: `Unity.exe -batchmode -projectPath <path> -executeMethod Game.Tests.Headless.Run -seed 424242 -days 30 -output kpi.csv`.
   - Validierung: KPI-Snapshots mit Toleranzen (±2 %).
4. **PlayMode Smoke Tests**
   - Automatisierte Szenen-Loads, Tab-Wechsel, Save/Load Roundtrip.
   - Seeds über `Game.App.Config` injizieren (Default `424242`).

## Seed-Plan
- **Global Simulation Seed:** `424242` (Production default) – referenziert in Savegames.
- **Testing Seeds:**
  - Unit/Core: `1337` (Tick, RNG, Economy), `7331` (Team/Hiring), `9001` (Events).
  - Property Tests (Python): `20251006` per `PY_SEED` Environment.
  - Integration/Headless: `424242` (baseline) + `424243` (regression alt).
- Seeds werden in `docs/testing/seeds.md` (später) versioniert.

## Tooling
- **Unity:** `UnityEditor.TestTools` für Edit-/PlayMode.
- **Python:** `poetry run pytest`, `poetry run pytest --maxfail=1 --disable-warnings`, `poetry run mypy`.
- **CI:** GitHub Actions Matrix (Python 3.11/3.12 + Unity Batch Build).

## Reporting
- KPI-CSV in `artifacts/tests/<date>/kpi_<seed>.csv`.
- Coverage-Reports (C# via dotCover oder Unity Coverage Package, Python via `pytest --cov`).
- Fehlgeschlagene Tests erstellen Issues mit Seed + Repro-Schritten.

> **Next Steps:** Einrichtung der Testprojekte in Woche 1 (Schritte 15–24) und Anlegen eines `docs/testing`-Ordners zur Seed-Versionierung.
