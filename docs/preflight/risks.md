# Architektur-Risiken & Mitigations — KI-Dev-Tycoon (Preflight Schritt 8)

| Risiko | Beschreibung | Auswirkung | Mitigation |
| --- | --- | --- | --- |
| Determinismusbruch im Sim-Kernel | Direkte Nutzung von `random`, `datetime.now()` oder globalen States zerstört Reproduzierbarkeit. | Inkonsistente Savegames, unvorhersehbare Spielerfahrungen, Tests schlagen fehl. | Strikte Nutzung injizierter `RandomSource`/`TimeProvider`, Unit-/Property-Tests mit festen Seeds, CI-Checks (mypy/pytest/hypothesis). |
| Save-Migration fehlerhaft | Strukturänderungen ohne Versionierung führen zu inkompatiblen Saves. | Spieler verlieren Fortschritt, negative Reviews. | `MigrationRegistry` implementieren, Schema-Version in Savegame pflegen, Roundtrip-Tests, Dokumentation (`docs/migrations`). |
| PyInstaller-Build instabil | Fehlende Abhängigkeiten, falsche Hooks oder signierte DLLs führen zu Crashes. | Build-Blocker, Launch-Verzögerungen. | Frühzeitige Build-Pipeline (`nox -s build`), Logging der PyInstaller-Ausgabe, Smoke-Test jedes Artefakts, Fallback `onedir`-Build. |
| Steamworks-Python-Integration instabil | Wrapper lädt SDK nicht, Achievements werden nicht synchronisiert. | Achievements/Overlay funktionieren nicht, QA- und Launch-Risiko. | Optionale Integration kapseln, Fallback (internes Achievement-Log), Tests mit Dummy-AppID, manueller QA-Plan in W4/W6. |
| Offline-Progress Berechnung fehlerhaft | Große Δt führen zu Overflow oder langer Rechenzeit. | Savegame-Korruption, Softlocks beim Laden. | Analytische Formeln (Schritt 36), Unit-Tests für Grenzwerte, Cap 8–12 h, Fallback segmentiert. |
| Budgetüberschreitung durch Tools/Assets | Kostenpflichtige Tools oder Assets würden Budgetlimit >€500 verletzen. | Verstoß gegen Projektziel, finanzielle Risiken. | Tooling-Stack ausschließlich kostenfrei (Schritt 5), Ausgaben-Tracker pflegen, jede Ausgabe via `budget_tracker.csv` prüfen. |
| Fehlende QA-Automatisierung | Ohne Tests/CI schleichen sich Regressionen ein. | Höhere Bugrate, Verzögerungen. | CI-Skripte für Python (nox, GH Actions) einrichten, nightly Headless-Runs planen, Tests in PR-Gate erzwingen. |

> **Follow-up:** Risiken in wöchentlichen Reviews aktualisieren; neue Risiken via Issues dokumentieren.
