---
name: prompt-enhancer
description: Turn vague, underspecified, or high-level user requests into precise execution prompts by inferring safe context, asking only high-value follow-up questions, identifying missing constraints, assigning reference authority, defining invariants, and producing a concise structured brief with Goal, Context, Constraints, Workflow, and Done When. Use when a request is ambiguous, likely to produce inconsistent results, lacks acceptance criteria, mixes creative and technical intent, or would benefit from a stronger Codex/ChatGPT/image-generation prompt before execution.
---

# Prompt Enhancer

Convert fuzzy intent into an executable specification without turning every request into an interrogation.

The purpose of this Skill is not to make prompts longer. It is to make them **more informative, more testable, and better matched to the downstream tool**.

## Core principle

A strong prompt usually contains the information the model cannot safely infer, while leaving obvious or low-risk details to the model.

Prefer:

```text
clear intent
+ relevant context
+ meaningful constraints
+ explicit invariants
+ reference authority
+ acceptance criteria
```

over repetition, motivational language, excessive examples, or generic requests to "think carefully."

## First decision: is enhancement needed?

Do not enhance a prompt merely because it is short.

A short prompt is sufficient when:

- the desired output is obvious;
- there are few meaningful choices;
- no hard technical constraints are implied;
- failure would be cheap and reversible;
- no identity, layout, runtime, legal, safety, or compatibility invariant is at risk.

Enhance when one or more of the following are true:

- multiple plausible interpretations could materially change the result;
- the task has downstream technical requirements;
- the user references an existing project, asset, person, style, file, or prior state that should be preserved;
- the user wants a production artifact rather than brainstorming;
- success needs tests, measurements, visual review, or runtime validation;
- a creative model must preserve identity, composition, handedness, palette, layout, camera, or other invariants;
- the task should route through specialized Skills or tools;
- the user appears to know the outcome they want but has not specified enough to make execution reliable.

## Clarification policy

Ask follow-up questions only when the answer would materially change execution.

### Ask when

Ask about missing information that has high downstream impact, such as:

- target platform / engine / framework;
- intended use of an image or asset;
- which existing reference is authoritative;
- must-preserve identity or asymmetrical traits;
- dimensions, orientation, runtime resolution, or output format;
- whether an animation loops;
- whether exact fidelity or stylistic reinterpretation matters more;
- compatibility or deployment constraints;
- whether a destructive change is acceptable;
- what counts as complete.

### Infer when

Infer details that are low-risk, conventional, or recoverable, and state the assumption when useful.

Examples:

- use project conventions already present in the repo;
- keep existing architecture unless the request requires changing it;
- preserve unrelated content during an edit;
- choose sensible filenames and directories;
- use nearest-neighbor scaling for true pixel art;
- keep a camera locked when generating sprite animation unless camera motion is explicitly desired.

### Never ask merely to ask

Do not ask questions whose answers can be obtained from:

- repository inspection;
- existing files;
- connected tools;
- attached references;
- project documentation;
- obvious task context.

Inspect first when the answer is available.

## Question priority

When clarification is needed, ask the **smallest set of highest-information questions**.

Rank candidate questions by:

1. How much could the answer change the result?
2. Can the answer be inferred from existing context or files?
3. Would choosing the wrong assumption cause expensive rework?
4. Is the choice subjective enough that the user should decide it?

Prefer 1–4 strong questions over a long questionnaire.

If the user does not answer or immediate execution is required, proceed with labeled assumptions rather than blocking unnecessarily.

## Enhancement workflow

### Step 1: Extract the user's actual intent

Identify:

- desired outcome;
- intended audience/user;
- target environment;
- whether the task is exploratory or production;
- what existing state must be preserved;
- what failure would look like.

Do not merely paraphrase the user's wording. Infer the likely operational objective.

### Step 2: Classify the task

Choose the dominant prompt mode:

- coding / agentic implementation;
- research / analysis;
- image generation;
- image editing;
- game asset production;
- 3D reconstruction;
- writing / content;
- data / structured output;
- mixed workflow.

Read `references/prompt-patterns.md` for mode-specific structure.

### Step 3: Inspect context before questioning

When tools/files are available, inspect the minimum relevant context first.

For coding tasks, look for:

- `AGENTS.md` or equivalent project instructions;
- README / architecture docs;
- relevant source files;
- tests;
- existing Skills;
- configuration and runtime constraints.

For image or game-asset tasks, identify:

- canonical identity/reference image;
- style reference;
- pose/layout reference;
- target engine/runtime;
- logical and display resolution;
- alpha/chroma requirements;
- animation/facing/handedness constraints.

### Step 4: Separate facts, assumptions, and questions

Internally classify missing details as:

- **KNOWN** — explicitly supplied or verified;
- **INFERABLE** — safe to infer from context;
- **ASK** — material ambiguity requiring user input;
- **OPTIONAL** — useful but not necessary.

Do not present this taxonomy unless it helps the user.

### Step 5: Ask high-value follow-ups when needed

Questions should be concrete and preferably offer useful choices.

Example:

```text
Before I finalize the production prompt, two choices materially affect the pipeline:
1. Is the pirate image a canonical identity anchor that must remain visually identical, or just a style reference?
2. Is the final sprite intended for Phaser pixel-art rendering at a fixed logical size, or is this only concept art?
```

