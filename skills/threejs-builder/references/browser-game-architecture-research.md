# Browser Game Architecture Research Reference

Status: `SOURCE-OBSERVED` + `TRANSFER-CANDIDATE`
Date: 2026-08-14

Purpose: give `threejs-builder` a durable cross-repository architecture reference for browser games that go beyond simple visual scenes.

This file is research guidance, not mandatory production behavior. The source projects were inspected at code level but have not yet been reproduced and benchmarked in our environment.

Primary sources studied:

- `mshumer/Claude-of-Duty`
- `ill-inc/biomes-game`
- `MavonEngine/Core`
- `iErcann/NotBlox`
- `swift502/Sketchbook`
- `mohsenheydari/three-fps`
- `tech-leads-club/nj-mmo`

For detailed NJ MMO findings, also read `nj-mmo-browser-mmo-patterns.md`.

# 1. Separate simulation from presentation

Claude-of-Duty provides a clear source example of a fixed deterministic gameplay update separated from render-rate `update`/`lateUpdate` presentation.

Transfer candidate:

```text
FIXED / AUTHORITATIVE SIMULATION
movement rules
ballistics
cooldowns
hit rules

RENDER-RATE PRESENTATION
camera response
viewmodel
particles
audio
HUD
```

The exact source update frequency is not a recommendation. Measure the appropriate rate for the target game and server budget.

# 2. Game feel is not one variable

Claude-of-Duty separates movement, camera recoil, viewmodel kick, camera trauma, weapon accuracy, animation, VFX, and audio.

Useful invariant:

```text
gameplay aim behavior
≠
viewmodel presentation
≠
camera impact feedback
```

For FPS work, avoid a single catch-all `recoilAmount` or “juice” value when independent layers need independent tuning and validation.

# 3. Conventional locomotion can remain explicit

Sketchbook is a readable reference for:

- camera-relative movement intent;
- target velocity vs spring-smoothed actual velocity;
- desired orientation vs spring-smoothed facing;
- capsule/ground physics;
- explicit locomotion state classes;
- state-driven animation;
- physical-state-informed landing transitions.

Transfer candidate:

```text
input
→ desired motion
→ response/smoothing
→ physics
→ semantic state
→ animation
→ render
```

This separation is useful even if Rapier replaces Sketchbook's Cannon.js physics.

# 4. ECS replication can be simple and inspectable

NotBlox uses shared network components with dirty flags. The server serializes changed components, sends snapshots, the client reconstructs/updates ECS components, and separate visual systems apply those values to Three.js meshes.

Transfer candidate:

```text
server semantic component
→ serialization
→ network
→ client semantic component
→ renderer adapter
```

This is cleaner than replicating renderer objects.

Important limitation: NotBlox explicitly documents no client-side prediction. Its position lerping should not be described as full snapshot interpolation or reconciliation.

# 5. Distinguish five networking concepts

Do not collapse these concepts:

```text
latest-state visual smoothing
≠
snapshot-buffer interpolation
≠
client-side prediction
≠
server reconciliation
≠
hitscan lag compensation
```

A future multiplayer reference or Skill should name which layer it actually implements.

# 6. MavonEngine has useful prediction scaffolding, not yet complete proof

Source-observed in the multiplayer template:

- Three.js + Rapier shared/base simulation concepts;
- server-authoritative physics;
- client commands with monotonically increasing sequence IDs;
- local command queue;
- server command buffer;
- replicated `lastProcessedSequenceId`;
- distance-based relevance;
- latency/bandwidth/CPU instrumentation.

The inspected client correction path applies authoritative state and drops acknowledged commands. We did not locate a complete replay loop that re-simulates the remaining unacknowledged inputs over the corrected state.

Therefore teach the source as:

```text
shared prediction-capable simulation
+
sequence acknowledgement
+
authoritative correction scaffolding
```

not as locally proven complete FPS reconciliation.

Full reconciliation candidate:

```text
server snapshot at ack N
→ reset predicted state
→ discard commands <= N
→ replay N+1...
```

# 7. Interest management is a first-class system

