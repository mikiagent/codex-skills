# Self-Improvement Patterns Behind the On-Failure Router

This Skill uses a synthesis of current Codex Skill guidance and agent self-correction research. The useful common theme is that reliable self-improvement needs **external feedback, structured diagnosis, explicit memory, and validation**, not just a generic instruction to "reflect."

## OpenAI Codex Skill Creator

Current OpenAI Skill Creator guidance explicitly treats real usage failures as inputs to Skill iteration:

```text
use Skill on real tasks
→ notice struggles or inefficiencies
→ identify how SKILL.md or bundled resources should change
→ implement changes
→ test again
→ forward-test complex/material revisions
```

Other relevant principles:

- keep Skills concise;
- put only non-obvious reusable knowledge in context;
- choose appropriate degrees of freedom;
- use deterministic scripts for fragile repeatable operations;
- protect validation integrity;
- validate the Skill folder after changes;
- use realistic forward tests for substantial revisions;
- treat raw artifacts, outputs, diffs, logs, and traces as better evaluation evidence than leaked intended answers.

Source:
- OpenAI Codex `skill-creator` sample, 2026.

## Reflexion

Reflexion introduced a useful artifact-level learning idea: agents can improve across attempts by converting feedback into a short verbal reflection stored in episodic memory rather than changing model weights.

Useful idea adopted here:

```text
failure feedback
→ explicit lesson
→ persistent memory
→ use lesson on later attempt
```

Limitation for our use:
A free-form reflection alone is not enough. Our implementation requires the reflection to be grounded in task artifacts and routed to an owning layer.

Source:
- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning," 2023.

## Self-Refine

Self-Refine formalized a simple iterative loop:

```text
initial output
→ feedback
→ refinement
→ repeat
```

Useful idea adopted here:
- explicit feedback and revision are separate operations;
- improvement can happen at inference time without retraining weights.

Limitation for our use:
The same model judging itself can reproduce the same blind spots. The On-Failure Router therefore prefers user feedback, tests, screenshots, logs, validators, and artifacts over self-feedback alone.

Source:
- Madaan et al., "Self-Refine: Iterative Refinement with Self-Feedback," 2023.

## Structured reflection for tool failures

Recent tool-agent research argues that simply prompting an agent to "think more" after a failed tool call is fragile. A stronger loop explicitly diagnoses the failed step and proposes an executable repair.

Useful idea adopted here:

```text
error
→ evidence-grounded diagnosis
→ corrected action
→ verify result
```

This motivates the separation between failure attribution and repair.

Source:
- Su et al., "Failure Makes the Agent Stronger: Enhancing Accuracy through Structured Reflection for Reliable Tool Interactions," 2025.

## Failure-driven inference-time self-improvement

Recent computer-use-agent work tested a failure-driven loop in which failed trajectories are diagnosed and turned into inference-time solutions and code patches, rather than discarded.

Useful idea adopted here:

```text
failed trajectory
→ diagnose failure mode
→ propose intervention
→ patch agent artifacts
→ verify
```

This is very close to the target architecture for Codex Skills. In our system the patch targets inspectable files such as `SKILL.md`, references, deterministic scripts, tests, routing rules, or project configuration.

Source:
- Sun et al., "Learning from Failure: Inference-Time Self-Improvement for Computer-Use Agents," 2026.

## Multi-Hypothesis Failure Attribution

Recent autonomous-research work reports that one monolithic reflection can collapse rich evidence into an unreliable critique. It instead generates multiple evidence-grounded failure explanations and routes the verified cause to the appropriate intervention level.

Useful idea adopted here:

```text
failure trajectory
→ several candidate causes
→ evaluate evidence
→ verify root cause
→ route to correct intervention layer
```

This directly motivates the On-Failure Router's hypothesis table and ownership levels.

Source:
- Ma et al., "One Reflection Is Not Enough: Self-Correcting Autonomous Research via Multi-Hypothesis Failure Attribution," 2026.

## Why external evidence matters

Recent work comparing LLM revision to human revision warns that self-reflection without additional information may behave more like conditioned re-generation than true correction and can even degrade outputs on some tasks.

Useful design consequence:

Do not use:

```text
bad result
→ tell same model to reflect harder
→ accept next answer
```

Prefer:

```text
bad result
→ add external information
   - user's concrete complaint
   - test output
   - logs
   - screenshot
   - artifact diff
   - validator result
→ diagnose
→ repair
→ replay
```

Source:
- Tao et al., "Reflection or Re-Generation? Why LLM Revision Fails Where Human Revision Succeeds," 2026.

## NJ MMO: deterministic lesson promotion and independent verification

A detailed source analysis is maintained in:

- `references/nj-mmo-self-improvement-patterns.md`
- repository-wide research status: `docs/LIVING_RESEARCH.md`

NJ MMO provides a useful **source-observed but not yet locally validated** implementation pattern that goes beyond a flat failure log:

```text
incident
→ grounded candidate lesson
→ recurrence across distinct features
→ confirmed guidance
→ monitor future applications
→ quarantine if repeatedly harmful
```

Its lesson-management script delegates semantic judgment to the model but keeps IDs, recurrence counts, candidate promotion, stale-candidate pruning, penalty counts, quarantine, and Markdown rendering deterministic. Its verifier is also intentionally independent from the implementing agent for material feature work.

The strongest transferable hypothesis is therefore:

> A failure should be recorded immediately, but the generalized lesson inferred from it should not automatically become trusted global guidance.

For this Skill repository, this remains a **transfer candidate**, not an adopted production rule. We have not yet tested NJ MMO's numeric thresholds, expiry window, or verifier economics against our own workload. Keep research claims labeled accordingly until local experiments corroborate them.

## Compiled architecture

The current baseline architecture is:

```text
EXECUTION
↓
FAILURE SIGNAL
↓
EVIDENCE PRESERVATION
↓
HIGH-VALUE CLARIFICATION
↓
MULTI-HYPOTHESIS ATTRIBUTION
↓
OWNER CLASSIFICATION
↓
SMALLEST DURABLE PATCH
↓
ARTIFACT VALIDATION
↓
BEHAVIORAL REPLAY
↓
NEIGHBOR / REGRESSION TEST
↓
FAILURE MEMORY
↓
FUTURE EXECUTION USES IMPROVED ARTIFACTS
```

The NJ MMO research suggests a candidate extension after behavioral validation:

```text
FAILURE MEMORY
↓
CANDIDATE LESSON
↓
INDEPENDENT CORROBORATION?
├── no → retain temporarily / expire if stale
└── yes → CONFIRMED GUIDANCE
              ↓
       harmful when reused?
       ├── no → remain confirmed
       └── yes → QUARANTINE + review
```

Do not enforce the extension until the local lesson-registry experiment has been run.

This is not model self-training. It is **system self-improvement through editable artifacts**.

## What can improve

The router may improve:

- task prompt templates;
- Skill trigger descriptions;
- Skill workflows;
- reference docs;
- deterministic scripts;
- validators;
- regression fixtures;
- orchestrator routing;
- installation instructions;
- state and retry policies;
- new Skills when a stable ownership boundary emerges.

## What should not become permanent automatically

Do not promote these directly into global Skill behavior:

- one-off aesthetic preferences;
- transient API outages;
- project-specific business rules;
- unexplained user dissatisfaction;
- fixes unsupported by replay/testing;
- changes that only make a validator stop complaining;
- externally observed research patterns that have not yet been tested in our own environment.

A self-improving agent becomes useful when its memory is selective, causal, and testable.