Avoid vague questions like:

```text
Can you provide more details?
```

### Step 6: Extrapolate missing production detail

Once the important ambiguities are resolved, add the constraints an expert would normally remember but a casual user may omit.

Examples:

For coding:

- inspect before editing;
- preserve existing behavior unless requested otherwise;
- identify files likely affected;
- define tests and acceptance criteria;
- use the smallest owning change;
- report assumptions and unresolved risks.

For images:

- intended use;
- subject;
- camera/view;
- composition;
- shape language;
- materials/palette;
- what may change;
- what must remain invariant;
- background / margin / crop rules;
- avoid list.

For game assets:

- canonical identity authority;
- runtime engine;
- working/logical/runtime resolution;
- facing and handedness;
- alpha/chroma strategy;
- animation loop behavior;
- frame recovery before pixel snapping;
- deterministic packing;
- quality gates.

### Step 7: Assign authority to references

When multiple references exist, state what each one controls.

Example:

```text
Reference authority:
- Image 1: character identity, outfit, proportions, palette.
- Image 2: pose only.
- Image 3: pixel-grid/block structure only.

Do not borrow unlisted properties from the secondary references.
```

This is especially important for image generation and game assets.

### Step 8: Separate CHANGE from PRESERVE

For edits and transformations, explicitly distinguish:

```text
CHANGE
```

from:

```text
PRESERVE
```

Preserve lists should contain the identity or structural invariants most likely to drift.

Examples:

- face;
- costume;
- eyepatch/scar side;
- weapon hand;
- palette;
- camera;
- subject scale;
- layout;
- API contract;
- data schema;
- unrelated existing behavior.

### Step 9: Add completion criteria

A production prompt should define what evidence establishes success.

Use a `Done when` section for coding/agent tasks.

Examples:

- tests pass;
- target build succeeds;
- visual comparison reviewed;
- output dimensions match contract;
- runtime loader math is measured, not guessed;
- no identity drift;
- artifact path exists;
- quality gate reports pass;
- remaining uncertainties are disclosed.

Do not let successful command execution substitute for semantic success.

### Step 10: Keep the final prompt lean

Remove:

- duplicated rules;
- filler;
- repeated adjectives;
- generic "think deeply" language;
- instructions already guaranteed by a loaded Skill;
- examples that do not add a new constraint.

The enhanced prompt should be as short as possible while still containing the information required for reliable execution.

## Output behavior

Use one of three modes depending on the user's request.

### Mode A: Ask first

When unresolved choices are material, respond with the high-value questions only, plus a short statement of what will be inferred automatically.

### Mode B: Enhance now

When enough context exists, output:

```text
Enhanced prompt
```

followed by the rewritten prompt.

Optionally include a compact `Assumptions` section when important inferred details were added.

### Mode C: Enhance and execute

When the user asks for both enhancement and execution, create the improved internal brief and then execute it. Do not force the user to approve a rewritten prompt unless approval is actually needed.

## Canonical structures

### Codex / coding

```text
GOAL

CONTEXT

CONSTRAINTS

WORKFLOW
[only when order matters]

DONE WHEN
```

### Research / analysis

```text
TASK

CONTEXT

SOURCES / EVIDENCE

PRIORITIES

UNCERTAINTIES TO FLAG

OUTPUT
```

### Image generation / game asset

```text
PURPOSE

SUBJECT

VIEW / CAMERA

SHAPE LANGUAGE

STYLE / MEDIUM

MATERIALS / PALETTE

COMPOSITION

REFERENCE AUTHORITY

CHANGE
[when editing]

PRESERVE
[when identity/layout must remain stable]

PIPELINE CONSTRAINTS

AVOID
```

## Prompt-quality checks

Before returning an enhanced prompt, verify:

- Does it state the actual goal?
- Does it give the model only relevant context?
- Are important invariants explicit?
- Are references assigned specific authority?
- Are creative and deterministic responsibilities separated where appropriate?
- Is there a definition of done for production work?
- Did we avoid asking questions that could have been answered by inspection?
- Did we avoid inventing precise requirements the user never implied?
- Did we remove repetitive wording?
- Could a competent agent execute this without guessing the expensive parts?

## Special rule for game assets

For game-asset prompts, treat creative generation as source material unless the workflow explicitly says otherwise.

Prefer:

```text
AI generates intent/reference
→ constrained intermediate representation
→ deterministic normalization
→ validation
→ runtime handoff
```

When relevant, route through specialized Skills such as identity anchoring, frame recovery, pixel snapping, alignment, cleanup, packing, quality gating, or image-to-3D reconstruction instead of stuffing all domain expertise into the task prompt.

## Anti-patterns

Do not:

- make every prompt longer;
- repeat the same rule several ways;
- ask ten low-impact questions;
- ask the user for information already present in the repo;
- silently choose a high-impact subjective requirement;
- turn style references into identity authorities unless instructed;
- treat an AI-generated sprite sheet as authoritative runtime geometry;
- use a creative generator for deterministic packing/math;
- replace a specialized Skill with a giant one-off prompt;
- declare success without the evidence specified by the task.
