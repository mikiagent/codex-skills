# Failure Taxonomy for Self-Improving Codex Skills

Use this taxonomy to avoid vague reflection and route failures to the correct intervention level.

## 1. Environment / discovery failure

Symptoms:
- Skill exists but is not visible to Codex.
- Binary/tool not found.
- Wrong `CODEX_HOME`.
- Broken symlink.
- Permission denied.
- Provider/model unavailable.
- Dependency version mismatch.

Evidence:
- filesystem paths
- `skills/list`
- shell errors
- package versions
- provider status

Fix owner:
- installation/configuration/environment

Do not rewrite Skill behavior unless the Skill's installation instructions are themselves wrong.

## 2. Prompt / intent failure

Symptoms:
- output is plausible but not what the user wanted;
- critical subjective choice was silently guessed;
- preservation requirement was not stated;
- intended use was missing.

Evidence:
- original request
- conversation context
- prompt sent to downstream model

Fix owner:
- task prompt/context or `$prompt-enhancer`

Promote to Skill rule only if the same missing requirement should be inferred or asked for repeatedly.

## 3. Trigger / router failure

Symptoms:
- expected Skill never loaded;
- wrong Skill loaded;
- required component skipped;
- two Skill descriptions overlap enough to create unstable routing.

Evidence:
- available Skill metadata
- invoked Skill list
- orchestration logs
- frontmatter descriptions

Fix owner:
- Skill `description`
- router Skill
- orchestrator

## 4. Workflow / ordering failure

Symptoms:
- correct tools exist but run in the wrong order;
- downstream transformation destroys evidence needed upstream;
- a validation stage happens too late;
- a required intermediate artifact is missing.

Evidence:
- Skill instructions
- command history
- artifact timestamps
- state/log files

Fix owner:
- `SKILL.md` workflow/contract

## 5. Knowledge / reference failure

Symptoms:
- agent follows the workflow but lacks an edge case;
- API/platform behavior is stale;
- known failure mode was never documented;
- prompt recipe omits a domain-specific constraint.

Evidence:
- reference docs
- authoritative external docs
- repeated incidents

Fix owner:
- targeted file under `references/`

## 6. Deterministic implementation failure

Symptoms:
- calculation is wrong;
- parser/cropper/packer fails;
- API pagination/retry behavior is broken;
- validator reports false positive/negative;
- script succeeds while producing malformed output.

Evidence:
- reproducible input fixture
- stack trace
- output diff
- unit/regression test

Fix owner:
- script/tool + regression test

Prefer code enforcement over adding more prose to the Skill.

## 7. Acceptance / validation failure

Symptoms:
- agent says done while output is visibly wrong;
- tests cover syntax but not semantics;
- validator can be bypassed by wording;
- missing evidence is treated as pass.

Evidence:
- quality contract
- artifact review
- test coverage
- status decision logic

Fix owner:
- quality gate / acceptance contract / regression tests

Never weaken a validator merely to make a failing artifact pass.

## 8. Provider / model limitation

Symptoms:
- model consistently drifts despite correct prompt/reference;
- requested capability is unsupported;
- stochastic output exceeds tolerance;
- local model cannot fit memory/runtime constraints.

Evidence:
- repeated controlled runs
- provider documentation
- comparison across providers/settings

Fix owner:
- provider choice
- conditioning strategy
- deterministic post-processing
- retry/budget policy

Do not encode false guarantees in Skill instructions.

## 9. Architecture / missing capability

Symptoms:
- same class of failure keeps falling between existing Skills;
- one Skill owns too many unrelated concerns;
- repeated manual repair has a stable workflow and acceptance contract.

Evidence:
- failure log clusters
- repeated correction history
- ownership ambiguity

Fix owner:
- new component Skill or architectural split

Use `$skill-creator` and require concrete examples before creation.

# Multi-hypothesis attribution template

For uncertain failures, write 2-5 entries:

```text
HYPOTHESIS:

EVIDENCE FOR:

EVIDENCE AGAINST / MISSING:

OWNING LAYER:

CHEAPEST VERIFICATION:
```

Verify before patching whenever possible.

# Evidence hierarchy

Prefer evidence roughly in this order:

1. reproducible test failure
2. direct artifact inspection
3. command/log trace
4. deterministic measurement
5. user-observed symptom
6. model self-critique without external evidence

User feedback is extremely important because it defines dissatisfaction, but the root cause should be grounded in inspectable evidence when possible.

# Promotion rule

Use the following ladder:

```text
complaint
→ observable symptom
→ reproduction
→ verified cause
→ local repair
→ regression check
→ repeated pattern
→ durable Skill improvement
```

Do not universalize a one-off complaint prematurely.
