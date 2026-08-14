# Destiny Raid Design Patterns

Status: `SOURCE-OBSERVED` + `PLAYER-EXPERT-OBSERVED` + `TRANSFER-CANDIDATE`

Purpose: preserve reusable design lessons from Destiny/Destiny 2 raid research for the `raid-encounter-designer` Skill.

This is not permission to copy Destiny content. Transfer design invariants, not encounter names, lore, symbols, layouts, characters, or proprietary assets.

The full project-level study lives in `mikiagent/vibe-coding/research/destiny-2-raid-design-study.md`.

---

# 1. Social feeling is the target

Industry reporting on Luke Smith's raid-design comments describes the goal as creating feelings of responsibility, accountability, communication, and visible teammate impact rather than directly transplanting MMO mechanics into a shooter.

**Transfer:** start with desired cooperative emotion, then choose mechanics.

```text
shared discovery
individual accountability
visible teammate contribution
trust under pressure
clutch recovery
```

---

# 2. Hidden information creates real communication

Bungie's Deep Stone Crypt retrospective explicitly calls hidden-information mechanics a tool for enforcing coordination and communication.

Pattern:

```text
A sees information
B has permission to act
A and B must communicate
team sees result
```

**Transfer:** write an information graph. Do not rely on generic instructions such as "players must communicate."

---

# 3. Roles compress responsibility into language

Deep Stone Crypt's augment roles demonstrate how role names can imply information/action permissions and can transfer between players.

**Transfer:** roles should own unique information, permission, timing, movement, combat-control, or recovery decisions.

Role transfer is a cheap way to add new execution pressure without introducing a new mechanic noun.

---

# 4. The raid teaches a language

Deep Stone Crypt repeatedly develops role/terminal/core mechanics and culminates by combining learned mechanics. Vow repeatedly uses a glyph vocabulary. Root mostly reuses node-linking, with Macrocosm becoming memorable partly because it deliberately breaks the established pattern.

**Transfer:** teach → reinforce → recombine → twist → culminate.

Do not confuse coherence with total uniformity.

---

# 5. Blind discovery and weekly mastery must both work

Deep Stone Crypt designers explicitly describe balancing the blind launch experience with fun repeat execution once the strategy is known.

**Transfer:** validate two products:

```text
BLIND
Can a team form and test hypotheses?

REPEAT
Is the solved encounter still enjoyable rather than bureaucratic?
```

A long mysterious process can become terrible farm content after the mystery disappears.

---

# 6. "Aha" moments require feedback

Bungie wants strategy to unfold across attempts, with breakthroughs when teams correctly understand the rule.

Salvation's Edge World First players described Verity as difficult partly because many actions gave limited feedback, while the first hard confirmation that a change mattered was a major breakthrough.

**Transfer:** a blind puzzle needs evidence that lets teams discriminate hypotheses.

```text
observe
→ hypothesize
→ act
→ feedback
→ revise
```

Mystery is not the same as absence of information.

---

# 7. Participation matters

Salvation's Edge World First players explicitly said they enjoy encounters where each player has an opportunity to shine and participate.

**Transfer:** map role participation and avoid spectator syndrome.

Generic add clear is a meaningful role only when combat control materially enables mechanics.

---

# 8. Active bosses can preserve challenge during DPS

Rhulk and the Witness demonstrate vulnerability phases where the boss remains a spatial threat.

Salvation's Edge World First players strongly praised the Witness damage phase for requiring movement while maintaining damage output.

**Transfer:** ask what decisions remain during vulnerability.

Avoid automatically making the boss harmless when the damage window starts.

Readability remains mandatory: active threat should be telegraphed, not erratic noise.

---

# 9. Pacing contrast produces memorable peaks

Deep Stone Crypt's spacewalk intentionally slows the experience after Atraks so players can absorb the environment and music before the raid escalates again.

**Transfer:** raid pacing can include combat, puzzle, traversal, quiet spectacle, chase, boss, and relief.

Maximum intensity at all times flattens perceived intensity.

---

# 10. Spectacle works best when embodied

Deep Stone Crypt's launch to orbit and station crash happen as part of player-controlled experience rather than only through passive cinematics.

**Transfer:** let players remain responsible while the world changes around them.

```text
arena moves
world transforms
boss destroys space
players travel physically
```

---

# 11. Environment and mechanic should support the same fantasy

The Deep Stone Crypt retrospective describes early collaboration between design, narrative, art, technical design, audio, testing, and production. Mechanics, locations, and story beats were built to reinforce one another.

**Transfer:** every encounter spec should answer:

> Why does this mechanic make sense in this place and in this story?

---

# 12. Callouts are interface design

Vow of the Disciple uses a large glyph language and gives those glyphs canonical names, reducing arbitrary naming variance across fireteams.