MavonEngine filters state by distance per connected player. Biomes goes further by giving client synchronization its own service tier backed by world replicas and spatial relevance.

Transfer progression:

```text
small prototype
→ per-instance relevance radius

larger system
→ spatial interest model

only after scale pressure
→ dedicated sync/gateway tier
```

Do not broadcast every entity forever merely because it is simple at five entities.

# 8. Bounded instances first; distributed world services later

NJ MMO is a useful reference for bounded authoritative room/instance architecture.

Biomes is the stronger reference for a larger persistent world:

```text
transactional world authority
→ change stream
→ service-local replicas
→ logic / NPC / environment workers
→ client sync tier
```

Biomes also separates static content definitions from dynamic ECS world state and shards expensive NPC simulation across workers.

Transfer rule:

> Design an MVP around bounded authoritative instances, but keep persistence, synchronization, and expensive simulation boundaries explicit enough to split later if measurements require it.

Do not reproduce Biomes's service count for an MVP.

# 9. Procedural generation should encode semantics

Claude-of-Duty's procedural architecture uses meaningful modules and states, not only randomized dimensions/colors.

Transfer candidate:

```text
authored grammar
→ meaningful modules
→ seeded variation
→ deterministic geometry
→ collision/runtime semantics
```

A good procedural test should include:

- same seed → same output;
- representative seed sweep;
- bounds/performance validation;
- perceptual inspection;
- no impossible overlaps/runtime-invalid states.

# 10. Keep the first-person viewmodel separate where appropriate

Claude-of-Duty renders world and first-person weapon/viewmodel separately.

Transfer candidate for FPS work:

```text
world scene/camera
+
viewmodel scene/camera
→ composite final image
```

Potential benefits include preventing weapon/world clipping and allowing presentation-specific FOV/depth behavior. Validate shadows, lighting, post-processing, and compositing before adoption.

# 11. Performance evidence needs tail metrics

Claude-of-Duty records a case where seemingly healthy median/static measurements hid severe gameplay stalls caused by lazy WebGL program compilation.

For real-time game work, prefer a gameplay representative measurement set:

```text
p50 frame time
p95
p99
worst frame
long-frame count
shader/program creation during play
renderer.info metrics
```

Average FPS alone is insufficient when large hitches dominate perceived quality.

# 12. Deterministic visual fixtures require isolated state

A source-observed Claude-of-Duty failure involved visual captures sharing a browser page, allowing particles, decals, exposure, and other temporal state to leak between shots.

Transfer candidate fixture:

```text
fresh page/process when state isolation matters
fixed seed
fixed engine time / frame budget
fixed camera
fixed gameplay state
fixed viewport / DPR
explicit asset-ready signal
```

For advanced effects, also test no-post baselines, diagnostic views, distance envelope, temporal stability, and parameter/seed extremes.

# 13. Small readable repos remain valuable

`three-fps` is not a modern architecture template, but it remains useful educationally because the whole boot/update structure is visible:

```text
load assets
→ renderer
→ physics
→ entity manager
→ player/NPC components
→ requestAnimationFrame
→ physics step
→ entity update
→ render
```

Use small references to understand ownership before studying distributed systems.

# 14. Recommended experiment order

Before turning these candidates into stronger Three.js builder behavior:

1. deterministic fixed-step local FPS controller;
2. Rapier movement lab;
3. replicated ECS/server-authority demo;
4. prediction + acknowledgement + replay reconciliation lab;
5. remote snapshot-buffer interpolation;
6. hitscan/projectile latency lab;
7. relevance/bandwidth benchmark;
8. deterministic browser capture harness;
9. gameplay frame-time tail profiler;
10. only after scale pressure, transactional world/replica/sync prototypes.

# 15. Non-conclusions

This research does not establish that:

- one networking library is universally best;
- Three.js alone is an MMO engine;
- MavonEngine currently solves full FPS reconciliation;
- NotBlox interpolation substitutes for prediction;
- Biomes's distributed topology is appropriate for an MVP;
- Claude-of-Duty's custom physics or exact fixed frequency should be copied;
- procedural-only assets are the right final art strategy for every project.

Research tells us what to test next. Local evidence decides what becomes durable guidance.