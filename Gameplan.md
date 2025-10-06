# KI‑Dev‑Tycoon — Produktions‑ & Game‑Design‑Plan (GDD/PRD)

> **Ziel:** Vollständig ausgearbeiteter Plan für ein mobile‑fokussiertes Tycoon‑Spiel, das den Aufbau eines KI‑Unternehmens simuliert. Optimiert für kurze Sessions (5–10 Minuten), langlebige Progression, ethische Entscheidungen und Free‑to‑Play‑Monetarisierung ohne Pay‑to‑Win.

---

## 1) Executive Summary

**Elevator Pitch:** Starte im Home‑Office, baue mit Daten, Modellen und einem wachsenden Team ein KI‑Imperium. Reagiere auf Hype‑Zyklen, entscheide zwischen Produkt‑ und Lizenzstrategie, manövriere Ethik‑Risiken und dominiere die Branche.

**USP:**

* Glaubwürdige KI‑Anspielungen (Transformer, RL, Gen‑KI) + humorvolle, zugängliche Darstellung.
* Schnelle Sessions (Idle + Minispiele für Tuning), tiefe Meta‑Progression (Tech‑Tree, Reputation, Team‑Synergien).
* „Ethik & Reputation“ als echter Gameplay‑Hebel, nicht nur Flavor.

**Kern‑KPIs (Soft‑Launch‑Ziele):** D1 ≥ 35 %, D7 ≥ 12 %, D30 ≥ 4 %, ARPDAU ≥ 0,08 €, Ad‑Fill ≥ 90 %, Crash‑Rate ≤ 0,3 %.

---

## 2) Zielgruppe & Plattformen

* **Plattformen:** iOS & Android (Portrait).
* **Zielgruppe:** 16–45, Tech‑affin, Casual‑bis‑Midcore‑Tycoon‑Spieler.
* **Sitzungs‑Design:** 5–10 Minuten; Idle‑Erträge bei Abwesenheit (8–12 Stunden Cap).
* **Barrierefreiheit:** An-/Abschaltbare Animationen, Farbblind‑Modus, skalierbare UI‑Schrift.

---

## 3) Kern‑Spielstruktur

### 3.1 Core Loop

1. **Projektwahl** (Thema × Zielgruppe × Plattform).
2. **Ressourcen zuweisen** (Daten, Compute, Teamzeit).
3. **Training/Entwicklung** (Idle‑Timer + Minispiele).
4. **Release** (Produkt oder API/Lizenz) → Einnahmen + Feedback.
5. **Reinvest** (Forschung, Team, Marketing, Infrastruktur).

### 3.2 Meta Loop

* **Tech‑Tree** (Algorithmen/Anwendungen) → neue Projekte/Boosts.
* **Team‑Ausbau** (Rollen, Skills, Training, Burnout‑Management).
* **Ethik/Reputation** (Risiko ↔ Investments) steuert Nachfrage & Deals.
* **Standortwechsel** (Home‑Office → Büro → Campus) als Meilensteine.

### 3.3 Zeitleisten/Hypes

* **Frühphase:** Klassische ML‑Aufgaben, knappe Mittel.
* **Boom:** Cloud & Deep Learning, Venture Deals, schnelleres Wachstum.
* **Reife:** Generative KI, Robotik, Regulierung, hohe Skalierungskosten.

---

## 4) Systemdesign

### 4.1 Projekte & Markt‑Fit

* **Projekttypen:** Chatbot, Vision, Empfehlung, Gen‑Art, AV‑Module, Healthcare‑KI, Fin‑KI, Quanten‑KI‑Prototypen (spät).
* **Attribute:** Thema, Zielgruppe, Komplexität, Datenbedarf, Regulatorik‑Level, Time‑to‑Market, Risiko.
* **Erfolgsformel (vereinfacht):**

```
Erfolgsscore = Fit(Thema, Zielgruppe) * Qualität * (1 + HypeMod) * ReputationMod * MarketingReach
Qualität     = f(Daten^α, Compute^β, TeamSkill^γ, ToolchainBonus) – TechDebt
Nachfrage    = BaseDemand * g(Preis, Konkurrenz) * RegulatorikCap
```

### 4.2 Forschung (Tech‑Tree)

