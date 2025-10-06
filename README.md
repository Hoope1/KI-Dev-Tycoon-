# KI Dev Tycoon – Simulation Kernel

Dieses Repository enthält den deterministischen Python-Kern des Mobile-Spiels **KI Dev Tycoon**. Der Code bildet die Grundlage für weitere Ausbaustufen wie Wirtschaftssimulation, Forschungsbäume, Team-Management sowie API-Anbindung.

## Aktueller Stand

- Grundlegende Paketstruktur mit Poetry
- Deterministische Zufallsquelle (`RandomSource`)
- Tick-basierter Zeitgeber (`TickClock`)
- Stark vereinfachte Finanzsimulation inklusive Reputationstracking
- CLI-Befehl `ki-sim run` zur Ausführung einer Beispielsimulation
- Erste Unit-Tests für RNG und Simulation

## Installation

```bash
poetry install --with dev
```

## Simulation ausführen

```bash
poetry run ki-sim run --ticks 30 --seed 42 \
  --daily-active-users 5000 --arp-dau 0.12 --operating-costs 450
```

Das Kommando gibt einen JSON-Snapshot mit Kapital- und Reputationswerten auf stdout aus.

## Tests

```bash
poetry run pytest -q
```

Weitere Linting- und Typprüfungen können gemäß `pyproject.toml` ausgeführt werden.
