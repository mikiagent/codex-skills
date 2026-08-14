# NJ MMO Self-Improvement Patterns

Research source: `tech-leads-club/nj-mmo`, inspected 2026-08-14.

This document captures patterns observed in NJ MMO that may improve the Codex Skills self-improvement system. It intentionally separates **source observation** from **our inference** and **our validation status**.

## Status legend

- **OBSERVED** — directly present in NJ MMO source, specs, scripts, or project documentation.
- **INFERRED** — a transferable design conclusion we are drawing from the observed implementation.
- **UNTESTED HERE** — we have not yet reproduced the behavior in `mikiagent/codex-skills` or validated that the same parameters are appropriate for our workflows.
- **CANDIDATE** — worth prototyping, but must not silently become a global Skill rule until tested.

## Executive finding

NJ MMO does not treat self-improvement as unrestricted agent reflection. It externalizes the important state into inspectable artifacts:

```text
ROADMAP
  ↓
feature spec
  ↓
design
  ↓
tasks
  ↓
implementation
  ↓
independent validation
  ↓
validation signals
  ↓
candidate lessons
  ↓
recurrence / corroboration
  ↓
confirmed guidance
```

The most important transfer for our `on-failure-router` is the distinction between:

```text
failure incident ≠ trusted lesson
```

A failure can be logged immediately, while the rule inferred from that failure remains a **candidate** until corroborated.

---

## 1. Driver-only orchestration

### OBSERVED

NJ MMO's `spec-driven-execution` Skill describes itself as a **driver only**. The orchestrator does not plan, implement, or verify. It sequences fresh Planner → Implementer → Verifier agents, handles PASS/FAIL, and advances the roadmap only after verification.

The flow is approximately:

```text
Orchestrator
  ↓
Planner
  ↓
artifacts exist?
  ↓
Implementer
  ↓
Verifier (fresh agent)
  ↓
PASS? ── no → targeted fix → reverify, bounded
  │
 yes
  ↓
advance roadmap + update state
```

### INFERRED

This reduces role contamination. A coordinator that also authors the solution has an incentive and context bias toward accepting its own work.

For our system, this suggests keeping `on-failure-router` focused on:

- evidence preservation;
- root-cause attribution;
- ownership routing;
- correction-budget control;
- deciding what gets promoted into durable memory.

Domain Skills should continue owning domain-specific repairs.

### CANDIDATE / UNTESTED HERE

Prototype an optional independent verifier role for material Skill changes. Do not require an expensive second agent for every tiny edit until the cost/benefit is measured.

---

## 2. Author and verifier should be independent for material changes

### OBSERVED

NJ MMO explicitly records that the Verifier is independent from the Implementer (`author ≠ verifier`). Validation documents identify the diff range, acceptance criteria, evidence, prior gaps, and independent re-verification.

### INFERRED

For self-modifying Skill systems, independent verification is more important than additional free-form reflection by the same agent.

A strong repair loop is:

```text
Agent A changes behavior
        ↓
Agent B checks the declared contract
        ↓
objective tests / artifacts / screenshots
        ↓
PASS or specific gaps
```

### CANDIDATE / UNTESTED HERE

For broad changes to `SKILL.md`, routing rules, deterministic scripts, or validators, test a fresh-verifier path that receives:

- original failure;
- expected behavior;
- changed files / diff;
- acceptance criteria;
- relevant evidence;
- no hidden implementation rationale beyond what is needed to test the contract.

---

## 3. Tests are the trust boundary, not the agent's confidence

### OBSERVED

NJ MMO's `AGENTS.md` states that the test runner decides when work is done. Tests derive from spec acceptance criteria and must not be weakened or skipped merely to produce a pass.

The project uses three layers:

1. unit tests for formulas, rules, curves, and wiring;
2. Colyseus room-integration tests for complete multiplayer message paths;
3. seed/data tests for imported game data.

### INFERRED

Our self-improvement system should prefer the cheapest test layer that proves the behavior, but it should not substitute a cheaper test when the contract explicitly requires an integration boundary.

This is stronger than “add a regression test.” It means the failure record should know **which boundary actually proves the behavior**.

### CANDIDATE / UNTESTED HERE

Add a future `validation_layer` field to structured failure/lesson records, for example:

```json
{
  "validation_layer": "unit | integration | visual | e2e | artifact | manual"
}
```

