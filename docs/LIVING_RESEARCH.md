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

Primary research documents:

- `skills/on-failure-router/references/nj-mmo-self-improvement-patterns.md`
- `skills/threejs-builder/references/nj-mmo-browser-mmo-patterns.md`

## Overall status

`SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`

We inspected repository source, architecture decisions, agent Skills, validation artifacts, lesson-management code, testing structure, game architecture, asset workflow, and project documentation.

We have not yet cloned/run/load-tested NJ MMO locally. Playability, performance, WAN behavior, concurrency, and numeric lesson thresholds remain source claims/choices rather than local proof.

## High-value observations

### Spec-driven Planner → Implementer → independent Verifier

The orchestrator acts primarily as a driver. Feature intent is preserved in durable spec/design/tasks/validation artifacts, and the verifier is independent from the author for material work.

**Status:** `SOURCE-OBSERVED`

### Tests as trust boundary + fault injection

Acceptance criteria map to concrete evidence, with multiple proof layers. Verification can deliberately mutate behavior to ensure tests discriminate good from bad behavior.

**Status:** `SOURCE-OBSERVED`

### Candidate → confirmed → quarantined lesson memory

New lessons remain candidates until independent recurrence. Stale candidates can be removed; harmful confirmed guidance can be quarantined without erasing history.

**Status:** `SOURCE-OBSERVED`

### Deterministic lesson bookkeeping

LLMs supply semantic judgment while code owns IDs, recurrence counts, state transitions, pruning, quarantine counters, and rendered docs.

**Status:** `SOURCE-OBSERVED`

### Deterministic simulation tests

Server/room tests can disable background simulation, advance the world explicitly, await real message delivery, and inject deterministic RNG rather than using wall-clock sleeps.

**Status:** `SOURCE-OBSERVED`

### Architecture decisions preserve history

Decisions include rationale, trade-offs, scope, date/status, and explicit supersession/amendment.

**Status:** `SOURCE-OBSERVED`

### Structural + perceptual visual gate

A valid artifact or captured screenshot is not equivalent to a correct-looking result. Fidelity and licensing are separate axes.

**Status:** `SOURCE-OBSERVED`

### Brain → signal → body animation architecture

Semantic animation decisions, authoritative replicated signals, and GLTF/AnimationMixer implementation are distinct layers.

**Status:** `SOURCE-OBSERVED`

---

## Existing self-improvement transfer candidates

### C-001 — Separate failure incidents from trusted lessons

```text
failure incident
→ candidate lesson
→ independent corroboration
→ confirmed
→ quarantine if harmful
```

**Status:** `TRANSFER-CANDIDATE`

### C-002 — Deterministic lesson registry

Add script-backed lesson-state mechanics adjacent to raw failure memory.

**Status:** `TRANSFER-CANDIDATE`

### C-003 — Independent verifier for material Skill changes

Compare fresh verification against author self-review before making this mandatory.

**Status:** `TRANSFER-CANDIDATE`

### C-004 — Acceptance criterion → evidence map

Material repairs should say exactly what observation proves each repaired requirement.

**Status:** `TRANSFER-CANDIDATE`

### C-005 — Targeted fault injection

Intentionally corrupt behaviors to verify validators/tests fail for the right reason.

**Status:** `TRANSFER-CANDIDATE`

### C-006 — Expire uncorroborated lessons

Test time-based versus usage/scenario-based staleness before choosing policy.

**Status:** `TRANSFER-CANDIDATE`

### C-007 — Quarantine harmful guidance without deleting history

Preserve why a once-trusted rule became stale/harmful.

**Status:** `TRANSFER-CANDIDATE`

### C-008 — Multi-layer visual gates

At minimum combine deterministic structural QA with perceptual inspection. Advanced mechanisms may also need temporal/parameter/performance validation.

**Status:** `TRANSFER-CANDIDATE`

### C-009 — Separate decisions, research, experiments, failures, lessons, and handoff

Do not use one generic memory file for incompatible knowledge types.

**Status:** `TRANSFER-CANDIDATE`

### C-010 — Spec-driven feature artifacts for ambitious autonomous projects

Use durable per-feature spec/design/tasks/validation artifacts while Skills retain reusable methodology.

**Status:** `TRANSFER-CANDIDATE`

---

# 2026-08-14 — Comparative browser-game architecture study

Sources inspected:

