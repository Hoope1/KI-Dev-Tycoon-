# KI‑Dev‑Tycoon — Produktions‑ & Game‑Design‑Plan (GDD/PRD)

> **Einordnung:** Dieses Dokument ergänzt [`Zusatz.md`](./Zusatz.md) und vertieft die dort definierten Leitplanken für den Steam‑MVP (Windows x64, offline, Solo‑Dev, Budget ≤ €500). Alle Angaben folgen der Paid‑Upfront‑Strategie (€5.99) ohne Online‑Pflicht.

> **Ziel:** Vollständig ausgearbeiteter Plan für einen Desktop‑Tycoon, der den Aufbau eines KI‑Unternehmens simuliert. Optimiert für kurze bis mittlere Sessions (5–20 Minuten), langlebige Meta‑Progression, ethische Entscheidungen und faire Monetarisierung ohne Live‑Ops‑Abhängigkeiten.

---

## 1) Executive Summary

**Elevator Pitch:** Starte im Home‑Office, baue mit Daten, Modellen und einem wachsenden Team ein KI‑Imperium. Reagiere auf Hype‑Zyklen, entscheide zwischen Produkt‑ und Lizenzstrategie, manövriere Ethik‑Risiken und dominiere die Branche.

**USP:**

* Glaubwürdige KI‑Anspielungen (Transformer, RL, Gen‑KI) + humorvolle, zugängliche Darstellung.
* Schnelle Sessions (Idle + Minispiele für Tuning), tiefe Meta‑Progression (Tech‑Tree, Reputation, Team‑Synergien).
* „Ethik & Reputation“ als echter Gameplay‑Hebel, nicht nur Flavor.

**Kern‑KPIs (Launch + 2 Wochen):** Wishlist→Sale CR ≥ 10 %, Refund‑Rate ≤ 8 %, ≥ 75 % positive Steam‑Reviews (n≥20), Crash‑Rate ≤ 0,3 %.

---

## 2) Zielgruppe & Plattformen

* **Plattform (Launch):** Windows x64 (Steam, 16:9, Maus/Keyboard). Steam‑Deck wird als „Should“-Have getestet.
* **Zielgruppe:** 16–45, Tech‑affin, Casual‑bis‑Midcore‑Tycoon‑Spieler:innen mit Interesse an KI‑Trends.
* **Sitzungs‑Design:** 5–20 Minuten; Offline‑Simulation verarbeitet Abwesenheit bis ca. 12 Stunden.
* **Barrierefreiheit:** Skalierbare UI‑Schrift (90–120 %), farbenblind‑sichere Palette, reduzierbare Animationen.

---

## 3) Kern‑Spielstruktur

### 3.1 Core Loop

1. **Projektwahl** (Thema × Segment × Plattform).
2. **Ressourcen zuweisen** (Daten, Compute, Teamzeit).
3. **Training/Entwicklung** (0,5 s Tick‑Loop + optionale Minispiele).
4. **Release** (Produkt oder API/Lizenz) → Einnahmen + Feedback, Steam‑Achievement‑Hooks.
5. **Reinvest** (Forschung, Team, Marketing, Infrastruktur) → Vorbereitung auf nächste Ära.

### 3.2 Meta Loop

* **Tech‑Tree** (Algorithmen/Anwendungen) → neue Projekte/Boosts.
* **Team‑Ausbau** (Rollen, Skills, Training, Burnout‑Management).
* **Ethik/Reputation** (Risiko ↔ Investments) steuert Nachfrage & Deals.
* **Standortwechsel** (Home‑Office → Büro → Campus) als Meilensteine.

### 3.3 Zeitleisten/Hypes

* **Frühphase:** Klassische ML‑Aufgaben, knappe Mittel, Fokus auf Break‑Even.
* **Boom:** Cloud & Deep Learning, gesteigerte Nachfrage, Steam‑Achievement „First 1k“.
* **Reife:** Generative KI, Regulierung, hohe Skalierungskosten, Risiken durch Events.

---

## 4) Systemdesign

### 4.1 Projekte & Markt‑Fit

* **Projekttypen:** Chatbot, Vision, Empfehlung, Gen‑Art, AV‑Module, Healthcare‑KI, Fin‑KI, Quanten‑Prototypen (spät).
* **Attribute:** Thema, Zielgruppe, Komplexität, Datenbedarf, Regulatorik‑Level, Time‑to‑Market, Risiko.
* **Erfolgsformel (vereinfacht):**

```
Erfolgsscore = Fit(Thema, Zielgruppe) * Qualität * (1 + HypeMod) * ReputationMod * MarketingReach
Qualität     = f(Daten^α, Compute^β, TeamSkill^γ, ToolchainBonus) – TechDebt
Nachfrage    = BaseDemand * g(Preis, Konkurrenz) * RegulatorikCap
```

### 4.2 Forschung (Tech‑Tree)

