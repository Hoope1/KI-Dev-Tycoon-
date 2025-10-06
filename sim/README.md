# KI Dev Tycoon – Simulation Kernel (Python Support Stack)

Dieses Verzeichnis enthält den deterministischen Python-Simulationskern, der für Balancing-Experimente, Property-Tests und Tooling rund um den Steam-MVP von **KI Dev Tycoon** eingesetzt wird. Die produktive Implementierung erfolgt laut [`Zusatz.md`](../Zusatz.md) in Unity/C#, doch der Python-Stack bleibt für schnelle Iterationen, Datenexporte und Regressionstests bestehen.

## Aktueller Stand

- Paketstruktur mit Poetry (`sim/pyproject.toml`).
- Deterministische Zufallsquelle (`RandomSource`) und Tick-Zeitgeber (`TickClock`).
- Vereinfachte Finanzsimulation inklusive Reputationstracking.
- CLI-Befehl `ki-sim` zur Ausführung deterministischer Beispielsimulationen.
- Unit- und Property-Tests für RNG, Simulation und Persistenz.

## Installation

```bash
poetry install --with dev
```

## Simulation ausführen

```bash
poetry run ki-sim --ticks 30 --seed 42 \
  --daily-active-users 5000 --arp-dau 0.12 --operating-costs 450
# Optional: detaillierte Tick-Ausgaben aktivieren
# poetry run ki-sim --ticks 5 --log-level DEBUG
```

Das Kommando gibt einen JSON-Snapshot mit Kapital- und Reputationswerten auf stdout aus.

## API-Adapter (Preview)

Der optionale FastAPI-Adapter stellt unter `/state` deterministische Dummy-States bereit. Damit lassen sich UI-Prototypen oder Analyse-Tools speisen, bis der Unity-Kernel (siehe `Zusatz.md`) voll funktionsfähig ist.

```bash
poetry run uvicorn ki_dev_tycoon.api.app:app --reload
# oder als Python-Modul:
poetry run python -m uvicorn ki_dev_tycoon.api.app:app --reload
```

Die Antwortstruktur wird über Pydantic-DTOs in `ki_dev_tycoon/api/dto.py` beschrieben.

## Tests

```bash
poetry run pytest -q
```

Weitere Linting- und Typprüfungen können gemäß `pyproject.toml` ausgeführt werden. Erkenntnisse aus den Python-Simulationen sind regelmäßig mit den Vorgaben aus `Zusatz.md` und den C#-Implementierungen zu synchronisieren (Seeds, KPIs, Formeln).

## Code-Qualität & Automatisierung

- `pre-commit install` aktiviert lokale Hooks (Black, isort, Ruff, mypy, pytest).
- `nox -l` listet verfügbare Sessions.
- `nox -s lint typecheck tests` führt alle Kernprüfungen aus.
