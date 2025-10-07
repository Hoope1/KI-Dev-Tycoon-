# Tooling-Stack — KI-Dev-Tycoon (Preflight Schritt 5)

Dieser Stack erfüllt die Vorgaben aus `Zusatz.md`: ausschließliche Nutzung kostenfreier Werkzeuge, Fokus auf Windows x64, Solo-Entwicklung. Alle Tools sind lizenzkostenfrei (Community/Open-Source) und decken Programmierung, Versionierung, Art, Audio und Produktivität ab.

## Entwicklungsumgebung
- **IDE/Editor:** Visual Studio Code (Python-Erweiterungen, Textual Devtools) oder PyCharm Community.
- **Python Runtime:** Python 3.11.8 (Windows Store oder offizielle Installer) + Poetry ≥ 1.8.
- **Terminal & Shell:** Windows Terminal + PowerShell 7 bzw. `pwsh` für Builds/Skripte.

## Versionskontrolle & Zusammenarbeit
- **Git:** Standard-Versionsverwaltung (bereits im Projekt). GUI-Option: GitHub Desktop (kostenfrei).
- **Git LFS:** Aktivieren, sobald Binärassets >100 MB anfallen (z. B. Audio-Quellen).
- **Issue-Tracking:** GitHub Projects/Boards (kostenfrei) für Sprint-Planung.

## Grafik & UI
- **2D-Art & Texturen:** Krita (Digital Painting) und GIMP (Rasterbearbeitung).
- **Vektor-Assets & Icons:** Inkscape.
- **Mockups/Wireframes:** Penpot (Open Source, browserbasiert) oder Figma Free Plan (Limit beachten).
- **ASCII/Font Tools:** `figlet`, `monodraw` (alternativ open-source Tools) für Terminal-Darstellung.

## Audio
- **Editing & Mastering:** Audacity.
- **Sound-Bibliothek:** Sonniss GDC Bundles / freesound.org (CC0) – nur lizenzfreie Quellen verwenden.

## Produktivität & Dokumentation
- **Notizen/Planung:** Obsidian (kostenfrei für Personal Use) oder Markdown im Repo.
- **Tabellen/Kalkulation:** LibreOffice Calc (für Budget/Auswertung) zusätzlich zum bestehenden `budget_tracker.csv`.
- **Mindmaps/Diagramme:** draw.io (diagrams.net) offline/Desktop-Version.

## Builds & Automatisierung
- **Python Build-Tools:** Poetry, nox, PyInstaller, Briefcase (optional) – bereits im Repo vorgesehen.
- **CI:** GitHub Actions (Python 3.11/3.12 Matrix), lokale nox-Skripte.
- **Testing Tools:** pytest, hypothesis, textual.testing, mypy, ruff, bandit, pip-audit.

> **Hinweis:** Alle Tools müssen regelmäßig auf Updates geprüft werden; kostenpflichtige Erweiterungen sind zu vermeiden, um das Budgetlimit ≤ €500 einzuhalten.
