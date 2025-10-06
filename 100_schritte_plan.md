# 100-Schritte-Plan — KI-Dev-Tycoon (Steam-MVP Solo-Dev)

> **Verbindliche Arbeitsanweisung:** Schritte strikt in Reihenfolge gemäß `Zusatz.md` abarbeiten. Ein Schritt gilt erst als erledigt, wenn Ergebnis dokumentiert, getestet und mit den Leitplanken aus `Zusatz.md` abgeglichen ist.

Phasen: **Preflight (1–10)** · **W1 – Projekt & Kernel (11–25)** · **W2 – Daten & Ökonomie (26–40)** · **W3 – UI First Pass (41–55)** · **W4 – Steam & Content (56–70)** · **W5 – Polish & Beta (71–85)** · **W6 – Release (86–95)** · **Post-Launch (96–100)**

---

## Preflight & Governance (1–10)

1. [ ] Budget-Obergrenze (≤ €500) bestätigen, Ausgaben-Tracker anlegen.
2. [ ] Steam-Account-Status prüfen (Partner-Programm aktiv, Zahlungsdaten hinterlegt).
3. [ ] Unity 6 LTS (6000.x) via Hub installieren; Projekteinstellungen für Windows x64 vorbereiten.
4. [ ] Repository-Setup überprüfen: `Zusatz.md` als Source of Truth referenzieren, Legacy-Dokumente kennzeichnen.
5. [ ] Tooling-Stack festlegen (Rider/VS, Git, Git LFS falls nötig, Art-Tools, Audio-Tools) – ausschließlich kostenfrei.
6. [ ] Naming- und Namespace-Konventionen definieren (`Core.Sim`, `Game.App`, `Game.UI`, `Platform.Steam`).
7. [ ] Issue-/Task-Board für W1–W6 anlegen; Checkpoints aus `Zusatz.md` übertragen.
8. [ ] Architektur-Risiken erfassen (Determinismus, Save-Migration, Steamworks) und Mitigations notieren.
9. [ ] Test-Strategie definieren (Unit, Property, Headless-Runner, KPI-CSV) inkl. Seed-Plan.
10. [ ] Release-Kalender mit Meilensteinen und Deadlines (W1–W6) veröffentlichen.

---

## W1 — Projekt & Kernel (11–25)

