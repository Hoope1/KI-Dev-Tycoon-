# 100-Schritte-Plan — KI-Dev-Tycoon (Steam-MVP Solo-Dev, Python-only)

> **Verbindliche Arbeitsanweisung:** Schritte strikt in Reihenfolge gemäß `Zusatz.md` abarbeiten. Ein Schritt gilt erst als erledigt, wenn Ergebnis dokumentiert, getestet und mit den Leitplanken aus `Zusatz.md` abgeglichen ist.

Phasen: **Preflight (1–10)** · **W1 – Projekt & Kernel (11–25)** · **W2 – Daten & Ökonomie (26–40)** · **W3 – UI First Pass (41–55)** · **W4 – Distribution & Content (56–70)** · **W5 – Polish & Beta (71–85)** · **W6 – Release (86–95)** · **Post-Launch (96–100)**

---

## Preflight & Governance (1–10)

1. [x] Budget-Obergrenze (≤ €500) bestätigen, Ausgaben-Tracker anlegen. (siehe `docs/preflight/`)
2. [ ] Steam-Account-Status prüfen (Partner-Programm aktiv, Zahlungsdaten hinterlegt, PyInstaller-Builds erlaubt).
3. [ ] Python 3.11.8 + Poetry ≥ 1.8 installieren, `poetry env use` konfigurieren.
4. [x] Repository-Setup überprüfen: `Zusatz.md` als Source of Truth referenzieren, Legacy-Dokumente kennzeichnen.
5. [x] Tooling-Stack festlegen (VS Code/PyCharm, Git, OBS, Krita/Inkscape, Audacity) – ausschließlich kostenfrei.
6. [x] Naming- und Namespace-Konventionen definieren (`ki_dev_tycoon.core`, `.ui`, `.api`, `.cli`).
7. [ ] Issue-/Task-Board für W1–W6 anlegen; Checkpoints aus `Zusatz.md` übertragen.
8. [x] Architektur-Risiken erfassen (Determinismus, PyInstaller, Steamworks-Python) und Mitigations notieren.
9. [x] Test-Strategie definieren (pytest, hypothesis, textual.testing, CLI-Snapshots) inkl. Seed-Plan.
10. [x] Release-Kalender mit Meilensteinen und Deadlines (W1–W6) veröffentlichen.

---

## W1 — Projekt & Kernel (11–25)

11. [ ] Poetry-Workspace einrichten (`sim/`, `app/`), gemeinsame `pyproject.toml`-Konfiguration prüfen.
12. [ ] Basis-Paket `ki_dev_tycoon.core` erstellen (Tick-Loop, `RandomSource`, `TimeProvider`).
13. [ ] CLI-Grundlage (`ki-sim`) mit Typer anlegen (`poetry run ki-sim --help`).
14. [ ] Deterministische Tick-Schleife implementieren (0,5 s) und Unittests (`tests/unit/core/test_tick_loop.py`).
15. [ ] Ereignisbus (`EventBus`) erstellen, Publikation/Subscription testen.
16. [ ] Savegame-Schema `v1` definieren (Pydantic-Modelle, JSON + zstd) inkl. Roundtrip-Test.
17. [ ] Dependency-Injection (Factory/Providers) für Simulation, RNG, Clock implementieren.
18. [ ] Logging-Framework (structlog oder logging + Rich) konfigurieren, CLI-Output formatieren.
19. [ ] Basiskonfiguration (`config/default.yaml`) + Loader (`config.loader`) implementieren.
20. [ ] Pre-commit-Hooks (ruff, black, isort, mypy, pytest, bandit, pip-audit) aktivieren.
21. [ ] GitHub Actions/CI aktualisieren (Python 3.11/3.12 Matrix, nox Sessions `lint`, `typecheck`, `tests`).
22. [ ] Erste Hypothesis-Property-Tests für RNG/Clock-Invarianten erstellen.
23. [ ] CLI-Dokumentation (`sim/README.md`) aktualisieren, Beispiele beifügen.
24. [ ] Headless-Smoke-Test (`nox -s smoke`) definieren (10 Tage Simulation, Log-Check).
25. [ ] Abschluss-W1-Review: Kernel, CLI, Save/Load, Tests durchgehen; Findings dokumentieren.

---

## W2 — Daten & Ökonomie (26–40)

