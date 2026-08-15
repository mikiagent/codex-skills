# Delegation Contract

Use this reference when assigning material work to a child agent.

## Child prompt template

```text
Role
You are the <specialist role>.

Objective
Produce <one bounded outcome>.

Scope
Work only within:
- <paths / subsystem / sources>

Authoritative sources
Inspect these before relying on memory:
- <source/path>

Constraints
- <must preserve>
- <must not assume/change>
- Do not broaden scope without reporting why.

Output artifact
Return or create:
- <patch/report/evidence packet/test result>

Acceptance criteria
- <observable requirement 1>
- <observable requirement 2>

Validation evidence
Provide:
- exact paths/sources inspected;
- commands/tests run;
- artifact identifiers or screenshots when relevant;
- unresolved uncertainty or contradictions.

Return format
Finding / outcome
Evidence
Changes
Validation
Uncertainty
Recommended next action
```

## Planner contract

A planner should produce:

- requirement interpretation;
- ownership boundaries;
- proposed architecture;
- exact files likely to change;
- constraints;
- acceptance criteria;
- cheapest valid validation layers;
- implementation risks.

A planner should not silently implement and then describe its own implementation as the plan.

## Implementer contract

An implementer should receive the requirement/plan plus authoritative current source.

It should return:

- files changed;
- why each change is required;
- tests/checks run;
- known limitations;
- anything that deviated from the plan and why.

The implementer should not self-certify final acceptance when an independent verifier is required.

## Verifier contract

The verifier should receive:

- original requirement;
- acceptance criteria;
- current artifact/source state;
- relevant test/validation commands.

It should not depend on the implementer's narrative as the primary evidence.

Return:

```text
Criterion
Evidence
PASS | FAIL | INCONCLUSIVE

Overall verdict
Remaining gaps
```

For visual requirements, inspect the rendered result perceptually in addition to structural checks.

## Research child contract

A research child should distinguish:

```text
SOURCE-OBSERVED
INFERENCE
TRANSFER-CANDIDATE
UNVERIFIED CLAIM
```

It should return exact source identities and avoid converting vendor/self-reported claims into local proof.

## Conflict-resolution child

When sibling agents disagree, give a verifier only the disputed question and the authoritative evidence sources.

Avoid asking it to rerun the entire original task.

```text
Dispute
A says: ...
B says: ...

Decisive question
...

Authoritative evidence to inspect
...

Return
Which claim is supported, exact evidence, and remaining uncertainty.
```

## Context budget rule

Do not paste the whole parent transcript into child prompts.

Prefer pointers to durable source artifacts plus the minimal task-specific facts required to interpret them.
