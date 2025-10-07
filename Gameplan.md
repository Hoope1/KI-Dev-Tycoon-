# KI‑Dev‑Tycoon — Produktions- & Game-Design-Plan (GDD/PRD)

> **Einordnung:** Dieses Dokument ergänzt [`Zusatz.md`](./Zusatz.md) und vertieft die dort definierten Leitplanken für den Steam-MVP (Windows x64, offline, Python-only). Alle Angaben folgen der Paid-Upfront-Strategie (€5.99) ohne Online-Pflicht.

> **Ziel:** Vollständig ausgearbeiteter Plan für einen Desktop-Tycoon, der den Aufbau eines KI-Unternehmens simuliert. Optimiert für kurze bis mittlere Sessions (5–20 Minuten), langlebige Meta-Progression, ethische Entscheidungen und faire Monetarisierung ohne Live-Ops-Abhängigkeiten. Das gesamte Erlebnis läuft in Python (Textual-Frontend + deterministische Simulation).

---

## 1) Executive Summary

**Elevator Pitch:** Starte im Home-Office, baue mit Daten, Modellen und einem wachsenden Team ein KI-Imperium. Reagiere auf Hype-Zyklen, entscheide zwischen Produkt- und Lizenzstrategie, manövriere Ethik-Risiken und dominiere die Branche – alles in einer stylischen Terminal-Oberfläche.

**USP:**

* Glaubwürdige KI-Anspielungen (Transformer, RL, Gen-KI) + humorvolle, zugängliche Darstellung.
* Schnelle Sessions (Idle + Minispiele für Tuning), tiefe Meta-Progression (Tech-Tree, Reputation, Team-Synergien).
* „Ethik & Reputation“ als echter Gameplay-Hebel, nicht nur Flavor.
* Vollständig Python-basiert → leicht erweiterbar, modbar, testbar.

**Kern-KPIs (Launch + 2 Wochen):** Wishlist→Sale CR ≥ 10 %, Refund-Rate ≤ 8 %, ≥ 75 % positive Steam-Reviews (n≥20), Crash-Rate ≤ 0,3 %.

---

## 2) Zielgruppe & Plattformen

* **Plattform (Launch):** Windows x64 (Steam, PyInstaller-Build). Fokus auf Textual-Fenster (≥ 120×40 Zeichen), optional Vollbild-Terminal. Steam-Deck wird als „Should“-Have getestet.
* **Zielgruppe:** 16–45, Tech-affin, Casual-bis-Midcore-Tycoon-Spieler:innen mit Interesse an KI-Trends.
* **Sitzungs-Design:** 5–20 Minuten; Offline-Simulation verarbeitet Abwesenheit bis ca. 12 Stunden.
* **Barrierefreiheit:** Skalierbare UI-Schrift (90–160 %), Farbschemata (Light/Dark, farbenblind-sicher), reduzierte Animationen, vollständige Tastatursteuerung.

---

## 3) Kern-Spielstruktur

### 3.1 Core Loop

1. **Projektwahl** (Thema × Segment × Plattform) über Karten/Listen im Textual-Dashboard.
2. **Ressourcen zuweisen** (Daten, Compute, Teamzeit) mit interaktiven Sliders/Inputs.
3. **Training/Entwicklung** (0,5 s Tick-Loop + optionale Minispiele in separaten Screens).
4. **Release** (Produkt oder API/Lizenz) → Einnahmen + Feedback, Achievements.
5. **Reinvest** (Forschung, Team, Marketing, Infrastruktur) → Vorbereitung auf nächste Ära.

### 3.2 Meta Loop

* **Tech-Tree** (Algorithmen/Anwendungen) → neue Projekte/Boosts.
* **Team-Ausbau** (Rollen, Skills, Training, Burnout-Management).
* **Ethik/Reputation** (Risiko ↔ Investments) steuert Nachfrage & Deals.
* **Standortwechsel** (Home-Office → Loft → Campus) als Meilensteine.

### 3.3 Zeitleisten/Hypes

* **Frühphase:** Klassische ML-Aufgaben, knappe Mittel, Fokus auf Break-Even.
* **Boom:** Cloud & Deep Learning, gesteigerte Nachfrage, Achievement „First 1k“.
* **Reife:** Generative KI, Regulierung, hohe Skalierungskosten, Risiken durch Events.