Do not make this mandatory until the existing failure logger and workflows are migrated safely.

---

## 4. Evidence-or-zero acceptance criteria

### OBSERVED

NJ MMO validation files map acceptance criteria to concrete `file:line` evidence and assertions. When an acceptance criterion lacks the declared test layer, the verifier records it as a gap instead of inferring that nearby tests are “probably enough.”

The Phase 6 validation file, for example, enumerates spec-defined outcomes, the exact assertions that prove them, and gaps that survived earlier verification.

### INFERRED

This can make our failure router substantially less impressionistic.

A material repair should be able to answer:

```text
Which requirement failed?
What observable outcome proves the fix?
Where is that proof?
What adjacent behavior proves we did not overfit?
```

### CANDIDATE / UNTESTED HERE

For substantial repairs, generate a small acceptance-evidence table in the failure record rather than only a prose summary.

---

## 5. Fault injection tests test the tests

### OBSERVED

NJ MMO's verifier performs behavior-level scratch mutations, such as deliberately removing a guard or changing a seeded value, then verifies that the relevant tests fail. Its validation reports call this a discrimination sensor.

Example pattern:

```text
correct implementation + green tests
        ↓
introduce deliberate behavioral fault
        ↓
expected test must fail
        ↓
revert fault
        ↓
green again
```

### INFERRED

This addresses a major weakness in autonomous coding: an agent can write a test that looks relevant yet does not discriminate correct from incorrect behavior.

For our Skills, mutation-style verification is especially attractive for deterministic validators and repair scripts.

### CANDIDATE / UNTESTED HERE

Use targeted fault injection selectively for high-value rules, such as:

- asset validator should reject a deliberately malformed artifact;
- sprite-sheet validator should fail after corrupting one dimension;
- router regression should fail if a required stage is intentionally bypassed;
- a network authority test should fail if the client is allowed to set a server-owned result.

Do not add heavyweight generalized mutation-testing infrastructure until targeted mutations show enough value.

---

## 6. Candidate → confirmed → quarantined lesson lifecycle

### OBSERVED

NJ MMO maintains a machine-owned lesson store and renders a human/agent-readable `LESSONS.md`.

A new lesson starts as a **candidate**. Candidates are explicitly “tracked, not trusted.” A lesson is promoted to **confirmed** only after recurrence across distinct features reaches a threshold. Confirmed guidance can accumulate a harmful count and become **quarantined** if applying it recurs alongside failures.

Default values in NJ MMO at inspection time are:

```text
promotion threshold: 2 distinct features
candidate window:     45 days
quarantine threshold: 2 harmful applications
```

These numbers are implementation choices, not universal truths.

### INFERRED

This is the strongest improvement over our present failure-log model.

Our maturity ladder should become two related but separate lifecycles:

```text
INCIDENT LIFECYCLE
complaint
→ observed failure
→ reproduced failure
→ verified cause
→ repair
→ regression evidence

LESSON LIFECYCLE
candidate lesson
→ corroborated in independent case(s)
→ confirmed guidance
→ monitored when applied
→ quarantine if harmful
```

A repair can be correct after one incident without the inferred rule automatically becoming global policy.

### CANDIDATE / UNTESTED HERE

Build a deterministic lesson registry adjacent to `.codex-skill-feedback/failures.jsonl`, rather than embedding promotion logic only in prompts.

Potential state:

```text
.codex-skill-feedback/
├── failures.jsonl
├── lessons.json
└── LESSONS.md
```

Initial states:

```text
candidate
confirmed
quarantined
```

Do **not** copy NJ MMO's thresholds blindly. Test them against real Skill usage first.

---

## 7. Mechanical memory management should be code, not prose

### OBSERVED

NJ MMO's `scripts/lessons.py` says the LLM supplies judgment while the deterministic script owns:

- IDs;
- recurrence counting;
- distinct-feature tracking;
- promotion;
- pruning;
- penalties/quarantine;
- rendering the readable lesson document.

The script refuses ungrounded lesson additions: a lesson requires a known validation signal, feature identifier, source evidence, and meaningful text.

### INFERRED

This follows the same philosophy already used elsewhere in this Skill repository:

> keep semantic judgment in the model; move fragile mechanical state transitions into deterministic code.