* **Kategorien:** Algorithmen (Transformer, RL, GNN), Anwendungen (Healthcare, Fin, NLP), Toolchain (MLOps, A/B‑Suite), Ethik (Bias‑Monitoring), Infrastruktur (GPU‑Cluster, Edge).
* **Freischaltung:** Forschungspunkte (FP) aus Projekterfolg + Basisertrag pro Tick.
* **Gates:** Abhängigkeiten + Zeitalter; Ethik‑Knoten reduzieren Skandalsrisiko global.

### 4.3 Team & Produktivität

* **Rollen:** Data Scientist, ML‑Engineer, Backend, MLOps, Designer, PM, Ethik‑Officer.
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

### 4.6 Marketing & Trends

* **Kanäle:** PR, Content, Ads, Konferenzen, Thought Leadership.
* **Modell:** Reichweite ~ Budget^δ * Kreativitäts‑Multiplikator; PR profitiert von Reputation.
* **Hype‑Impulse:** Zeitgesteuerte Multiplikatoren; Gegenmaßnahmen via Ethik/Transparenz.

### 4.7 Minispiele (kurz & skill‑basiert)

* **Parameter‑Tuning:** „Lock‑in“ Bonus‑Perks durch kurze Zielwerte (Timing/Slider).
* **Bug‑Hunt:** Muster finden → reduziert Tech‑Debt.
* **Pitch‑Deck:** Kartenwahl für Investor‑Meetings → bessere Terms bei Erfolg.

### 4.8 Idle‑Mechanik

* **Offline‑Berechnung:**

```
Ertrag_offline = min(Cap, f(Aktive Pipelines, Subscriptions, API‑Traffic))
Diminishing Returns nach 8–12h; täglicher Login‑Boost (einmalig)
```

---

## 5) Content‑Plan (Season 0 → 2)

| Season      | Ära/Schwerpunkt     | Neue Projekte                | Forschung                       | Events                          | Ziel                     |
| ----------- | ------------------- | ---------------------------- | ------------------------------- | ------------------------------- | ------------------------ |
| S0 (Launch) | Frühphase           | Chatbot, Vision, Recommender | Transformer‑Basics, MLOps I     | KI‑Winter‑Rückblick, PR‑Skandal | Onboarding, Retention    |
| S1          | Boom (Cloud/DL)     | Gen‑Art, Speech              | RL‑Grundlagen, A/B‑Suite        | Konferenz‑Expo, Audit           | Monetarisierung/Live‑Ops |
| S2          | Reife (Gen‑KI/Reg.) | AV‑Module, Healthcare        | Bias‑Monitoring, Red‑Team, Edge | Regulierungspaket, Leak         | Tiefe/Metagame           |

---

## 6) Monetarisierung (F2P, fair)

* **Ads:** Rewarded Video (Speed‑Boost, Soft‑Währung), Interstitials nur nach Missionen (Frequency Cap: 1/5 Min, max 4/Tag).
* **IAP:**

  * **Premium‑Währung:** „Compute‑Credits“ (z. B. 1,99 € bis 49,99 €).
  * **Kosmetik:** Office‑Skins, Charakter‑Outfits, Themen‑UIs.
  * **QoL‑Pässe:** Zusätzliche Save‑Slots, Automations‑Queue.
* **Einmalkauf (No‑Ads):** 6,99–9,99 €, + Szenario „KI in der Medizin“.
* **Fairness‑Guardrails:** Keine Pay‑Gates bei Kernprogression; Monetarisierung beschleunigt, ersetzt nicht.

---

## 7) UX/UI‑Leitlinien

* **Main Screens:** HQ‑Dashboard → Projekte → Forschung → Team → Markt → Ethik.
* **Informationsdichte:** Karten‑Layout, Tooltips, kontextuelle Glossare.
* **Tutorial (≤ 6 Min):** 1) Erstes Projekt 2) Training & Release 3) Forschungspunkte 4) Teamhire 5) Ethik‑Entscheidung 6) Marketing.
* **Benachrichtigungen:** Sanft, bündelbar, stille Nachtzeiten.

---

## 8) Technik & Architektur

