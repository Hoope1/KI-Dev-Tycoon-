# AGENTS.md — Leitfaden für OpenAI‑Agenten (Python)

Siehe Gameplan.md **und** 100_schritte_plan.md!
> Folge dem in `100_schritte_plan.md` dokumentierten Ablauf strikt Schritt für Schritt. Markiere einzelne Schritte erst als abgeschlossen, nachdem ihre Ergebnisse umfassend getestet, dokumentiert und mit den in Gameplan.md beschriebenen Zielen abgeglichen wurden.
> **Ziel:** Dieses Dokument macht den Python‑Code der Simulation von **KI‑Dev‑Tycoon** für AI‑Agenten (z. B. OpenAI Codex) eindeutig navigier‑ und erweiterbar. Es standardisiert Struktur, Konventionen, Tests, PR‑Abläufe und automatisierte Checks, damit AI‑Beiträge sofort lauffähig sind und Review‑Aufwand minimal bleibt.

---

## Projektüberblick

**Repository‑Scope:** Backend‑/Simulations‑Kernel des Mobile‑Spiels „KI‑Dev‑Tycoon“. Die Spiel‑Logik (Wirtschaft, Forschung, Events, Idle‑Progression) läuft deterministisch in Python; ein separater Client (z. B. Unity/Godot oder Web) bindet diesen Kernel via API/SDK ein.

**Technologie:** Python ≥ 3.11 · Poetry · FastAPI (optionales API‑Gateway) · Pydantic v2 · pytest · Hypothesis · mypy (strict) · ruff · black · isort · pre‑commit · nox · GitHub Actions · pip‑audit · bandit.

**Läufe:**

```bash
# Setup (lokal)
poetry install --with dev
pre-commit install

# Simulations‑CLI ausführen
poetry run ki-sim --help
poetry run ki-sim run --ticks 365 --seed 42 --profile default

# Dev‑API (optional) starten
poetry run uvicorn ki_dev_tycoon.api.app:app --reload

# Test‑Suite & Checks
poetry run pytest -q
poetry run pytest --cov=ki_dev_tycoon --cov-report=term-missing
poetry run mypy src
poetry run ruff check src tests
poetry run black --check . && isort --check-only .
poetry run pip-audit && poetry run bandit -r src
```

---

## Projektstruktur (für Agenten‑Navigation)

**Wichtige Grundsätze:**

* **Public API** liegt unter `ki_dev_tycoon.*`. Änderungen an Signaturen oder Datenschemata **müssen** als Breaking/Feature Commit gekennzeichnet und getestet werden.
* **Determinismus:** Simulationen nutzen einen injizierbaren RNG (`RandomSource`) und `TimeProvider`. Keine direkten `random.*`‑ oder `datetime.now()`‑Aufrufe in Domänenlogik.

