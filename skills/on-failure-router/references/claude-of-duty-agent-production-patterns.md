# Claude-of-Duty Agent Production Patterns

Status: `SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`
Date: 2026-08-14
Source repository: `mshumer/Claude-of-Duty`

Purpose: record AI-production and failure-diagnosis lessons from a large Three.js FPS built by orchestrated AI agents.

These findings are not yet promoted into mandatory `on-failure-router` behavior. They should be tested in our own workflows first.

# 1. Parallelism depends on coupling

The project reports that parallel directory-owner passes worked poorly when the actual concern crossed tightly coupled visual systems such as materials, sky, exposure, tonemapping, and indirect-light approximations. Sequential ownership over the coupled concern produced a better result than several rounds of parallel fan-out.

Transfer candidate:

```text
independent ownership domains
→ parallel workers

tightly coupled optimization domain
→ one owner or explicitly ordered passes

material result
→ independent verifier
```

This refines rather than rejects agent parallelism.

## Failure-router implication

When repeated fixes from different owners conflict or oscillate, add a root-cause hypothesis:

> The failure may belong to a coupled system whose ownership boundary is larger than the current patch scope.

Do not automatically respond by spawning more agents against adjacent files.

# 2. Feedback names symptoms more reliably than causes

The project documents a weapon-material problem repeatedly described by critics as “untextured.” Prior agents responded by changing albedo in the requested direction. Measurement later showed the important mechanism was specular-dominated lighting/material response and insufficient diffuse contribution; the literal complaint was not a causal diagnosis.

This strongly supports the existing router rule:

```text
user/critic feedback
= high-value error signal
≠ guaranteed root cause
```

Transfer candidate diagnostic sequence:

```text
complaint
→ restate observable failure without causal assumption
→ generate competing mechanisms
→ collect discriminating evidence
→ identify owning layer
→ patch
```

A user's causal hypothesis can be included as one candidate hypothesis, not silently accepted as ground truth.

# 3. Deterministic visual evidence can itself be broken

An early screenshot workflow reused one browser page for multiple named shots. Particle age, decal state, exposure adaptation, and other temporal state leaked from earlier shots into later ones. Identical nominal runs therefore produced different images.

The replacement baseline workflow isolated shots in fresh page state and used fixed frame budgets, enabling reproducible image comparisons.

Transfer candidate:

```text
visual failure evidence
must itself have a validity contract
```

For visual regression fixtures consider:

- fresh page/process where cross-test state is possible;
- fixed RNG seed;
- fixed engine time/frame count;
- fixed camera/state;
- fixed viewport/DPR;
- explicit “assets ready” boundary;
- known intentional stochastic regions.

## Failure-router implication

Before patching the product because a visual regression changed, include an evidence-integrity hypothesis:

> Did the fixture/capture process itself introduce nondeterminism or stale state?

This is especially important if identical source code produces changing screenshots.

# 4. Median performance can hide the real failure

The source documents an initially reassuring performance measurement while actual gameplay contained very large stalls associated with lazy WebGL program compilation. The profiling workflow was changed to inspect frame-time distributions and hitch attribution.

Transfer candidate metrics for real-time failures:

```text
p50
p95
p99
worst frame
long-frame count
program/shader creation during play
```

## Failure-router implication

When the user says “performance sucks” but average/median FPS looks acceptable, do not dismiss the complaint. Competing hypotheses should include:

- rare shader compilation;
- asset upload/decode spikes;
- GC pauses;
- first-use initialization;
- occasional CPU simulation spikes;
- render-target reallocations;
- network/main-thread contention.

Use distribution/timeline evidence rather than only aggregate FPS.

# 5. Optimization can be constrained by output invariants

The source's optimization pass used pixel-diff evidence to enforce “no visual change” while changing performance behavior.

General transfer pattern:

```text
optimize mechanism
while holding requested external behavior invariant
```

Possible invariants in our workflows:

- same rendered pixels for a visual-neutral optimization;
- same public API output;
- same spritesheet bytes/dimensions;
- same game simulation trajectory under deterministic inputs;
- same validated schema/content;
- same network protocol behavior.

## Failure-router implication

A repair should state what must change and what must remain unchanged. Neighbor/regression tests should verify both.

# 6. Architecture contracts help agent ownership

Claude-of-Duty uses an architecture contract defining subsystem ownership, shared context/interface surfaces, and cross-system event vocabulary.

Transfer candidate:

```text
agent ownership
should follow semantic system boundaries
not arbitrary file-count partitioning
```

Parallel work is safer when agents share stable contracts rather than importing directly into each other's internal implementations.

# 7. A correction budget should reconsider ownership, not just retry prompts

The source's reported oscillation across coupled visual passes supports our existing correction-budget idea.

If several targeted repairs at the same ownership level fail:

```text
stop repeating local edits
→ reconsider root cause
→ reconsider owning layer
→ reconsider coupling boundary
→ reconsider evidence validity
```

Do not interpret “the agent tried three times” as evidence that a fourth paraphrase is the right intervention.

# 8. Candidate experiments before adoption

These findings should remain transfer candidates until tested locally.

## Experiment A — parallel vs sequential coupled work

Choose one deliberately coupled visual concern.

Run:

1. parallel independent owners;
2. sequential single concern owner;
3. independent verifier on each result.

Measure:

- defects introduced;
- acceptance criteria passed;
- merge/conflict corrections;
- total correction count;
- final perceptual score/evidence.

## Experiment B — symptom vs cause

Create a failure where the supplied user causal explanation is plausible but wrong.

Success condition:

The router records the complaint, generates alternatives, finds discriminating evidence, and patches the real owner instead of obeying the causal suggestion literally.

## Experiment C — evidence nondeterminism

Create a visual fixture with hidden temporal state leakage.

Success condition:

The router identifies the test fixture/capture layer as the owner before making product-code changes.

## Experiment D — tail-latency diagnosis

Create a workload with acceptable median FPS but one recurring long frame.

Success condition:

The router requests/uses p95/p99/worst-frame timeline evidence and identifies the spike source.

# 9. Proposed durable rule only after corroboration

If the experiments succeed independently, the likely durable invariant is:

> Failures should be diagnosed across product behavior, ownership/coupling boundaries, and evidence integrity. User feedback is a valuable symptom signal, while tests, measurements, artifacts, and reproduction discriminate root cause.

Do not add this as mandatory global behavior from this source observation alone.