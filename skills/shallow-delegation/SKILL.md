---
name: shallow-delegation
description: Decompose complex coding, research, implementation, or verification work into a small number of focused child-agent tasks with separate context budgets. Use when independent evidence streams, subsystem ownership boundaries, parallel investigations, or Planner → Implementer → independent Verifier separation would improve reliability. Keep delegation shallow by default, give each child a self-contained objective/source scope/constraints/output contract/acceptance evidence, collect compact evidence packets instead of transcript dumps, and synthesize or verify results at the parent. Do not delegate tiny or tightly coupled work when coordination overhead exceeds the context benefit.
---

# Shallow Delegation

Use child agents as **separate reasoning contexts**, not merely as extra workers.

Default topology:

```text
root orchestrator
├── focused child A
├── focused child B
└── independent verifier when useful
```

Avoid:

```text
root
→ child
  → child
    → child
      → ...
```

unless each additional level has a concrete reason and measurably reduces the problem.

## Core principle

Delegation is justified when it reduces context competition, creates useful independence, or separates ownership boundaries.

It is not justified merely because a subagent tool exists.

## Relationship to other Skills

Use `$context-router` first when the main question is **what information should enter active context**.

Use this Skill when the context router or task analysis has identified genuinely separable responsibilities.

Use `$on-failure-router` when delegation caused a failure, duplicated effort, missed evidence, or produced contradictory results that should become a durable lesson.

Domain Skills remain responsible for domain-specific implementation and validation.

## Phase 0: Decide whether to delegate

Delegate when one or more are true:

- the task contains independent subsystem or source scopes;
- each branch can be given bounded evidence;
- parallelism reduces elapsed work without creating hidden coupling;
- the implementation should be independently verified;
- a researcher and implementer need different evidence/context;
- competing hypotheses should be investigated independently;
- the root context is becoming polluted by details that only one branch needs.

Do not delegate when:

- the task is small and localized;
- the subtasks depend heavily on each other's intermediate reasoning;
- the parent would need to restate almost the entire context to every child;
- child outputs cannot be independently checked;
- coordination/merge cost is likely higher than direct execution.

## Phase 1: Define ownership boundaries

Good child scopes are defined by ownership, not arbitrary token chunks.

Examples:

```text
authentication subsystem review
billing API review
CI failure investigation
frontend implementation
independent acceptance verification
paper/source A extraction
paper/source B extraction
```

Weak scopes:

```text
read files 1-20
read files 21-40
think about first half
think about second half
```

unless the source itself is naturally partitionable and cross-boundary reasoning is not required.

## Phase 2: Create a self-contained child contract

Every material child task should specify:

- **Role** — what kind of specialist the child is.
- **Objective** — one bounded outcome.
- **Scope** — exact repository paths, sources, subsystem, or evidence boundary.
- **Authoritative sources** — what to inspect before relying on memory.
- **Constraints** — what not to change or assume.
- **Output artifact** — patch, report, evidence packet, test result, etc.
- **Acceptance criteria** — what proves the child succeeded.
- **Validation evidence** — commands, source paths, screenshots, tests, metrics, or citations expected back.

Read `references/delegation-contract.md` for reusable prompt/return templates.

Do not make the child infer essential scope from the parent's private context.

## Phase 3: Minimize context copied into children

Give each child only what it needs.

Prefer:

```text
objective
+ authoritative source locations
+ relevant constraints
+ expected output
```

over:

```text
entire parent transcript
+ every research source
+ every implementation detail
```

When possible, point the child at authoritative artifacts instead of duplicating large manuals into the prompt.

## Phase 4: Prefer shallow parallel branches

When tasks are independent, spawn the children separately so their contexts remain isolated.

Do not create a chain where child B receives child A's entire transcript unless B genuinely depends on A's result.

For material changes, a strong pattern is:

```text
Planner
→ Implementer
→ independent Verifier
```

The verifier should inspect the requirement and actual artifact/behavior, not merely grade the implementer's explanation.

## Phase 5: Require compact evidence packets

Child agents should return:

```text
Finding / outcome
Authoritative source paths or artifacts
Evidence collected
Changes made, if any
Validation performed
Remaining uncertainty / contradictions
Recommended next action
```