The `on-failure-router` should not be trusted to remember whether a lesson has occurred once or twice by reading arbitrary prose logs.

### CANDIDATE / UNTESTED HERE

Add a deterministic `lessons.py`-style helper after designing a schema. The first version should be deliberately small and auditable.

---

## 8. Recurrence should mean independent corroboration

### OBSERVED

NJ MMO counts recurrence by **distinct feature**, not by how many times the same lesson is emitted during one feature's debugging session.

### INFERRED

This prevents one noisy failure from promoting its own explanation merely because an agent repeated the same diagnosis several times.

For our Skill ecosystem, possible independence keys include:

```text
project
skill
scenario / fixture
feature
provider
workflow run family
```

The right key depends on the lesson scope.

### CANDIDATE / UNTESTED HERE

Require a future lesson registry to record a `scope` plus a corroboration key. Promotion should require evidence from genuinely independent cases, not repeated retries of one failure.

---

## 9. Stale hypotheses should expire

### OBSERVED

NJ MMO auto-prunes uncorroborated candidate lessons after a configurable window.

### INFERRED

Self-improving systems otherwise accumulate “folk wisdom”: rules inferred once, never reproduced, but permanently loaded into future context.

Expiry is a useful antidote to prompt bloat and accidental overfitting.

### CANDIDATE / UNTESTED HERE

Candidates may need either:

- time-based expiry;
- usage-count-based expiry;
- explicit archival after N unrelated opportunities without recurrence.

Time alone may be a poor measure for rarely-used Skills, so test alternatives before adopting NJ MMO's 45-day window.

---

## 10. A lesson can later become harmful

### OBSERVED

NJ MMO can penalize a confirmed lesson. Repeated harmful applications move it into quarantine rather than deleting history.

### INFERRED

This is important because a once-useful heuristic can become stale, overly broad, or wrong after architecture/provider changes.

Do not overwrite history. Keep the lesson plus the evidence that caused quarantine so a maintainer can understand why guidance changed.

### CANDIDATE / UNTESTED HERE

Future lesson metadata should retain:

```text
status
positive evidence
harmful applications
last seen
scope
reason for quarantine
```

---

## 11. Determinism and speed are agent-system requirements

### OBSERVED

NJ MMO treats slow/flaky tests as defects because autonomous agents burn cycles waiting on feedback. Its room tests disable background simulation, advance time deterministically, await actual message delivery, isolate mutable state, and avoid wall-clock sleeps.

One architecture decision reports a server-test reduction from roughly 9.2 seconds to roughly 2.3 seconds after removing repeated simulation sleeps.

### INFERRED

Test performance is not merely developer convenience in an agentic coding loop. It changes how many correction cycles are practical and therefore changes reliability.

### CANDIDATE / UNTESTED HERE

Our validators and Skill regression suites should record runtime and flag tests that become unexpectedly slow or flaky. Do not weaken assertions for speed.

---

## 12. Persistent architecture decisions + handoff state

### OBSERVED

NJ MMO keeps `.specs/STATE.md` with numbered architecture decisions (`AD-NNN`) containing decision, reason, trade-off, scope, date, status, and later supersession/amendment. The same document maintains a handoff state for autonomous continuation.

### INFERRED

A self-improving agent should distinguish:

- **architecture decisions** — intentional choices and trade-offs;
- **lessons** — empirically learned guidance;
- **failure incidents** — raw evidence;
- **current handoff** — where work should resume.

Collapsing all four into “memory” makes later agents confuse an experiment with a rule.

### CANDIDATE / UNTESTED HERE

When our orchestration grows beyond isolated Skills, adopt separate durable stores for decisions, lessons, incidents, and execution state.

---

## 13. Visual outputs require structural AND perceptual gates

### OBSERVED

NJ MMO's `game-designer` Skill records a hard lesson: green logic tests can still produce visually wrong assets.

Its visual gate has two layers:

1. **structural/deterministic** checks such as duplicate GLBs, invalid skeleton/animation categories, empty stubs;
2. **perceptual/fidelity** review of an actual rendered image against the intended entity.

The Skill explicitly rejects “screenshot captured” as sufficient evidence. The image must actually be inspected for semantic fidelity.

### INFERRED

This directly generalizes to our sprite, 3D asset, UI, and video Skills:

```text
machine-valid ≠ visually correct
```

