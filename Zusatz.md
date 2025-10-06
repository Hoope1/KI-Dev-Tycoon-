# Zusatz — KI-Dev-Tycoon (Steam-MVP, Solo-Dev, ≤ €500)

*Stand: 06.10.2025 (Europe/Vienna)*

Dieses Dokument ist die zentrale Referenz für alle Architektur-, Design- und Produktionsentscheidungen des Projekts **KI-Dev-Tycoon**. Ziel ist eine sofort umsetzbare Solo-MVP-Umsetzung auf Steam (Windows, offline) mit einem einmaligen Kaufpreis von €5.99 und einem Gesamtbudget ≤ €500.

---

## 1) Entscheidungen & Projektleitplanken (Summary)

- **Plattform (MVP):** Steam (Windows x64, Desktop)
- **Team & Budget:** Solo-Entwickler:in, Gesamtbarbudget ≤ €500
- **Online/Cloud:** Kein Backend, keine Cloud-Komponenten, reine Offline-Simulation
- **Monetarisierung:** Paid up-front (€5.99), keine Ads, keine IAPs
- **Region (Launch-Pflicht):** Fokus Österreich (Steam-Release weltweit zulässig)
- **Engine:** Unity 6 LTS (6000.x)
- **Architektur:** Strikte Trennung Sim-Kernel (deterministisch) ↔ Client/UI
- **Tick-Rate:** Fix 0,5 s (Accumulator-Loop)
- **Achievements:** 8–12 Steam-Achievements (kein Cloud-Save, keine Leaderboards)
- **Lokalisierung & Accessibility:** EN/DE, skalierbare Schrift, farbenblind-sichere Paletten, reduzierte Animationen optional
- **Art-Direction:** „Tycoon bunt“, isometrisch/2.5D, kontrastreiche verspielte UI
- **Nicht-Ziele (MVP):** Keine Ads/IAPs/Push/Telemetry-Cloud/PvP/UGC/Always-Online

---

## 2) Background

**Produktidee & Zielsetzung.** Desktop-Tycoon, der den Aufbau eines KI-Unternehmens simuliert. Fokus: glaubwürdige KI-Anspielungen, Sessions 5–20 Minuten, langfristige Meta-Progression, faire Monetarisierung.

**Plattform & Audience.** Windows (Steam, 16:9, Maus/Keyboard), Zielgruppe 16–45, tech-affin.

**Erfolgsmaße (Post-Launch-Gate).** Wishlist→Kauf-Conversion ≥ 10 % am Launch-Tag, Refund-Rate ≤ 8 %, ≥ 75 % positive Reviews (n≥20), Crash-Rate ≤ 0,3 %.

**Architektur-Leitplanken.** Simulations-Kernel deterministisch (Seed/Time-Injection), Tests ≥ 90 % Coverage, stabile API/Versionierung, CI/CD mit Lint/Typing/Tests. Keine Unity-APIs im Kernel.

**Prozess.** Source of Truth: dieses Dokument. Balancing-Assets nur via Review. Seeds/Snapshots reproduzierbar halten.

---

## 3) Requirements (MoSCoW)

**Must**

- Budget/Team: Solo-Dev, ≤ €500 (inkl. Gebühren/Assets/Store)
- Plattform: Windows (Steam), 16:9, Ziel 60 FPS; IL2CPP im Release
- Offline-Only: deterministische Tick-Simulation, lokale Save-Slots + Migration; kein Backend
- Kern-Loops: Hiring, Forschung (Modelle/Datasets), Training (Kosten/Qualität), Produkt-Launches, Umsatz/Skalierung, Events
- Monetarisierung: €5.99, ohne Ads/IAPs
- Distribution: Veröffentlichung mindestens in Österreich
- Compliance: GDPR-freundlich; minimale Berechtigungen; keine externen Tracker
- Lokalisierung & Accessibility: EN/DE, skalierbare Schrift, farbenblind-freundliche Paletten
- Build/CI: Unity 6 LTS, deterministischer Kernel (Tests ≥ 90 %), Lint/Static-Analysis, Nightly Local Builds

**Should**

- Store-Assets: 30–45 s Trailer (In-Engine Captures), 6 Screenshots, Key-Art
- Steam-Deck-Check: Basiskompatibilität prüfen
- Optionale Demo: itch.io-Build für Wishlist/Feedback

**Could**

- Cosmetics/Skins, Challenges, erweiterte Achievements
- Season-Mini-Events (rein kosmetisch)

**Won't (MVP)**

