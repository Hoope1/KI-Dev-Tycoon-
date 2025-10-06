# 100-Schritte-Plan — KI-Dev-Tycoon (Arbeitsliste)

> **Verbindliche Arbeitsanweisung:** Abarbeitung strikt Schritt für Schritt. Einen Schritt erst nach erfolgreichem, dokumentiertem und gründlich geprüften Abschluss (inkl. Tests) als erledigt markieren.
>
> Phasen: **Foundations (1–20)** · **Core-Gameplay (21–40)** · **System-Tiefe (41–60)** · **Monetarisierung & UX (61–80)** · **Soft-Launch & Global (81–100)**

---

## Foundations (1–20)

1. [ ] **Vision & KPIs fixieren:** Zielmetriken (D1/D7/D30, ARPDAU, Crash-Rate) schriftlich festhalten.
2. [ ] **Projektstruktur anlegen:** Monorepo mit `/client` (Unity/Godot) und `/sim` (Python) + Grund-Readme.
3. [ ] **AGENTS.md & GDD übernehmen:** Dateien ins Repo legen, als „Source of Truth“ verankern.
4. [ ] **Tooling einrichten:** Poetry, pre-commit, black, ruff, mypy, pytest, nox; Basiskonfiguration prüfen.
5. [ ] **CI/CD aufsetzen:** GitHub Actions (Lint, Typing, Tests, Coverage ≥90 % Ziel), Release-Workflow skeleton.
6. [ ] **Code-Ownership & Branching:** CODEOWNERS, Conventional Commits, Branch-Namensschema.
7. [ ] **Determinismus-Kernel starten:** `rng.py` und `time.py` (Seed/Clock-Injection) inkl. Unit-Tests.
8. [ ] **GameState-Gerüst:** `state.py` (immutable Snapshots) + einfache Serialisierung.
9. [ ] **Tick-Loop & CLI:** `ki-sim run --ticks` implementieren; Smoke-Test mit Seed=42 grün.
10. [ ] **Logging-Basis:** Strukturierte Logs (Tick, Duration, Seed); Silence-Levels konfigurierbar.
11. [ ] **Config-Lader:** YAML/TOML-Loader + Pydantic-Schemas; ein Beispiel-Profil `default` bereitstellen.
12. [ ] **Ereignisbus (EventBus):** Publish/Subscribe-Grundgerüst; leere Events für spätere Systeme.
13. [ ] **Persistenz-Roundtrip:** `savegame.py` (JSON) + Test `state == load(save(state))`.
14. [ ] **Benchmark-Skeleton:** pytest-benchmark setuppen; Basis-Messung für Tick-Loop einfrieren.
15. [ ] **Client-Projekt initialisieren:** Leere Szenen/Scenes (Dashboard-Mock), Build-Pipeline lauffähig.
16. [ ] **API-Adapter (optional):** FastAPI-Stub mit `/state` (GET) → Client liest Dummy-State.
17. [ ] **Fehlerklassen:** Domänen-Exception-Hierarchie + zentraler Handler im Sim-Kernel.
18. [ ] **Feature-Flags:** Remote-Config-Keypfad definieren; lokale Fallbacks implementieren.
19. [ ] **Risikoregister aufsetzen:** Top-5 Risiken + Frühindikatoren + Response-Owner.
20. [ ] **Design-System/Styleguide:** UI-Typo, Farben, Komponentenmuster; Figma/Wireframes grob.

## Core-Gameplay (21–40)

21. [ ] **Projektkatalog (MVP):** Projekttyp „Chatbot“ mit Attributen (Komplexität, Daten, Reg-Level).
22. [ ] **Qualitätsformel (MVP):** Daten/Compute/Skill/TechDebt → Qualitäts-Score + Unit-Tests.
23. [ ] **Ökonomie-Grundlagen:** Cashflow (CAPEX/OPEX), einfache Einnahmen nach Release.
24. [ ] **Nachfrage & Preiselastizität (MVP):** Basis-Demand + Preisfunktion; niemals Nachfrage <0.
25. [ ] **Release-Flow (MVP):** Projektphasen (Plan→Train→Ship) + Ergebnis-Berechnung + Feedback.
26. [ ] **Forschungspunkte (FP):** FP-Generierung aus Projekterfolg + Basisertrag pro Tick.
27. [ ] **Tech-Tree (MVP):** 6 Knoten (Transformer-Basics, MLOps I, A/B-Suite, Bias-Monitoring, Diffusion-Intro, RL-Grundlagen) + Gates.
28. [ ] **Team-System (MVP):** Rollen DS/ML-Eng/Backend; Skill 0–100; Gehälter; Hiring-Kosten.
29. [ ] **Produktivität & Training:** Training ↑Skill; Crunch ↑Geschwindigkeit, ↑Burnout; Caps testen.
30. [ ] **Ethik & Reputation (MVP):** Reputation 0–100 beeinflusst Nachfrage ± 10 %; erstes Skandal-Event.
31. [ ] **Marketing (MVP):** Ein Kanal „PR-Push“ mit Budget→Reichweite-Kurve; Abklingzeit.
32. [ ] **Hype-Zyklus (MVP):** Zeitbasierte Modifikatoren (Früh/Boom/Reife) wirken auf Nachfrage.
33. [ ] **Idle-Mechanik (MVP):** Offline-Ertrag f(Δt) mit Cap 10 h; Round-Trip-Tests.
34. [ ] **Speichersystem (Client):** Lokale Saves verschlüsselt; Sync-Stub vorbereitet.
35. [ ] **Minispiel #1 – Parameter-Tuning:** 10–20 s Timing-Skillcheck; kleiner Qualitäts-Boost.
36. [ ] **Tutorial v1:** Geführtes erstes Projekt inkl. Release; Telemetrie-Event „tutorial_step_*“.
37. [ ] **Szenario-Runner:** Seeds `{1,7,42,1337}` laufen 1 In-Game-Jahr ohne Fehler.
38. [ ] **Performance-Ziel:** `projects.simulator` ≤ 2 ms/Tick auf CI; Profiling-Bericht ablegen.
39. [ ] **First Playable Build:** Interner Test auf 3 Geräten; Crash-Rate erheben.
40. [ ] **Review & Adjust:** Bugs fixen, KPIs des internen Tests dokumentieren.

