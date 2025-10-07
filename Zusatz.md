# Zusatz — KI-Dev-Tycoon (Steam-MVP, Solo-Dev, ≤ €500)

*Stand: 06.10.2025 (Europe/Vienna)*

Dieses Dokument ist die zentrale Referenz für alle Architektur-, Design- und Produktionsentscheidungen des Projekts **KI-Dev-Tycoon**. Ziel ist eine sofort umsetzbare Solo-MVP-Umsetzung auf Steam (Windows, offline) mit einem einmaligen Kaufpreis von €5.99 und einem Gesamtbudget ≤ €500. Sämtliche Komponenten werden ausschließlich mit Python 3.11+ und frei verfügbaren Paketen umgesetzt; es existieren keine Abhängigkeiten zu proprietären Engines oder externen Services.

---

## 1) Entscheidungen & Projektleitplanken (Summary)

- **Plattform (MVP):** Steam (Windows x64, Desktop) — Distribution via PyInstaller-Bundle
- **Team & Budget:** Solo-Entwickler:in, Gesamtbarbudget ≤ €500
- **Technologie-Stack:** Python 3.11+, Poetry, Textual (TUI) + Rich, FastAPI (lokale API), Pydantic v2, SQLModel/SQLite, Typer-CLI, pytest/hypothesis, mypy (strict), ruff, black, isort, pre-commit, nox, pip-audit, bandit, PyInstaller
- **Online/Cloud:** Kein Backend, keine Cloud-Komponenten, reine Offline-Simulation; optionale lokale API für Mods
- **Monetarisierung:** Paid up-front (€5.99), keine Ads, keine IAPs
- **Region (Launch-Pflicht):** Fokus Österreich (Steam-Release weltweit zulässig)
- **Architektur:** Monorepo mit Python-Paketen `ki_dev_tycoon` (Simulation/Core), `ki_dev_tycoon.ui` (Textual-Frontend), `ki_dev_tycoon.api` (lokale FastAPI)
- **Tick-Rate:** Fix 0,5 s (Accumulator-Loop) — deterministisch über injizierbare RNG/Clock
- **Achievements:** In-Game-Achievement-System; Steam-Achievements optional via `steamworks`-Python-Binding (Wrap über lokales SDK)
- **Lokalisierung & Accessibility:** EN/DE, skalierbare Schriftgrößen im TUI, Screenreader-freundliche Struktur, reduzierbare Animationen, vollständige Tastatursteuerung
- **Art-Direction:** „Tycoon bunt“ über Rich-Themes/ASCII-Art; optionale einfache Tiles mit `textual.widgets`
- **Nicht-Ziele (MVP):** Keine Ads/IAPs/Push/Telemetry-Cloud/PvP/UGC/Always-Online, kein Zwang zu nativen GUIs außerhalb Textual

---

## 2) Background

**Produktidee & Zielsetzung.** Desktop-Tycoon, der den Aufbau eines KI-Unternehmens simuliert. Fokus: glaubwürdige KI-Anspielungen, Sessions 5–20 Minuten, langfristige Meta-Progression, faire Monetarisierung. Das komplette Spielerlebnis (Simulation + UI + Persistence) läuft innerhalb einer Python-Laufzeit und kann headless getestet werden.

**Plattform & Audience.** Windows (Steam, 16:9 Terminal/Fenster über Textual, Maus optional), Zielgruppe 16–45, tech-affin.

**Erfolgsmaße (Post-Launch-Gate).** Wishlist→Kauf-Conversion ≥ 10 % am Launch-Tag, Refund-Rate ≤ 8 %, ≥ 75 % positive Reviews (n≥20), Crash-Rate ≤ 0,3 %.

**Architektur-Leitplanken.** Simulation deterministisch (Seed/Time-Injection), Tests ≥ 90 % Coverage, stabile API/Versionierung, CI/CD mit Lint/Typing/Tests. Keine Engine-spezifischen Abhängigkeiten; sämtliche Assets (JSON/YAML) werden über Pydantic-Modelle validiert. UI und API konsumieren ausschließlich die publizierte Python-API.

**Prozess.** Source of Truth: dieses Dokument. Balancing-Assets nur via Review. Seeds/Snapshots reproduzierbar halten. Jeder Build entsteht aus Poetry-Lockfile und wird via PyInstaller reproduzierbar erzeugt.

