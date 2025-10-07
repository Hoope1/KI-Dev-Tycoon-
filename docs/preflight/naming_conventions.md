# Naming- & Namespace-Konventionen — KI-Dev-Tycoon (Preflight Schritt 6)

Die folgenden Konventionen leiten sich aus `Zusatz.md` ab und gelten für alle Python-Pakete (`sim/`, `app/`, `tools/`) sowie ergänzende Dokumente. Sie stellen sicher, dass der deterministische Sim-Kernel klar von UI-, API- und Build-Schichten getrennt bleibt.

## Python Pakete

- **`ki_dev_tycoon.core`** — Deterministischer Simulationskernel. Unterpakete:
  - `core.time`, `core.rng`, `core.economy`, `core.research`, `core.team`, `core.market`, `core.persistence`.
- **`ki_dev_tycoon.data`** — Asset-Lader & Schemas (`config.loader`, `config.schemas`).
- **`ki_dev_tycoon.ui`** — Textual-App (Screens, Widgets, Presenter, Theme-System).
- **`ki_dev_tycoon.api`** — Optionale FastAPI-Schicht (Read-Only Sim-Adapter).
- **`ki_dev_tycoon.cli`** — Typer-Kommandos (`ki-sim`, `ki-ui`, `ki-api`).
- **`ki_dev_tycoon.platform`** — Integrationen (Steamworks, OS-spezifische Adapter).
- **`ki_dev_tycoon.tests`** — Test-Hilfsfunktionen (Factories, Fixtures, Faker).

## Dateien & Ordner

- Modulpfade spiegeln Paketstruktur (`app/src/ki_dev_tycoon/ui/screens/dashboard.py`).
- Assets in `assets/` nutzen Kebab-Case (`roles.basic.yaml`, `events.launch.yaml`).
- Tests liegen gespiegelt zu den Modulen (`tests/core/test_economy.py`, `app/tests/ui/test_dashboard.py`).
- Tools/Build-Skripte in `tools/` verwenden Snake-Case (`build_app.py`, `steam_upload.py`).
- Konfigurationsdateien (`pyproject.toml`, `noxfile.py`, `.pre-commit-config.yaml`) definieren Formatierung (black, isort, ruff) als Single Source of Truth.

## Coding-Standards (Kurzfassung)

- Strikte Typannotationen (`from __future__ import annotations`, `mypy --strict`).
- Funktionen nehmen `RandomSource` und `TimeProvider` als explizite Parameter.
- Öffentliche APIs dokumentieren Docstrings (reStructuredText), verwenden aussagekräftige Parameter.
- Module vermeiden Seiteneffekte (keine IO bei Import). CLI/Entry Points unter `if __name__ == "__main__":` vermeiden.
- Tests nutzen `pytest` + `hypothesis`. Assertions sind aussagekräftig (`assert actual == expected` mit Fehlermeldung).

## Textual UI

- Screens `PascalCaseScreen` (z. B. `DashboardScreen`), Widgets `PascalCase`, CSS-IDs `kebab-case` (`#cash-panel`).
- Actions benennen: `action_save_game`, `action_switch_tab` (Snake Case).
- Themes liegen in `app/src/ki_dev_tycoon/ui/themes/`, Dateien `theme_dark.css`, `theme_light.css`.

## CLI & Tools

- Typer-Kommandos im Verb-Substantiv-Stil (`ki-sim run`, `ki-ui record`, `ki-api serve`).
- Logging-Namen `ki_dev_tycoon.<bereich>` (z. B. `ki_dev_tycoon.core.economy`).
- Build-Skripte geben Exit-Code ≠0 bei Fehlern zurück, nutzen `argparse` oder Typer.

> **Wartung:** Neue Systeme müssen die Namenskonventionen in Pull Requests dokumentieren. Abweichungen sind nur mit expliziter ADR erlaubt.