## System-Tiefe (41–60)

41. [ ] **Weitere Projekttypen:** Vision, Recommender; Balance-Parameter hinzufügen.
42. [ ] **Produkt vs. Lizenzmodell:** API-Tiers (Free/Pro/Enterprise) + Produktverkäufe/Subscriptions.
43. [ ] **Enterprise-Deals:** Meilenstein-Verträge mit Bonus/Penalty; Vertriebs-UI-Karten.
44. [ ] **Preismodelle & A/B:** Zwei Preis-Kurven; Remote-Umschaltung via Feature-Flag.
45. [ ] **Team-Erweiterung:** Designer, PM, MLOps, Ethik-Officer; Synergie-Tags (NLP/Vision/Infra).
46. [ ] **Moral & Burnout-Dynamik:** Einflüsse (Crunch, Perks) + Regeneration; Unit-/Property-Tests.
47. [ ] **Office-Perks:** Kantine, Weiterbildung, Sabbatical; kleine Buffs, Kosten pro Tick.
48. [ ] **Tech-Debt-System:** Schuldenaufbau durch Crunch/Bugs; Effekte auf Qualität/Velocity.
49. [ ] **Regulatorik-Level:** Projektattribute beeinflussen Risiko & Time-to-Market.
50. [ ] **Ethik-Forschung vertiefen:** Bias-Monitoring, Red-Team (einmaliger Blocker/Season).
51. [ ] **Events-Pool v1:** Datensatz-Leak, Konferenz-Preis, Audit-Hearing; Entscheidungen mit Konsequenz.
52. [ ] **Hype-Feinheiten:** Ereignisgetriggerte Impulse; Dämpfung über Transparenzberichte.
53. [ ] **MLOps II:** −10 % Trainingszeit global; Deploy-Stabilität ↑.
54. [ ] **A/B-Suite Effekte:** Marketingeffizienz +8 %; Events zur Auswertung.
55. [ ] **Diffusion/Gen-Art Projekte:** Pipeline & Asset-Kosten; neue Zielgruppen.
56. [ ] **Speech/NLP Projekte:** ASR/TTS/NLU als Unterkategorien; Fit-Funktionen anpassen.
57. [ ] **Healthcare-KI:** Hohe Regulatorik, höhere Margen; zusätzliche Audit-Checks.
58. [ ] **Reputation 2.0:** Einfluss auf Bewerberqualität, Investoren-Terms; UI-Feedback.
59. [ ] **Golden-Snapshots:** Sim-Outputs für Referenzszenarien einfrieren; CI-Drift-Checks.
60. [ ] **Device-Farm Smoke:** 10 Gerätekonfigurationen automatisiert; Crash-Hotspots sammeln.

## Monetarisierung & UX (61–80)

