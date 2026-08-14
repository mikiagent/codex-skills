# NJ MMO Browser-MMO Patterns for Three.js

Research source: `tech-leads-club/nj-mmo`, inspected 2026-08-14.

Purpose: capture reusable architectural lessons for browser-based shared-world games, especially a future low-poly Destiny-like Three.js project.

## Status legend

- **OBSERVED** — present in NJ MMO source/docs/specs.
- **INFERRED** — our transfer conclusion.
- **UNTESTED HERE** — not yet reproduced by us.
- **NOT PROVEN** — NJ MMO does not establish this capability.

---

# 1. What NJ MMO actually demonstrates

### OBSERVED

NJ MMO's current documented stack is:

```text
Three.js client
        ↓ intent / state sync
Colyseus authoritative server
        ↓
shared TypeScript game-core
        ↓
SQLite + Drizzle persistence
```

It is organized as an Nx monorepo with client, server, and shared rules. The project documentation says the browser client renders and sends intent while the server owns gameplay outcomes such as movement, damage, XP, drops, trading, and skills.

The source also contains persistent characters, combat, NPCs, quests, items/economy, party/social systems, monsters, world/pathfinding, GLTF animation, VFX, maps/UI, and automated room-integration tests.

### UNTESTED HERE

We have inspected source and project documentation but have **not yet cloned, installed, run, load-tested, or independently playtested NJ MMO**.

Claims in its README such as “all phases complete,” exact playable feature counts, and end-to-end stability should therefore be treated as **repository claims until reproduced locally**.

---

# 2. What NJ MMO does NOT prove for a Destiny-like FPS

### NOT PROVEN

NJ MMO is an MMORPG-style implementation whose documented basic interaction model is click-to-move, target selection, and server-resolved combat. That is not the same latency profile as a responsive first-person shooter.

NJ MMO does **not by itself prove** that the same networking layer already provides:

- FPS client-side movement prediction;
- server reconciliation of predicted motion;
- high-frequency snapshot interpolation;
- rewind / lag compensation for hitscan;
- authoritative projectile simulation appropriate for fast weapons;
- competitive anti-cheat robustness;
- Destiny-like movement feel under 50–150 ms latency;
- large simultaneous player counts per combat instance;
- production horizontal server scaling.

These need separate prototypes and benchmarks.

### INFERRED

NJ MMO is best viewed as evidence for the **persistent shared-world/backend architecture**, not as a ready-made Destiny FPS engine.

For a Destiny-like project, likely reuse/adaptation split:

```text
LIKELY REUSABLE IDEAS
accounts / persistence
server authority
Colyseus room structure
shared game-core
inventory / items / progression patterns
AI / encounter state organization
spec + testing workflow
asset + visual validation pipeline

NEEDS FPS-SPECIFIC WORK
first-person controller
camera
weapon feel
prediction
reconciliation
snapshot interpolation
lag compensation
hit registration
projectile policy
high-rate network tuning
FPS animation / viewmodels
```

---

# 3. Server authority as the invariant

### OBSERVED

NJ MMO records server authority as architecture decision AD-001. Positions, HP/MP, combat, XP, drops, and other game outcomes are server-owned. The client sends intent and renders replicated state.

Its testing contract uses server authority as the test boundary.

### INFERRED

For a looter shooter this is the correct default ownership model too:

```text
CLIENT MAY PREDICT / PRESENT
camera
input responsiveness
viewmodel animation
particles
shell casings
screen shake
provisional local movement

SERVER MUST OWN OUTCOMES
legal position
health/shields
ammo truth
cooldowns
ability resolution
damage
kills
loot
mission objectives
inventory changes
currency
```

The hard FPS problem is not whether the server is authoritative; it is how to hide the round-trip latency without allowing the prediction layer to become truth.

### UNTESTED HERE

The exact Colyseus schemas, tick rates, message rates, and reconciliation design for a shooter still need benchmarking.

---

# 4. Shared pure game-core is a major reusable pattern

### OBSERVED

NJ MMO keeps reusable game rules in `libs/game-core`, separate from Three.js rendering and Colyseus room wiring. Architecture decisions repeatedly prefer pure functions for movement, animation-state selection, terrain/walkability, formulas, and other rules so they can be unit-tested cheaply.

### INFERRED

A Destiny-like project should preserve this split:

```text
packages/game-core/
  weapons/
  damage/
  abilities/
  stats/
  loot/
  movement-rules/
  encounter-rules/
  progression/

server/
  authority
  rooms / instances
  persistence
  anti-cheat validation

client/
  Three.js rendering
  controls
  prediction
  audio / VFX
  UI
```