```
/pyproject.toml             # Build, Tools, Black/Ruff/Mypy/pytest‑Config
/poetry.lock
/.pre-commit-config.yaml
/.github/workflows/ci.yml
/Makefile or /noxfile.py    # Conveniences (optional)
/docs/                      # Architektur‑Notizen, Glossare, ADRs
/assets/                    # Balancing‑Daten (CSV/JSON/YAML) – vom Code lesen, nicht generieren
/scripts/                   # Hilfsskripte (Migration, Datengenerierung)
/src/
  ki_dev_tycoon/
    __init__.py
    app.py                  # CLI‑Entrypoint (tycoon‑Loop, Szenario‑Runner)
    config/
      loader.py             # Laden/Validieren von YAML/TOML‑Konfigurationen
      schemas.py            # Pydantic‑Modelle für Config/Assets
    core/
      time.py               # Tick‑/Kalender‑System, Zeitleisten (Ären/Hypes)
      rng.py                # RandomSource, Seeds, Repro‑Utilities
      events.py             # Ereignisbus, Zufalls‑/Skript‑Events (z. B. KI‑Winter)
      state.py              # GameState, Serialisierung, Snapshots
    economy/
      cashflow.py           # Einnahmen/Kosten, Schulden, Zinsen, CAPEX/OPEX
      pricing.py            # Preis‑ und Nachfragefunktionen
      kpis.py               # Metriken (MAU, Retention, Reputation)
    research/
      tech_tree.py          # Forschungsbaum (Transformer, RL, Gen‑KI …)
      unlocks.py            # Gates/Abhängigkeiten
      training.py           # Daten/Compute/Infra‑Invest & Lernkurven‑Sim
    projects/
      catalogue.py          # Projekt‑/Produkt‑Typen (Chatbot, Vision, AV …)
      simulator.py          # Erfolgschancen, Qualität, Time‑to‑Market
      licensing.py          # Produkt vs. API/Lizenz‑Erlöse
    team/
      people.py             # Rollen/Skills (DS/DE/Research/Ethics)
      productivity.py       # Synergien, Training, Burnout/Fokus
      hiring.py             # Recruiting‑Pipelines, Kosten
    ethics/
      compliance.py         # Datenschutz, Bias‑Risiko, Regulatorik‑Ereignisse
      reputation.py         # Reputationseffekte auf Nachfrage/Verträge
    market/
      trends.py             # Trend‑Signale, Hype‑Zyklen
      marketing.py          # Kampagnen, Investor‑Verhandlungen
    idle/
      offline.py            # Offline‑Progression (Δt‑Verarbeitung, Caps)
    api/
      app.py                # FastAPI‑App (Read‑Only Sim‑Adapter)
      dto.py                # Pydantic DTOs (stabile API‑Schicht)
    persistence/
      savegame.py           # Save/Load (JSON), Migrations
    utils/
      validation.py         # Eingabeprüfungen, Fehlerklassen
      logging.py            # Strukturierte Logs
/tests/
  unit/                     # Modultests, schnelle Ausführung
  property/                 # Hypothesis‑Suiten (Ökonomie/Event‑Invarianten)
  integration/              # End‑to‑End (Szenario‑Seeds)
  api/                      # Contract‑Tests für FastAPI
  data/                     # Testdaten, Golden‑Snapshots
/benchmarks/                # pytest‑benchmark‑Szenarien
```

**Nicht editieren (durch Agenten):** `/assets/**`‑Rohdateien, Binär‑Artefakte, generierte Coverage‑/Cache‑Ordner. Änderungen an Assets **erfordern** Snapshot‑Updates & Balancing‑Checks (siehe unten).

---

## Coding Conventions (Python‑spezifisch)

* **Stil & Linting**: `black` (line‑length 88), `isort` (profile=black), `ruff` (Lint + Import‑Ordnung). Keine ungenutzten Exporte.
* **Typing**: `mypy --strict`. Öffentliche Funktionen/Datenmodelle **müssen** vollständige Typannotationen tragen. `TypedDict`/`Protocol` wo sinnvoll.
* **Datenmodelle**: Pydantic v2 (`BaseModel`, `field_validator`). Datums/Zeit über `time.py` abstrahieren.
* **Fehlerbehandlung**: Eigene `DomainError`‑Hierarchie; Exceptions sind Teil der Funktionssignaturen (Docstring „Raises“).
* **Determinismus**: RNG/Time via Dependency‑Injection. Reine Funktionen bevorzugen; Seiteneffekte explizit kapseln.
* **Dokstrings**: Google‑Stil. Beispiel:

```python
def run_tick(state: GameState, *, rng: RandomSource) -> GameState:
    """Advance the simulation by one tick.

    Args:
        state: Immutable snapshot of current game state.
        rng: Deterministic random source.

    Returns:
        New immutable state after applying economy/research updates.

    Raises:
        DomainError: On invalid transitions (e.g., negative cash beyond allowed debt).
    """
```

* **Logging**: Strukturierte Logs (`utils.logging`) mit Event‑Name, Tick, Seed, Dauer. Keine sensiblen Daten loggen.
* **Performance**: Heißpfade (z. B. `projects.simulator`) sind O(N) pro Tick; Allokationen minimieren; Benchmark‑Suiten bewahren Budgets.

---

## Testing Requirements

**Frameworks:** `pytest`, `pytest-cov`, `hypothesis`, `pytest-benchmark`, `requests`/`httpx` für API‑Tests.

**Abdeckung:** Mindest‑Coverage **90 % Lines/Branches** für `src/ki_dev_tycoon/**` (ausgenommen `api/app.py`).

**Testarten & Invarianten:**