A visual workflow needs both measurable integrity checks and a semantic look-at-the-output step.

### CANDIDATE / UNTESTED HERE

Where our current quality gates are structural only, add a perceptual gate before declaring visual work complete. Preserve deterministic checks as the first layer rather than replacing them with subjective judgment.

---

## 14. Fidelity and licensing are separate axes

### OBSERVED

NJ MMO explicitly records a prior verifier mistake: accepting an asset because it came from an allowed pack even when it visually represented the wrong thing. The current Skill treats fidelity and licensing as independent checks.

### INFERRED

More generally, passing one quality dimension must never imply another:

```text
valid file format ≠ correct content
licensed asset ≠ correct asset
successful API call ≠ successful task
passing unit test ≠ complete integration
captured screenshot ≠ visually acceptable result
```

### CANDIDATE / UNTESTED HERE

Add orthogonal quality dimensions to validators where a single green score currently hides semantic failure.

---

## 15. Generic brain → authoritative signal → asset-specific body

### OBSERVED

NJ MMO separates animated entities into:

- **Brain**: generic pure logic that chooses semantic animation state (`idle/move/attack/cast/die`);
- **Signal**: authoritative replicated state/events from the server;
- **Body**: asset-specific GLB + clip-name map + `AnimationMixer` playback.

The architecture survived a rendering-backend change from procedural rigs to GLTF skeletal animation because the semantic state machine and server signal stayed stable.

### INFERRED

This is a strong example of choosing an abstraction at the semantic contract rather than at the current implementation.

The same pattern can inform reusable game Skills:

```text
game rule / intent
→ authoritative normalized state
→ engine- or asset-specific adapter
```

### CANDIDATE / UNTESTED HERE

Apply this selectively when building reusable Three.js character, weapon, VFX, and multiplayer Skills. Avoid forcing this vocabulary onto domains where it does not fit.

---

## 16. Self-contained sub-agent prompts use pointers, not duplicated manuals

### OBSERVED

NJ MMO notes that sub-agents cannot see the orchestrator chat. Prompts therefore include the needed role, feature context, output paths, autonomous-mode behavior, and pointers to project glue files. They intentionally avoid pasting entire templates and quality manuals into every prompt.

### INFERRED

A scalable Codex orchestration system should compile a compact, explicit task packet:

```text
role
objective
scope
required artifact paths
current handoff
authoritative docs to read
constraints
expected evidence
```

This avoids both missing context and context duplication.

### CANDIDATE / UNTESTED HERE

Use this pattern when we introduce Planner/Implementer/Verifier orchestration into Codex workflows.

---

# Proposed evolution of `on-failure-router`

Current conceptual loop:

```text
failure
→ evidence
→ attribution
→ repair
→ validation
→ failure memory
```

Research candidate:

```text
failure
→ preserve incident
→ attribution
→ smallest repair
→ behavioral replay
→ regression evidence
→ candidate lesson
        ↓
independent recurrence?
   no → retain / eventually expire
   yes
        ↓
confirmed lesson
        ↓
observe future applications
        ↓
harmful recurrence?
   no → keep confirmed
   yes → quarantine + maintainer review
```

This should remain a **research candidate** until implemented and exercised on real failures.

# What we should test next

1. Add a tiny deterministic lesson registry without changing router behavior.
2. Feed it historical/synthetic incidents and verify deduplication, recurrence, expiry, and quarantine mechanics.
3. Run the existing `on-failure-router` on several independent real failures and compare:
   - incident logging only;
   - immediate rule promotion;
   - candidate/confirmed promotion.
4. Measure false promotions and missed reusable lessons.
5. Test a fresh independent verifier on one material Skill repair.
6. Add one targeted fault-injection test to a deterministic Skill validator and confirm it catches the introduced defect.
7. Test a two-layer structural + perceptual gate on one visual asset workflow.
8. Only after evidence, promote successful patterns into mandatory `SKILL.md` behavior.

# Explicit non-conclusions

We have **not** established that:

- NJ MMO's numeric thresholds are optimal for our system;
- every Skill change needs a separate verifier agent;
- time-based expiry is better than usage-based expiry;
- NJ MMO's AI-authorship claims independently prove every phase was built without human intervention;
- its validation artifacts are free of blind spots;
- these patterns outperform our current router on our own workload.

Those remain testable hypotheses, not settled rules.