---

## 4) Systemdesign

### 4.1 Projekte & Markt-Fit

* **Projekttypen:** Chatbot, Vision, Empfehlung, Gen-Art, AV-Module, Healthcare-KI, Fin-KI, Quanten-Prototypen (spät).
* **Attribute:** Thema, Zielgruppe, Komplexität, Datenbedarf, Regulatorik-Level, Time-to-Market, Risiko.
* **Erfolgsformel (vereinfacht):**

```
Erfolgsscore = Fit(Thema, Zielgruppe) * Qualität * (1 + HypeMod) * ReputationMod * MarketingReach
Qualität     = f(Daten^α, Compute^β, TeamSkill^γ, ToolchainBonus) – TechDebt
Nachfrage    = BaseDemand * g(Preis, Konkurrenz) * RegulatorikCap
```

### 4.2 Forschung (Tech-Tree)

* **Kategorien:** Algorithmen (Transformer, RL, GNN), Anwendungen (Healthcare, Fin, NLP), Toolchain (MLOps, Experimentation), Ethik (Bias-Monitoring), Infrastruktur (GPU-Cluster, Edge).
* **Freischaltung:** Forschungspunkte (FP) aus Projekterfolg + Basisertrag pro Tick; Speed durch Mitarbeiter-Skills.
* **Gates:** Abhängigkeiten + Ära; Ethik-Knoten reduzieren Skandalsrisiko global (Achievement „Tier-2 Unlocked“).

### 4.3 Team & Produktivität

* **Rollen:** Data Scientist, ML Engineer, Backend, MLOps, Designer, PM, Ethik-Officer.
* **Werte:** Skill (0–100), Synergie-Tags (NLP/Vision/Infra), Moral, Burnout, Gehalt.
* **Mechaniken:** Training ↑Skill; Crunch ↑Speed aber ↑Burnout; Diversität ↓Bias-Risiko leicht.
* **Office-Perks:** Kantine, Weiterbildung, Sabbaticals → Moral-Buffs.

### 4.4 Ethik & Reputation

* **Risikoquellen:** Datenschutz, Bias, Halluzinationen, IP-Verstöße.
* **Ereignisse:** Audits, Medienberichte, Regulierung.
* **Mitigation:** Invest in Ethik-Forschung, Red-Team-Budget, Transparenzberichte.
* **Effekt:** Reputation 0–100 skaliert Nachfrage ± 20 %, Investorendeals, Bewerberqualität.

### 4.5 Ökonomie

* **Kosten:** CAPEX (Server/GPU), OPEX (Gehälter, Cloud), Marketing, Lizenzgebühren.
* **Erlöse:** Produktverkäufe (Einmal/Subscription), API-Calls (Tiered), Enterprise-Deals (Milestones).
* **Produkt vs. Lizenz:** Produkt = höhere Margin, volatil; Lizenz = planbar, gedeckelt.
* **Cash-Flow-Regeln:** Keine negativen Kontostände jenseits Kreditlinie; Zinsen ab Schwelle.

### 4.6 Go-to-Market & Trends

* **Kanäle:** Steam Discovery Queue, Devlog-Posts, Fachpresse (Tech/AI), Influencer-Streams, Wishlist-Kampagnen.
* **Modell:** Fokus auf Wishlists → Conversion am Launch-Tag; Reputation steigert PR-Reichweite.
* **Hype-Impulse:** Äraabhängige Nachfrage-Boosts; Ethik-/Transparenz-Investitionen dämpfen Negativtrends.

### 4.7 Minispiele (kurz & skill-basiert)

* **Parameter-Tuning:** Slider-Herausforderung zur Optimierung von Qualitätsboni.
* **Bug-Hunt:** Muster finden → reduziert Tech-Debt, triggert Toasts.
* **Pitch-Deck:** Kartenauswahl für Investor-Meetings → bessere Terms bei Erfolg.

Minispiele laufen als separate Textual-Screens mit eigenem Event-Loop, bleiben jedoch deterministisch (RNG-Streams).

### 4.8 Idle-Mechanik

* **Offline-Berechnung:** 0,5 s Fixed-Tick; Offline-Cap 8–12 h; analytische Formeln für große Δt (siehe `Zusatz.md`).
* **Präsentation:** Beim Spielstart zeigt das Dashboard eine Zusammenfassung (ASCII-Grafik + Tabellen).