1. **Unit‑Tests (deterministisch):**

   * Ökonomie: Cashflow nie NaN/Inf; keine impliziten Rundungsfehler; Schuldenobergrenze eingehalten.
   * Forschung: Unlock‑Gates strikt; Zyklen im Tech‑Tree verboten; Trainingskurven monoton nicht‑fallend.
   * Team: Produktivität ∈ [0, cap]; Training erhöht Skill, Burnout senkt temporär.
   * Offline‑Progression: `apply_offline(delta)` ist idempotent für `delta=0` und **monoton** für `delta>0`.

2. **Property‑Based (Hypothesis):**

   * Ereignisgenerator: Keine Dead‑Ends; Wahrscheinlichkeitssummen ≈ 1; verbotene Zustände unerreichbar.
   * Preis/Nachfrage: Elastizität bleibt innerhalb definierter Bandbreiten; negative Nachfrage unmöglich.
   * Persistenz: `state == load(save(state))` (Round‑Trip) bei festen Seeds & Versionen.

3. **Integration/Scenario:**

   * Seeds `{1, 7, 42, 1337}` über 1 In‑Game‑Jahr laufen **ohne Fehler** und erfüllen KPI‑Schranken (z. B. kein Bankrott im Tutorial‑Profil).
   * Produkt vs. Lizenzmodell: Beide Pfade liefern Einnahmen; Margen‑Differenzen im erwarteten Bereich.

4. **API‑Contract (optional):**

   * FastAPI‑Schemas entsprechen DTO‑Versionen; Abwärtskompatibilität via SemVer.

5. **Snapshots & Balancing:**

   * Golden‑Snapshots für `/assets/**` → `tests/data/` aktualisieren nur mit „balance‑approved“ PR‑Label. Änderungen prüfen Metriken (Durchschnittsprofit, Progressionstempo).

6. **Performance‑Budgets:**

   * `projects.simulator` ≤ **2 ms** pro Tick (Durchschnitt, CI‑Runner) bei Referenzszenario.

**Befehle:**

```bash
poetry run pytest -q
poetry run pytest tests/property -q
poetry run pytest --cov=ki_dev_tycoon --cov-report=term-missing
poetry run pytest --benchmark-only
```

---

## PR‑Richtlinien

* **Branches:** `feature/<kurz-beschreibung>`, `fix/<ticket>`, `chore/<bereich>`.

* **Commits:** Conventional Commits (`feat:`, `fix:`, `refactor:`, `perf:`, `test:`, `docs:` …). Breaking Changes via `!` oder `BREAKING CHANGE:`.

* **PR‑Größe:** ≤ ~400 LOC netto. Größere PRs in logisch getrennte Teile splitten.

* **Checklist (muss erfüllt sein):**

  1. [ ] Tests hinzugefügt/aktualisiert (inkl. Property‑/Snapshot‑Tests, falls betroffen)
  2. [ ] `pre-commit run -a` grün (black, isort, ruff, mypy, bandit, pip‑audit)
  3. [ ] Changelog/Docs aktualisiert (falls Public API/Assets)
  4. [ ] Performance‑Budgets eingehalten (Benchmarks belegt)
  5. [ ] Repro‑Seed in PR‑Beschreibung (bei Sim‑Änderungen)

* **Review‑Fokus:** Public‑API‑Stabilität, Determinismus, Balancing‑Effekte, Sicherheits‑/Compliance‑Aspekte (Ethik/Reputation), Performance.

---

## Programmatic Checks (CI/CD & lokale Hooks)

**pre‑commit Hooks (Auszug):**

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks: [{ id: black }]
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks: [{ id: isort }]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.8
    hooks: [{ id: ruff }]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks: [{ id: mypy, additional_dependencies: [pydantic] }]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks: [{ id: bandit }]
  - repo: https://github.com/pypa/pip-audit
    rev: v2.7.3
    hooks: [{ id: pip-audit }]
  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks: [{ id: codespell }]
  - repo: https://github.com/jumanjihouse/pre-commit-hooks
    rev: 3.0.0
    hooks:
      - { id: markdownlint }
      - { id: shellcheck }
  - repo: local
    hooks:
      - id: validate-assets
        name: Validate balancing assets (YAML/JSON schemas)
        entry: poetry run python scripts/validate_assets.py
        language: system
        files: ^assets/.*\.(ya?ml|json)$
