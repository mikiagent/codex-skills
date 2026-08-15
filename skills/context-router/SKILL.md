---
name: context-router
description: Manage large or noisy working context for repository research, long documents, logs, datasets, multi-file investigations, and long-running coding tasks. Use when the task risks context overload, requires evidence from many locations, or would benefit from probing/searching/filtering external sources before reading them deeply. Build a bounded working set by probing structure, narrowing candidates, admitting only relevant evidence, delegating separable scopes when useful, synthesizing results, and validating evidence coverage. Prefer simple direct reads for small localized tasks and do not add recursive scaffolding unless it earns its complexity.
---

# Context Router

Treat context as a **working set**, not as the database.

The core loop is:

```text
PROBE
→ NARROW
→ ADMIT
→ DELEGATE when justified
→ SYNTHESIZE
→ VALIDATE
```

The goal is not to maximize how much source material reaches the model. The goal is to preserve authoritative source material outside the active context and admit the smallest evidence set that supports the next reasoning step.

## Why this Skill exists

Large context windows are storage capacity, not a guarantee that every included token will be used reliably. Repository-scale and corpus-scale tasks often fail because unrelated evidence competes inside one context.

Use this Skill to choose among:

- direct reading;
- deterministic search/filtering;
- structural probing;
- targeted retrieval;
- compaction;
- externalized context in files/data structures;
- focused child-agent delegation.

Do not turn any one mechanism into a universal rule.

## Relationship to other Skills

Use `$shallow-delegation` when independent subproblems deserve separate context budgets.

Use `$on-failure-router` when a context-management decision caused a bad result and the system should learn from the failure.

Use domain Skills for the actual implementation, testing, asset generation, research, or platform-specific work. This Skill owns **context admission and evidence routing**, not domain logic.

## Phase 0: Decide whether context routing is needed

Stay simple when:

- the task is localized to one or a few known files;
- the user supplied a short source that can be read directly;
- an exact symbol/path/error already identifies the owning area;
- the additional routing machinery would cost more than simply reading the source.

Use context routing when one or more are true:

- the repository/corpus is unfamiliar and large;
- relevant evidence is distributed across many files or sources;
- the task requires aggregation rather than one-line lookup;
- prior context is already noisy or long;
- multiple independent investigations can be separated cleanly;
- exact source evidence must be preserved while only summaries enter the root context.

Do not use a fixed token threshold as a universal rule. Complexity, ambiguity, evidence distribution, and task coupling matter more than raw size alone.

## Phase 1: Establish the authority and objective

Before reading broadly, identify:

- the exact user objective;
- the authoritative repository/source set;
- the expected output artifact or decision;
- the evidence needed to prove completion;
- known constraints, paths, versions, branches, or time ranges.

When the task is repository-specific, inspect current source files before relying on prior chat summaries.

## Phase 2: Probe before reading deeply

Learn the shape of the source without loading its contents wholesale.

For repositories, prefer structural operations such as:

- list top-level directories;
- inspect file paths and sizes;
- inspect extension/language distribution;
- locate manifests, entrypoints, tests, docs, schemas, configs, and ownership boundaries;
- search exact symbols, errors, feature names, and likely concepts;
- inspect recent diffs/commits when the question is change-related.

When local filesystem access is available, `scripts/context_inventory.py` can create a deterministic repository inventory without reading file bodies.

Example:

```bash
python skills/context-router/scripts/context_inventory.py . --json
```

The output is orientation evidence, not an answer.

## Phase 3: Build an evidence map

Convert the task into evidence questions.

Example:

```text
Question: Why does authentication refresh fail after resume?

Evidence map:
- session persistence owner
- refresh token owner
- resume lifecycle owner
- related tests
- recent changes touching those paths
```

For each evidence question, record:

```text
Evidence needed
Likely source/path
Cheap probe
Deep-read condition
Status: unknown | candidate | confirmed | contradicted
```

This prevents broad reading from becoming aimless accumulation.

## Phase 4: Narrow deterministically first

Prefer cheap exact operations before semantic reasoning when they can reduce the search space.

Useful operations include:

- filename/path filtering;
- symbol search;
- grep/search queries;
- structured metadata inspection;
- JSON/CSV/database filtering;
- sorting by size/date/type;
- parsing manifests or indexes;
- extracting only matching log windows;
- comparing changed files.

General principle:

> Use deterministic operations to decide what deserves expensive semantic attention.

Do not summarize or embed an entire source merely because tooling makes it possible.

## Phase 5: Admit a bounded working set