26. [ ] Assets-Ordner (`assets/`) strukturieren; YAML-Schemata (roles, products, markets, research, events) anlegen.
27. [ ] Loader/Validator für Assets (Pydantic `RootModel`) implementieren; Schema-Tests.
28. [ ] Start-Datenbestand erstellen: 5 Rollen, 3 Marktsegmente, 1 Produkt, Basis-Event-Pool.
29. [ ] Wirtschaftliche Konstanten definieren (Start-Cash, laufende Kosten, Kapazitätsgrenzen) + Tests.
30. [ ] Forschungssystem: Forschungsqueue, Fortschrittsberechnung pro Tick implementieren.
31. [ ] Hiring-System: Kandidaten-Generator (Poisson/Normal) mit RNG-Stream `hiring` umsetzen.
32. [ ] Training/Skill-Progression pro Tick implementieren (inkl. Burnout-Tracking, Moral-Effekte).
33. [ ] Produkt-Qualitätsformel (tanh + log Datenmenge) implementieren, Unittests & Hypothesis.
34. [ ] Nachfrage-/Revenue-Modelle (S-Kurve, Preis-Anpassung) in Sim-Kernel integrieren.
35. [ ] Ereignissystem: Weighted-Random-Picker mit Multiplikator-Effekten (Events-Stream) realisieren.
36. [ ] Offline-Progress-Funktion implementieren (analytisch, Cap 10 h) + Tests.
37. [ ] Savegame-Serialisierung für neue Module (Team, Forschung, Produkte, Economy) ergänzen.
38. [ ] Property-Tests/Unit-Tests für Invarianten (Quality ∈ [0,1], Cash ≥ 0 ohne Kredit, Adoption ≤ TAM) schreiben.
39. [ ] Headless-Batchrunner (CLI) erstellen, der 30 Ingame-Tage simuliert und KPI-CSV exportiert.
40. [ ] Abschluss-W2-Review: Balancing-Outputs prüfen, Budget-Impact dokumentieren.

---

## W3 — UI First Pass (41–55)

41. [ ] Textual-App-Grundgerüst (`ki_dev_tycoon.ui.app:TycoonApp`) erstellen.
42. [ ] Navigation (Tab-Bar oder Dock) mit fünf Haupt-Screens (Dashboard, Team, Forschung, Produkte, Markt) implementieren.
43. [ ] Dashboard-Greybox: Cash, Burn, Reputation, aktive Projekte, Event-Log.
44. [ ] Team-Screen: Liste der Mitarbeitenden, Bewerbungsbatch, Hiring-Dialog (Mock-Daten).
45. [ ] Forschungs-Screen: Tech-Tree-Visualisierung (Tree Control oder Table + Tooltip) prototypen.
46. [ ] Produkt-Screen: Blueprint→Launch-Flow, Qualitäts-KPI, Pricing-Slider abbilden.
47. [ ] Markt-Screen: Segmente, TAM, Preis-/Qualitäts-Fit, Hype-Indikator darstellen.
48. [ ] Event/Log-Screen: Chronologische Liste mit Tooltip-Effekten und Dauer.
49. [ ] Presenter-Schicht (ViewModel) erstellen, Domain-Events abonnieren.
50. [ ] Theme-System implementieren (Light/Dark, farbenblind-sicher) inkl. Settings-Dialog.
51. [ ] Internationalisierung vorbereiten (gettext oder `babel`, String-Ressourcen EN/DE).
52. [ ] Erste Icon-/ASCII-Art-Pass integrieren, Placeholder kennzeichnen.
53. [ ] Navigation & Zustandsspeicherung testen (Tab-Wechsel, Modal-Dialoge, Backstack).
54. [ ] Textual-Snapshot-Tests (`textual.testing`) für Hauptscreens einrichten.
55. [ ] Abschluss-W3-Review: UX-Notizen sammeln, Performance-Check (Tick ≤ 5 ms, UI-Frame ≤ 16 ms).

---

## W4 — Distribution & Content (56–70)