Do not bury weapon formulas, loot rules, cooldown logic, or encounter rules inside Three.js scene objects.

This makes Codex-generated features much easier to test and migrate.

---

# 5. Design temporary systems around the future migration boundary

### OBSERVED

NJ MMO's AD-008 is a useful migration pattern. Early movement was temporarily client-local, but implemented as a pure movement step consuming intent with an explicit boundary so the same logic could later move to the authoritative room rather than be rewritten.

### INFERRED

For an ambitious prototype, temporary shortcuts are acceptable if their eventual ownership boundary is explicit.

Example:

```text
Phase 1 local FPS prototype
input → pure movement simulation → renderer

Phase 2 multiplayer
input → predicted local simulation
     → command to server
server → same authoritative movement rules
       → state/snapshot
client → reconcile prediction
```

The mistake is not prototyping locally. The mistake is coupling prototype logic so tightly to rendering that networking requires a rewrite.

---

# 6. Semantic contracts survive implementation changes

### OBSERVED

NJ MMO first used procedural segmented character rigs, then superseded them with rigged GLTF/GLB skeletal animation. The generic animation-state vocabulary and authoritative action signal remained intact while the visual backend changed.

Current semantic vocabulary is approximately:

```text
idle
move
attack
cast
die
```

Each asset maps its actual clip names onto that generic contract.

### INFERRED

For our future game, define gameplay-facing semantic contracts independent of asset vendors and animation libraries.

For example:

```text
locomotion.idle
locomotion.walk
locomotion.run
locomotion.sprint
locomotion.airborne
weapon.fire
weapon.reload
weapon.melee
ability.cast
state.stagger
state.die
```

Then use asset-specific adapters/clip maps.

This lets us replace generated assets, Mixamo rigs, purchased packs, or animation systems without rewriting combat state.

---

# 7. Brain → authoritative signal → body

### OBSERVED

NJ MMO's game-designer Skill explicitly teaches a three-layer model for animated entities:

```text
Brain
pure semantic animation decision
        ↓
Signal
authoritative replicated event/state
        ↓
Body
GLB + AnimationMixer + clip mapping
```

The server sends render-only action/actionSeq signals for events that cannot reliably be inferred from position alone. Those fields are cosmetic mirrors and are not allowed to feed gameplay outcomes back into the server.

### INFERRED

This is especially useful for multiplayer shooter third-person representations.

For example:

```text
server says:
weaponFireSeq += 1
abilityAction = GRENADE
movementState = ...

remote client:
reads signal
→ selects animation / VFX
→ never invents whether the shot actually happened
```

Local first-person viewmodel animation can be predicted for responsiveness, while authoritative third-person/world outcomes remain server-derived.

---

# 8. Cosmetic authoritative signals can be separate from gameplay state

### OBSERVED

AD-015 distinguishes render-only replicated action signals from persistent/gameplay state. They are authoritative enough to represent what happened, but gameplay logic is forbidden from reading them as causal inputs.

### INFERRED

This distinction is useful for networked VFX and animation events:

```text
server outcome
→ lightweight event sequence
→ clients render effect
```

Potential shooter signals:

- weapon fired;
- reload committed;
- shield break;
- ability cast;
- melee resolved;
- death;
- boss phase transition.

Sequence counters are useful when identical consecutive actions need to trigger more than once.

---

# 9. Colyseus room-integration tests are a useful authority test boundary

### OBSERVED

NJ MMO uses `@colyseus/testing` to test join/leave, messages, validation, persistence/reconnect, transactions, proximity checks, combat, and replicated state without relying on a browser for every multiplayer rule.

### INFERRED

For a Destiny-like architecture, separate tests into:

```text
PURE UNIT
weapon formulas
loot rolls
cooldowns
movement constraints
ability rules

ROOM / INSTANCE INTEGRATION
join instance
send movement/fire intent
server validates
state broadcasts
damage ownership
loot ownership
reconnect
party state

CLIENT UNIT
snapshot mapping
HUD state
animation-event mapping
prediction math

BROWSER / PLAYTEST
input feel
camera
visual correctness
real WebGL/WebGPU integration
latency experience
```

Do not require a full browser session merely to prove that a client cannot award itself loot.

---

# 10. Deterministic simulation is especially important for network games

### OBSERVED

NJ MMO's test harness disables automatic simulation during room tests and advances simulation explicitly. Tests await actual message delivery rather than sleeping through fixed tick intervals. Random outcomes use injected seeded RNG.

One recorded decision reports substantial test-runtime improvement after eliminating repeated wall-clock tick waits.

### INFERRED

A future FPS simulation should expose deterministic stepping from the start:

```text
simulate(dt)
applyCommand(command)
produceSnapshot()
```