* **Kategorien:** Algorithmen (Transformer, RL, GNN), Anwendungen (Healthcare, Fin, NLP), Toolchain (MLOps, Experimentation), Ethik (Bias‑Monitoring), Infrastruktur (GPU‑Cluster, Edge).
* **Freischaltung:** Forschungspunkte (FP) aus Projekterfolg + Basisertrag pro Tick; Speed durch Mitarbeiter‑Skills.
* **Gates:** Abhängigkeiten + Ära; Ethik‑Knoten reduzieren Skandalsrisiko global (Steam‑Achievement „Tier‑2 Unlocked“).

### 4.3 Team & Produktivität

* **Rollen:** Data Scientist, ML‑Engineer, Backend, MLOps, Designer, PM, Ethik‑Officer (ScriptableObject‑Definitions gemäß `Zusatz.md`).
* **Werte:** Skill (0–100), Synergie‑Tags (NLP/Vision/Infra), Moral, Burnout, Gehalt.
* **Mechaniken:** Training ↑Skill; Crunch ↑Speed aber ↑Burnout; Diversität ↓Bias‑Risiko leicht.
* **Office‑Perks:** Kantine, Weiterbildung, Sabbaticals → Moral‑Buffs.

### 4.4 Ethik & Reputation

* **Risikoquellen:** Datenschutz, Bias, Halluzinationen, IP‑Verstöße.
* **Ereignisse:** Audits, Medienberichte, Regulierung.
* **Mitigation:** Invest in Ethik‑Forschung, Red‑Team‑Budget, Transparenzberichte.
* **Effekt:** Reputation 0–100 skaliert Nachfrage ± 20 %, Investorendeals, Bewerberqualität.

### 4.5 Ökonomie

* **Kosten:** CAPEX (Server/GPU), OPEX (Gehälter, Cloud), Marketing, Lizenzgebühren.
* **Erlöse:** Produktverkäufe (Einmal/Subscription), API‑Calls (Tiered), Enterprise‑Deals (Milestones).
* **Produkt vs. Lizenz:** Produkt = höhere Margin, volatil; Lizenz = planbar, gedeckelt.
* **Cash‑Flow‑Regeln:** Keine negativen Kontostände jenseits Kreditlinie; Zinsen ab Schwelle.

### 4.6 Go-to-Market & Trends

* **Kanäle:** Steam Discovery Queue, Devlog-Posts, Fachpresse (Tech/AI), Influencer-Streams, Wishlist-Kampagnen.
* **Modell:** Fokus auf Wishlists → Conversion am Launch-Tag; Reputation steigert PR-Reichweite.
* **Hype-Impulse:** Zeitalter-abhängige Nachfrage-Boosts; Ethik-/Transparenz-Investitionen dämpfen Negativtrends.

### 4.7 Minispiele (kurz & skill-basiert)

* **Parameter-Tuning:** „Lock-in“ Bonus-Perks durch Timing/Slider (optional, offline spielbar).
* **Bug-Hunt:** Muster finden → reduziert Tech-Debt, triggert Steam-Toasts.
* **Pitch-Deck:** Kartenwahl für Investor-Meetings → bessere Terms bei Erfolg.

### 4.8 Idle-Mechanik

* **Offline-Berechnung:** 0,5 s Fixed-Tick; Offline-Cap 8–12 h; analytische Formeln für große Δt (siehe `Zusatz.md`).

---

## 5) Milestone-Roadmap (W1–W6)

| Woche | Fokus                | Kernlieferobjekte                                          |
| ----- | -------------------- | ---------------------------------------------------------- |
| W1    | Projekt & Kernel     | Unity-Projekt, Tick-Loop, RNG, Save/Load, Steam-Bootstrap  |
| W2    | Daten & Ökonomie     | ScriptableObjects, Hiring/Forschung/Ökonomie, Offline-Cap  |
| W3    | UI First Pass        | Greybox aller Screens, Presenter, Localization-Setup       |
| W4    | Steam & Content      | Achievements, Rich Presence, Screenshots, Store-Texte      |
| W5    | Polish & Beta        | Balancing, Profiling, Audio, Accessibility, Beta-Feedback  |
| W6    | Release              | Finaler Build, Store-Go-Live, Kommunikation, Hotfix-Pfad   |

---

## 6) Monetarisierung (Paid Upfront)

- **Preis:** €5.99 einmalig, keine Rabatte zum Launch (Wishlist-Konversion messen).
- **Keine Ads/IAPs:** Monetarisierung erfolgt ausschließlich über den Kaufpreis.
- **Value-Kommunikation:** „Solo-Dev, deterministische KI-Unternehmenssimulation“ + Transparenz über Updates.
- **Achievements & Extras:** 8–12 Achievements als Mehrwert, optionale Demo (itch.io) zur Wishlist-Generierung.

---

## 7) UX/UI-Leitlinien

