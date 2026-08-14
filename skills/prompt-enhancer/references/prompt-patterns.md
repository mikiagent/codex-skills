# Prompt Enhancer Reference Patterns

Use this file to choose the smallest useful prompt structure for the task.

## 1. Codex / coding tasks

Use when the user wants implementation, debugging, refactoring, repo work, automation, or agentic execution.

```text
GOAL
What outcome should exist when the task is complete?

CONTEXT
What repo/files/features/current behavior matter?
Which Skills/tools should be used?

CONSTRAINTS
What must be preserved?
What technical boundaries exist?
What must not change?

WORKFLOW
Only include this when ordering materially affects correctness.

DONE WHEN
What tests, artifacts, runtime checks, or evidence prove success?
```

High-value follow-up questions often concern:

- target platform/runtime;
- whether current behavior must remain backward compatible;
- whether architecture can change;
- which implementation is authoritative when duplicate paths exist;
- what counts as acceptance.

Infer ordinary repo conventions by inspection.

## 2. Research / analysis

```text
TASK
What are we trying to learn or decide?

CONTEXT
Why does the answer matter?

SOURCES / EVIDENCE
What sources are authoritative or preferred?

PRIORITIES
What dimensions matter most?

UNCERTAINTIES TO FLAG
What claims require explicit uncertainty?

OUTPUT
What format would be most useful?
```

Ask follow-ups when the answer depends heavily on scope, date range, geography, or decision criteria.

## 3. Image generation

```text
PURPOSE
What will the image be used for?

SUBJECT
Who/what is depicted?

VIEW / CAMERA
Framing, angle, lens/perspective, crop.

SHAPE LANGUAGE
Geometric/organic construction and silhouette.

STYLE / MEDIUM
Rendering medium and aesthetic direction.

MATERIALS / PALETTE
Concrete surfaces, colors, textures.

COMPOSITION
Placement, spacing, background, hierarchy.

REFERENCE AUTHORITY
What property comes from each reference?

PRESERVE
Identity/layout invariants.

PIPELINE CONSTRAINTS
Requirements caused by downstream use.

AVOID
Specific failure modes.
```

For simple images, collapse this into a few sentences instead of forcing every heading.

## 4. Image editing

Always distinguish transformation from invariants.

```text
CHANGE
Exactly what should be different.

PRESERVE
Exactly what should remain the same.

REFERENCE AUTHORITY
What each reference controls.

OUTPUT CONSTRAINTS
Dimensions/background/use.
```

Useful wording:

```text
Change only X.
Preserve Y, Z, camera, composition, identity, and unrelated details.
```

## 5. 2D game character / sprite source

```text
PURPOSE
Canonical source image for a deterministic sprite pipeline.

CHARACTER IDENTITY
Silhouette, face, clothing, asymmetries, weapon/hand rules.

VIEW
Facing and camera.

WORKING SIZE
Usually a large supported generation size.

TARGET LOGICAL SIZE
Compact runtime identity scale if known.

BACKGROUND / ALPHA
True alpha or chroma color absent from subject.

COMPOSITION
Full body, safe margins, no crop.

PRESERVE
Long-term identity invariants.

AVOID
Shadows, scenery, text, extra characters, perspective drift, tiny unreadable details.
```

Do not request every animation in the source-generation step. Establish identity first.

## 6. Sprite animation

```text
PURPOSE
Which runtime action is being produced?

CANONICAL ANCHOR
Which facing/identity image is authoritative?

ACTION CONTRACT
Loop or one-shot; intended frame count/range; timing/cadence.

FRAME SCHEDULE
One ordered description per intended meaningful sprite frame.

PRESERVE
Identity, facing, scale, handedness, camera, costume, palette.

INTENTIONAL MOTION
What displacement must alignment preserve?

PIPELINE
Generate source material → recover → curate → snap → align → clean → pack → QA.
```

## 7. Multi-reference image prompting

Assign authority explicitly.

```text
Image 1: identity authority only.
Image 2: pose authority only.
Image 3: style authority only.
Image 4: grid/structure authority only.

Do not borrow unlisted properties from secondary references.
```

This prevents a style reference from silently changing identity or composition.

## 8. Procedural 3D game asset

```text
PURPOSE
Runtime use and target camera/distance.

REFERENCE
What image(s) provide evidence?

OBSERVED FEATURES
Silhouette, components, materials, attachments.

UNCERTAINTY
Which surfaces are unseen or inferred?

RUNTIME CONTRACT
Scale, up/forward axes, ground anchor, pivots, sockets, colliders, budgets.

QUALITY CONTRACT
Required views, likeness thresholds, interaction requirements.

DONE WHEN
Controlled renders and runtime structure both pass.
```

A visually convincing front render is not sufficient evidence of game-ready geometry.

## 9. UI / frontend generation

```text
GOAL
What interaction/business outcome matters?

REFERENCE AUTHORITY
Which screenshot/design controls layout, typography, spacing, branding?

EXISTING SYSTEM
Framework/components/design tokens already present.

PRESERVE
Existing functionality/accessibility/responsiveness.

CHANGE
Specific visual or interaction changes.

DONE WHEN
Build/tests pass and target breakpoints visually match.
```

## 10. Vague idea → executable project brief

When the user says something like:

```text
Make a cozy farming game.
```

Do not immediately invent a huge product spec as fact.

Extract likely dimensions and identify only the decisions that materially define the product:

- platform;
- core loop;
- active vs passive play;
- visual representation;
- monetization/business goal if relevant;
- scope of first playable version.

Then infer ordinary production details and produce a brief such as:

```text
GOAL
Build a portrait mobile-friendly cozy passive animal-collecting farm prototype.

CORE LOOP
Acquire animal → animal earns passive currency → collect → upgrade → unlock next animal.

FIRST PLAYABLE SCOPE
4 species, one pasture, local save, offline earnings, upgrades, simple progression.

ART DIRECTION
Stylized reconstruction-friendly voxel animals.

TECH
Three.js browser prototype.

DONE WHEN
The full loop is playable from a fresh save and works at phone aspect ratios.
```

Clearly label major assumptions when they were not explicitly chosen by the user.
