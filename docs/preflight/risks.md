# Architektur-Risiken & Mitigations — KI-Dev-Tycoon (Preflight Schritt 8)

| Risiko | Beschreibung | Auswirkung | Mitigation |
| --- | --- | --- | --- |
| Determinismusbruch im Sim-Kernel | Direkte Nutzung von `System.Random`, `DateTime.Now` oder Unity-spezifischen Ticks könnte deterministische Abläufe zerstören. | Inkonsistente Savegames, unvorhersehbare Spielerfahrungen, Tests schlagen fehl. | Strikte Nutzung injizierter `IRng`/`ITimeProvider`, Unit-/Property-Tests mit festen Seeds, Code-Reviews auf Random/Time-Aufrufe, CI-Checks (mypy/pytest) im Python-Prototyp. |
| Save-Migration fehlerhaft | Strukturänderungen ohne Versionierung führen zu inkompatiblen Saves. | Spieler verlieren Fortschritt, negative Reviews. | `ISaveMigrator`-Interface implementieren, Schema-Version in Savegame pflegen, Migrations-Tests (Roundtrip), Dokumentation der Änderungen (`docs/migrations`). |
| Steamworks-Integration instabil | Falsche Initialisierung/Shutdown, fehlende Callbacks, Achievements werden nicht gespeichert. | Achievements/Overlay funktionieren nicht, QA- und Launch-Risiko. | SteamManager-Wrapper mit Init/Shutdown-GUards, Logging, Integrationstests mit Dummy-AppID, Checklisten für Release (Schritt 69). |
| Offline-Progress Berechnung fehlerhaft | Große Δt führen zu Overflow oder langer Rechenzeit. | Savegame-Korruption, Softlocks beim Laden. | Analytische Formeln implementieren (Schritt 36), Unit-Tests für Grenzwerte, Cap von 8–12 h, Fallback auf segmentierte Berechnung. |
| Budgetüberschreitung durch Tools/Assets | Kostenpflichtige Tools oder Assets würden Budgetlimit >€500 verletzen. | Verstoß gegen Projektziel, finanzielle Risiken. | Tooling-Stack ausschließlich kostenfrei (Schritt 5), Ausgaben-Tracker pflegen, jede Ausgabe via `budget_tracker.csv` prüfen. |
| Fehlende QA-Automatisierung | Ohne Tests/CI schleichen sich Regressionen ein. | Höhere Bugrate, Verzögerungen. | CI-Skripte für Unity/Python aufsetzen (Schritt 23), nightly Builds planen, Tests in PR-Gate erzwingen. |

> **Follow-up:** Risiken in wöchentlichen Reviews aktualisieren; neue Risiken via Issues dokumentieren.