- **Main Screens:** HQ-Dashboard → Projekte → Forschung → Team → Markt → Events.
- **Informationsdichte:** Karten-Layout, Tooltips, Glossare; Controller-Support optional spätere Erweiterung.
- **Onboarding (≤ 10 Min):** Erstes Projekt abschließen, Forschung freischalten, Hiring durchführen, Preis anpassen.
- **Notifications:** In-Game Log & Toasts, keine Pushes; Fokus-Modus (reduzierte Animationen) optional.

---

## 8) Technik & Architektur

- **Client:** Unity 6 LTS, Windows x64, IL2CPP Release, Addressables lokal.
- **Sim-Kernel:** Reines C# (`Core.Sim`), deterministisch, keine Unity-Abhängigkeiten; Python-Kernel dient als Test-Harness.
- **Persistenz:** JSON + GZip, Versionierung mit `ISaveMigrator`.
- **Automation:** Lokale CI (nox/pytest für Python, Unity Batchmode für Builds), kein externer Backend-Service.

**Savegame (MVP):**

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
- **Lokale Logs:** Optionale CSV-Exports für Tests, Debug-Konsole im Dev-Build.
- **Business-Metriken:** Steam Backoffice (Sales, Refunds, Reviews) + manuelle KPI-Sheets.

---

## 10) Balancing-Modell (Formeln & Parameter)

- **Qualität:** `quality = tanh(a*modelQuality + b*ln(dataQty+1) + c*infraCap)`
- **Nachfrage:** `BaseDemand * fit(price, quality) * (1 + hype) * (1 + reputation/100)`
- **Skandal-Risiko:** `p = base * (1 - ethicsInvest) * (1 - diversity) * (1 + hype)`
- **Offline-Ertrag:** `min(cap, tickIncome * f(Δt))`, mit `f(Δt) = 1 - exp(-μ*Δt)`
- **Startparameter:** `a=0.9`, `b=0.7`, `c=0.15`, `μ=0.12`, Offline-Cap = 10 h, Boom-Hype = +30 %.

---

## 11) Post-Launch Outlook

- **Kostenlose Updates:** Weitere Projekttypen, Tech-Tree-Erweiterungen, zusätzliche Events.
- **Community-Wünsche:** Quality-of-Life-Features (Controller, Mod-Support) evaluieren.
- **Optional Demo:** itch.io Demo für zusätzliche Wishlists (nach Launch bewerten).

---

## 12) Produktion & Ressourcen

- **Team:** Solo-Dev (Design, Code, Art) + punktuelle Freelancer (Art/SFX) ≤ €150 Budget.
- **Zeitplan:** 6 Wochen gemäß Milestone-Roadmap, tägliche Fokusblöcke (4–6 h).
- **Werkzeuge:** Unity Personal, Inkscape, Krita, Audacity, CC0-Asset-Bibliotheken.
- **Dokumentation:** Wöchentlicher Devlog, Fortschritt im Repo (`docs/diary/` optional).

---

## 13) QA, Sicherheit & Compliance

- **Tests:** Unit-/Property-Tests (Kernel), Play-/Edit-Mode-Tests (Unity), Headless Runner.
- **Manuelle QA:** Save-Rotation, Offline-Progress, Achievements, Performance (≤ 16 ms FrameTime auf Mittelklasse-PC).
- **Datenschutz:** Keine personenbezogenen Daten; Impressum/Privacy-Hinweis in Readme/Store.
- **Lizenzen:** CC0/CC-BY Assets korrekt attribuieren; Third-Party-Libraries dokumentieren.

---

## 14) Marketing & Launch-Plan

- **Pre-Launch:** Devlog-Serie, Wunschlisten-Kampagne, Newsletter/Discord-Aufbau.
- **Store-Assets:** 6 Screenshots, 30–45 s Trailer, Capsule-Art in drei Formaten, Feature-Bullets (DE/EN).
- **Launch-Kommunikation:** Steam-News, Social Posts (Twitter/Bluesky/Mastodon), Indie-Subreddits.
- **Nach Launch:** Review-Antworten, Patch-Notes, Transparenz über Roadmap.

---

## 15) Risiko-Register & Mitigation

| Risiko                         | Auswirkung          | Wahrscheinlichkeit | Mitigation                                                   |
| ------------------------------ | ------------------- | -----------------: | ------------------------------------------------------------ |
| Zeitplan rutscht               | Launch verzögert     |              Mittel | Wöchentliche Reviews, Scope kontrollieren                    |
| Balancing unausgewogen         | Schlechte Reviews    |              Mittel | Headless-Tests, Feedback-Runden, Hotfix-Priorisierung        |
| Performance-Probleme           | Negative Spielerfahrungen | Niedrig       | Profiling (W5), Zielplattform testen                         |
| Steamworks-Integration fehlschlägt | Keine Achievements/Overlay | Niedrig | Frühe Implementierung (W1/W4), Fallbacks implementieren      |
| Art-Assets nicht ausreichend   | Schwache Store-Wirkung | Mittel         | CC0-Packs prüfen, Budget-Puffer für 1–2 Premium-Packs nutzen |

---