Player accessibility reports also show that symbol contrast, size, and distance readability can still become problems.

**Transfer:** communication difficulty and cue legibility are independent axes.

Validate:

- short names
- distinct silhouettes
- color-independent cues
- orientation consistency
- expected viewing distance
- audio/visual redundancy where appropriate

---

# 13. Challenge should change rules, not only stats

Bungie has repeatedly explored raid difficulty through Contest Mode, challenge conditions, weekly modifiers, and later Feats / challenge customization.

Older Prestige planning explicitly moved away from a design that would have relied primarily on enemies being more lethal and harder to kill.

**Transfer:** challenge variants should ideally require deeper encounter understanding.

Examples:

- forced role rotation
- constrained routing
- synchronized actions
- fewer recovery opportunities
- altered boss pressure
- time trials

---

# 14. Technical failure destroys puzzle trust

Raid mechanics often involve multi-room state, transfers, objects, timers, death/revive, and network synchronization. A bug can cause an entire attempt to fail and can mislead a blind team about the intended rule.

The RAD team's public discussions of dungeon/raid technical issues and community raid bug reports make this especially important.

**Transfer:** reliability is an encounter acceptance criterion.

Test role/object ownership around death, disconnects, phase changes, duplicate interaction, and latency.

---

# 15. Contest challenge needs a trustworthy difficulty contract

Contest Mode is intended to challenge teamwork, puzzle solving, loadouts, and execution under normalized combat disadvantage.

The 2025 Desert Perpetual launch generated reports of harsher-than-advertised power deltas, inconsistent rally restoration, very high damage checks, and poor rewards. Bungie publicly investigated these concerns.

**Transfer:** a DPS check is valid only if power rules, ammo/resource systems, and encounter state are trustworthy.

Players need to know whether failure means:

```text
strategy problem
execution problem
build problem
or broken system
```

---

# 16. High coordination cost needs strong aspiration

Bungie treats raids as aspirational content with exclusive weapons, armor, and Exotics. Deep Stone Crypt introduced Spoils/caches that increased agency in repeated raid reward pursuit.

**Transfer:** high social friction should be justified by strong reward identity and repeat-pursuit agency.

Raid rewards should feel connected to the activity rather than generic drops from a harder source.

---

# 17. World First changes encounter design incentives

Raid races are spectator events as well as gameplay.

World First interviews show the importance of:

- strong team protocols
- puzzle solving
- recognizable breakthroughs
- iconic boss attacks
- environmental scale
- memorable encounter variety

**Transfer:** aspirational encounters benefit from visually legible milestones and moments worth retelling.

---

# 18. Playtest with real social groups

Bungie's GDC user-research overview explicitly mentions using pre-existing gamer clans to test hardcore endgame raids.

**Transfer:** do not validate social mechanics only with isolated designers who already know the solution.

Use intact groups so real communication habits, leadership, vocabulary, and role specialization emerge.

---

# 19. Representative success patterns

These are design-pattern observations, not templates to copy.

## Split knowledge / split permission

Useful when the desired feeling is trust and communication.

## Relay / rotating responsibility

Useful when the desired feeling is shared accountability and recovery.

## Reused language under new context

Useful for mastery and coherence.

## Deliberate mechanic departure

Useful for surprise after expectations have been established.

## Active boss threat during damage

Useful when the boss should feel like an opponent rather than a puzzle reward.

## Quiet traversal after high pressure

Useful for contrast, scale, and memory formation.

## Culmination encounter

Combine previously learned language rather than explaining a completely new system at the climax.

---

# 20. Representative failure patterns

## Spectator syndrome

Too few players own meaningful mechanic decisions.

## Callout tax

Difficulty comes primarily from arbitrary vocabulary rather than reasoning or execution.

## Opaque feedback

Blind teams cannot distinguish correct from irrelevant actions.

## Unfair wipe bugs

State/network errors are indistinguishable from player mistakes.

## Stat-only challenge

Higher health/damage dominates mechanical mastery.

## Static DPS

The boss stops being an encounter participant during vulnerability.

## Repeat bureaucracy

Once solved, the encounter has too much waiting, travel, or low-agency procedure.

---

# Sources

Primary sources consulted in the project-level research include:

- Bungie — `Tales From the (Deep Stone) Crypt` (2021)
- Bungie — `Developer Insight - Raids and Dungeons` (2024)
- Bungie — Salvation's Edge World First interview / TWID 2024-06-13
- Bungie — Root of Nightmares World First interview (2023)
- Bungie / GDC — `User Research on Destiny` (2015)
- Bungie — Prestige raid redesign notes (2018)
- Bungie — Contest Mode communications

Secondary sources include Game Developer's reporting on Luke Smith's WoW/raid design comments and GameSpot's mechanical documentation of Vow of the Disciple.

All patterns remain transferable hypotheses until tested in our own prototypes.