```

**GitHub Actions (Kurzform):**

* `ci.yml` Matrix {python: ["3.11", "3.12"]} · Schritte: `poetry install --with dev` → Ruff/Black/Isort → mypy → pytest (Coverage ≥ 90 %) → pip‑audit → bandit → Benchmark Smoke.
* `release.yml` (optional): Tag‑Release erstellt Wheel, veröffentlicht internen Artefakt‑Build oder PyPI (privat).

**Policy‑Checks zur Laufzeit:**

* Assertions in Debug‑Builds: Kein negativer Cash < erlaubter Verschuldungsgrenze; Reputation ∈ [0, 100]; Nachfrage ≥ 0; RNG‑Seed gesetzt; Zeit monoton.
* Feature‑Flags: Neue Systeme (z. B. „Quanten‑KI“) hinter Flag + Migrationsskript.

---

## Erweiterungsleitfaden für Agenten (Do/Don’t)

**Bevorzugte Erweiterungspunkte:**

* Neue Projekt‑/Produkt‑Typen → `projects/catalogue.py` + Logik in `projects/simulator.py` + DTOs in `api/dto.py`.
* Neue Forschung (Algorithmen/Anwendungen) → `research/tech_tree.py` & `research/unlocks.py` + Asset‑Einträge.
* Markt‑/Event‑Typen → `market/trends.py` bzw. `core/events.py` mit klaren Wahrscheinlichkeiten.

**Do:**

* Schreibe reine, typisierte Funktionen. Akzeptiere `rng: RandomSource` & `clock: TimeProvider` als Parameter.
* Halte Persistenz kompatibel: Migration in `persistence/savegame.py` + Round‑Trip‑Tests.
* Dokumentiere Wirkungsfunktionen (z. B. Preis‑Elasticität) als Formel im Docstring.

**Don’t:**

* Keine direkten Netzwerk‑/Datei‑Zugriffe in Domänenlogik.
* Assets in `/assets/` nicht „on‑the‑fly“ ändern; stattdessen PR + Snapshot‑Update.
* Kein globaler Zustand; keine versteckten Singletons.

**Beispiel‑Workflow: Neues Forschungsfeld „Quanten‑KI“**

1. Asset‑Eintrag in `/assets/research.yaml` (Kosten, Gates, Effekte). 2) `research/tech_tree.py` um Node + Validierungen erweitern. 3) Effekt‑Hook in `projects/simulator.py` (z. B. Trainingszeit‑Modifier). 4) Tests: Unit (Gate/Effekt), Property (keine Zyklen), Snapshot (Assets), Integration (Seed‑Szenario). 5) Benchmarks aktualisieren.

---

## Daten‑/Konfig‑Schemata

* **Assets**: YAML/JSON, per Pydantic validiert. Schema‑Dateien liegen unter `config/schemas.py`.
* **Versionierung**: `assets_version` im Savegame + Migrationspfad.
* **Lokalisierung**: Schlüssel in Assets (z. B. `i18n.key`), kein UI‑Text im Kernel.

---

## Sicherheits‑ & Compliance‑Hinweise

* **Keine** personenbezogenen Daten in Logs/Assets/Tests.
* `bandit`‑Warnungen beheben/unterdrücken nur mit Begründung.
* Abhängigkeiten via `pip‑audit` regelmäßig prüfen; unsichere Versionen blockieren.

---

## Glossar (domänenspezifisch)

* **Idle‑Mechanik**: Fortschritt während Inaktivität, berechnet aus Δt zwischen Saves.
* **Hype‑Zyklus**: Ära‑abhängige Multiplikatoren für Nachfrage/Forschung.
* **Reputation**: Skala 0–100, konditioniert Marketing/Verträge/Ereignisse.

---

## Kontakt & Ownership

* **Codeowners**: `docs/CODEOWNERS` pflegt Reviewer‑Zuständigkeiten.
* **Architekturentscheidungen**: ADRs unter `/docs/adr/`.
* **Fragen**: Issues mit Label `question` + reproduzierbarem Seed/Szenario eröffnen.

---

> **Kurzfassung für Agenten:** Halte die Simulation deterministisch, strikt typisiert und getestet. Änderungen an Public‑API und Assets sind versions‑ und snapshot‑pflichtig. Führe alle lokalen/CI‑Checks aus, bevor du Code vorschlägst oder PRs erstellst.
