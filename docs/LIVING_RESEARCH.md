# Living Research Ledger

This is the durable intake layer for external patterns that may improve the Codex Skills repository.

The purpose of this file is to prevent a dangerous collapse between:

```text
we found an interesting pattern
```

and:

```text
we tested it and should enforce it globally
```

Research should move through evidence states before becoming mandatory Skill behavior.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `SOURCE-OBSERVED` | Directly observed in source code/docs of the researched project. |
| `TRANSFER-CANDIDATE` | We have a reasoned hypothesis that the pattern could improve our system. |
| `LOCAL-PROTOTYPE` | Implemented experimentally in our repo/workspace but not sufficiently validated. |
| `LOCALLY-TESTED` | Reproduced successfully against defined tests/scenarios in our environment. |
| `CORROBORATED` | Succeeded across independent scenarios/features and is a strong candidate for durable guidance. |
| `ADOPTED` | Intentionally encoded into production Skill behavior. |
| `QUARANTINED` | Previously useful/credible guidance that later produced harmful results or became stale. |
| `REJECTED` | Tested or reviewed and intentionally not adopted. |

A source can be excellent and still remain `SOURCE-OBSERVED` for our purposes until we run it or test the transferred behavior ourselves.

---

# 2026-08-14 — NJ MMO deep research

Source repository: `tech-leads-club/nj-mmo`

Primary research documents added to this repository:

- `skills/on-failure-router/references/nj-mmo-self-improvement-patterns.md`
- `skills/threejs-builder/references/nj-mmo-browser-mmo-patterns.md`

## Research status

**Overall status: `SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`.**

We inspected repository source, architecture decisions, agent Skills, validation artifacts, tests/documentation structure, lesson-management code, package configuration, and game/asset workflow documentation.

We have **not yet cloned and run NJ MMO locally**, so repository claims about complete playability, performance, feature completeness, WAN behavior, concurrency, and stability are not promoted to `LOCALLY-TESTED`.

---

## High-value source observations

### Agentic development system

NJ MMO uses a durable spec-driven development model built around:

```text
ROADMAP
→ Planner
→ spec/design/tasks artifacts
→ Implementer
→ independent Verifier
→ validation evidence
→ bounded fixes/re-verification
→ roadmap/state update
```

The orchestrator is intentionally a driver rather than the agent that also plans, codes, and judges the result.

**Status:** `SOURCE-OBSERVED`

### Independent verification

Validation records explicitly use an independent verifier (`author ≠ verifier`) and map acceptance criteria to concrete evidence.

**Status:** `SOURCE-OBSERVED`

### Tests as a trust boundary

The project states that tests derive from acceptance criteria and the test runner decides “done.” Tests are split by cheapest valid proof layer: pure unit, multiplayer room integration, and seed/data.

**Status:** `SOURCE-OBSERVED`

### Discrimination / fault-injection sensor

Verification intentionally introduces small behavior-level defects and checks that tests actually fail, preventing superficially relevant but non-discriminating tests from being accepted.

**Status:** `SOURCE-OBSERVED`

### Candidate → confirmed → quarantined lesson memory

NJ MMO stores machine-managed lessons separately from raw feature failures. New lessons remain candidates until they recur across independent features; stale uncorroborated candidates can be pruned; confirmed lessons can be penalized and quarantined when harmful.

**Status:** `SOURCE-OBSERVED`

### Deterministic lesson bookkeeping

The model supplies semantic judgment, while a deterministic script owns IDs, recurrence, promotion, pruning, quarantine counters, and rendered documentation.

**Status:** `SOURCE-OBSERVED`

### Deterministic simulation + no wall-clock sleeps

Room tests disable background simulation and explicitly step the world, while waiting for actual message delivery rather than sleeping for guessed durations. The project records meaningful test-runtime improvement from this change.

**Status:** `SOURCE-OBSERVED`

### Persistent architecture decisions

`.specs/STATE.md` stores numbered architecture decisions with reason, trade-off, scope, date, status, and explicit supersession/amendment. This distinguishes current rules from historical choices rather than deleting architectural history.

**Status:** `SOURCE-OBSERVED`

### Two-layer visual quality gate

The asset workflow separates deterministic structural validation from perceptual fidelity inspection. Capturing a screenshot is explicitly not equivalent to looking at it and judging whether it is actually the requested asset.

**Status:** `SOURCE-OBSERVED`

### Fidelity and licensing are orthogonal

A legally clean asset can still be the wrong asset. NJ MMO documents prior failures where a source-pack asset passed superficial checks despite representing the wrong thing.

**Status:** `SOURCE-OBSERVED`

### Brain → signal → body animation architecture

Generic semantic animation logic is separated from authoritative replicated event/state and from asset-specific GLTF/AnimationMixer playback. This allowed an asset/rendering architecture change without discarding the semantic state machine.

**Status:** `SOURCE-OBSERVED`

### Authoritative browser MMO foundation

The project uses Three.js client + Colyseus server + shared TypeScript game-core + SQLite/Drizzle persistence, with the server owning gameplay outcomes.

**Status:** `SOURCE-OBSERVED`

---

## Transfer candidates for this Skill repository

These are **not yet mandatory rules**.

### C-001 — Separate failure incidents from trusted lessons

Proposed evolution:

```text
failure log
        ↓
candidate lesson
        ↓ independent recurrence
confirmed lesson
        ↓ harmful recurrence
quarantine
```

Reason: prevents a single dramatic failure from rewriting global Skill behavior.

