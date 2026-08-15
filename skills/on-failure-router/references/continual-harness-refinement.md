# Continual Harness Refinement Patterns

## Status

`SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`

This reference distills self-improvement ideas from Prime Agent's continual-harness implementation and the Continual Harness research into rules suitable for the existing `on-failure-router`.

The patterns are useful, but source success is not local proof. Promote them through our normal failure/replay/regression/corroboration process.

## 1. Keep an immutable outer layer

A self-improving agent should not casually rewrite every instruction that governs its own behavior.

Use the conceptual split:

```text
immutable outer policy / safety / project authority
+
editable supplemental Skill instructions
+
editable references
+
editable deterministic scripts
+
editable router rules
+
project-local memory/artifacts
```

The failure router may improve the editable layer, but should preserve higher-authority system/user/project constraints.

## 2. Evidence-backed edits, not free-form reflection

Refinement should be derived from trajectory evidence:

- user complaint;
- failed artifact;
- logs;
- tests;
- diffs;
- screenshots;
- repeated correction history;
- exact source state.

The output of reflection is a **proposal**, not proof.

## 3. Small CRUD-like edits

Prefer a small explicit mutation:

```text
CREATE narrow rule/reference/test
UPDATE one owning instruction/script/router
DELETE or QUARANTINE stale harmful guidance
```

over rewriting an entire Skill from scratch.

For each edit, preserve:

- reason;
- evidence;
- expected outcome;
- validation method;
- previous state or diff so rollback is possible.

## 4. Local versus global scope

Not every learned fact belongs in a reusable Skill.

### Project/session-local

Use for:

- current task state;
- one project's conventions;
- temporary blockers;
- project-specific architecture facts;
- subjective requirements unique to the current artifact.

### Reusable Skill/global

Consider only for:

- repeated cross-task failure patterns;
- durable tool/environment facts;
- reusable procedures;
- stable routing/validation rules;
- lessons independently corroborated beyond one incident.

When uncertain, prefer the narrower scope.

## 5. Promotion ladder

Use this maturity path:

```text
failure incident
→ observable failure
→ candidate hypothesis
→ verified local cause
→ smallest local patch
→ replay failed case
→ neighbor/regression test
→ candidate reusable lesson
→ independent corroboration
→ durable Skill rule/tool
```

A single incident is evidence, not a universal rule.

## 6. Quarantine instead of erasure

If previously trusted guidance becomes harmful or stale:

- stop applying it;
- preserve the history and reason;
- mark it quarantined where the knowledge system supports that state;
- test a replacement before promoting it.

Do not silently delete evidence simply to make the system look cleaner.

## 7. Success trajectories can teach too

Continual-harness systems can refine from successful trajectories as well as failures.

For this Skill, do not automatically turn every success into a rule. Promote a successful pattern only when it is:

- clearly causal rather than coincidental;
- reusable;
- cheaper or more reliable than alternatives;
- independently observed again or deliberately tested.

## 8. Context-management failures are a distinct class

When a task failed because the agent:

- loaded too much irrelevant context;
- trusted a stale summary;
- missed an owning file during narrowing;
- delegated too deeply;
- cloned the same large context into many children;
- failed to reserve context for verification;

route the repair through `$context-router` or `$shallow-delegation` as appropriate rather than patching unrelated domain Skills.

## 9. Rollback is part of self-improvement

A Skill edit is not sacred because it was intended as an improvement.

If the patch worsens the replay or neighbor cases:

```text
preserve evidence
→ revert / quarantine the patch
→ update the root-cause hypothesis
→ test a narrower alternative
```

## 10. Measure before broad promotion

Where practical, compare before/after on:

- original failure outcome;
- neighboring cases;
- correctness;
- evidence coverage;
- retries;
- token usage;
- latency;
- cost.

Do not promote a more complicated scaffold if a simpler rule or deterministic check is equally reliable.
