# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Games

Open files directly in a browser — no build step, no server required:

```bash
open game.html    # top-down shooter
open index.html   # tic-tac-toe
```

## Git & GitHub Workflow

**Commit and push after every meaningful unit of work** — do not batch up multiple features or fixes into one commit. The goal is that GitHub always reflects the latest working state so nothing is ever lost and any change can be reverted cleanly.

Rules to follow on every task:
- Commit locally and push to `https://github.com/gmmacfar/ClaudeCodeTest` (`main` branch) as work progresses, not just at the end.
- Write clean, specific commit messages that describe *what changed and why* (e.g. `"Add screen shake on player damage"` not `"update game"`).
- If a task involves multiple logical steps (e.g. add a feature, then tweak balance), make a separate commit for each step.
- Never leave the repo in a state where local commits haven't been pushed.

## Project Structure

- **`game.html`** — self-contained retro top-down shooter (800×600 Canvas)
- **`index.html`** — self-contained tic-tac-toe game

Each file is fully standalone: HTML + CSS + JS in one file, no external dependencies, no assets.

## game.html Architecture

All game logic lives in a single `<script>` block. Key globals:

- `state` — game state machine: `menu` → `playing` → `level-clear` → `playing` → `game-over`
- `player`, `enemies[]`, `bullets[]`, `deathRings[]` — live entity arrays, reset each level via `setupLevel()`
- `ENEMY_DEFS` — stat definitions (hp, speed, color, size, score) for the 4 types: `grunt`, `rusher`, `flanker`, `tank`
- `LEVEL_DEFS[1..5]` — enemy composition arrays per level (index 0 is unused)
- `spawnQueue[]` — shuffled list of enemy types to drip-spawn during a level; level ends when both `enemies` and `spawnQueue` are empty

**Game loop** (`loop()` via `requestAnimationFrame`):
1. `update()` — input → move player → spawn from queue → move enemies → move bullets → collision detection → level-complete check
2. `render()` — clear → background grid → death rings → bullets → enemies → player → HUD → state overlays

**Sprites** are drawn purely with `ctx.fillRect` pixel art (no images). Each enemy type has a distinct `drawEnemy()` branch. Player gun arm rotates via `ctx.rotate(player.angle)` inside a `ctx.save/restore`.

**Collision model**: circle–circle using Euclidean distance. Bullet radius uses `enemy.size * 0.7`; contact damage uses `enemy.size * 0.6 + player.radius * 0.6`. Player has a 60-frame invincibility window after taking damage.

**Difficulty scaling**: enemy speed multiplied by `1 + (currentLevel - 1) * 0.08` at spawn time. Spawn interval decreases with level: `Math.max(20, 60 - currentLevel * 5)` frames.
