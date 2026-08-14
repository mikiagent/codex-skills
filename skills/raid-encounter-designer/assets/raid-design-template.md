# Raid Design: <name>

Status: draft
Designer: <name/agent>
Target game/project: <project>

# 1. Fantasy and Emotional Targets

## Raid fantasy

<What adventure are the players undertaking?>

## Target cooperative feelings

- <shared discovery>
- <individual accountability>
- <trust / relay / controlled panic / mastery>

## What should players remember?

<Iconic image, decision, social moment, boss behavior, or traversal beat.>

# 2. Player Count and Experience Target

- Fireteam size: <N>
- Expected prior knowledge: <none / mechanic A / advanced raid literacy>
- Blind-clear target: <description>
- Repeat-clear target: <description>
- Challenge/master target: <description>

# 3. Raid Mechanic Vocabulary

| Primitive / noun | What it means | Where introduced | How it evolves |
|---|---|---|---|
| <A> | <rule> | <encounter> | <twists> |

# 4. Raid Sequence and Pacing Curve

| Beat | Type | Intensity | Mechanic purpose | Story/spectacle purpose |
|---|---|---:|---|---|
| Entrance | traversal | low | orientation | establish scale |
| Encounter 1 | <type> | <1-5> | <teach A> | <story> |

# 5. Encounter Cards

Repeat this section for every encounter.

## Encounter: <name>

### Fantasy

<What is happening fictionally?>

### Objective

<What must the fireteam accomplish?>

### Mechanic primitives

- <observe>
- <relay>
- <split team>

### Information graph

```text
<Role A> --<callout>--> <Role B>
<Role B> --<state change>--> <Role C>
```

| Information | Who can see it? | Who needs it? | Valid for how long? | Confirmation |
|---|---|---|---|---|
| <target> | <observer> | <operator> | <seconds/state> | <feedback> |

### Role graph

| Role | Unique information | Unique action | Depends on | Failure impact | Transferable? |
|---|---|---|---|---|---|
| <role> | <info> | <action> | <role> | <impact> | yes/no |

### State machine

```text
SETUP
→ <STATE>
→ <STATE>
→ VULNERABILITY / RESOLUTION
→ RESET / NEXT CYCLE
→ COMPLETE
```

| State | Entry trigger | Player actions | Exit trigger | Visible feedback | Timeout/failure |
|---|---|---|---|---|---|
| <state> | <trigger> | <actions> | <trigger> | <feedback> | <failure> |

### Pressure axes

| Axis | Level | How it affects mechanics |
|---|---:|---|
| Combat | <1-5> | <effect> |
| Time | <1-5> | <effect> |
| Information | <1-5> | <effect> |
| Space | <1-5> | <effect> |
| Movement | <1-5> | <effect> |
| Resource | <1-5> | <effect> |
| Recovery scarcity | <1-5> | <effect> |

### Combat integration

<How do enemies/boss behavior materially alter mechanic execution?>

### Feedback ladder

| Scale | Correct-action feedback | Incorrect-action feedback |
|---|---|---|
| Micro | <sound/icon/animation> | <response> |
| Meso | <room/timer/buff change> | <response> |
| Macro | <phase advance> | <wipe/reset cue> |

### Failure and recovery topology

| Failure | Severity | Player-visible cause | Recovery | Reset cost |
|---|---|---|---|---|
| <mistake> | local/recoverable/phase/wipe | <cue> | <action> | <cost> |

### Boss / DPS behavior

<If applicable: signature attacks, vulnerability logic, active DPS decisions, last stand, telegraphs. Otherwise write N/A.>

### Callout / accessibility contract

- Canonical role names: <...>
- Symbol/token names: <...>
- Orientation convention: <...>
- Color-independent encoding: <...>
- Expected viewing distance: <...>
- Audio/visual redundancy: <...>
- Likely simultaneous-callout collisions: <...>

### Blind-solve experience

- First observable clue: <...>
- Likely first hypothesis: <...>
- What proves/disproves it: <...>
- Intended breakthrough: <...>
- What prevents brute-force-only solving: <...>

### Repeat-clear experience

- Known-strategy active decisions: <...>
- Potential dead time: <...>
- Role monotony risk: <...>
- How mastery reduces risk/time: <...>
- Recovery/clutch opportunities: <...>

### Relation to raid mechanic language

<teach / reinforce / recombine / twist / culminate>

### Encounter acceptance evidence

- <informed state-machine test>
- <blind playtest>
- <repeat clear>
- <reliability cases>

# 6. Raid-Level Failure and Recovery Philosophy

<Which mistakes are local, recoverable, phase-resetting, or wipes across the raid?>

# 7. Reward and Aspiration Hooks

- Raid-specific visual identity: <...>
- Reward mechanical identity: <...>
- Targeted repeat pursuit: <...>
- Prestige/challenge rewards: <...>

# 8. Accessibility and Communication Contract

- Visual readability: <...>
- Color vision independence: <...>
- Symbol/callout vocabulary: <...>
- Audio cue support: <...>
- Orientation conventions: <...>
- Teaching / sherpa affordances: <...>

# 9. Blind Playtest Plan

## Informed state-machine test

<Who, what, evidence>

## Blind team test

<No-guide conditions, capture plan, success criteria>

## Intact-team / clan test

<Real social-group conditions and observations>

## Mixed-experience teaching test

<How experienced players teach newcomers; what to capture>

# 10. Repeat-Clear Validation

- Number of repeats: <...>
- Clear time: <...>
- Dead time: <...>
- Role participation: <...>
- Communication collisions: <...>
- Wipe distribution: <...>

# 11. Technical Reliability Matrix

| Case | Expected result | Evidence |
|---|---|---|
| player dies before handoff | <recover/reset> | <test> |
| player dies during handoff | <recover/reset> | <test> |
| carrier disconnects | <recover/reset> | <test> |
| duplicate interaction | <ignored/idempotent> | <test> |
| late interaction | <defined> | <test> |
| phase change during carry | <defined> | <test> |
| join in progress | <defined/disabled> | <test> |

# 12. Challenge / Mastery Variant

<Change rules or dependencies rather than only stats.>

- New constraint: <...>
- What deeper mastery it tests: <...>
- Recovery changes: <...>
- Reward justification: <...>

# 13. Open Risks and Hypotheses

| Risk / hypothesis | Evidence needed | Owner | Status |
|---|---|---|---|
| <risk> | <playtest> | <owner> | open |

# 14. Implementation Handoff

- Authoritative mechanic state owner: <server/shared/local>
- Required encounter state/events: <...>
- Required visual/audio feedback: <...>
- Required telemetry: <...>
- Required tests: <...>
- Dependencies: <...>