---

## 5) Content Roadmap (MVP)

| Bereich     | Inhalt (MVP)                                        | Erweiterungen Post-Launch |
| ----------- | --------------------------------------------------- | ------------------------- |
| Projekte    | Chatbot, Vision, Recommendation, Gen-Art, Healthcare| Finance AI, Autonomous     |
| Forschung   | Transformer Basics, RL, Bias Monitor, GPU Cluster   | Quantum Sim, Causal ML     |
| Events      | Audit, Datenleck, KI-Winter, Hypewave, Konkurrent   | Regulatorische Großereignisse |
| Team        | 5 Kernrollen + 10 Bewerber-Templates                | Freelancer, Advisor        |
| Achievements| 10 Stück (First 1k, Ethics Champ, IPO Ready, …)     | Season Challenges          |

---

## 6) Produktionsplan (6 Wochen)

| Woche | Fokus                     | Kernlieferobjekte                                                    |
| ----- | ------------------------- | -------------------------------------------------------------------- |
| W1    | Projekt & Kernel          | Poetry Workspace, deterministischer Sim-Kern, CLI (`ki-sim`)         |
| W2    | Daten & Ökonomie          | Assets (YAML), Ökonomie-Modelle, Hiring/Research-Systeme             |
| W3    | UI First Pass (Textual)   | Screens (Dashboard/Team/Research/Market), Presenter-Layer            |
| W4    | Distribution & Content    | PyInstaller-Builds, Achievement-System, Marketing-Assets             |
| W5    | Polish & Beta             | Balancing-Pass, Performance-Profiling, Accessibility, Beta-Test      |
| W6    | Release                   | Finaler Build, Steam-Upload, Launch-Kommunikation, Hotfix-Pfad       |

---

## 7) UX/UI-Leitlinien

- **Main Screens:** Dashboard → Projekte → Forschung → Team → Markt → Events/Log.
- **Layout:** Flex-Layout (Textual Grid), modulare Panels, Farbschema anpassbar.
- **Navigation:** Tastatur (Tab/Shift+Tab, Pfeile, Hotkeys), Maus optional über Textual Mouse Support.
- **Informationsdichte:** Tabellen, Sparkline-Charts (Rich), Tooltips, Glossar.
- **Onboarding (≤ 10 Min):** Erstes Projekt abschließen, Forschung freischalten, Hiring durchführen, Preis anpassen.
- **Notifications:** Toast-Panel + Log-Stream; Fokus-Modus (reduzierte Animationen) optional.

---

## 8) Technik & Architektur

- **Runtime:** Python 3.11, deterministischer Sim-Kern (`ki_dev_tycoon.core`).
- **UI:** Textual (>= 0.58) mit modularen Screens und Presenter-Schicht.
- **API:** Optionale FastAPI (`ki_dev_tycoon.api`) für externe Tools, automatisierte Tests via TestClient.
- **Persistenz:** JSON (zstd) + optional SQLite Stats; Versionierung `v1` → `vN` Migrationen.
- **Automation:** nox Sessions (lint, typecheck, tests, build), GitHub Actions (Python 3.11/3.12 Matrix).
- **Builds:** PyInstaller (`app/tools/build_app.py`), Dist-Folder `dist/windows/`.
- **Savegame (MVP):**

```json
{
  "version": 1,
  "seed": 9201531,
  "last_time": "2025-10-06T10:00:00Z",
  "company": {"cash": 20000, "reputation": 0.0},
  "employees": {...},
  "research": {...},
  "products": {...},
  "rng_stream": {"hiring": 12345, "events": 777}
}
```

---

## 9) Telemetrie & Messung

- **Kein Online-Tracking:** Keine externen Analytics oder Remote Config im MVP.
- **Lokale Logs:** Optionale CSV/JSON-Exports, Dev-Konsole in der Textual-App.
- **Business-Metriken:** Steam Backoffice (Sales, Refunds, Reviews) + manuelle KPI-Sheets.

---

## 10) Balancing-Modell (Formeln & Parameter)