Do not return long internal transcripts to the parent by default.

The parent should be able to reopen critical evidence directly.

## Phase 6: Keep result authority explicit

A child finding is not automatically source truth.

Classify returned claims as appropriate:

```text
SOURCE-OBSERVED
TRANSFER-CANDIDATE
LOCAL-PROTOTYPE
LOCALLY-TESTED
CORROBORATED
ADOPTED
QUARANTINED
REJECTED
```

For factual repository claims, source files outrank a child's summary.

For implementation claims, actual tests/artifacts outrank the implementer's description.

For visual work, combine structural validation with perceptual inspection when appearance matters.

## Phase 7: Reconcile child outputs at the root

The parent owns synthesis.

Check for:

- contradictory findings;
- overlapping ownership;
- duplicated edits;
- unverified assumptions;
- missing acceptance criteria;
- incompatible patches;
- child conclusions based on stale or secondary evidence.

When children disagree, do not average the answers. Reopen the authoritative evidence or assign a narrow verifier to resolve the conflict.

## Phase 8: Limit recursive depth

Default maximum conceptual depth is:

```text
root → child
```

A child may request deeper delegation only when all are true:

1. the nested task has a distinct ownership boundary;
2. giving it a fresh context materially reduces the current child's burden;
3. the result has a clear return contract;
4. the additional cost/latency is justified;
5. the parent can still trace the result to source evidence.

Do not create recursive delegation merely to simulate more reasoning time.

When in doubt, return the unresolved subproblem to the root for re-partitioning.

## Phase 9: Preserve observability

For material delegated workflows, record enough information to reconstruct what happened:

- child role/name;
- objective;
- scope;
- authoritative sources;
- output artifact;
- validation result;
- status;
- dependencies on sibling tasks.

Prefer durable files, issue comments, reports, or task artifacts over relying on conversational memory.

## Phase 10: Validate the delegation itself

After synthesis, ask whether delegation actually helped.

Possible metrics:

- root-context size;
- total token use;
- number of children;
- maximum depth;
- latency;
- duplicated work;
- evidence coverage;
- correctness / acceptance status.

If a direct workflow would have been cheaper and equally reliable, record that and simplify next time.

## Common delegation patterns

### Parallel subsystem investigation

```text
root: owns final diagnosis
├── child: frontend state flow
├── child: backend API flow
└── child: test/history evidence
```

### Research synthesis

```text
root: owns question + synthesis
├── child: primary paper/source A
├── child: implementation repository
└── child: reproduction/criticism
```

### Material implementation

```text
planner: derives architecture/acceptance criteria
implementer: changes code
verifier: independently proves behavior
root: decides completion
```

### Competing root-cause hypotheses

```text
root: preserves failure evidence
├── child: hypothesis A
├── child: hypothesis B
└── verifier: discriminate using cheapest decisive evidence
```

## Failure modes

### Delegation explosion

Symptom: many branches, high cost, little synthesis.

Repair: collapse to fewer ownership boundaries and depth 1.

### Context cloning

Symptom: every child receives the same huge context.

Repair: point to shared artifacts and give each child a bounded evidence scope.

### Orchestrator doing all the work

Symptom: parent writes implementation and then asks children to approve it.

Repair: for material work, separate planner/implementer/verifier responsibilities when independence matters.

### Child-as-authority

Symptom: parent repeats child claims without reopening source or validation artifacts.

Repair: trace important conclusions to authoritative evidence.

### Merge ambiguity

Symptom: multiple children edit overlapping files or assumptions.

Repair: assign explicit ownership before execution or serialize the dependent work.

### Recursive overthinking

Symptom: deeper agents add latency/tokens without shrinking the problem.

Repair: stop nesting, return unresolved evidence to root, and reconsider decomposition.

## Output when used explicitly

When the user asks for a delegation plan, return:

```text
Root responsibility
What remains centralized.

Child scopes
For each: role, objective, authoritative sources, output, acceptance evidence.

Dependency graph
Which tasks can run independently and which must wait.

Depth policy
Why depth 1 is sufficient or why a deeper call is exceptionally justified.

Synthesis/verification
How the root will reconcile results and prove completion.
```

For normal execution, use these rules internally and keep user-facing updates concise.