Tests can then express:

```text
send input
advance N ticks
inspect authoritative state
```

instead of `sleep(500)` and hope networking/timers have settled.

This will matter enormously once Codex is running repeated regression loops.

---

# 11. Fast tests are an architecture feature for agentic development

### OBSERVED

NJ MMO treats slow test files as defects and uses Nx affected/caching to avoid rerunning unrelated work. Its docs explicitly connect test latency to agent iteration cost.

### INFERRED

As the game grows, the optimal architecture is not merely “testable.” It is **cheaply testable at the layer where the rule lives**.

This favors:

- pure game-core modules;
- dependency injection for RNG/time;
- deterministic simulation stepping;
- isolated DB fixtures;
- server tests without WebGL;
- selective visual gates only for visual behavior.

---

# 12. Database/data imports need independent tests

### OBSERVED

NJ MMO imports source game data into its own SQLite schema and uses seed/data tests against isolated databases/fixtures. External reference data is not required at runtime.

### INFERRED

For our game, large content catalogs should become our own normalized game data rather than ad hoc constants scattered through code.

Potential data-driven catalogs:

```text
weapons
weapon archetypes
perks
enemies
encounters
loot tables
quests
vendors
zones
abilities
```

Generated content should be validated before it becomes live game data.

This is also a good interface for AI-assisted content generation: agents generate structured candidate data, deterministic validators enforce schema/ranges/invariants, and only validated data enters runtime.

---

# 13. Local coordinate space is safer for browser worlds

### OBSERVED

NJ MMO records a near-origin metric coordinate system where roughly 1 unit ≈ 1 meter, avoiding use of huge raw external world coordinates due to Three.js float precision / z-fighting concerns.

### INFERRED

For larger Destiny-like worlds, use zone-local coordinates and instance/world transforms rather than enormous coordinates across an imaginary seamless universe.

This naturally fits instancing:

```text
account universe
  ↓
planet / destination
  ↓
zone instance
  ↓
local coordinate space
```

This is another argument for a shared-world game composed of instances rather than one gigantic authoritative simulation.

---

# 14. Semantic walkability before heavyweight nav technology

### OBSERVED

NJ MMO uses terrain sampling, slope/step constraints, blockers, and grid A* instead of adopting heavyweight source-game geodata immediately.

### INFERRED

A low-poly shooter prototype should first implement the minimum navigation representation required by its actual enemies and spaces.

Potential staged progression:

```text
simple navmesh / grid
→ encounter-authored links / jumps
→ dynamic blockers
→ specialized flying AI
→ only then more complex navigation if justified
```

Do not adopt a large world/pathfinding stack merely because a full MMO might eventually need one.

---

# 15. Visual quality requires a separate gate

### OBSERVED

NJ MMO explicitly learned that logic correctness does not prove visual fidelity. Its asset workflow combines deterministic structural checks with rendered perceptual inspection.

It also separates asset fidelity from asset licensing.

### INFERRED

For our low-poly game, every imported/generated 3D asset pipeline should check independent axes:

```text
STRUCTURE
file loads
mesh exists
expected skeleton/animations
no duplicate accidental asset
reasonable scale/bounds

PERFORMANCE
poly budget
texture dimensions
material count
animation count
payload size

FIDELITY
looks like requested entity
readable silhouette
correct category
style consistency

LICENSE / PROVENANCE
source recorded
allowed usage
replace-before-launch flags
```

A model being valid GLB is not proof it belongs in the game.

---

# 16. Asset-specific knowledge belongs in manifests/adapters

### OBSERVED

NJ MMO inspects actual GLB track names and bone names rather than assuming all rigs match. Asset-specific clip maps and attachment metadata localize those differences.

### INFERRED

A future asset manifest might include:

```json
{
  "id": "enemy_raider_01",
  "model": "/models/enemies/raider01.glb",
  "scale": 1.15,
  "forwardAxis": "-Z",
  "clips": {
    "idle": "Idle_A",
    "run": "Run_Fwd",
    "attack": "Rifle_Fire",
    "die": "Death_02"
  },
  "sockets": {
    "rightHand": "mixamorigRightHand",
    "weaponMuzzle": "Muzzle"
  }
}
```

Never invent track/bone names because another model happened to use them.

---

# 17. Specs can be executable project memory

### OBSERVED

NJ MMO stores each roadmap phase under a durable directory containing:

```text
spec.md
design.md
tasks.md
validation.md
```

Validation points back to acceptance criteria and concrete proof. `.specs/STATE.md` stores numbered architecture decisions and current handoff.

### INFERRED

For an ambitious Codex-built game, this is much safer than relying on chat context.

Recommended future project structure:

