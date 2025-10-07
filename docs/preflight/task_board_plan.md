# Issue- & Task-Board Setup — KI-Dev-Tycoon (Preflight Schritt 7)

Da das tatsächliche GitHub-Projektboard außerhalb des Repos verwaltet wird, beschreibt dieses Dokument die Struktur und Checkpoints gemäß `Zusatz.md`.

## Board-Plattform
- **Tool:** GitHub Projects (Beta) oder klassische Kanban-Ansicht (kostenfrei).
- **Projektname:** `KI-Dev-Tycoon Roadmap W1–W6`.
- **Zugriff:** Privat, nur Solo-Dev; optional Reviewer:innen mit Read-Rechten.

## Spaltenstruktur
1. **Backlog** – Unpriorisierte Ideen/Stretch-Ziele.
2. **Todo (Aktueller Sprint)** – Aufgaben der laufenden Woche.
3. **In Progress** – Aktiv bearbeitete Tasks.
4. **Review/Blockiert** – Aufgaben mit Pending-Check (z. B. externe Abhängigkeit, QA).
5. **Done** – Abgeschlossene Tasks mit Tests/Docs.

## Wöchentliche Milestones & Key Tasks
- **W1 — Projekt & Kernel**
  - Poetry-Workspace einrichten, Tick-Loop + RNG implementieren, Save/Load, CI grün.
  - Tasks: `Workspace setup`, `Implement tick loop`, `Event bus + RNG`, `Save schema v1`, `CI pipeline ready`.
- **W2 — Daten & Ökonomie**
  - YAML-Assets, Hiring/Forschung/Training Systeme, Ökonomie-Konstanten, Events.
  - Tasks: `Define asset schemas`, `Implement research queue`, `Hiring generator`, `Economy constants`, `Event picker`.
- **W3 — UI First Pass**
  - Textual-App Grundgerüst, Tab-Navigation, Screens Greybox, Presenter-Layer, i18n Setup.
- **W4 — Distribution & Content**
  - Achievements, PyInstaller Spec, Save-Versionierung, Store-Assets (Screenshots, Texte), Build-Skripte.
- **W5 — Polish & Beta**
  - Balancing-Pass, Profiling, UI-/Audio-Polish, Accessibility, Beta-Feedback.
- **W6 — Release**
  - Finaler Build, Depot Upload, Pricing/Compliance, Launch Runbook, Hotfix Pfad.

## Checkpoints & Reporting
- Wöchentliche Review-Notiz im Repo (`docs/reports/week_<n>.md`, später erstellen).
- Offene Blocker (z. B. Steam-Account, PyInstaller Code Signing) im Board als Karten (`Blocker: Steam Partner check`).
- Jede Karte referenziert `Zusatz.md` Abschnitt + relevante Schritt-Nummer.

> **Next Action:** Board im GitHub-Webinterface anlegen, Spalten & Karten laut Liste erstellen, anschließend Link im Repo (z. B. README/Docs) ergänzen.