61. [ ] **Rewarded-Ads Integration:** Adapter (ironSource/AdMob) → nur nach Missionen; Frequency Cap.
62. [ ] **Interstitial-Ads (sparsam):** Nach großen Releases; Skip/No-Ads-Guardrail prüfen.
63. [ ] **IAP-Katalog:** Compute-Credits (5 Preis-Stufen), No-Ads, QoL-Pass; Store-Sandbox testen.
64. [ ] **Kosmetik-System:** Office-Skins, Charakter-Outfits, UI-Themes; keinerlei Gameplay-Vorteile.
65. [ ] **QoL-Funktionen:** Extra-Save-Slots, Automations-Queue; nur Komfort, keine Progression.
66. [ ] **Cloud-Sync:** Platform-SDKs (GPGS/iCloud) + Konfliktlösung (neuester vollständiger Fortschritt).
67. [ ] **Crash-Reporting:** Crashlytics/Sentry integrieren; DSN/PII-Filter aktiv.
68. [ ] **Datenschutz & GDPR:** Opt-in-Dialoge, Tracking-Toggles, „Daten löschen“ im Client.
69. [ ] **Barrierefreiheit:** Skalierbare Schrift, Farbmodi, reduzierte Animationen.
70. [ ] **UI-Polish Pass:** Micro-Interaktionen, Haptik, Ladezeiten; NPS-Fragen nach 5 Sitzungen.
71. [ ] **Minispiel #2 – Bug-Hunt:** Muster erkennen → Tech-Debt −x; 20 s, skill-basiert.
72. [ ] **Minispiel #3 – Pitch-Deck:** Kartenwahl → bessere Investor-Terms bei Erfolg.
73. [ ] **Tutorial v2:** Kürzer, entscheidungsreich; Abbruchstellen aus Telemetrie geschlossen.
74. [ ] **Live-Ops Grundgerüst:** Wöchentliche Challenge (Seed-Preset), Leaderboard (Client-seitig fair).
75. [ ] **Analytics-Dashboards:** D1/D7, FTUE-Funnel, ARPDAU, Ad-Fill; Looker/Metabase einrichten.
76. [ ] **A/B-Framework:** Variant-Zuweisung, Guardrails, Auswertung nach Kohorten.
77. [ ] **Remote-Config Live:** Preise, Idle-Cap, Ad-Frequenzen live steuerbar.
78. [ ] **Lokalisierung EN/DE:** String-Externalisierung, Kontext-Screens, QA.
79. [ ] **Store-Assets v1:** 6 Screens, 30 s Trailer-Skript, ASO-Keywords.
80. [ ] **Pressekit & Community:** Website/Discord, FAQ, devlog-Post vorbereiten.

## Soft-Launch & Global (81–100)

81. [ ] **Content Season 0 komplettieren:** 3–4 Projekttypen, kleiner Tech-Tree, Events-Mix.
82. [ ] **Soft-Launch-Märkte wählen:** CAN/NZ/Skandinavien; Pricing & Ads konservativ.
83. [ ] **Build-Qualifizierung:** Stability ≥ 99,7 %, Crash-Top-3 gefixt, Cold-Start < 3 s.
84. [ ] **Submission & Review:** Store-Compliance prüfen (Privacy, Ads, Zahlungen, Jugendschutz 12+).
85. [ ] **Soft-Launch Live (T-0):** Monitoring 24/48/72 h; War-Room-Runbook bereit.
86. [ ] **FTUE-Optimierung (Woche 1):** Tutorial-Abbrüche fixen; D1-Hebel testen.
87. [ ] **Ökonomie-Feintuning (Woche 2):** Nachfrage/Preis-Kurven kalibrieren; Bottlenecks lösen.
88. [ ] **Ads-Tuning (Woche 3):** Frequency Caps/Placements A/B; No-Ads-Conversion tracken.
89. [ ] **IAP-Preisleiter (Woche 3):** Anker/Bundle-Tests; Refund-Flow prüfen.
90. [ ] **Retention-Layer (Woche 4):** Daily-Quests & Login-Serie (rein kosmetische Rewards).
91. [ ] **Season-Roadmap ankündigen:** S1-Teaser (Gen-Art/Speech), Transparenz zu Fairness.
92. [ ] **Kohorten-Analyse (Woche 5):** D7/D30 & ARPDAU gegen Ziele; Go/No-Go-Gate.
93. [ ] **Lokalisierung v2:** Zusätzliche Sprachen (ES/FR) abhängig vom Potenzial.
94. [ ] **Skalierung Backends:** Ad-Mediation/Analytics Quoten, API-Raten, CDN-Assets prüfen.
95. [ ] **Security-Pass:** Dependency-Audit, Pen-Test-Checkliste, Secrets-Rotation.
96. [ ] **Global-Launch-Checkliste:** Store-Texte final, Trailer, Influencer-Slots, UTM-Links.
97. [ ] **Global Launch (T-0):** Staged Rollout 10%→50%→100%; Monitoring & Hotfix-Pfad.
98. [ ] **Post-Launch Patch 1:** Crash/Balance-Fixes, QoL aus Feedback; Notizen veröffentlichen.
99. [ ] **Season 1 Release:** Neue Projekte (Gen-Art/Speech), Forschung (RL-Grundlagen), Event „Konferenz-Expo“.
100. [ ] **Roadmap H2 & Team-Scaling:** Neue Hiring-Slots, Produktionskalender, Quartals-OKRs festlegen.

---

**Abnahme-Kriterium je Schritt:** „Messbarer Artefakt-Nachweis“ (PR, Build, Dashboard, Testbericht). Erledigte Schritte dokumentieren inklusive Verweis auf die bestandenen Tests.
