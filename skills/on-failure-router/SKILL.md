---
name: on-failure-router
description: Diagnose user-reported failures such as "this failed", "this sucks", "that didn't work", "wrong result", or repeated correction requests, then ask only high-value follow-up questions, inspect the failed trajectory and relevant Skill files, generate multiple evidence-grounded root-cause hypotheses, route the verified failure to the smallest owning layer, patch the owning Skill/reference/script/router when justified, validate the revision, rerun or forward-test the failed scenario, and record the lesson for future runs. Use when a Codex task or Skill produced a bad result and the user wants the system to learn from the failure rather than merely retry the same task.
---

# On Failure Router

Turn failures into durable improvements without blindly rewriting Skills.

The user may provide very little information, for example:

```text
this failed
this sucks
that didn't work
you messed this up
it still does the same thing
wrong result
why did the skill do that?
```

Treat these as **failure signals**, not as sufficient diagnoses.

The goal is:

```text
failure signal
→ preserve evidence
→ clarify only what is missing
→ inspect trajectory + artifacts + Skills
→ generate multiple root-cause hypotheses
→ verify ownership
→ patch smallest owning layer
→ validate
→ replay / forward-test
→ record lesson
```

Do not use free-form "reflection" as the entire recovery method. Reflection without new evidence can degrade into re-generation. Prefer logs, diffs, screenshots, test failures, generated artifacts, user observations, prompts, Skill instructions, script output, and reproducible behavior.

## Core principles

1. **Failure is training data.** Preserve the failed prompt, invoked Skills, artifacts, logs, and user feedback before editing anything.
2. **User feedback is an error signal, not necessarily a root-cause diagnosis.** Respect the complaint while independently locating the owning layer.
3. **Generate competing explanations.** Do not commit to the first plausible cause.
4. **Patch the smallest owning layer.** Do not rewrite a Skill when the problem belongs to a task prompt, script, provider, environment, reference file, or router.
5. **Preserve working behavior.** A fix for one failure must not silently destroy previously useful behavior.
6. **Validate the Skill as an artifact and the behavior as a workflow.** Syntax validation alone is not enough.
7. **Record durable lessons, not every annoyance.** Promote repeated or generalizable failures into Skill knowledge.
8. **Bound self-modification.** If evidence is weak or the proposed edit changes broad behavior, stop at a proposed patch and explain the uncertainty instead of making speculative changes.

## Relationship to other Skills

Use `$prompt-enhancer` when the failure is primarily caused by an underspecified task request and the user needs clarification or a stronger execution brief.

Use `$context-router` when the failure came from context overload, premature summarization, missed source ownership during narrowing, or poor evidence admission.

Use `$shallow-delegation` when the failure came from bad decomposition, duplicated child context, excessive recursion, weak child contracts, or missing independent verification.

Use the system `$skill-creator` when a new Skill must be created or an existing Skill needs substantial structural redesign. Follow its validation and forward-testing guidance.

Use specialized validators, tests, Playwright, asset QA, build tools, or domain Skills when they can provide objective evidence.

Do not duplicate another Skill's domain logic inside this Skill. This Skill owns **failure attribution, routing, improvement, and validation of the correction loop**.

Before promoting a local fix into broad reusable harness behavior, read `references/continual-harness-refinement.md` and apply its local/global scope, rollback, and corroboration discipline.

## Phase 0: Detect failure context

Identify what just failed.

Recover as much as possible from the current session and workspace:

- the user's original request;
- the most recent assistant/Codex action;
- explicitly invoked Skills;
- implicitly relevant Skills;
- commands that were run;
- changed files;
- generated artifacts;
- test/build output;
- screenshots or visual outputs;
- provider/model/job IDs when relevant;
- previous correction attempts;
- the user's exact failure statement.

Do not ask the user to repeat information already present in the conversation, repo, logs, or artifacts.

## Phase 1: Convert vague dissatisfaction into observable failure

If the user says only "this sucks" or similar, determine whether the failure is already observable.

If not, ask the smallest set of questions needed to make the failure testable.

Prefer questions like:

```text
What specifically is wrong in the result: appearance, behavior, missing functionality, or a crash?
What did you expect to happen instead?
Does the failure happen every time or only under a particular condition?
Which part is unacceptable even if the rest is correct?
```

Ask at most 1-4 questions in one round unless the task genuinely requires more.

Avoid generic requests such as:

```text
Can you provide more details?
```

When possible, offer concrete categories inferred from the evidence.

Example:

```text
I can see three plausible failures here: the sprite changed identity, the animation timing is wrong, or the sheet metadata is wrong. Which one are you reacting to most strongly?
```

## Phase 2: Preserve the failed case

Before modifying Skill logic, preserve the evidence needed to learn from it.

Create or append a failure record using `scripts/log_failure.py` when practical.

Record:

- timestamp;
- user complaint;
- original task;
- Skills involved;
- artifacts/logs inspected;
- observed failure;
- expected behavior;
- candidate causes;
- verified cause when known;
- files changed by the repair;
- validation performed;
- final outcome.

Default log location inside a project or Skill repo:

```text
.codex-skill-feedback/failures.jsonl
```

Do not store secrets, auth tokens, private credentials, or unnecessary personal data in the log.

## Phase 3: Multi-hypothesis failure attribution

Read `references/failure-taxonomy.md`.

Generate 2-5 plausible causes when the root cause is not obvious.

Each hypothesis should include:

```text
Hypothesis
Evidence for
Evidence against / missing
Owning layer
Cheap verification
```

Example:

```text
H1: The task prompt omitted the canonical identity reference.
Evidence for: output drifted; Skill requires identity authority.
Evidence against: anchor may have been supplied indirectly.
Owner: task/context.
Verify: inspect prompt and input list.

H2: The sprite Skill description failed to trigger the identity-anchor Skill.
Evidence for: identity normalization stage is absent from logs.
Evidence against: Skill may have been invoked manually.
Owner: routing / Skill description.
Verify: inspect invoked Skill list and description.

H3: The identity-anchor workflow ran but produced a bad anchor.
Evidence for: downstream frames all share the same incorrect feature.
Owner: component Skill or source artifact.
Verify: inspect canonical anchor and QA report.
```

Do not patch until one hypothesis is strongly supported or the patch is low-risk and reversible.

## Phase 4: Route to the owning layer

Classify the verified failure into the smallest useful intervention level.

### Level 0 — Environment / installation

Examples:

- missing binary;
- broken symlink;
- wrong `CODEX_HOME`;
- unavailable model/provider;
- permissions;
- stale cache;
- incompatible dependency.

Action: fix environment or installation. Do not rewrite Skill logic merely to hide an environment failure.

### Level 1 — Task prompt / context

Examples:

- intended outcome was ambiguous;
- crucial reference was omitted;
- user preference was not captured;
- preservation constraints were missing;
- too much irrelevant source material was admitted;
- a stale summary displaced exact source evidence.

Action: improve task brief or route through `$prompt-enhancer` / `$context-router` as appropriate.

Patch a Skill only if this omission is recurrent enough that the Skill should automatically infer, inspect, or ask for it in future.

### Level 2 — Router / trigger

Examples:

- correct Skill did not trigger;
- wrong Skill triggered;
- multiple Skills overlap ambiguously;
- orchestrator skipped a required component Skill;
- delegation boundaries caused duplicated or missing ownership.

Action: revise Skill description, routing rules, orchestration order, or route through `$shallow-delegation`. Descriptions are trigger surfaces; treat them as executable routing metadata.

### Level 3 — Skill workflow / contract

Examples:

- required step missing;
- stages in wrong order;
- Skill permitted a known bad shortcut;
- acceptance criteria too weak;
- user-visible assumption should have been clarified.

Action: patch `SKILL.md` or a directly referenced contract file.

### Level 4 — Reference / domain knowledge

Examples:

- missing failure mode;
- stale API/platform note;
- absent edge case;
- incomplete prompt recipe;
- quality threshold not documented.

Action: patch the smallest relevant file under `references/`.

### Level 5 — Deterministic script / tool implementation

Examples:

- parser/cropper/packer/validator bug;
- wrong calculation;
- fragile shell command;
- incorrect API call;
- missing retry/pagination/error handling.

Action: patch the script/tool, add a regression test or fixture, and avoid compensating with prose when code should enforce correctness.

### Level 6 — Provider/model limitation

Examples:

- image/video model cannot reliably preserve a feature;
- API does not support requested mode;
- model output is stochastic beyond acceptable tolerance.

Action: change provider, conditioning strategy, deterministic post-processing, or validation. Do not lie to the Skill by pretending stronger prompting guarantees unsupported behavior.

### Level 7 — Missing capability / new Skill

Examples:

- repeated failures share a distinct ownership boundary not covered by any current Skill;
- existing Skill has become too broad;
- a deterministic tool needs its own workflow and validation contract.

Action: propose or create a new Skill using `$skill-creator`. Avoid creating a new Skill merely because one case was inconvenient.

## Phase 5: Decide whether the Skill should learn

Not every failure should modify a Skill.

### Patch the Skill when

- the failure is reproducible;
- the cause lies in Skill instructions, routing, references, or bundled scripts;
- the lesson generalizes to future tasks;
- the fix can be stated as a durable rule, test, contract, or deterministic operation;
- the change does not encode a one-off aesthetic preference as a universal rule.

### Do not patch the Skill when

- the failure was caused by a transient provider outage;
- the user simply changed their mind;
- the issue is unique to one project's business logic;
- the evidence is too weak;
- an existing project file, test, or configuration is the true owner;
- a broad Skill edit would create more ambiguity than it removes.