---

## 3) Requirements (MoSCoW)

**Must**

- Budget/Team: Solo-Dev, ≤ €500 (inkl. Gebühren/Assets/Store)
- Plattform: Windows (Steam), 16:9 Terminalfenster (min. 120×40 Zeichen), Ziel 60 FPS bei TUI-Refresh; Distribution via PyInstaller
- Offline-Only: deterministische Tick-Simulation, lokale Save-Slots + Migration; kein Backend
- Kern-Loops: Hiring, Forschung (Modelle/Datasets), Training (Kosten/Qualität), Produkt-Launches, Umsatz/Skalierung, Events
- Monetarisierung: €5.99, ohne Ads/IAPs
- Distribution: Veröffentlichung mindestens in Österreich (Steam-Depot mit PyInstaller-Build)
- Compliance: GDPR-freundlich; minimale Berechtigungen; keine externen Tracker
- Lokalisierung & Accessibility: EN/DE, skalierbare Schrift über Textual-Themes, farbenblind-freundliche Farbpalette, vollständige Tastaturbedienbarkeit
- Build/CI: Poetry + nox, deterministischer Kernel (Tests ≥ 90 %), Lint/Static-Analysis, Nightly Headless-Sim-Runs

**Should**

- Store-Assets: 30–45 s Trailer (Screen Capture Textual UI), 6 Screenshots, Key-Art (ASCII/Vector)
- Steam-Deck-Check: Test PyInstaller-Build im Steam-Deck-Kompatibilitätsmodus
- Optionale Demo: eigenständiger PyInstaller-Demo-Build (begrenzte Spielzeit)

**Could**

- Rich-Grafiken via `textual` Canvas, partielle Soundeffekte via `simpleaudio`
- Modding-Hooks über JSON-Assets + CLI-Loader

**Won't (MVP)**

- Native 3D/2D-Engine, Touch/Controller-Support, Online-Services, externe Telemetrie, Always-Online, PvP, UGC

---

## 4) Method (Technische Methode)

### 4.1 Architektur (Steam · Offline · Solo-Dev · Python)

**Runtime & Packaging.** Python 3.11 (embedded via PyInstaller OneFile/OneDir). Windows-Installer optional via `briefcase` oder `Inno Setup` Script.

**Module.**

- `ki_dev_tycoon.core` — deterministischer Sim-Kernel (Pydantic-Modelle, Services, Tick-Loop)
- `ki_dev_tycoon.data` — statische Balancing-Daten (YAML/JSON) + Loader (`config/schemas.py`)
- `ki_dev_tycoon.persistence` — Save/Load (JSON + optional SQLite), Versionierung & Migrationen
- `ki_dev_tycoon.ui` — Textual-App (Screens, Widgets, Presenter-Schicht)
- `ki_dev_tycoon.api` — optionale FastAPI für externe Tools/Mods
- `ki_dev_tycoon.cli` — Typer-Befehle (`ki-sim`, `ki-admin`, `ki-ui`)

**Determinismus.** Fixe Tick-Rate 0,5 s; `TimeProvider`/`RandomSource` injizieren; kein direkter Zugriff auf `random` oder `datetime.now()` in der Domänenlogik. Sämtliche Seeds über `RandomStreamId` verwaltet.

**Persistenz.** JSON-Saves (komprimiert via zstd) + optional SQLite für Statistiken. Save-Versionierung `vN`, Migrationen in `persistence/migrations.py`. Drei Rotations-Slots + Autosave. Checksum/Hash zur Integrität.

**Daten-Pipeline.** Assets in `/assets/*.yaml`, Validierung via `config/schemas.py`, Build-Skript generiert kompilierte JSON-Snapshots für Releases.

```text
@startuml
package "Textual UI" {
  [App] --> [Screen:Dashboard]
  [App] --> [Screen:Team]
  [App] --> [Screen:Research]
  [App] --> [Screen:Market]
}
package "Core" {
  [Simulation] --> [RandomSource]
  [Simulation] --> [TimeProvider]
  [Simulation] --> [EventBus]
}
package "Persistence" {
  [SaveManager] --> [JSON.zst]
}
package "API" {
  [FastAPI]
}
[App] --> [Simulation]
[FastAPI] --> [Simulation]
[Simulation] --> [SaveManager]
[CLI] --> [Simulation]
@enduml
```