11. [ ] Unity-Projekt `ai-dev-tycoon` erstellen (2D Core Template, URP deaktivieren).
12. [ ] Basis-Ordnerstruktur laut `Zusatz.md` anlegen (`Scripts/Core.Sim` etc.).
13. [ ] Steamworks.NET via UPM Git einbinden; `steam_appid.txt` konfigurieren.
14. [ ] Bootstrap-Szene mit GameLoop-Script und SteamManager-Placeholder erstellen.
15. [ ] Interfaces `ITimeProvider` und `IRng` implementieren (inkl. PCG32-Tests in C#).
16. [ ] Deterministischen Tick-Loop (0,5 s) implementieren und Unit-Test (Mock-Sim) hinzufügen.
17. [ ] Domain-Grundgerüst `Sim` mit Tick-Dispatch und Event-Publisher anlegen.
18. [ ] Save/Load-Schnittstelle `SaveIO` (JSON + GZip) implementieren, inklusive Pfad-Resolver.
19. [ ] Rotation von 3 Save-Slots (Slot-Metadaten + Autosave) definieren.
20. [ ] Dependency-Injection für Sim/Time/RNG in Bootstrap verkabeln (ScriptableInstaller oder eigenes Setup).
21. [ ] Logging/Diagnostics in Editor-Modus aktivieren (Console + optional Textfile im Dev-Build).
22. [ ] Erste Play-Mode-Tests (EditMode/PlayMode) für Tick & Save ausführen.
23. [ ] Continuous-Integration-Check vorbereiten (lokaler Build + Test-Script).
24. [ ] Dokumentation der Kernel-APIs (XML Comments + `docs/`-Kurzübersicht) verfassen.
25. [ ] Abschluss-W1-Review: Tick-Loop, RNG, Save, Steam-Bootstrap manuell testen und Notizen sammeln.

---

## W2 — Daten & Ökonomie (26–40)

26. [ ] ScriptableObject-Basis `RoleDef`, `ResearchNodeDef`, `ProductDef`, `MarketSegmentDef`, `EventDef` anlegen.
27. [ ] Editor-Inspector anpassen (Custom Editors) für bessere Dateneingabe.
28. [ ] Start-Datenbestand erstellen: 5 Rollen, 3 Marktsegmente, 1 Produkt, Basis-Event-Pool.
29. [ ] Wirtschaftliche Konstanten definieren (Start-Cash, laufende Kosten, Kapazitätsgrenzen).
30. [ ] Forschungssystem: Forschungsqueue, Fortschrittsberechnung pro Tick implementieren.
31. [ ] Hiring-System: Kandidaten-Generator (Poisson/Normal) mit RNG-Stream `hiring` umsetzen.
32. [ ] Training/Skill-Progression pro Tick implementieren (inkl. Burnout-Tracking).
33. [ ] Produkt-Qualitätsformel aus `Zusatz.md` implementieren (tanh + log Datenmenge).
34. [ ] Adoption/Revenue-Modelle (S-Kurve, Preis-Anpassung) in Sim-Kernel integrieren.
35. [ ] Ereignissystem: Weighted-Random-Picker mit Multiplikator-Effekten (Events-Stream) realisieren.
36. [ ] Offline-Progress-Funktion implementieren (analytische Auswertung vs. Tick-Schleife).
37. [ ] Save-Game-Serialisierung für neue Module (Team, Forschung, Produkte, Economy) ergänzen.
38. [ ] Property-Tests/Unit-Tests für Invarianten (Quality ∈ [0,1], Cash ≥ 0 ohne Kredit, Adoption ≤ TAM) schreiben.
39. [ ] Headless-Batchrunner (CLI) erstellen, der 30 Ingame-Tage simuliert und KPI-CSV exportiert.
40. [ ] Abschluss-W2-Review: Balancing-Outputs prüfen, Budget-Impact dokumentieren.

---

## W3 — UI First Pass (41–55)

41. [ ] UI-Foundation: Canvas + EventSystem einrichten, Responsive Layout (16:9) konfigurieren.
42. [ ] Bottom-Navbar mit 5 Tabs (HQ, Team, Forschung, Produkte, Markt) layouten.
43. [ ] HQ-Dashboard-Greybox (Cash, Burn, Reputation, aktive Projekte, Events-Ticker) erstellen.
44. [ ] Team-Ansicht: Liste der Mitarbeitenden, Bewerbungsbatch, Hiring-Dialog (Dummy-Daten) aufbauen.
45. [ ] Forschungs-Screen: Tech-Tree-Visualisierung (Tier-Gruppen, Tooltips) prototypen.
46. [ ] Produkt-Screen: Blueprint→Launch-Flow, Qualitäts-KPI, Pricing-Slider abbilden.
47. [ ] Markt-Screen: Segmente, TAM, Preis-/Qualitäts-Fit, Hype-Indikator darstellen.
48. [ ] Events/Log-Screen: Chronologische Liste mit Tooltip-Effekten und Dauer.
49. [ ] UI-Presenter-Schicht (MVP-Pattern) erstellen, Domain-Events abonnieren.
50. [ ] Tooltips & Hover-States implementieren; Accessibility-Schalter (Animation reduzieren) ergänzen.
51. [ ] TextMeshPro-Styling nach Styleguide (Rubik/Inter, Farbpalette aus `Zusatz.md`).
52. [ ] Erste Icon-/Illustrations-Pass (CC0-Assets) integrieren, Placeholder markieren.
53. [ ] Navigation & Zustandsspeicherung testen (Tab-Wechsel, Modal-Dialoge).
54. [ ] Lokalisierungspipeline vorbereiten (Unity Localization, String-Tables EN/DE).
55. [ ] Abschluss-W3-Review: UX-Notizen sammeln, Performance-Check im Editor (FrameTime ≤ 16 ms).

---

## W4 — Steam & Content (56–70)

56. [ ] Steamworks-Initialisierung finalisieren (Overlay, Callback-Handling, Shutdown-Safety).
57. [ ] Achievement-System `Ach.Unlock` mit Domain-Events verknüpfen.
58. [ ] Startliste Achievements (8–12) final definieren und in Steamworks eintragen.
59. [ ] Rich Presence Strings entwerfen und im Steam-Adapter implementieren.
60. [ ] Savegame-Versionierung (`version`, Migrations-Interface) einführen.
61. [ ] ContentBuilder-Ordnerstruktur vorbereiten (`app_build_<appid>.vdf`).
62. [ ] Automatisiertes Build-Script (Batch/PowerShell) für Headless Windows-Build erstellen.
63. [ ] Erste Windows-IL2CPP-Builds testen (manuell starten, Steam-Overlay prüfen).
64. [ ] Trailer-Capture-Plan erstellen (Shot-Liste, Timeline 30–45 s).
65. [ ] Screenshot-Set (6 Stück) aufnehmen, UI aufräumen.
66. [ ] Store-Text (EN/DE) entwerfen: Short-Description, Long-Description, Feature-Bullets.
67. [ ] Capsule-Art V1 (Header, Library, Hero) gestalten oder aus Asset-Template ableiten.
68. [ ] Presskit-/Marketing-Ordner im Repo anlegen (Screens, Logos, Beschreibung).
69. [ ] QA-Pass: Achievements, Rich Presence, Save/Load Rotation, Offline-Cap testen.
70. [ ] Abschluss-W4-Review: Steam-Checklist abgleichen, Feedback loggen.

---

## W5 — Polish & Beta (71–85)

71. [ ] Balancing-Pass durchführen (Einnahmen, Kosten, Reputation-Drift) anhand Headless-Daten.
72. [ ] Performance-Profiling (Unity Profiler) auf Problemstellen prüfen (CPU/GPU, GC).
73. [ ] UI-Polish: Animationen (LeanTween), Hover/Press-Feedback, Achievement-Toast.
74. [ ] Audio-Pass: UI-Foleys, Münz-SFX, Lautstärke-Balancing, Audio-Toggle.
75. [ ] Accessibility-Review: Farbkontrast ≥ 4.5:1 validieren, Focus-Outlines setzen.
76. [ ] Bugfix-Sprint: Kritische Bugs aus QA-Liste beheben.
77. [ ] Beta-Build intern verteilen (Freundeskreis/Closed Group), Feedback-Formular bereitstellen.
78. [ ] Feedback auswerten, Backlog priorisieren (Must-Fix vs. Post-Launch).
79. [ ] Lokalisierung DE finalisieren, QA-Lauf (Proofread, Layout-Anpassung).
80. [ ] Savegame-Migrationstest (v1 → v1) durchführen, Vorbereitung auf v2 skizzieren.
81. [ ] Automatisierte Tests erweitern (zusätzliche Property-Checks, Regression Seeds).
82. [ ] Crash- und Exception-Logging (Unity Cloud Diagnostics optional deaktiviert) lokal prüfen.
83. [ ] Finaler Code-Review (Self-Review + Checkliste) durchführen.
84. [ ] Release-Notizen (Changelog v0.1.0) schreiben.
85. [ ] Abschluss-W5-Review: Beta-Feedback, Restaufgaben, Launch-Go/No-Go bestätigen.

---

## W6 — Release (86–95)

86. [ ] Finalen Release-Build (IL2CPP) erzeugen, Smoke-Test durchführen.
87. [ ] Steam Depots hochladen (ContentBuilder), Build genehmigen lassen.
88. [ ] Preis €5.99 im Steam-Backend setzen, Steuern prüfen.
89. [ ] Altersfreigaben & rechtliche Hinweise (GDPR, Datenschutzhinweis) bestätigen.
90. [ ] Store-Seite veröffentlichen, sichtbare QA (Screens, Text, Tags) final checken.
91. [ ] Kommunikations-Post (Devlog/Steam News) vorbereiten.
92. [ ] Launch-Day-Runbook (Zeitplan, Checkliste, Support-Kanäle) dokumentieren.
93. [ ] Letzter QA-Pass: Achievements, Save/Load, Offline-Progress, Performance.
94. [ ] Launch durchführen, Status auf allen Kanälen (Website, Social) teilen.
95. [ ] Hotfix-Pfad definieren (Branching, Patch-Build-Schritte).

---

## Post-Launch Monitoring (96–100)

96. [ ] Wishlist→Sale-, Refund-, Review-Daten in den ersten 48 Stunden monitoren und protokollieren.
97. [ ] Crash-Rate prüfen (Steam-Backoffice, Spieler:innen-Feedback) und Issues priorisieren.
98. [ ] Gate A bewerten (Umsatz ≥ €1.000?) und Early-Access-Roadmap ableiten.
99. [ ] Gate B prüfen (CR < 5 % oder Reviews < 80 %?) und Balancing/UX-Plan definieren.
100. [ ] Post-Mortem v0.1.0 verfassen (Was lief gut/schlecht, nächste Schritte) und mit `Zusatz.md` abgleichen.

