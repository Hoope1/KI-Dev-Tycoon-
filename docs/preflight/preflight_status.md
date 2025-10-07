# Preflight Status — KI-Dev-Tycoon

Diese Übersicht dokumentiert den Fortschritt der Preflight-Schritte aus dem `100_schritte_plan.md` und verweist auf zugehörige Artefakte. Alle Entscheidungen sind mit den Leitplanken aus `Zusatz.md` (Python-only) abgeglichen.

## Schritt 1 — Budget-Obergrenze bestätigen & Ausgaben-Tracker anlegen
- **Status:** Erledigt (2025-10-06)
- **Budgetlimit:** ≤ €500 Gesamtbudget gemäss `Zusatz.md`
- **Tracker:** [`budget_tracker.csv`](./budget_tracker.csv) mit laufender Ausgabenübersicht (Datum, Kategorie, Betrag, kumuliert)
- **Annahmen:** Solo-Dev trägt alle Kosten; initialer Stand 0 €
- **Nächste Schritte:** Tracker nach jedem Kauf aktualisieren, monatlich mit tatsächlichen Kontoauszügen abgleichen

## Schritt 2 — Steam-Account-Status prüfen (Partner-Programm aktiv, Zahlungsdaten hinterlegt)
- **Status:** Blockiert (manuelle Prüfung außerhalb des Repos erforderlich)
- **Letzter Check:** 2025-10-06 – Zugriff auf das Steamworks Partner-Portal steht noch aus
- **Aktion:** Beim nächsten Login im Steamworks-Dashboard bestätigen, dass Partner-Programm aktiv ist und Zahlungsdaten verifiziert sind; Screenshot + Kurznotiz im Repo hinterlegen
- **Risiko:** Verzögerte Auszahlung/Veröffentlichung falls Status unklar; frühzeitig erledigen

## Schritt 3 — Python 3.11.8 & Poetry ≥ 1.8 installieren und Umgebung konfigurieren
- **Status:** Blockiert (Installation außerhalb des Containers nötig)
- **Letzter Check:** 2025-10-06 – Lokale Maschine benötigt aktualisierte Python-/Poetry-Version
- **Aktion:** Python 3.11.8 + Poetry 1.8.x installieren, `poetry env use` auf das Projekt zeigen, Versionen in `docs/preflight/tooling_stack.md` ergänzen
- **Risiko:** Ohne korrekte Umgebung können spätere Schritte (Poetry Workspace, PyInstaller) nicht durchgeführt werden

## Schritt 4 — Repository-Setup prüfen und `Zusatz.md` als Source of Truth referenzieren
- **Status:** Erledigt (2025-10-06)
- **Prüfung:** README im Repo-Hauptverzeichnis verweist explizit auf `Zusatz.md` als verbindliche Referenz; `Gameplan.md` und weitere Leitdokumente kennzeichnen sich als Ergänzungen
- **Aktion:** Keine weiteren Maßnahmen nötig, zukünftige Dokumente müssen denselben Hinweis enthalten
- **Risiko:** Niedrig – solange neue Dateien die Source-of-Truth-Regel respektieren

## Schritt 5 — Tooling-Stack festlegen (nur kostenfreie Tools)
- **Status:** Erledigt (2025-10-06)
- **Dokumentation:** [`tooling_stack.md`](./tooling_stack.md) listet Entwicklungs-, Art-, Audio- und Produktivitäts-Tools, alle lizenzkostenfrei gemäß `Zusatz.md`
- **Highlights:** VS Code/PyCharm, Git/GitHub Desktop, Krita/GIMP/Inkscape, Audacity, LibreOffice, draw.io, OBS, Poetry/nox
- **Risiko:** Niedrig – regelmäßige Updates prüfen, kostenpflichtige Erweiterungen vermeiden

## Schritt 6 — Naming- und Namespace-Konventionen definieren
- **Status:** Erledigt (2025-10-06)
- **Dokumentation:** [`naming_conventions.md`](./naming_conventions.md) beschreibt Struktur für `ki_dev_tycoon.core/ui/api/cli`, Assets & Tests
- **Highlights:** Einheitliche Paketstruktur, gespiegelt Tests, Themes/Widgets-Konventionen, Coding-Standards
- **Risiko:** Niedrig – künftige Abweichungen benötigen explizite ADR

## Schritt 7 — Issue-/Task-Board für W1–W6 anlegen
- **Status:** Blockiert (2025-10-06)
- **Dokumentation:** [`task_board_plan.md`](./task_board_plan.md) definiert GitHub-Projects-Setup, Spalten & Milestone-Karten
- **Aktion:** Board im GitHub-Webinterface anlegen und mit Karten befüllen; Link anschließend im Repo ergänzen
- **Risiko:** Mittel – fehlendes Board erschwert Sprint-Tracking; abhängig von GitHub-Zugriff außerhalb des Repos

## Schritt 8 — Architektur-Risiken erfassen & Mitigations notieren
- **Status:** Erledigt (2025-10-06)
- **Dokumentation:** [`risks.md`](./risks.md) fasst Determinismus, Save-Migration, PyInstaller, Steamworks, Offline-Progress, Budget & QA-Risiken zusammen
- **Highlights:** Tabelle mit Beschreibung, Auswirkung, Mitigation; Follow-up-Prozess für Reviews
- **Risiko:** Mittel – Aktualisierung erforderlich, initiale Abdeckung vorhanden

## Schritt 9 — Test-Strategie definieren (inkl. Seed-Plan)
- **Status:** Erledigt (2025-10-06)
- **Dokumentation:** [`test_strategy.md`](./test_strategy.md) beschreibt Testebenen (Unit, Property, Headless, Textual, API) und Seed-Plan
- **Highlights:** Seed-Zuordnung (`1337`, `7331`, `9001`, `424242`, `20251006`, `5150`), KPI-CSV-Export, Reporting-Fluss
- **Risiko:** Mittel – Umsetzung erfordert Einrichtung der Testpakete in W1

## Schritt 10 — Release-Kalender mit Meilensteinen & Deadlines veröffentlichen
- **Status:** Erledigt (2025-10-06)
- **Dokumentation:** [`release_calendar.md`](./release_calendar.md) legt W1–W6 Zeiträume, Deadlines und Launch-Termin fest
- **Highlights:** Wöchentliche Kerntermine, Reminder-Setup, Abhängigkeit zu Steam-Check (Schritt 2)
- **Risiko:** Mittel – Verzögerungen müssen via Board & Reports nachverfolgt werden

## Offene Punkte
- Schritt 2 bleibt Voraussetzung für die Freigabe von Schritt 3.
- Nach Abschluss der externen Checks (Steam, Python-Setup) Status hier aktualisieren und den `100_schritte_plan.md` synchronisieren.