Read the smallest source regions that can answer the current evidence questions.

Prefer:

```text
exact source excerpt / file region
+ path or source identity
+ why it matters
```

over:

```text
large unstructured paste
```

Keep authoritative source material in its original artifact. Summaries are indexes and working notes, not replacements for source truth.

If a summary becomes decision-critical, reopen the underlying source before finalizing the claim.

## Phase 6: Choose the right context mechanism

### Direct read

Use when the source is small, localized, and tightly relevant.

### Deterministic search/retrieval

Use when likely relevance can be identified cheaply before deeper reasoning.

### Compaction

Use when old interaction history is no longer needed verbatim and can safely become a lossy summary.

Never use compaction to discard exact evidence that is still needed for validation.

### Externalized context

Keep large sources in files, repositories, databases, variables, notebooks, or other inspectable artifacts and query them programmatically.

Use when the task requires adaptive search, aggregation, repeated passes, or sources too large/noisy to admit directly.

### Separate child context

Use `$shallow-delegation` when a subproblem can be given a narrow objective and source scope with limited coupling to sibling work.

## Phase 7: Delegate only when it reduces context competition

Good delegation boundaries include:

- independent subsystem reviews;
- separate research sources;
- implementation versus verification;
- distinct benchmark/evidence streams;
- parallel file ownership areas.

Bad delegation boundaries include:

- arbitrary chunks with heavy cross-dependencies;
- subtasks whose outputs cannot be independently validated;
- tiny tasks where coordination costs dominate;
- deep recursive trees created only because recursion is available.

Default to **shallow delegation**. A root agent with focused children is preferred over an unbounded tree unless deeper recursion has an explicit, measurable justification.

## Phase 8: Require evidence packets, not transcript dumps

When work returns from a child agent or auxiliary process, synthesize a bounded packet:

```text
Finding
Source paths / artifacts
Evidence
Confidence / uncertainty
Contradictions
Recommended next action
```

Do not pull entire child transcripts into the root context unless debugging the child itself.

Critical claims should be traceable back to authoritative source artifacts.

## Phase 9: Synthesize from the evidence map

Before producing the answer or patch, revisit the evidence questions.

Mark each as:

```text
CONFIRMED
CONTRADICTED
UNRESOLVED
NOT NEEDED
```

Do not let a polished synthesis hide missing evidence.

When sources disagree, preserve the disagreement and identify which source is authoritative for the requested decision.

## Phase 10: Validate context coverage

A context strategy is successful only if it supports the requested outcome.

Check:

- Did every material conclusion have source evidence?
- Were critical source files reopened rather than trusted through stale summaries?
- Did narrowing accidentally exclude an owning layer?
- Did delegation create contradictions or duplicated work?
- Did the final validation inspect the actual requested artifact/behavior?

For material work, prefer Planner → Implementer → independent Verifier when that independence improves reliability.

## Metrics for experiments

When comparing context strategies, measure where practical:

- root-context tokens;
- total tokens;
- number of source files/chunks admitted;
- child-agent count;
- maximum delegation depth;
- latency;
- cost;
- evidence coverage;
- correctness / acceptance status.

Do not declare a sophisticated context workflow better merely because it feels more agentic. The cheapest workflow that reliably proves the requirement should win.

## Failure modes

### Context dumping

```text
read everything
→ huge prompt
→ hope attention finds the important parts
```

Repair: return to PROBE → NARROW → ADMIT.

### Premature summarization

A lossy summary replaces source evidence too early.

Repair: preserve source identity and reopen exact evidence for decision-critical claims.

### Search tunnel vision

An initial keyword search becomes the only evidence path.

Repair: inspect ownership boundaries, neighboring files, tests, and alternative hypotheses.

### Delegation explosion

Children spawn children without shrinking the problem.

Repair: collapse back to the root, reduce depth, and require a concrete reason for every additional context.

### Context duplication

The same large source is independently loaded into multiple agents without need.

Repair: partition by evidence responsibility or share durable artifacts while keeping reasoning contexts narrow.

### Validation starvation

All context budget is spent researching/implementing and none remains for verification.

Repair: reserve a final independent evidence pass.

## Output when used explicitly

When the user asks for a context plan, return a compact structure:

```text
Objective
What must be proven.

Probe
Cheap structural observations to collect first.

Evidence map
Questions and likely source owners.

Admission plan
What enters the root context and why.

Delegation
Focused child scopes, if any.

Validation
How evidence coverage and the final outcome will be checked.
```

For normal tasks, use this process internally and keep the user-facing answer focused on the requested result.
