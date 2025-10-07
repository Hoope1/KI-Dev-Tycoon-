# KI Dev Tycoon – Simulation Kernel (Python Support Stack)

Dieses Verzeichnis enthält den deterministischen Python-Simulationskern, der für Balancing-Experimente, Property-Tests, UI-Anbindung und Tooling rund um den Steam-MVP von **KI Dev Tycoon** eingesetzt wird. Laut [`Zusatz.md`](../Zusatz.md) bildet dieser Kernel gemeinsam mit dem Textual-Frontend das vollständige Produkt.

## Aktueller Stand

- Paketstruktur mit Poetry (`sim/pyproject.toml`).
- Deterministische Zufallsquelle (`RandomSource`) und Tick-Zeitgeber (`TickClock`).
- Ökonomische Module (Cashflow, Nachfrage, Reputation) + Forschung/Hiring.
- CLI-Befehl `ki-sim` zur Ausführung deterministischer Beispielsimulationen.
- Unit-, Property- und Integrationstests für RNG, Simulation, Persistenz.

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

## API-Adapter (optional)

Der optionale FastAPI-Adapter stellt unter `/state` deterministische States bereit. Damit lassen sich UI-Prototypen, externe Tools oder Mods anbinden.

```bash
poetry run uvicorn ki_dev_tycoon.api.app:app --reload
# oder als Python-Modul:
poetry run python -m uvicorn ki_dev_tycoon.api.app:app --reload
```

Die Antwortstruktur wird über Pydantic-DTOs in `ki_dev_tycoon/api/dto.py` beschrieben.

## Tests

```bash
poetry run pytest -q
poetry run pytest --cov=ki_dev_tycoon --cov-report=term-missing
poetry run mypy src
```

Weitere Linting- und Typprüfungen können gemäß `pyproject.toml` und `noxfile.py` ausgeführt werden. Erkenntnisse aus den Simulationen sind regelmäßig mit den Vorgaben aus `Zusatz.md` und den UI/Build-Anforderungen zu synchronisieren (Seeds, KPIs, Formeln).

## Code-Qualität & Automatisierung

- `pre-commit install` aktiviert lokale Hooks (black, isort, ruff, mypy, pytest).
- `nox -l` listet verfügbare Sessions.
- `nox -s lint typecheck tests` führt alle Kernprüfungen aus.
- `nox -s build` erzeugt PyInstaller-Smoke-Builds (siehe `app/tools`).