### 4.2 Tick-Loop & Offline-Berechnung

- Fixed-Tick-Accumulator: `acc += delta; while acc >= tick: sim.tick(); acc -= tick`
- Offline-Progress: `dt = clamp(now-last_save, 0, cap_hours*3600)`; `n = floor(dt / tick)`; analytische Formeln (S-Kurven) für ökonomische Größen, ohne jede Iteration zu simulieren
- Seeds & RNG: PCG64/Philox via `numpy.random.Generator` oder `randomgen`; Stream-Aufteilung nach Feature (`hiring`, `events`, `market`, …)
- Performance: Ziel < 5 ms pro Tick für Standard-Szenario (Profiling via `cProfile` + `pyinstrument`)

### 4.3 Datenmodelle & Schemas (MVP)

**IDs.** Referenzen per `str` (kebab-case). Keine direkten Objekt-Referenzen in Saves. Validierung via `Annotated[str, Field(pattern="^[a-z0-9\-]+$")]`.

**Assets (YAML).**

- `roles.yaml` → `RoleDef { id, name_key, base_salary, skills{ml,data,eng,prod}, hire_weight }`
- `research.yaml` → `ResearchNodeDef { id, tier, category, cost_fp, time_hours, prereq_ids[], effects{ quality+, infra+, features[] } }`
- `products.yaml` → `ProductDef { id, segment_id, base_k, churn, price_range, cost_per_user }`
- `markets.yaml` → `MarketSegmentDef { id, tam, price_elasticity, tech_affinity, regulation_level }`
- `events.yaml` → `EventDef { id, weight, triggers, effects{ type, magnitude, duration } }`

**Save (JSON v1 Beispiel).**

```json
{
  "version": 1,
  "created_at": "2025-10-06T08:00:00Z",
  "last_time": "2025-10-06T10:00:00Z",
  "seed": 9201531,
  "company": {
    "name": "My AI Co",
    "reputation": 0.0,
    "cash": 20000,
    "burn_rate": 0,
    "employees": ["emp-001", "emp-002"],
    "research_queue": ["res-basic-nlp"],
    "active_products": ["prod-chatbot-a"]
  },
  "employees": {
    "emp-001": {
      "role": "ml-engineer",
      "level": 1,
      "skills": {"ml": 3, "data": 2, "eng": 2, "prod": 1},
      "salary": 2200
    }
  },
  "research": {"unlocked": ["res-basic-nlp"], "in_progress": []},
  "products": {
    "prod-chatbot-a": {
      "def": "chatbot",
      "launch_day": 10,
      "users": 0,
      "price": 6.99,
      "quality": 0.42
    }
  },
  "economy": {"day": 12, "inflation": 0.02},
  "rng_stream": {"hiring": 12345, "events": 777, "market": 444}
}
```

### 4.4 Kern-Formeln (einfach, erweiterbar)

- **Qualität:** `quality = tanh(a*model_quality + b*ln(data_qty+1) + c*infra_cap) - debt_penalty`
- **Nachfrage:** `base_demand * fit(price, quality) * (1 + hype) * (1 + reputation/100)`
- **Skandal-Risiko:** `p = base * (1 - ethics_invest) * (1 - diversity) * (1 + hype)`
- **Offline-Ertrag:** `min(cap, tick_income * (1 - exp(-μ*Δt)))`
- **Reputation Drift:** `rep += ethics_delta - scandal_penalty + marketing_boost`

Parameter werden in `assets/balancing.yaml` versioniert und über Tests abgesichert.

---

## 5) Content & Feature Scope (MVP)

- **Projekte:** Chatbot, Vision-Assistent, Empfehlungssystem, Healthcare-KI, Generative Art
- **Rollen:** Data Scientist, ML Engineer, Backend Engineer, MLOps, Ethics Officer
- **Forschung:** Transformer Basics, Reinforcement Learning, Bias Monitoring, GPU Cluster, AutoML Toolkit
- **Events:** Audit, Regulatorische Auflagen, KI-Winter (Nachfrage -20 %), Datenleck (Reputation -15, Kosten), Hype-Welle (Nachfrage +30 %)
- **Achievements:** 10 Stück (z. B. „First 1k Users“, „Ethics Champion“, „IPO Ready“); Tracking im Core, optional Steam-Sync
- **Meta-Progression:** Tech-Tree Tiers 1–3, Standort-Upgrade (Home Office → Loft → Campus) als Meilensteine