In those cases, fix the task/project and log the incident without promoting it to Skill knowledge.

## Phase 6: Make the smallest durable patch

Before editing, inspect the current Skill folder and relevant references/scripts.

Prefer this order of intervention:

```text
example / reference clarification
→ narrow Skill rule
→ trigger/description refinement
→ deterministic validation/test
→ script/tool patch
→ orchestrator redesign
→ new Skill
```

Use the least invasive change that prevents recurrence.

When editing a Skill:

- preserve unrelated instructions;
- keep descriptions concise but comprehensive enough to trigger correctly;
- keep high-variability decisions as instructions/heuristics;
- move fragile repeatable operations into deterministic scripts;
- add explicit failure behavior where the previous Skill silently guessed;
- add acceptance evidence where the previous Skill declared success too easily.

## Phase 7: Validate the revision

Validation has two layers.

### A. Artifact validation

For a Codex Skill, use the official Skill Creator validation workflow when available, including `quick_validate.py` or equivalent checks for:

- valid YAML frontmatter;
- required `name` and `description`;
- naming rules;
- valid paths/references;
- script syntax where applicable.

### B. Behavioral validation

Re-run the original failed case whenever feasible.

If replay is expensive or destructive, create a smaller representative test or fixture that isolates the failure.

Then forward-test at least one neighboring scenario for material Skill changes to reduce overfitting.

Example:

```text
Failure: cleaner deleted detached sword.
Regression test: detached sword remains.
Neighbor test: actual green speck is still removed.
```

Never treat successful Skill syntax validation as proof the behavior is fixed.

## Phase 8: Compare before and after

Summarize:

```text
Observed failure
Verified cause
Owning layer
Files changed
Why this patch should prevent recurrence
Validation evidence
Remaining uncertainty
```

If the repair did not fix the original complaint, do not stack speculative changes indefinitely. Return to multi-hypothesis attribution with the new evidence.

Default correction budget:

- up to 3 targeted corrections at the same ownership level;
- then reconsider the root-cause classification;
- after repeated failures, consider whether the capability needs a new Skill, provider, deterministic tool, or architecture change.

## Phase 9: Promote recurring failures into durable memory

A single incident belongs in the failure log.

Repeated incidents may justify:

- a new `SKILL.md` rule;
- a new reference entry;
- a deterministic validator;
- a regression fixture;
- a router update;
- a new component Skill.

Use this maturity ladder:

```text
complaint
→ observed failure
→ reproduced failure
→ verified cause
→ local fix
→ regression test
→ repeated pattern
→ durable Skill rule/tool
```

Do not jump directly from complaint to universal rule.

## Continual-harness promotion discipline

For broad or reusable self-modification, apply the stricter promotion ladder from `references/continual-harness-refinement.md`:

```text
failure incident
→ observable failure
→ candidate hypothesis
→ verified local cause
→ smallest local patch
→ replay failed case
→ neighbor / regression test
→ candidate reusable lesson
→ independent corroboration
→ durable Skill rule/tool
```

Keep the highest-authority outer constraints immutable. Treat project/session facts as local unless there is clear reason to promote them. Preserve diffs and evidence so a harmful refinement can be reverted or quarantined instead of silently becoming permanent guidance.

A successful self-edit is still a hypothesis until replay and neighboring evidence support it.

## Self-improvement loop

The intended long-term system is:

```text
Codex executes task
↓
user / test / validator reports failure
↓
$on-failure-router
↓
inspect evidence
↓
clarify missing signal
↓
multi-hypothesis attribution
↓
route to owning layer
↓
patch task / Skill / reference / script / router
↓
validate
↓
replay
↓
record lesson
↓
future Codex session uses improved artifact
```

This is **artifact-level self-improvement**, not model-weight self-training. The system improves by updating inspectable instructions, tools, tests, references, and routing logic.

## Important safeguards

- Never modify unrelated Skills just because they were loaded in the same session.
- Never turn one user's subjective preference into a global rule without evidence it is intended to be global.
- Never delete prior failure evidence to make the new behavior appear successful.
- Never weaken a validator solely so a failing artifact passes.
- Never change expected outputs to match a bug unless the user explicitly changed the requirement.
- Never store credentials or secrets in feedback logs.
- Never repeatedly self-edit without replaying or testing the behavior being changed.
- Prefer reversible, reviewable patches.
- Treat context-management and delegation failures as their own owning layers instead of compensating with unrelated domain instructions.

## Output format after a failure repair

Keep the user-facing report compact:

```text
Failure
What actually went wrong.

Cause
The verified owning cause and evidence.

Improvement
Which Skill/reference/script/router was changed and why.

Validation
How the original failure and at least one relevant neighboring behavior were checked.

Learned rule
The durable lesson now encoded for future runs.
```

When the user only wants the task fixed and not the Skill changed, repair the task and report whether the failure exposed a potential Skill improvement without silently modifying global behavior.