56. [ ] Achievement-System implementieren (Core-Tracking, UI-Anzeige, optional Steamworks-Binding).
57. [ ] PyInstaller-Konfiguration erstellen (Spec-File, Assets bundeln, CLI + UI entrypoints).
58. [ ] Build-Skript `app/tools/build_app.py` implementieren (OneFile/OneDir, Versionierung, Hash).
59. [ ] Steam-Upload-Skript (`app/tools/steam_upload.py`) vorbereiten (steamcmd, Depot-Struktur).
60. [ ] Savegame-Versionierung (`version`, Migration-Interface) finalisieren.
61. [ ] Automatisiertes Build-&-Test-Szenario (`nox -s build`) definieren (Build + Smoke-Test aus Artifact).
62. [ ] Marketing-Assets vorbereiten: Theme-Export, Fonts, ASCII-Keyart.
63. [ ] Trailer-Capture-Plan erstellen (Shot-Liste, Timeline 30–45 s) + OBS-Scene-Setup.
64. [ ] Screenshot-Set (6 Stück) aufnehmen (Textual Themes, unterschiedliche States).
65. [ ] Store-Text (EN/DE) entwerfen: Short-Description, Long-Description, Feature-Bullets.
66. [ ] Presskit-/Marketing-Ordner im Repo anlegen (`docs/presskit/`).
67. [ ] QA-Pass: Achievements, Save/Load Rotation, Offline-Cap, PyInstaller-Builds testen.
68. [ ] Lokale API (`ki_dev_tycoon.api`) lauffähig machen, UI-Autodetect zwischen Embedded/HTTP.
69. [ ] Benchmark-Szenarien (`benchmarks/`) konfigurieren (pytest-benchmark, 30 Tage Simulation).
70. [ ] Abschluss-W4-Review: Distribution-Checklist abgleichen, Feedback loggen.

---

## W5 — Polish & Beta (71–85)

71. [ ] Balancing-Pass durchführen (Einnahmen, Kosten, Reputation-Drift) anhand Headless-Daten.
72. [ ] Performance-Profiling (pyinstrument, Textual Devtools) auf Problemstellen prüfen (CPU/GPU, GC).
73. [ ] UI-Polish: Animationen (Textual `animate`), Hover/Press-Feedback, Achievement-Toast.
74. [ ] Audio-Pass: UI-Foleys (simpleaudio), Lautstärke-Balancing, Audio-Toggle.
75. [ ] Accessibility-Review: Farbkontrast ≥ 4.5:1 validieren, Screenreader-Labels setzen.
76. [ ] Bugfix-Sprint: Kritische Bugs aus QA-Liste beheben.
77. [ ] Beta-Build intern verteilen (Steam-Branch oder Itch-Key), Feedback-Formular bereitstellen.
78. [ ] Feedback auswerten, Backlog priorisieren (Must-Fix vs. Post-Launch).
79. [ ] Lokalisierung DE finalisieren, QA-Lauf (Proofread, Layout-Anpassung).
80. [ ] Savegame-Migrationstest (v1 → v1) durchführen, Vorbereitung auf v2 skizzieren.
81. [ ] Automatisierte Tests erweitern (zusätzliche Property-Checks, Regression Seeds, UI-Snapshots).
82. [ ] Crash- und Exception-Logging (structured logs, optional Sentry-Selfhost) evaluieren.
83. [ ] Finaler Code-Review (Self-Review + Checkliste) durchführen.
84. [ ] Release-Notizen (Changelog v0.1.0) schreiben.
85. [ ] Abschluss-W5-Review: Beta-Feedback, Restaufgaben, Launch-Go/No-Go bestätigen.

---

## W6 — Release (86–95)

86. [ ] Finalen PyInstaller-Build erzeugen (OneFile + OneDir), Smoke-Test durchführen.
87. [ ] Steam Depots hochladen (steamcmd), Build genehmigen lassen.
88. [ ] Preis €5.99 im Steam-Backend setzen, Steuern prüfen.
89. [ ] Altersfreigaben & rechtliche Hinweise (GDPR, Datenschutzhinweis) bestätigen.
90. [ ] Store-Seite veröffentlichen, sichtbare QA (Screens, Text, Tags) final checken.
91. [ ] Kommunikations-Post (Devlog/Steam News) vorbereiten.
92. [ ] Launch-Day-Runbook (Zeitplan, Checkliste, Support-Kanäle) dokumentieren.
93. [ ] Letzter QA-Pass: Achievements, Save/Load, Offline-Progress, Performance (Release-Build).
94. [ ] Launch durchführen, Status auf allen Kanälen (Website, Social) teilen.
95. [ ] Hotfix-Pfad definieren (Branching, Patch-Build-Schritte, Versionierung).

---

## Post-Launch Monitoring (96–100)

96. [ ] Wishlist→Sale-, Refund-, Review-Daten in den ersten 48 Stunden monitoren und protokollieren.
97. [ ] Crash-Rate prüfen (Steam-Backoffice, Logs) und Issues priorisieren.
98. [ ] Gate A bewerten (Umsatz ≥ €1.000?) und Early-Access-Roadmap ableiten.
99. [ ] Gate B prüfen (CR < 5 % oder Reviews < 80 %?) und Balancing/UX-Plan definieren.
100. [ ] Post-Mortem v0.1.0 verfassen (Was lief gut/schlecht, nächste Schritte) und mit `Zusatz.md` abgleichen.

