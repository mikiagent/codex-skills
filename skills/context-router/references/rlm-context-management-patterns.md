# RLM and Context-Management Patterns

## Status

`SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`

This reference records reusable context-management ideas derived from the following sources:

- Alex L. Zhang, Tim Kraska, Omar Khattab — Recursive Language Models
- Alex Zhang's 2025 RLM blog post
- `alexzhang13/rlm`
- Prime Intellect `prime-agent`
- Chroma context-rot research
- Continual Harness
- later RLM reproduction work

These sources support the architectural direction, but they do not prove that every transferred heuristic improves Codex in every task. Treat the Skill behavior as a local prototype until measured against simpler baselines.

## 1. Context capacity is not context utilization

A model accepting a large prompt does not imply all of that prompt is equally useful to reasoning.

Transfer:

```text
context window = storage capacity
active working set = evidence needed now
```

Keep durable sources outside active context until the task requires them.

## 2. Prompt-as-variable / source-as-object

RLMs move large source material out of the model prompt and expose it programmatically.

The transferable abstraction is broader than Python:

```text
large source remains authoritative outside prompt
→ inspect/search/filter/transform
→ admit selected observations
→ reason
```

Files, repositories, SQL tables, notebooks, logs, indexes, and structured tool results can all serve as externalized context.

## 3. Probe before deep semantic reading

Structural inspection can cheaply answer:

- What exists?
- Where are likely ownership boundaries?
- Which files are large?
- Which languages/types dominate?
- Where are tests/configs/manifests?
- Which exact symbols or terms occur?

Only then spend semantic attention on selected regions.

## 4. Retrieval, compaction, and externalization solve different problems

### Retrieval

Find likely relevant chunks before reasoning.

### Compaction

Turn old interaction history into a lossy summary when exact details are no longer necessary.

### Externalized context

Keep the full source intact outside the prompt and let the agent adaptively query or transform it.

Do not substitute one mechanism blindly for another.

## 5. Subagents are context partitions

A useful child agent has:

- a bounded objective;
- a bounded source scope;
- an independent context;
- an explicit output contract;
- evidence traceable to source artifacts.

The child should return a compact evidence packet, not its entire transcript.

## 6. Shallow recursion by default

The original RLM experiments demonstrated value from recursive subcalls, but later reproduction work showed deeper recursion can increase cost/latency and can hurt performance through overthinking.

Transfer:

```text
root orchestrator
→ focused children
```

should be the default shape.

Deeper delegation should require evidence that each additional level materially shrinks the problem or provides necessary independence.

## 7. Preserve exact evidence outside summaries

Summaries are useful orientation artifacts but are lossy.

Decision-critical claims should be checked against source truth before finalization.

A good evidence packet includes source paths/identifiers so the parent can reopen exact evidence.

## 8. Measure scaffolding overhead

Context architecture should earn its complexity.

Useful comparison metrics:

- answer correctness / acceptance status;
- evidence coverage;
- root tokens;
- total tokens;
- number of source regions admitted;
- child count;
- maximum delegation depth;
- latency;
- cost.

The simplest workflow that reliably satisfies the requirement should win.

## 9. Context architecture is not permission architecture

Persistent Python, shell access, subagents, and durable state increase capability, but do not create a security sandbox.

Keep security boundaries explicit and separate from context-management design.

## Local experiment to run

Hold the model and task constant and compare:

```text
A. direct broad read / giant prompt
B. deterministic search + normal reasoning
C. probe → narrow → admit
D. probe → narrow → focused child contexts
```

Measure correctness, evidence coverage, token usage, latency, and cost before promoting these transfer candidates into stronger global rules.
