# Raid Encounter Grammar

Purpose: provide a reusable vocabulary for designing cooperative endgame encounters without depending on any single game or IP.

## 1. Encounter equation

```text
ENCOUNTER =
fantasy
+ objective
+ mechanic primitives
+ information graph
+ role graph
+ state machine
+ pressure
+ feedback
+ failure/recovery
+ combat integration
+ accessibility
+ mastery/replay
```

A mechanic is useful when it changes player decisions or social behavior, not merely because it looks novel.

---

# 2. Mechanic primitives

## Information primitives

- observe hidden state
- identify target
- compare views
- call symbol / number / direction
- remember sequence
- infer rule from feedback
- track timer/status
- distinguish decoy/original

## Permission primitives

- role grants interaction
- buff grants visibility
- object grants ability
- location grants action
- temporary immunity
- temporary vulnerability

## Transfer primitives

- pass role
- pass object
- relay buff
- swap positions
- escort carrier
- deposit / retrieve
- cleanse / convert

## Spatial primitives

- split fireteam
- reunite fireteam
- parallel rooms
- mirrored rooms
- rotating safe zones
- moving platforms
- route planning
- chase / escape
- line-of-sight dependency

## Timing primitives

- synchronized action
- ordered sequence
- alternating window
- race timer
- periodic hazard
- enrage
- last stand
- cadence / rhythm

## Combat primitives

- defend mechanic user
- priority target unlocks progress
- aggro / gaze manipulation
- interrupt
- moving damage phase
- add pressure changes with phase
- resource competition
- target-selection puzzle

## Failure primitives

- local penalty
- role lockout
- object loss
- rescue requirement
- phase reset
- wipe

Use the fewest primitives that create the desired behavior.

---

# 3. Information graph

Represent information flow explicitly.

Example:

```text
Scanner
  sees target index
      │
      ▼
Caller
  translates to room language
      │
      ▼
Operator
  performs authorized interaction
      │
      ▼
Runner
  moves resulting object
```

For each edge record:

- source
- destination
- vocabulary
- latency budget
- validity duration
- acknowledgement
- failure consequence

A raid's communication difficulty can often be understood by the number and timing of these edges.

---

# 4. Role graph

A role should own at least one meaningful responsibility.

```text
ROLE
├ unique information
├ unique permission
├ unique timing
├ unique movement
├ combat-control responsibility
└ recovery responsibility
```

Useful role properties:

- transferable vs fixed
- visible vs hidden
- simultaneous vs sequential
- mandatory vs optional
- high-frequency vs burst responsibility

### Spectator check

Ask:

> If this player were replaced by an aim bot that kills normal enemies, would the cooperative mechanic still work unchanged?

If yes for most of the raid, that player's participation may be too shallow.

---

# 5. Mechanic-language progression

Useful progression patterns:

```text
INTRODUCE
A

REINFORCE
A under pressure

RECOMBINE
A + role split

EXPAND
A + B

TWIST
known rules in a new context

CULMINATE
learned language + highest pressure
```

A deliberate unrelated encounter can provide surprise, but it should be a conscious pacing/design decision.

---

# 6. Pressure matrix

Tune pressure axes independently.

| Axis | Low | High |
|---|---|---|
| Combat | forgiving enemies | lethal priority threats |
| Density | sparse | continuous crowd pressure |
| Time | generous | seconds matter |
| Information | one obvious state | multiple distributed states |
| Memory | persistent cues | temporary sequences |
| Space | one room | separated/moving regions |
| Movement | stationary | precision traversal while solving |
| Roles | fixed/simple | frequent transfer/rotation |
| Resources | abundant | ammo/ability competition |
| Recovery | easy | scarce revives / hard reset |

Do not maximize every axis at once unless that overload is the explicit final challenge.

---

# 7. Feedback ladder

A blind encounter needs discriminating evidence.

## Micro feedback

- interaction animation
- click / tone
- symbol change
- indicator light
- buff text

## Meso feedback

- door opens
- timer changes
- arena object moves
- boss shield changes
- role becomes available

## Macro feedback

- phase transition
- vulnerability
- arena transformation
- wipe prevented
- completion

### Feedback quality test

A good cue does not need to explain the rule, but it should help players distinguish:

```text
that action mattered
vs
nothing happened
```

---

# 8. Failure topology

Design mistakes at several scales.

## Local penalty

Examples:

- lose time
- spawn threat
- player takes damage
- short lockout

## Recoverable role failure

Examples:

- object drops
- role transfers
- teammate must rescue
- position must be recovered

## Phase failure

Examples:

- damage window lost
- cycle reset
- resource penalty

## Full wipe

Reserve for truly unrecoverable or intentionally high-stakes states.

### Recovery is gameplay

Clutch recovery can be as memorable as perfect execution. Do not remove it accidentally.

---

# 9. Boss grammar

A boss encounter can be broken into:

```text
THREAT
what the boss actively does

CONTROL
how the team creates opportunity

VULNERABILITY
why damage becomes possible

DPS DECISIONS
what remains interactive while damaging

RESET
how the fight returns to mechanic state

LAST STAND
how the ending changes tempo
```

Avoid a boss whose only unique property is a large health pool.

### Active-DPS options

- telegraphed movement attacks
- shifting safe zones
- mobile weak points
- interrupt targets
- rotating formation requirements
- boss pursuit
- timed role actions during damage

Readability is mandatory. Random-looking movement is not automatically skillful pressure.

---

# 10. Pacing grammar

A full raid should have an emotional curve.

Possible beat types:

- threshold / entrance
- environmental survival
- mechanic introduction
- boss gatekeeper
- traversal
- puzzle
- chase
- quiet spectacle
- escalating multi-role encounter
- final boss
- escape / aftermath

Contrast creates intensity.

---

# 11. Callout design

Treat communication vocabulary as UI/API design.

Good callouts are:

- short
- distinct
- orientation-stable
- visually grounded
- hard to confuse under audio pressure

For larger symbol sets, provide canonical names where possible.

Avoid making color the sole identifier.

### Communication collision test

Map moments when more than one player must speak simultaneously.

If several critical messages compete at the same instant, either that is deliberate coordination pressure or a communication-design defect.

---

# 12. Blind vs repeat design

## Blind solve

Success means:

- teams can discover the rule from evidence
- false hypotheses can be disproven
- breakthroughs feel meaningful

## Repeat clear

Success means:

- known solution remains active
- little forced dead time
- roles still make decisions
- clean execution meaningfully reduces time/risk

Test both independently.

---

# 13. Difficulty without stat inflation

Challenge variants can change:

- route constraints
- role rotation
- interaction order
- simultaneous execution
- safe-zone rules
- number of recoveries
- boss pressure
- encounter timer

Stats can be one axis, not the entire design.

---

# 14. Technical reliability matrix

Raid mechanics are especially vulnerable to state/network edge cases.

Test:

```text
player dies before role transfer
player dies during role transfer
carrier dies
carrier disconnects
interaction repeats
interaction is late
phase changes during carry
revive happens during transition
wrong role interacts
join-in-progress occurs
all players change region simultaneously
```

Every result should be either recoverable or deterministically fail with understandable feedback.

---

# 15. Playtest evidence

Capture:

- blind hypothesis timeline
- wipe causes
- unclear failures
- role actions
- idle time
- callout collisions
- recoveries
- known-strategy clear time
- repeated waiting
- combat-vs-mechanic deaths

Use evidence to revise the smallest owning layer:

```text
cue
role
state transition
combat pressure
arena layout
failure rule
```

Do not redesign the entire encounter because one cue is unreadable.