* **Client:** Unity (C#) oder Godot (GDScript/C#), Mobile Portrait, Addressables/AssetBundles, lokal verschlüsselter Save.
* **Sim‑Kernel (optional getrennt):** Python (siehe AGENTS.md), deterministisch, API via FastAPI/HTTP oder eingebettete Lib.
* **Offline‑Support:** Delta‑Zeit‑Berechnung, Konfliktlösung bei Cloud‑Sync.
* **Analytics:** Client‑Events → Backend (Batch), Remote Config/Feature‑Flags.
* **Build‑Pipeline:** CI (GitHub Actions), Testgerätefarm, Symbol‑Upload (Crashlytics/Sentry).

**Datenstruktur (Savegame, vereinfacht):**

```json
{
  "version": 5,
  "tick": 12345,
  "rng_seed": 42,
  "cash": 125000,
  "reputation": 67,
  "projects": [...],
  "research": {"unlocked": ["transformer_basic"], "fp": 12},
  "team": [...],
  "market": {"hype": 0.2},
  "ethics": {"risk": 0.08, "invest": 2}
}
```

---

## 9) Analytics & A/B‑Testing

**Kern‑Events:** `session_start`, `tutorial_step`, `project_start/release`, `fp_gain/spend`, `ethics_event`, `reputation_change`, `ad_watch`, `iap_purchase`, `churn_flag`, `returning_user`.

**Funnel‑Metriken:** Install → Tutorial Complete → Erstes Release → Forschung Spend → 24h Retention → Monetarisierungs‑Kontakt.
**Experimente (Beispiele):** Tutorial‑Reihenfolge A/B, Rewarded‑Placement, Idle‑Cap 8 vs. 12 Std, Preisanker für IAP.

---

## 10) Balancing‑Modell (Formeln & Parameter)

**Qualität:**
$$\text{Qualität} = k_0 + k_1\log(1+\text{Daten}) + k_2\log(1+\text{Compute}) + k_3\cdot \text{TeamSkill} - \text{TechDebt}$$

**Nachfrage:**
$$\text{Nachfrage} = B\cdot \text{Fit}(t,z)\cdot (1+H)\cdot (1+\rho/100)\cdot e^{-\lambda,Preis}$$

**Skandal‑Risiko:**
$$p_{skandal}=p_0\cdot (1-\text{EthikInvest})\cdot (1-\text{Diversität})\cdot (1+H)$$

**Idle‑Ertrag:**
$$E_{offline}=\min(Cap,; E_{tick}\cdot f(\Delta t))\quad,; f(\Delta t)=1- e^{-\mu,\Delta t}$$

**Start‑Parameter (vorschlagen, Feintuning in Beta):**

* (k_1=0.8, k_2=0.6, k_3=0.02, \lambda=0.15, \mu=0.12), Idle‑Cap = 10 h, HypeMod im Boom = +30 %.

---

## 11) Live‑Ops & Community

* **Wöchentliche Challenges:** „Bestes Gen‑Art‑Modell“ (Seeds & Parameter vorgegeben).
* **Monatliche Events:** Szenario‑Runs mit Leaderboard (fair, ohne P2W).
* **Koop‑Projekte:** Gilde‑ähnliche Forschungspools (nur kosmetische Rewards).
* **UGC‑Leichtgewicht:** Presets teilen (keine externen Daten).

---

## 12) Produktionsplan (18 Wochen Soft‑Launch)

**Team (Kern, FTE‑Äquivalente):** 1 Producer, 2 Gameplay, 1 Client‑UI, 1 Backend/Sim, 1 Designer, 0.5 Artist, 0.5 QA, 0.5 Data/Live‑Ops.

**Milestones:**

* **M0 (2 Wochen):** Konzept‑Prototype (Core Loop, 1 Projekt, 1 Minispiel).
* **M1 (6 Wochen):** Vertical Slice: 3 Projekte, kleiner Tech‑Tree, Ethik‑Event, Ads‑Stub.
* **M2 (10 Wochen):** Content S0 fertig, Onboarding, Analytics, Crash‑Stabilität ≥ 99,7 %.
* **M3 (14 Wochen):** Soft‑Launch (2 Länder), A/B‑Tests, Pricing‑Feinschliff.
* **M4 (18 Wochen):** Global Launch, Season 1 live, Marketing‑Burst.

**Budget grob (18 Wochen, EUR):**

* Personal ≈ € 220–280k, Art/Audio € 15k, UA/Marketing Soft‑Launch € 30k, Tools/Backend € 8k, Puffer € 20k → **Summe ≈ € 295–353k**.

---

## 13) QA, Sicherheit & Compliance

* **QA:** Testpläne für Tutorial, Offline‑Caps, Monetarisierung, Edge‑Geräte (Low‑RAM).
* **Automatisiert:** Unit‑/Integrationstests (Sim‑Kernel), Device‑Farm Smoke‑Runs.
* **Datenschutz:** Minimal‑Telemetry, Opt‑in‑Dialoge, Lösch‑Anfragen im Client.
* **Regeln:** App‑Store‑Guidelines, GDPR, Jugendschutz (12+), keine realen personenbezogenen Daten.

---

## 14) Marketing & Launch‑Strategie

* **Pre‑Launch:** Devlog, TikTok/YouTube Shorts (Minispiele), Landing‑Page & Newsletter.
* **Store‑Assets:** 6 Screenshots, 1 Video (20–30 s), ASO: Keywords „Tycoon, AI, Idle“.
* **UA:** Soft‑Launch‑Kanäle (Meta, Google App‑Campaigns), Lookalikes ab D7‑Kohorten.
* **Influencer:** Tech‑YouTuber, Indie‑Dev‑Kanäle; Pressekit mit humorvollen KI‑Bezügen.
* **Community:** Monats‑Challenges, Discord, Transparenz über Balancing‑Änderungen.

---

## 15) Risiko‑Register & Gegenmaßnahmen

| Risiko               | Auswirkung       | Wahrscheinlichkeit | Mitigation                               |
| -------------------- | ---------------- | -----------------: | ---------------------------------------- |
| Balancing misslingt  | Churn            |             Mittel | Telemetrie + schnelle Hotfix‑Zyklen      |
| P2W‑Wahrnehmung      | Negatives Rating |            Niedrig | Klare Fairness‑Leitplanken, No‑Ads‑Kauf  |
| Gerätefragmentierung | Crashes          |             Mittel | Device‑Farm + Feature‑Fallbacks          |
| Ethik‑Themen heikel  | PR‑Gegenwind     |            Niedrig | Humorvoll, abstrakt, keine realen Firmen |
| Content‑Durst        | D7 stagniert     |             Mittel | Seasons + Events Roadmap                 |

---

## 16) Anhang A: Beispiel‑Tech‑Tree (Auszug)

```
[Algorithmen]
  ├─ Transformer‑Basics (FP: 5) → +5% Qualität NLP
  ├─ RL‑Grundlagen (FP: 5)      → neue Projektklasse „Agenten“
  └─ Diffusion‑Intro (FP: 6)    → Gen‑Art freigeschaltet
[Toolchain]
  ├─ MLOps I (FP: 4)            → -10% Trainingszeit
  └─ A/B‑Suite (FP: 6)          → Marketingeffizienz +8%
[Ethik]
  ├─ Bias‑Monitoring (FP: 4)    → Skandal‑Risiko −15%
  └─ Red‑Team (FP: 6)           → einmaliger „Skandal‑Blocker“/Season
```

---

## 17) Anhang B: Beispiel‑Ereignisse

* **„Datensatz‑Leak“:** –10 Reputation; Option „Ehrlicher Report“ (Kosten €), +PR‑Boost später.
* **„Regulierungs‑Hearing“:** Bei Erfolg Reputation +8, sonst −5 & Lizenzgebühren +2 % für 30 Tage.
* **„Konferenz‑Best Paper“:** Sofort FP +5; Marketing‑Push Rabatt.

---

## 18) Nächste Schritte (konkret)

1. Feasibility‑Prototype (M0): Core Loop + 1 Minispiel + 1 Ethik‑Event.
2. KPI‑Instrumentierung früh integrieren.
3. Content‑Pipelines & Remote‑Config vorbereiten (S0/S1).
4. Soft‑Launch‑Märkte auswählen (z. B. CAN/NZ/SCAND).
5. Usability‑Tests mit 10–15 Probanden (Think‑Aloud) vor M1.

---

> **Erfolgsmesser:** Erreichen der Soft‑Launch‑KPIs, stabile Crash‑Rate, positive Store‑Ratings (≥ 4,3), gesunder Mix aus Ads/IAP. Der Plan unterstützt schnelle Iteration, ethisch sinnvolle Entscheidungen und langfristige Content‑Erweiterbarkeit.