---

## 6) Produktion & Ressourcen

- **Zeitplan:** 6 Wochen gemäß `100_schritte_plan.md`
- **Organisation:** Kanban-Board (TODO → Doing → Review → Done) in Obsidian/Notion/GitHub Projects
- **Werkzeuge:** Poetry, VS Code/PyCharm, Textual Devtools, Krita/Inkscape für Assets, Audacity (CC0-Sounds), OBS für Capture
- **Dokumentation:** Devlog (`docs/diary/`), Tech Notes (`docs/adr/`), Balancing-Notebooks (`notebooks/` via Jupyter)

---

## 7) QA, Sicherheit & Compliance

- **Tests:** pytest + hypothesis (Property-Tests für Ökonomie), Snapshot-Tests (Assets), Textual-Widget-Tests (`textual.testing`), API-Contract-Tests (FastAPI/TestClient)
- **Static Analysis:** mypy (strict), ruff, bandit, pip-audit
- **Performance:** Profiling via `nox -s profile`, Benchmark-Szenarien in `benchmarks/`
- **Save-Integrität:** Roundtrip-Tests + Schema-Validierung, Hash-Check beim Laden
- **Datenschutz:** Keine personenbezogenen Daten; Offlinedaten optional exportierbar als CSV

---

## 8) Distribution & Release Management

- **Builds:** PyInstaller `onefile` + `onedir` Artefakte (`dist/windows/`), Signierung optional via Self-Signed Cert
- **Steam-Upload:** `steamcmd` Skript (`tools/steam/upload.py`) packt PyInstaller-Output in Depot
- **Versionierung:** SemVer (`v0.1.0` MVP), Build-Metadaten in `__version__`
- **Updates:** Delta-Patches durch erneutes PyInstaller-Packen; Save-Migrationen sicherstellen
- **Demo:** Separater PyInstaller-Build mit eingeschränkter Spielzeit (z. B. 30 Ingame-Tage)

---

## 9) Marketing & Launch-Plan

- **Pre-Launch:** Devlog (Markdown + GIFs/ASCII), Wishlist-Kampagne, Discord/Newsletter optional
- **Store-Assets:** Screenshots & Trailer direkt aus Textual UI (OBS + GIF-Encoder), Key-Art (SVG → PNG)
- **Launch-Kommunikation:** Steam-News, Social Posts (Mastodon/Bluesky), Hacker News „Show HN“
- **Nach Launch:** Patch-Notes, Balancing-Updates, Community-Feedback sammeln

---

## 10) Risiko-Register & Mitigation

| Risiko                              | Auswirkung                | Wahrscheinlichkeit | Mitigation                                 |
| ----------------------------------- | ------------------------- | -----------------:| ------------------------------------------- |
| Textual-Leistung unzureichend       | Schlechte Spielerfahrung  |            Mittel | Profiling, UI vereinfachen, Animationen aus |
| PyInstaller-Build instabil          | Launch verzögert          |             Niedrig | Frühe Build-Pipeline, Smoke-Tests           |
| Balancing unausgewogen              | Negative Reviews          |            Mittel | Headless-Tests, KPI-Dashboards, Beta-Feedback |
| Steam-Integration (Python) scheitert| Keine Achievements        |             Niedrig | Fallback: rein internes Achievement-System |
| Zeitplan rutscht                    | Launch verzögert          |            Mittel | Wöchentliche Reviews, Scope-Management      |

---

## 11) Glossar

- **Idle-Mechanik:** Fortschritt während Inaktivität, berechnet aus Δt zwischen Saves über analytische Formeln.
- **Hype-Zyklus:** Ära-abhängige Multiplikatoren für Nachfrage/Forschung, gesteuert durch Event-Scheduler.
- **Reputation:** Skala 0–100, beeinflusst Nachfrage, Bewerberqualität, Investorendeals.

---

> **Kurzfassung:** KI-Dev-Tycoon wird komplett in Python ausgeliefert. Simulation, UI, Persistenz und Build-Pipeline sind deterministisch, getestet und ohne proprietäre Abhängigkeiten. PyInstaller erzeugt die Windows-Builds für Steam; der Textual-Client stellt das Spielerlebnis bereit.