- Ads, IAPs, Remote-Config, Push-Notifications, Telemetrie-Cloud, Always-Online, PvP, UGC

---

## 4) Method (Technische Methode)

### 4.1 Architektur (Steam · Offline · Solo-Dev)

**Engine & Versioning.** Unity 6.0 LTS (6000.x); Export Windows x64; IL2CPP Release, Mono im Editor.

**Steam-Integration.** Steamworks.NET (MIT) für Achievements/Overlay; ohne Steam Cloud; Integration via Unity Package Manager (Git).

**Schichten.**

- `Core.Sim` — deterministischer Sim-Kernel (reines C#, keine Unity-APIs)
- `Core.Data` — statische Balancing-Daten (ScriptableObjects) + Loader
- `Game.UI` — UGUI (Canvas/TMP), Presenter/MVP-Pattern
- `Game.App` — Bootstrap, Tick-Loop, DI-Wire-up, Save/Load
- `Platform.Steam` — dünner Adapter (Achievements/Rich Presence)

**Determinismus.** Fixe Tick-Rate 0,5 s; `ITimeProvider`/`IRng` injizieren; kein `DateTime.Now` oder `System.Random` im Kernel.

**Persistenz.** JSON + GZip, 1–3 Rotations-Slots, Migrations-Layer `ISaveMigrator` (`vN → vN+1`).

```
@startuml
package "Game Client (Unity)" {
  [Bootstrap] --> [GameLoop]
  [UI Layer] --> [Presenters]
}
package "Core" {
  [Sim Kernel] --> [RNG]
  [Sim Kernel] --> [Time Provider]
  [Sim Kernel] --> [Data Catalog]
}
package "Platform" {
  [Steam Adapter]
}
[Bootstrap] --> [Steam Adapter]
[GameLoop] --> [Sim Kernel]
[GameLoop] --> [Save System]
[Presenters] --> [Sim Kernel]
[Save System] --> [File (JSON.GZ)]
@enduml
```

### 4.2 Tick-Loop & Offline-Berechnung

- Fixed-Tick-Accumulator: `acc += delta; while (acc >= Tick) { Sim.Tick(); acc -= Tick; }`
- Offline-Progress: `dt = clamp(now-lastSave, 0, capHours*3600)`; `n = floor(dt / Tick)`; für große `dt` analytische Formeln (z. B. S-Kurven) statt per-Tick-Iteration
- Seed & RNG: PCG32 mit `worldSeed`, `companyId`, `dayIndex` als Stream-Keys (replayable)

```
@startuml
actor Player
Player -> App: Start
App -> SaveSystem: Load(ActiveSlot)
SaveSystem --> App: SaveState(lastTime, seed, ...)
App -> Sim: ApplyOfflineProgress(dt)
App -> UI: ShowMainMenu
== Runtime ==
loop Every Frame
  App -> GameLoop: Update(delta)
  GameLoop -> Sim: Tick() (0.5s)
  Sim --> UI: DomainEvents (pub/sub)
end
== Quit ==
UI -> SaveSystem: Save()
@enduml
```

### 4.3 Datenmodelle & Schemas (MVP)

**IDs.** Referenzen per `string id` (kebab-case); keine direkten Objekt-Referenzen in Saves.

**ScriptableObjects (statisch).**

- `RoleDef { id, name, baseSalary, skills{ml,data,eng,prod}, hireWeight }`
- `ResearchNodeDef { id, name, tier, cost, timeHrs, prereqIds[], grants{modelQuality+, infraCap+, featureFlags[]} }`
- `ProductDef { id, name, segmentId, baseK, baseChurn, priceRange, costPerUser }`
- `MarketSegmentDef { id, name, TAM, priceElasticity, techAffinity }`
- `EventDef { id, name, weight, triggerRules, effects{multiplier,target,duration} }`

**Save (JSON v1 Beispiel).**

```json
{
  "version": 1,
  "created_at": "2025-10-06T08:00:00Z",
  "last_time": "2025-10-06T10:00:00Z",
  "seed": 9201531,
  "company": {
    "name": "My AI Co",
    "reputation": 0.0,
    "cash": 20000,
    "burn_rate": 0,
    "employees": ["emp-001", "emp-002"],
    "research_queue": ["res-basic-nlp"],
    "active_products": ["prod-chatbot-a"]
  },
  "employees": {
    "emp-001": {
      "role": "ml-engineer",
      "level": 1,
      "skills": {"ml": 3, "data": 2, "eng": 2, "prod": 1},
      "salary": 2200
    },
    "emp-002": {
      "role": "data-scientist",
      "level": 1,
      "skills": {"ml": 2, "data": 3, "eng": 1, "prod": 1},
      "salary": 2100
    }
  },
  "research": {
    "unlocked": ["res-basic-nlp"],
    "in_progress": []
  },
  "products": {
    "prod-chatbot-a": {
      "def": "chatbot",
      "launch_day": 10,
      "users": 0,
      "price": 6.99,
      "quality": 0.42
    }
  },
  "economy": {"day": 12, "inflation": 0.02},
  "rng_stream": {"hiring": 12345, "events": 777, "market": 444}
}
```

### 4.4 Kern-Formeln (einfach, erweiterbar)

- **Hiring (pro Tag):** `N ~ Poisson(λ)` Kandidat:innen; Qualität `q ~ Normal(μ(role)+β*reputation, σ)`; Gehalt `salary = baseSalary(role) * (1 + q * k_q + marketAdj)`
- **Forschung/Training (pro Tick):** `dp = (Σ staffSkill * roleWeight) * labMultiplier * (1 - burnout)`; Abschluss bei Σdp ≥ `cost`
- **Produkt-Qualität:** `quality = tanh(a * modelQuality + b * ln(dataQty + 1) + c * infraCap)`
- **Adoption (S-Kurve):** `users(t) = K / (1 + e^(−r*(t−t0)))`, `K = TAM * fit(quality, price)`, `r` skaliert mit Reputation/Marketing
- **Umsatz pro Tick:** `rev = users * price / ticksPerDay * ARPUmult - costPerUser * users / ticksPerDay`
- **Events:** gewichtete Auswahl; Effekte als Multiplikatoren mit Dauerfenster

### 4.5 Dateistruktur & Pakete

```
Assets/
  _Project/
    Scripts/
      Core.Sim/
      Core.Data/
      Game.UI/
      Game.App/
      Platform.Steam/
    Data/
      RoleDefs/*.asset
      Research/*.asset
      Products/*.asset
      Markets/*.asset
      Events/*.asset
    Resources/
    Addressables/
Build/
```

**Unity-Pakete.** TextMeshPro, Input System, Addressables (lokal), Localization (DE/EN).

### 4.6 Steam-Schnittstellen (MVP-Umfang)

- Init & Overlay: `SteamAPI.Init()` / `SteamAPI.Shutdown()`; Overlay Toggle; `steam_appid.txt` im Projektroot
- Achievements: 8–12 Ziele (z. B. erstes Produkt, 10k User, erste Forschung Tier 2)
- Rich Presence: Status-String (z. B. „Day 12 • 1 Product • 5 Staff“)

### 4.7 Vergleichende Referenzen (Design-Ableitungen)

- *Game Dev Tycoon* (Projekt-Phasen → Produkt-Score/Qualität)
- *Software Inc.* (Personal-Management → Rollen/Skills vereinfacht)
- *Startup Company* (Feature-Roadmaps → Research-Nodes/Feature-Flags)

### 4.8 Testbarkeit & Determinismus

- Golden-Seeds: fixe Seeds + Save-Snapshots für Regression
- Property-Tests: Invarianten (Adoption ≤ TAM, Cash nicht negativ ohne Kredit-System)
- Headless-Runner: CLI-Simulation N-Tage für Balancing-Batches (CSV-Dump lokal)

### 4.9 Visual Style Guide — „Tycoon bunt“ (isometrisch/2.5D)

- **Palette:** Primär Indigo #4F46E5; Akzente Amber #F59E0B, Emerald #10B981, Pink #EC4899; Neutrals #F5F7FB/#FFFFFF; Text #0F172A/#475569; Status Success #16A34A, Warning #F59E0B, Danger #EF4444; Kontrast Body ≥ 4.5:1
- **Typografie:** Headline Rubik (Semibold), Body Inter (Regular)
- **Komponenten:** Buttons Radius 14–16 px, Shadow (0,4,12,0.2), Hover +4 %, Press-Scale 0.96; Karten Radius 12 px; Badges/Chips gesättigt; keine 3D-Charts
- **Icons/Illustration:** isometrisch/2.5D, weicher Schatten (y 6–10, blur 12–18), Licht von rechts oben
- **Motion:** LeanTween easeOutBack (0.38–0.48 s); Achievement-Toast 250 ms → 1.5 s → 200 ms; Confetti 25–35 Partikel
- **Audio:** sanfte UI-Foleys; Münz-SFX bei Umsatz-Milestones; Pitch-Varianz ±5 %
- **A11y:** Farbblind-Check (Deuter/Protan), Fokus-Outline 2 px, Toggle „reduzierte Animationen“
- **Asset-Pfad:** Vektor-SVG → SDF in Unity; CC0-Packs oder Eigenproduktion (Inkscape/Krita)

---

## 5) Implementation (Schritte)

### 5.1 Projektaufsetzung (Tag 0–1)

- Unity 6 LTS via Hub, neues 2D-Core-Projekt `ai-dev-tycoon`
- Pakete: TextMeshPro, Input System, Localization, Addressables (lokal)
- Ordnerstruktur gemäß Abschnitt 4.5, Namespaces `Core.Sim`, `Game.App`, `Game.UI`, `Platform.Steam`
- Steamworks.NET via UPM-Git; `steam_appid.txt` im Projektroot; SteamManager in Bootstrap-Scene
- Build-Settings: StandaloneWindows64, IL2CPP (Release), DebugSymbols aus, Stripping Low

### 5.2 Kern-Code-Skeleton (Tag 1–5)

**Zeit & RNG**

```csharp
public interface ITimeProvider { double UtcNow(); }

public sealed class SystemTimeProvider : ITimeProvider
{
    public double UtcNow() => DateTimeOffset.UtcNow.ToUnixTimeSeconds();
}

public interface IRng
{
    uint NextUInt();
    float Next01();
}

public sealed class Pcg32 : IRng
{
    private ulong _state, _inc;

    public Pcg32(ulong seed, ulong seq)
    {
        _state = 0;
        _inc = (seq << 1) | 1;
        NextUInt();
        _state += seed;
        NextUInt();
    }

    public uint NextUInt()
    {
        ulong old = _state;
        _state = old * 6364136223846793005UL + _inc;
        uint xorshift = (uint)(((old >> 18) ^ old) >> 27);
        int rot = (int)(old >> 59);
        return (xorshift >> rot) | (xorshift << ((-rot) & 31));
    }

    public float Next01() => (NextUInt() >> 8) * (1.0f / 16777216f);
}
```

**Tick-Loop**

```csharp
public sealed class GameLoop : MonoBehaviour
{
    public float tickSeconds = 0.5f;
    private float _acc;
    private Sim _sim;
    private ITimeProvider _time;

    void Awake()
    {
        _time = new SystemTimeProvider();
        _sim = new Sim(/* deps */);
    }

    void Update()
    {
        _acc += Time.deltaTime;
        while (_acc >= tickSeconds)
        {
            _sim.Tick();
            _acc -= tickSeconds;
        }
    }
}
```

**Save/Load (JSON + GZip)**

```csharp
public static class SaveIO
{
    private static string PathFor(string slot)
        => Path.Combine(Application.persistentDataPath, $"save_{slot}.json.gz");

    public static void Write<T>(string slot, T obj)
    {
        var json = JsonSerializer.Serialize(obj);
        using var fs = File.Create(PathFor(slot));
        using var gz = new GZipStream(fs, CompressionLevel.SmallestSize);
        using var sw = new StreamWriter(gz);
        sw.Write(json);
    }

    public static T Read<T>(string slot)
    {
        using var fs = File.OpenRead(PathFor(slot));
        using var gz = new GZipStream(fs, CompressionMode.Decompress);
        using var sr = new StreamReader(gz);
        var json = sr.ReadToEnd();
        return JsonSerializer.Deserialize<T>(json)!;
    }
}
```

**Achievements (Steam)**

```csharp
public static class Ach
{
    public static void Unlock(string apiName)
    {
        if (!SteamManager.Initialized)
        {
            return;
        }

        SteamUserStats.SetAchievement(apiName);
        SteamUserStats.StoreStats();
    }
}
```

### 5.3 Daten & Balancing (Tag 3–10)

- ScriptableObjects: 5 Rollen, 12–18 Research-Nodes (Tier 1–3), 3 Produkt-Segmente
- Start-Ökonomie: Startcash €20k, einfache Mieten/Gehälter, 1 Produkt-Blueprint
- Events: 6–8 Einsteiger-Events (positiv/negativ) mit Multiplikatoren

### 5.4 UI/UX (Tag 6–14)

- Hauptscreens: HQ-Dashboard (Cash, Burn, Reputation), Team, Forschung, Produkt(e), Markt, Events/Log
- Navigation: Bottom-Bar (5 Tabs), kontextsensitive Panels, Tooltips
- Accessibility: Schriftgrößen 90–120 %, farbenblind-freundliche Darstellung

### 5.5 Steam-Setup & Builds (Tag 8–16)

- Steamworks-Partner-Backend: App anlegen, Achievements definieren (8–12)
- Depot-Struktur: 1× Windows x64 Depot
- ContentBuilder: `app_build_<appid>.vdf`; Batch für Headless-Build & Upload
- Store-Seite: Beschreibung (DE/EN), 6 Screenshots, Header Capsule, Preis €5.99, optional „Early Access“

### 5.6 QA & Tests (ab Tag 10, laufend)

- Unit-/Property-Tests für Kernel (Determinismus, Invarianten)
- Headless-Runner für 30 Ingame-Tage; KPI-Export (CSV) lokal
- Manuelle QA: Save-Rotation, Achievement-Trigger, Offline-Cap, Performance (FrameTime ≤ 16 ms)

### 5.7 Lokalisierung (Tag 12–15)

- EN zuerst, danach DE; Umschalter im Settings-Menü; Unity Localization Package Keys

### 5.8 Release-Checkliste (Tag 15–18)

- Version `v0.1.0` taggen, Build hochladen, Achievements testen, Pricing/Tax, Altersfreigaben, QA-Pass, Presskit-Readme

### 5.9 Budget (≤ €500; Ziel ≤ €200)

- Fix: Steam Direct Fee ≈ $100 (~€95)
- Tools: Unity Personal, GIMP/Krita, Inkscape, Audacity (0 €)
- Assets: bevorzugt freie/CC0-Packs (UI-Icons/SFX/Musik); optional €50–€100 für 1–2 Packs
- Puffer: Store-Grafiken Budget €50–€150

---

## 6) Milestones

- **W1 — Projekt & Kernel:** Unity-Projekt, Steamworks.NET integriert, Tick-Loop & RNG implementiert, ~30 Unit-Tests grün
- **W2 — Daten & Ökonomie:** ScriptableObjects, 1 Produkt, Hiring/Forschung/Training, Offline-Cap
- **W3 — UI-First-Pass:** Greybox aller Screens, Navigation & Tooltips, Save/Load-Rotation
- **W4 — Steam & Content:** 8–12 Achievements, 6 Screenshots, Capsule-Art V1, Store-Page im Review
- **W5 — Polish & Beta:** Balancing-Pass, Profiling, DE-Lokalisierung, Bugfix-Sprint
- **W6 — Release:** v0.1.0 live (AT/global), Preis €5.99, Kommunikations-Post, Hotfix-Plan

---

## 7) Gathering Results (Messung ohne Cloud)

**Launch + 2 Wochen Ziele.** Wishlist→Sale Conversion ≥ 10 %, Refund ≤ 8 %, ≥ 75 % positive Reviews (n≥20), Crash ≤ 0,3 %.

**Messung.** Steam Backoffice (Sales/Refunds/Wishlists/Reviews); optional lokaler CSV-Export im Dev-Modus.

**Gates.**

- Gate A: Umsatz ≥ €1.000 → Steam-Fee kompensiert; Roadmap für Early Access planen
- Gate B: CR < 5 % oder Reviews < 80 % → Balancing/UX-Pass vor Feature-Erweiterung

---

## 8) Anhang

### 8.1 Achievement-Startliste (Beispiele)

- **First Launch:** Erstes Produkt veröffentlicht
- **First 1k:** 1.000 Nutzer:innen
- **First 10k:** 10.000 Nutzer:innen
- **Tier-2 Unlocked:** Erste Forschung Tier 2 abgeschlossen
- **Profitable Month:** 30 Tage mit positivem Cashflow
- **Stable Release:** 7 Tage ohne Crash

### 8.2 Test-Invarianten (Property-Tests)

- Adoption ≤ TAM (pro Segment)
- Cash wird ohne Kreditsystem nicht negativ
- Produkt-Qualität ∈ [0, 1]
- RNG-Streams deterministisch pro Seed/StreamKey

### 8.3 UI-Screens (Wireframe-Plan)

- HQ-Dashboard: Cash, Burn, Reputation, laufende Projekte, Events-Ticker
- Team: Rollenliste, Bewerbungen (Tagesbatch), Hiring-Dialog
- Forschung: Tech-Tree (Tier 1–3), Queue, Fortschrittsbalken
- Produkt: Blueprint → Launch → KPIs (Users/Churn/Revenue)
- Markt: Segmente, TAM, Preis-/Qualitäts-Fit, Wettbewerbs-Noise (einfach)
- Events/Log: Zeitlich sortiert, Tooltip-Effekte, Dauer

---

> **Hinweis:** Für Architekturberatung bitte sammuti.com kontaktieren.

