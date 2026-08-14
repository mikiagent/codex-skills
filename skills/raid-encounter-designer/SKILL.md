---
name: raid-encounter-designer
description: "Design, critique, or revise cooperative raid/dungeon/endgame encounters with explicit roles, information flow, mechanics, failure/recovery, boss phases, pacing, accessibility, and blind/repeat validation. Trigger when prompts mention raid design, dungeon encounter design, raid boss mechanics, cooperative puzzle encounters, Destiny-like raids, MMO raid mechanics, or six-player endgame PvE."
metadata:
  short-description: "Design cooperative raid encounters as inspectable social systems."
---

# Raid Encounter Designer

Design cooperative endgame encounters as **information, responsibility, action, and feedback systems embedded inside combat**.

The goal is not to imitate Destiny mechanics. Use the research to extract durable design invariants: social dependency, readable responsibility, discoverable rules, satisfying mastery, fair pressure, and memorable pacing.

## Read First

| Task | Read |
|---|---|
| Designing or critiquing a raid/encounter | `references/raid-encounter-grammar.md` |
| Using Destiny as a design reference | `references/destiny-raid-design-patterns.md` |
| Producing a full design artifact | `assets/raid-design-template.md` |
| Validating a completed design artifact | `scripts/validate_raid_design.py` |

---

# Core Principle

A raid encounter is not merely:

```text
hard enemies + puzzle
```

Model it as:

```text
fantasy
+
objective
+
mechanic language
+
information graph
+
role / responsibility graph
+
action state machine
+
combat / time / spatial pressure
+
feedback ladder
+
failure + recovery topology
+
accessibility contract
+
blind-solve experience
+
repeat-clear experience
```

The most important question is:

> What social behavior does this mechanic cause the players to perform?

---

# Required Workflow

## 1. Define the fantasy and target feelings

Before inventing mechanics, state:

- player fantasy;
- encounter fantasy;
- desired emotional rhythm;
- desired cooperative feelings.

Examples of useful target feelings:

```text
shared discovery
individual accountability
controlled panic
trust during a relay
clutch recovery
mastery after repetition
spectacle under pressure
```

Do not begin from "we need an orb dunk" unless the mechanic already has a clear social purpose.

## 2. Define player count and experience target

Specify:

- intended fireteam size;
- expected prior mechanic knowledge;
- first-clear difficulty target;
- repeat-clear difficulty target;
- whether this is raid, dungeon, mission, or challenge variant.

Do not silently assume six players because Destiny uses six-player raids.

## 3. Choose a small mechanic vocabulary

Use mechanic primitives from `references/raid-encounter-grammar.md`.

Prefer a small reusable language over unrelated nouns in every room.

A raid progression may look like:

```text
teach A
→ A under pressure
→ A + B
→ twist / deliberate surprise
→ culmination
```

Novelty should be intentional rather than constant mechanic accumulation.

## 4. Draw the information graph

For every piece of required information, document:

```text
who can perceive it?
who needs it?
how does it travel?
how long is it valid?
what happens if it is wrong or late?
what confirms the interpretation?
```

Example:

```text
Observer A ──target callout──> Operator B
Operator B ──opens route──> Runner C
Runner C ──deposit result──> whole team
```

If one player can see and perform every important action, verify that the encounter intentionally wants low communication dependency.

## 5. Draw the role / responsibility graph

Each meaningful role should have at least one of:

- unique information;
- unique permission;
- unique timing responsibility;
- unique movement responsibility;
- meaningful combat-control responsibility;
- recovery responsibility.

Document dependencies and failure impact.

Avoid **spectator syndrome**: a few players perform the encounter while everyone else is generic add clear with no meaningful dependency.

Add clear is meaningful when combat control materially protects or enables mechanics.

## 6. Define the encounter state machine

Write explicit states and transitions.

Example:

```text
SETUP
→ DISCOVERY / ACQUIRE
→ ROUTE / TRANSFER
→ RESOLUTION
→ VULNERABILITY
→ RECOVERY / RESET
→ NEXT CYCLE
→ LAST STAND
→ COMPLETE
```

For each transition specify:

- trigger;
- authoritative state change;
- player-visible feedback;
- timeout;
- failure behavior.

Do not make the mechanic depend on ambiguous hidden scripting.

## 7. Add pressure deliberately

Tune separate pressure axes instead of multiplying all of them together:

- combat lethality;
- enemy density;
- time pressure;
- information complexity;
- memory burden;
- spatial separation;
- movement execution;
- role-switch frequency;
- resource pressure;
- recovery scarcity.

Combat should preferably interact with mechanic execution rather than existing as unrelated background noise.

## 8. Design a feedback ladder

A blind puzzle needs a discriminating loop:

```text
observe
→ hypothesize
→ act
→ receive feedback
→ revise
```

Provide feedback at multiple scales when appropriate:

```text
MICRO
interaction response / icon / sound

MESO
room / role / timer / boss state changes

MACRO
phase advance / vulnerability / arena transformation
```

Players do not need immediate explanations, but correct and incorrect actions must usually produce enough evidence to form better hypotheses.

## 9. Design failure and recovery topology

Explicitly classify mistakes:

```text
local penalty
recoverable role failure
phase failure
full wipe
```

For each failure define:

- cause;
- visible reason;
- recovery path;
- reset cost;
- whether another player can clutch the attempt.

Do not use full wipes as the default consequence for every small error.

## 10. Design the boss as an encounter participant

If this is a boss fight, define:

- boss fantasy;
- signature attacks;
- arena control;
- telegraphs;
- vulnerability logic;
- damage-phase behavior;
- last stand;
- interaction with the raid mechanic language.

Avoid automatically turning vulnerability into a harmless stationary DPS dummy.

For active DPS, maintain readable telegraphs and deterministic threat patterns. Difficulty must remain interpretable.

## 11. Design callouts and accessibility as an interface

Document:

- canonical role names;
- symbol/token vocabulary;
- room orientation;
- expected viewing distances;
- color-independent encoding;
- audio/visual redundancy where appropriate;
- short natural callouts;
- likely simultaneous-callout collisions.

Do not manufacture challenge from poor readability.

## 12. Design pacing across the raid

A raid is an adventure, not a row of mechanic rooms.

Use contrast:

```text
combat
→ puzzle
→ traversal
→ quiet spectacle
→ escalating encounter
→ boss
→ escape / relief
```

Traversal should have a purpose: communication, navigation, movement mastery, story, spectacle, regrouping, or danger.

## 13. Evaluate blind solve and repeat clear separately

### Blind-solve target

Ask:

- Can players form hypotheses without a guide?
- Does correct action create useful evidence?
- Is there a satisfying breakthrough?
- Is failure interpretable?

### Repeat-clear target

Ask:

- Is the known solution still fun to execute?
- Is there excessive waiting or travel?
- Are some roles boring once mystery disappears?
- Does execution mastery reduce time naturally?
- Can teams recover dynamically?

A strong Day-1 puzzle can still be a bad weekly encounter.

## 14. Design mastery/challenge variants by changing rules

Prefer challenge variants that demand deeper understanding:

- role rotation;
- constrained routing;
- synchronized execution;
- time trial;
- altered safe zones;
- new dependency edges;
- reduced recovery;
- new boss pressure.

Do not default to only more enemy health and damage.

## 15. Define validation evidence before implementation

For material designs, require:

```text
informed state-machine test
blind playtest
intact-team/clan blind test when possible
mixed-experience teaching test
repeat-clear test
accessibility/readability test
state/network reliability matrix
challenge-variant test
```

Capture wipe reasons, hypotheses, role participation, communication failures, and dead time.

---

# Output Contract

For a full raid design, use `assets/raid-design-template.md` and produce a durable artifact such as:

```text
design/raid-design.md
```

A complete result must contain:

1. fantasy and emotional targets;
2. player-count / experience assumptions;
3. raid mechanic vocabulary;
4. encounter sequence and pacing curve;
5. information graph;
6. role graph;
7. state machine;
8. pressure axes;
9. feedback ladder;
10. failure/recovery table;
11. boss/DPS behavior where applicable;
12. accessibility/callout contract;
13. blind-solve evaluation;
14. repeat-clear evaluation;
15. validation plan.

Run:

```bash
python3 skills/raid-encounter-designer/scripts/validate_raid_design.py path/to/raid-design.md
```

before declaring the design artifact structurally complete.

Structural validation does **not** prove the encounter is fun. Only playtesting can validate the requested player experience.

---

# Critique Mode

When asked to critique an existing encounter, do not merely give opinions.

Evaluate it against:

```text
SOCIAL DEPENDENCY
INFORMATION FLOW
ROLE PARTICIPATION
MECHANIC COHERENCE
FEEDBACK QUALITY
FAILURE FAIRNESS
COMBAT INTEGRATION
BOSS THREAT
PACING
ACCESSIBILITY
BLIND DISCOVERY
REPEAT MASTERY
TECHNICAL ROBUSTNESS
REWARD FIT
```

Separate:

```text
observable issue
from
hypothesized cause
from
recommended intervention
```

Example:

```text
OBSERVATION
four players spend most cycles doing generic add clear

HYPOTHESIS
information and permission graph only requires two actors

INTERVENTION
split information ownership or add meaningful protection/routing dependencies
```

---

# Anti-Patterns

Avoid unless intentionally justified:

- spectator syndrome;
- arbitrary callout tax;
- poor telegraph readability masquerading as difficulty;
- correct actions with no feedback;
- one-mistake-wipe for every error;
- boss becomes harmless during DPS;
- hard mode = stats only;
- new mechanic nouns every encounter;
- fake roles with no unique decision;
- forced waiting after the mystery is solved;
- mechanics whose network/state failure is indistinguishable from player error;
- encounter implementation before information/role/state contracts exist.

---

# Research Status

The Destiny-specific observations in `references/destiny-raid-design-patterns.md` are source-observed research, not proof that every pattern will work in every game.

Treat this Skill's workflow as a strong design hypothesis until local raid prototypes and playtests corroborate which parts deserve durable enforcement.

Do not copy Destiny-specific names, encounters, symbols, characters, locations, or proprietary content. Transfer the design invariant, not the surface implementation.