**Status:** `TRANSFER-CANDIDATE`

### C-002 — Deterministic lesson registry

Add a script-backed lesson store adjacent to `.codex-skill-feedback/failures.jsonl` so promotion/pruning/quarantine mechanics are not delegated to prompt memory.

**Status:** `TRANSFER-CANDIDATE`

### C-003 — Independent verifier for material Skill changes

Test a fresh verifier for broad workflow/router/script changes instead of relying entirely on the authoring agent's self-review.

**Status:** `TRANSFER-CANDIDATE`

### C-004 — Acceptance criterion → evidence map

For significant failure repairs, record exactly which observable outcome proves each repaired requirement and where the evidence comes from.

**Status:** `TRANSFER-CANDIDATE`

### C-005 — Targeted fault injection for validators/tests

Intentionally corrupt a behavior and verify the test/validator rejects it, particularly for deterministic asset tools and routing rules.

**Status:** `TRANSFER-CANDIDATE`

### C-006 — Expiring uncorroborated lessons

Avoid indefinite prompt growth from one-off observations. Test time-based vs usage-based expiry before choosing a policy.

**Status:** `TRANSFER-CANDIDATE`

### C-007 — Quarantine harmful guidance instead of deleting history

Retain evidence explaining why a once-trusted lesson became unsafe/stale.

**Status:** `TRANSFER-CANDIDATE`

### C-008 — Two-layer gates for visual Skills

Combine deterministic structural QA with actual perceptual inspection for sprites, 3D assets, game UI, and video.

**Status:** `TRANSFER-CANDIDATE`

### C-009 — Separate project decisions, lessons, failures, and handoff state

Do not collapse all durable context into one generic memory document.

**Status:** `TRANSFER-CANDIDATE`

### C-010 — Spec-driven feature artifacts for ambitious autonomous projects

For larger game/application builds, use durable per-feature `spec.md`, `design.md`, `tasks.md`, and `validation.md`, while keeping reusable methodology in Skills.

**Status:** `TRANSFER-CANDIDATE`

---

## Three.js / Destiny-like transfer candidates

### G-001 — Use NJ MMO as shared-world architecture evidence, not FPS-netcode proof

NJ MMO gives us a strong reference for server authority, persistence, shared rules, rooms, game data, tests, assets, and agent workflow.

It does **not** establish that Destiny-like movement/shooting will feel good under network latency.

**Status:** `TRANSFER-CANDIDATE`

### G-002 — Prototype FPS prediction/reconciliation separately

Before committing to the multiplayer stack, test:

- local prediction;
- server reconciliation;
- remote interpolation;
- snapshot/update rates;
- simulated latency/jitter/loss;
- hitscan lag policy;
- projectile authority;
- bandwidth;
- encounter CPU/GPU cost.

**Status:** `TRANSFER-CANDIDATE`

### G-003 — Keep pure game rules outside Three.js scene objects

Weapons, damage, abilities, loot, stats, encounters, and progression should live in testable shared modules.

**Status:** `TRANSFER-CANDIDATE`

### G-004 — Build explicit migration boundaries during local prototypes

Temporary local-only behavior should already consume/produce the same semantic state that an authoritative server can later own.

**Status:** `TRANSFER-CANDIDATE`

### G-005 — Use semantic animation contracts plus per-asset manifests

Do not make game logic depend on arbitrary GLB animation/bone names.

**Status:** `TRANSFER-CANDIDATE`

### G-006 — Treat the MMO as persistent services + bounded instances

A Destiny-like experience can get its shared-world feel from accounts, progression, hubs, patrol instances, matchmaking, strikes, and parties without one enormous synchronized simulation.

**Status:** `TRANSFER-CANDIDATE`

---

# Next validation queue

These are the highest-value experiments before promoting NJ-derived patterns.

1. **NJ MMO local reproduction**
   - clone into an isolated workspace;
   - install dependencies;
   - build shared core;
   - seed DB;
   - run unit/server/client/full gates;
   - launch two clients;
   - test basic multiplayer interactions.

2. **Lesson-registry prototype**
   - implement candidate/confirmed/quarantined state mechanically;
   - test recurrence across distinct scenarios;
   - test stale-candidate pruning;
   - test quarantine without deleting evidence.

3. **Independent-verifier experiment**
   - choose one material Skill repair;
   - compare self-review vs fresh verifier;
   - measure whether the fresh verifier finds meaningful additional gaps.

4. **Fault-injection experiment**
   - choose an existing deterministic validator;
   - deliberately create a defect;
   - verify the test actually catches it.

5. **Visual-gate experiment**
   - run deterministic structural QA;
   - render output;
   - perform semantic/fidelity review;
   - compare failures caught by each layer.

6. **FPS multiplayer vertical slice**
   - 2 players;
   - one small arena;
   - one hitscan weapon;
   - one projectile weapon;
   - server authority;
   - prediction/reconciliation/interpolation;
   - artificial latency/jitter/loss;
   - instrumentation for bandwidth and correction error.

Only successful experiments should move their corresponding candidate toward `LOCALLY-TESTED`, `CORROBORATED`, and eventually `ADOPTED`.

---

# Research discipline

When adding future sources, preserve this rule:

```text
source authority tells us how seriously to investigate a pattern;
our own validation tells us whether to enforce it in our system.
```

Do not promote a pattern merely because the source project is impressive. Do not discard a useful pattern merely because its exact implementation differs from ours. Record the evidence, identify the transferable invariant, test it, then promote or reject it deliberately.
