# Tooling-Stack — KI-Dev-Tycoon (Preflight Schritt 5)

Dieser Stack erfüllt die Vorgaben aus `Zusatz.md`: ausschließliche Nutzung kostenfreier Werkzeuge, Fokus auf Windows x64, Solo-Entwicklung. Alle Tools sind lizenzkostenfrei (Community/Open-Source) und decken Programmierung, Versionierung, Art, Audio und Produktivität ab.

## Entwicklungsumgebung
- **IDE/Editor:** Visual Studio Code (kostenfrei, umfangreiches Ökosystem) mit C#- und Unity-Erweiterungen.
- **Alternative IDE:** Visual Studio Community 2022 (für C#/Unity, Lizenz frei für Solo-Indies), optional Rider-Ersatz.
- **Terminal & Shell:** Windows Terminal + PowerShell 7 für Builds/Skripte.

## Versionskontrolle & Zusammenarbeit
- **Git:** Standard-Versionsverwaltung (bereits im Projekt). GUI-Option: GitHub Desktop (kostenfrei).
- **Git LFS:** Aktivieren, sobald Binärassets >100 MB anfallen (z. B. Art/Audio-Quellen).
- **Issue-Tracking:** GitHub Projects/Boards (kostenfrei) für Sprint-Planung.

## Grafik & UI
- **2D-Art & Texturen:** Krita (Digital Painting) und GIMP (Rasterbearbeitung).
- **Vektor-Assets & Icons:** Inkscape.
- **Mockups/Wireframes:** Penpot (Open Source, browserbasiert) oder Figma Free Plan (solange Limit ausreicht).

## Audio
- **Editing & Mastering:** Audacity.
- **Sound-Bibliothek:** Sonniss GDC Bundles / freesound.org (CC0) – nur lizenzfreie Quellen verwenden.

## Produktivität & Dokumentation
- **Notizen/Planung:** Obsidian (kostenfrei für Personal Use) oder Markdown im Repo.
- **Tabellen/Kalkulation:** LibreOffice Calc (für Budget/Auswertung) zusätzlich zum bestehenden `budget_tracker.csv`.
- **Mindmaps/Diagramme:** draw.io (diagrams.net) offline/Desktop-Version.

## Builds & Automatisierung
- **Unity Hub:** Verwaltung der Unity-Installationen (siehe Schritt 3, manuell).
- **CI-Skripte:** GitHub Actions (bestehende Pipeline) und lokale Batch-/PowerShell-Skripte.
- **Python-Tooling:** Poetry/Nox (bereits im Repo) für den Sim-Kernel.

> **Hinweis:** Alle Tools müssen regelmäßig auf Updates geprüft werden; kostenpflichtige Erweiterungen sind zu vermeiden, um das Budgetlimit ≤ €500 einzuhalten.
