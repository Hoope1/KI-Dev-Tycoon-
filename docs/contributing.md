# Beitragende Leitlinien

Dieses Dokument beschreibt das Arbeitsprotokoll für Commits, Branches und Reviews im KI-Dev-Tycoon Monorepo.

## Commit-Richtlinien

Wir verwenden das [Conventional Commits](https://www.conventionalcommits.org/) Schema:

```
<type>[optional scope]: <kurze beschreibung>
```

Zulässige `type`-Werte:

- `feat` – neue Features oder signifikante Erweiterungen
- `fix` – Bugfixes
- `docs` – Dokumentationsänderungen
- `chore` – Wartung, Tooling, Infrastruktur
- `refactor` – Umstrukturierung ohne funktionales Verhalten zu verändern
- `test` – Ergänzungen/Anpassungen an Tests
- `perf` – Performance-Optimierungen

Beispiele:

- `feat(sim): add idle cap validation`
- `docs: update onboarding checklist`
- `chore(ci): bump poetry version`

## Branch-Namensschema

Branches folgen dem Muster:

```
<kategorie>/<kurzbeschreibung-kebab>
```

Empfohlene Kategorien:

- `feature/` für neue Features
- `bugfix/` für Fehlerbehebungen
- `chore/` für Tooling oder Infrastruktur
- `release/` für Release-Vorbereitungen
- `hotfix/` für dringende Patches auf Produktions-Branches

Beispiel: `feature/chatbot-simulation-mvp`.

## Review-Prozess

1. Öffne einen Pull Request gegen `develop` (oder `main` für Hotfixes).
2. Der zuständige CODEOWNER wird automatisch als Reviewer hinzugefügt.
3. Stelle sicher, dass CI (Ruff, Black, mypy, pytest, Coverage) grün ist.
4. Dokumentiere verwendete Seeds/Parameter bei Simulationsänderungen im PR-Text.

## Release-Branches

- `main`: Produktion / Release-Kandidat
- `develop`: Integrationszweig für laufende Arbeiten
- `release/*`: Stabilisierung für anstehende Releases
- `hotfix/*`: schnelle Korrekturen, die direkt nach `main` gehen

## Weitere Hinweise

- Verwende `pre-commit` lokal, um Formatierung/Statik zu prüfen.
- Halte Branches aktuell, bevor du Reviews anforderst (`git fetch && git rebase`).
- Große Änderungen in kleinere, reviewbare Commits aufteilen.
