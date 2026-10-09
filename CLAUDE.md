# Assignment 2 – Heap Go Solver

## Overview

Write a Python 3 program (`a2.py`) that solves Heap Go positions as win or loss using an optimised boolean minimax search. The program determines who wins when both players play perfectly.

## Game Constraints

| Parameter         | Range                          |
| ----------------- | ------------------------------ |
| Number of heaps   | 1 – 20                         |
| Tokens per heap   | 1 – 20                         |
| Token color `c`   | `'b'` or `'w'`                 |
| Token value `n`   | 1 – 20 (integer)               |
| Komi              | integer + 0.5, range (-100, +100) |

Resource limits: 1 thread, 1 GB memory, 1 MB tgz submission.

## Commands to Implement / Modify

### `timelimit seconds`

- `seconds` is an integer, 1 ≤ seconds ≤ 100.
- Sets the max time for all subsequent `solve` commands until changed.
- **Default time limit (before any `timelimit` command): 1 second.**

### `solve`

- Takes no arguments.
- Attempts to compute the winner from the current position assuming perfect play by both sides.
- Solving starts with the current player (`self.game.toplay`).

**Output on success:**

```
= winner [move]
```

- `winner` is `b` or `w`.
- If `toplay` wins: also output a winning move (a legal move achieving the win), written as an integer `heap_number` (0-indexed).
- If `toplay` loses: output only the winner, **no move**.

**Output on timeout:**

```
= -1
```

- Do **not** guess the result.

### `genmove` (modify existing)

1. Call the solver with the current `timelimit`.
2. If solver finds a **win** → return a winning move.
3. If solver finds a **loss** or **times out** → return a random legal move (starter code behavior).

This ensures a move is always generated so a full game can be played.

## Special Cases

- `solve` and `genmove` will **not** be called when the game is over (all heaps empty).
- `toplay` is changed by commands like `play`, `toplay`, etc.
- If multiple winning moves exist, return any one.
- The solver must work for `toplay` being either Black or White.

## Project Structure

```
assignment2/
├── a2.py                            # Main file – implement here
├── assignment2-public-tests.txt     # Public test cases
└── a2test.py                        # Test runner
```

Run tests with:

```bash
python3 a2test.py a2.py assignment2-public-tests.txt
```

## Time Management

- The solver **must** stay within the time limit.
- Use `time.time()` or similar (see "Measuring Time in Python" resource).
- Returning `= -1` honestly on timeout is better than guessing — guessing loses marks.

## Optimisation Notes

Possible improvements (from lecture slides / preview slides):

- Transposition table / memoisation
- Alpha-beta style pruning (adapted for boolean minimax)
- Move ordering
- Symmetry detection
- Any other correct optimisation

**Correctness is paramount** — an incorrect optimisation that produces wrong results will lose marks.

## Marking (5 + 2 bonus)

| Marks | Criteria |
| ----- | -------- |
| 1     | `test.log` on a standard Linux undergrad machine + `readme.txt` |
| 1     | Passing public test cases |
| 1     | Code quality |
| 2     | Passing private test cases |
| +2    | Bonus for exceptional solvers (rare, instructor discretion) |

## Submission

- File: `assignment2.tgz`
- Keep `a2.py` name and location as in starter code.
- Include `test.log` and `readme.txt`.
- May add extra `.py` files in the same directory.
- Do not add directories or rename the `assignment2` directory.