- **Qualität:** `quality = tanh(a*model_quality + b*ln(data_qty+1) + c*infra_cap)`
- **Nachfrage:** `BaseDemand * fit(price, quality) * (1 + hype) * (1 + reputation/100)`
- **Skandal-Risiko:** `p = base * (1 - ethicsInvest) * (1 - diversity) * (1 + hype)`
- **Offline-Ertrag:** `min(cap, tickIncome * f(Δt))`, mit `f(Δt) = 1 - exp(-μ*Δt)`
- **Startparameter:** `a=0.9`, `b=0.7`, `c=0.15`, `μ=0.12`, Offline-Cap = 10 h, Boom-Hype = +30 %.

Parameter werden in YAML hinterlegt, Tests sichern Invarianten (Cash ≥ 0 ohne Kredit, Reputation ∈ [0,100], Nachfrage ≥ 0).

---

## 11) Post-Launch Outlook

- **Kostenlose Updates:** Weitere Projekttypen, Tech-Tree-Erweiterungen, zusätzliche Events.
- **Community-Wünsche:** Quality-of-Life-Features (Controller-Support via `textual`-Mouse/Hotkeys, Modding-API) evaluieren.
- **Optional Demo:** itch.io Demo für zusätzliche Wishlists (PyInstaller-Build mit Limitierungen).

---

## 12) Produktion & Ressourcen

- **Team:** Solo-Dev (Design, Code, Art) + punktuelle Freelancer (Art/SFX) ≤ €150 Budget.
- **Zeitplan:** 6 Wochen gemäß Milestone-Roadmap, tägliche Fokusblöcke (4–6 h).
- **Werkzeuge:** VS Code/PyCharm, Poetry, Textual Devtools, Inkscape/Krita, Audacity, OBS.
- **Dokumentation:** Wöchentlicher Devlog, Fortschritt im Repo (`docs/diary/`), ADRs (`docs/adr/`).

---

## 13) QA, Sicherheit & Compliance

- **Tests:** Unit-/Property-Tests (Kernel), Textual-Widget-Tests, Hypothesis für Ökonomie, CLI-Integrationstests.
- **Manuelle QA:** Save-Rotation, Offline-Progress, Achievements, Performance (≤ 16 ms Tick auf Mittelklasse-PC).
- **Datenschutz:** Keine personenbezogenen Daten; Impressum/Privacy-Hinweis in Readme/Store.
- **Lizenzen:** CC0/CC-BY Assets korrekt attribuieren; Third-Party-Libraries dokumentieren (`THIRD_PARTY.md`).

---

## 14) Marketing & Launch-Plan

- **Pre-Launch:** Devlog-Serie, Wishlist-Kampagne, Newsletter/Discord-Aufbau.
- **Store-Assets:** 6 Screenshots, 30–45 s Trailer (Textual Capture), Capsule-Art (SVG→PNG), Feature-Bullets (DE/EN).
- **Launch-Kommunikation:** Steam-News, Social Posts (Twitter/Bluesky/Mastodon), Indie-Subreddits, Hacker News.
- **Nach Launch:** Review-Antworten, Patch-Notes, Transparenz über Roadmap.

---

## 15) Risiko-Register & Mitigation

| Risiko                         | Auswirkung               | Wahrscheinlichkeit | Mitigation                                      |
| ------------------------------ | ------------------------ | -----------------:| ------------------------------------------------ |
| Textual-Performance            | UI-Lag                   |              Mittel | Profiling, Widgets vereinfachen, Animationen aus |
| PyInstaller-Fehler             | Build-Blocker            |              Niedrig | Früh testen, Logs automatisieren                 |
| Balancing unausgewogen         | Schlechte Reviews        |              Mittel | Headless-Tests, Feedback-Runden, KPI-Dashboards  |
| Steamworks-Python-Limitierungen| Keine Achievements       |              Niedrig | Fallback intern, optional API-Wrapper            |
| Zeitplan rutscht               | Launch verzögert         |              Mittel | Wöchentliche Reviews, Scope kontrollieren        |
| Accessibility unzureichend     | Negative Spielerfahrung  |              Niedrig | User-Tests, Theme-Optionen, Screenreader-Checks  |

---

> **Kurzfassung:** KI-Dev-Tycoon liefert einen deterministischen KI-Wirtschafts-Tycoon komplett in Python. Textual sorgt für eine reaktive Terminal-Oberfläche, PyInstaller für die Distribution, und der Sim-Kern bleibt strikt testbar und modbar.