- `mshumer/Claude-of-Duty`
- `ill-inc/biomes-game`
- `MavonEngine/Core`
- `iErcann/NotBlox`
- `swift502/Sketchbook`
- `mohsenheydari/three-fps`
- `majidmanzarpour/threejs-game-skills`
- `CloudAI-X/threejs-skills`
- `scottstts/Threejs-Awesome-Graphics-Agent-Skills`

New Skill research references:

- `skills/threejs-builder/references/browser-game-architecture-research.md`
- `skills/on-failure-router/references/claude-of-duty-agent-production-patterns.md`

Project-level detailed synthesis lives in `mikiagent/vibe-coding` rather than being duplicated into this Skill repo.

## Overall status

`SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`

The repositories were inspected at code level. They have not been cloned, benchmarked, WAN-tested, or validated against our Skills yet. These findings are intake, not automatic production rules.

---

## New game/runtime candidates

### G-001 — Shared-world architecture evidence is not FPS-netcode proof

NJ MMO/Biomes provide authority, persistence, world, and scale references. Twitch prediction/reconciliation/hit-registration needs its own experiments.

**Status:** `TRANSFER-CANDIDATE`

### G-002 — Prototype FPS prediction/reconciliation separately

Required lab should include client prediction, command sequences, server acknowledgements, replay reconciliation, remote snapshot interpolation, latency/jitter/loss, hitscan/projectile policy, and instrumentation.

**Status:** `TRANSFER-CANDIDATE`

### G-003 — Keep pure game rules outside Three.js scene objects

Weapons, damage, abilities, loot, stats, encounters, and progression should remain headless/testable where possible.

**Status:** `TRANSFER-CANDIDATE`

### G-004 — Build explicit migration boundaries in prototypes

Temporary local behavior should consume/produce semantic state compatible with eventual authority migration.

**Status:** `TRANSFER-CANDIDATE`

### G-005 — Semantic animation contracts + per-asset manifests

Game logic should not depend directly on arbitrary GLB clip/bone names.

**Status:** `TRANSFER-CANDIDATE`

### G-006 — Persistent services + bounded instances first

A shared-world game can use accounts/progression/routing plus bounded hub/patrol/mission instances without one global combat simulation.

**Status:** `TRANSFER-CANDIDATE`

### G-007 — Distinguish networking layers explicitly

```text
latest-state smoothing
≠ snapshot interpolation
≠ client prediction
≠ reconciliation
≠ hitscan lag compensation
```

NotBlox is a readable example of server authority/ECS replication and simple visual smoothing, not prediction. MavonEngine provides sequence/acknowledgement/shared-simulation scaffolding, but the inspected multiplayer template did not establish a complete replay of remaining unacknowledged inputs after correction.

**Status:** `TRANSFER-CANDIDATE`

### G-008 — Interest management is a first-class system

Start with per-instance/per-player relevance filtering. Only move to a dedicated sync tier when scale requires it.

**Status:** `TRANSFER-CANDIDATE`

### G-009 — Biomes-style transactional world/replica architecture is a scale migration target

Potential later decomposition:

```text
transactional world authority
→ change stream
→ replicas
→ logic / AI / environment workers
→ sync tier
```

Do not adopt this service topology for an MVP without measured need.

**Status:** `TRANSFER-CANDIDATE`

### G-010 — Procedural content should use semantic grammars

Claude-of-Duty suggests constrained meaningful module/state variation is more useful than unconstrained random noise.

**Status:** `TRANSFER-CANDIDATE`

### G-011 — Separate gameplay recoil from presentation kick

FPS feel should distinguish learnable aim/camera behavior from viewmodel motion, trauma, FX, and audio.

**Status:** `TRANSFER-CANDIDATE`

### G-012 — Performance contracts need frame-time tails

For real-time game claims, include p50/p95/p99/worst-frame or equivalent hitch evidence. Average FPS alone can hide severe first-use/compilation stalls.

**Status:** `TRANSFER-CANDIDATE`

---

## New agent/self-improvement candidates

### A-001 — Parallelism should follow coupling boundaries

Claude-of-Duty reports that parallel ownership was counterproductive for tightly coupled visual systems, while sequential ownership of the coupled concern worked better.

Candidate invariant:

```text
independent domains → parallelize
coupled concern → serialize / one owner
material output → independent verifier
```

**Status:** `TRANSFER-CANDIDATE`

### A-002 — Treat causal user/critic explanations as hypotheses

A complaint can accurately identify an observable defect while incorrectly naming the mechanism. Record the symptom, generate competing causes, and discriminate with evidence.