```text
.specs/
├── ROADMAP.md
├── STATE.md
├── LESSONS.md
└── features/
    └── <feature>/
        ├── spec.md
        ├── design.md
        ├── tasks.md
        └── validation.md
```

This can coexist with Codex Skills. Skills encode reusable methods; specs encode this game's current intent.

---

# 18. Architecture decisions should include trade-offs and supersession

### OBSERVED

NJ MMO's `STATE.md` records decisions with reason, trade-off, scope, date, status, and explicit supersession/amendment. For example, an early “procedural primitives only” art decision was later superseded by GLTF skeletal assets without pretending the original choice never existed.

### INFERRED

This is valuable for agentic development because later Codex sessions can distinguish:

```text
current rule
historical rule
why it changed
what still survives from the old design
```

That reduces the risk of an agent resurrecting an obsolete architecture from old docs.

---

# 19. Reference implementations should be translated, not coupled, when appropriate

### OBSERVED

NJ MMO uses L2J Classic as reference data/rules but deliberately avoids runtime dependency or original protocol/client assets. It parses data into its own schema and translates rules into TypeScript.

### INFERRED

For our Destiny-inspired project, we should similarly learn from open-source games and networking repos without letting the project become a fragile collage of incompatible engines.

Use references to extract:

- formulas;
- state machines;
- networking patterns;
- test strategies;
- content schemas;
- architecture ideas.

Then normalize them behind our own contracts.

Always respect source licenses.

---

# 20. A proposed Destiny-like architecture informed by NJ MMO

This is an **inference, not an NJ MMO implementation**:

```text
                         ACCOUNT / PERSISTENCE
                   characters • inventory • quests
                                │
                                ▼
                        MATCHMAKING / ROUTING
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
           HUB ROOM         PATROL ROOM         STRIKE ROOM
          10–30 users       ~8–16 users          3 users
              │                 │                  │
              └────────── authoritative servers ───┘
                                │
                    shared pure GAME CORE
                 weapons • damage • loot • AI
                                │
                                ▼
                         THREE.JS CLIENT
             prediction • interpolation • rendering
                      audio • VFX • UI
```

The MMO feeling comes from persistent identity, shared progression, matchmaking, social spaces, and multiple synchronized instances rather than from putting thousands of players into one simulation.

### UNTESTED HERE

The player-count ranges above are design targets, not NJ MMO benchmark results.

---

# 21. FPS-specific prototype gates before committing to the stack

Before declaring Colyseus + Three.js sufficient for the Destiny-like project, build a network combat slice that proves:

1. two remote players can move smoothly under simulated latency/jitter;
2. local movement prediction feels responsive;
3. server corrections do not produce unacceptable snapping;
4. remote interpolation looks smooth;
5. hitscan hit registration has an explicit latency policy;
6. projectile weapons remain authoritative and visually coherent;
7. weapon fire/reload/ability events do not duplicate or disappear;
8. enemy combat scales to the intended encounter density;
9. bandwidth per client remains within a defined budget;
10. browser CPU/GPU/frame time remains acceptable with target player/enemy counts.

Recommended test conditions should include multiple artificial latency/jitter/loss profiles, not merely localhost.

---

# 22. Candidate Skills suggested by this research

These are ideas, **not yet built or validated**:

```text
threejs-authoritative-multiplayer
threejs-fps-controller
fps-network-prediction
fps-lag-compensation
colyseus-instance-server
game-core-rules
shared-world-instance-router
threejs-character-manifest
threejs-visual-gate
gltf-game-asset-validator
encounter-authoring
loot-system
game-spec-driven-execution
```

Avoid creating all of these prematurely. A Skill should emerge when there is a stable reusable ownership boundary and enough tested knowledge to encode.

---

# 23. Research status and next tests

## High-confidence source observations

- authoritative Colyseus + Three.js split exists;
- server/client/shared-core monorepo exists;
- persistent SQLite/Drizzle layer exists;
- spec/design/tasks/validation lifecycle exists;
- deterministic unit + room integration + data tests exist;
- explicit architecture decision log exists;
- GLTF skeletal asset pipeline and visual gate are documented;
- lesson-management script exists.

## Important unverified claims

- full game quality / fun;
- README feature completeness in actual play;
- real-world concurrency/scaling;
- production security;
- WAN behavior;
- FPS suitability;
- mobile-browser performance;
- long-session memory stability;
- deployment economics.

## Next practical research step

Clone NJ MMO in an isolated test workspace and run:

```text
install
build shared core
seed DB
unit tests
server tests
client tests
full gate
launch server/client
2-client multiplayer smoke test
browser performance profile
network-throttled playtest
```

Only after that should source observations be promoted to “tested by us.”