**Status:** `TRANSFER-CANDIDATE`

### A-003 — Evidence fixtures have owners and failure modes too

Visual regressions can come from stale page state, timing drift, nondeterministic seeds, or readiness races. Before patching product code, consider whether the evidence/capture layer is invalid.

**Status:** `TRANSFER-CANDIDATE`

### A-004 — Deterministic visual fixtures should isolate relevant state

Candidate fixture contract:

```text
fixed seed
fixed engine time/frame budget
fixed viewport/DPR/camera/state
fresh page/process where leakage is possible
explicit asset-ready boundary
```

**Status:** `TRANSFER-CANDIDATE`

### A-005 — Performance failure diagnosis should inspect distributions

When median/average looks fine but users report stutter, request timeline/tail evidence rather than assuming the complaint is incorrect.

**Status:** `TRANSFER-CANDIDATE`

### A-006 — Broad Skills may benefit from evidence ledgers

`threejs-game-skills` tracks phase/reference/asset/evidence state. Test a lightweight version before deciding whether the overhead is justified for Vibe Coding.

**Status:** `TRANSFER-CANDIDATE`

### A-007 — Skill systems should separate knowledge, workflow, implementation vocabulary, and deterministic tooling

External Skill packs specialize differently:

```text
domain/API references
workflow/orchestration
detailed implementation examples
deterministic tooling/QA
```

Hypothesis: preserving these layers is better than building one giant Three.js Skill.

**Status:** `TRANSFER-CANDIDATE`

### A-008 — Advanced visual validation should test mechanism robustness

Beyond structural + perceptual inspection, sophisticated visual systems may need no-post baselines, diagnostic passes, seed/parameter sweeps, distance envelope tests, temporal stability, and GPU evidence.

**Status:** `TRANSFER-CANDIDATE`

---

# Current validation queue

Highest-value experiments before promotion:

1. **Two-player FPS networking lab**
   - shared movement simulation;
   - client prediction;
   - per-player sequence IDs;
   - authoritative acknowledgement;
   - replay unacknowledged inputs;
   - remote snapshot buffer interpolation;
   - artificial latency/jitter/loss;
   - correction/bandwidth/tick instrumentation.

2. **Hitscan/projectile authority lab**
   - one hitscan weapon;
   - one projectile;
   - server-owned outcomes;
   - timestamp/lag policy;
   - hit feedback vs authoritative confirmation.

3. **Visual fixture determinism experiment**
   - compare shared-page vs isolated-page captures;
   - fixed seed/time/camera/DPR;
   - verify stable diffs.

4. **Frame-time tail profiler**
   - report p50/p95/p99/worst;
   - inject a first-use shader/material hitch;
   - prove the instrumentation finds it.

5. **Parallel vs sequential ownership experiment**
   - use one deliberately coupled visual concern;
   - compare defects, correction count, final evidence, and coordination cost.

6. **Independent verifier experiment**
   - one material Skill or game feature change;
   - compare author self-review against fresh verification.

7. **Fault-injection experiment**
   - deliberately corrupt one validator-owned behavior;
   - confirm correct failure.

8. **Mechanism-level visual validation experiment**
   - structural checks;
   - final/no-post captures;
   - diagnostics;
   - seed/parameter/distance/time checks;
   - performance evidence.

9. **Lesson-registry prototype**
   - candidate/confirmed/quarantined mechanics;
   - independent recurrence;
   - stale pruning;
   - quarantine without deleting evidence.

10. **Evidence-ledger usability experiment**
    - trial a lightweight ledger on one broad game-build task;
    - evaluate whether it materially improves verification/handoff enough to justify context and bookkeeping cost.

11. **NJ MMO local reproduction**
    - clone isolated;
    - install/build/seed/test;
    - launch two clients;
    - reproduce documented behavior.

12. **Only after measured scale pressure**
    - prototype transactional world API;
    - world replicas/change stream;
    - dedicated sync tier;
    - sharded AI.

Only successful experiments should move corresponding candidates toward `LOCALLY-TESTED`, `CORROBORATED`, and eventually `ADOPTED`.

---

# Research discipline

Preserve this rule:

```text
source authority tells us how seriously to investigate a pattern;
our own validation tells us whether to enforce it in our system.
```

Do not promote a pattern merely because the source project is impressive. Do not discard a useful invariant merely because the source stack differs from ours. Record evidence, identify the transferable hypothesis, test it, then promote, quarantine, or reject deliberately.