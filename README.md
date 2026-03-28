# Chain Reaction AI Bot

## Overview

This project contains a competitive AI bot designed to play the **Chain Reaction** game in a hackathon or tournament environment. The bot is optimized for speed, reliability, and strategic decision-making under strict time constraints (less than 1 second per move).

The implementation focuses on efficient game simulation, intelligent move selection, and stable performance during chain reactions.

---

## Features

* Fast decision making (< 1 second per move)
* Minimax search algorithm
* Alpha-Beta pruning optimization
* Iterative deepening search
* Efficient explosion resolution using queue-based processing
* Adaptive and aggressive gameplay behavior
* Competition-compliant function interface

---

## Function Interface (Competition Requirement)

The bot exposes the required function:

```
def get_move(state, player_id)
```

### Parameters

**state**

* A 12 x 8 board matrix
* Each cell contains a tuple:

```
(owner_id, orb_count)
```

Where:

* owner_id: 0 or 1
* orb_count: number of orbs in the cell
* Empty cell: (None, 0)

**player_id**

* The ID assigned to the bot
* Either 0 or 1

### Return Value

```
(row, col)
```

The bot returns the coordinates of the selected move.

Valid moves:

* Empty cells
* Cells already owned by the player

---

## Game Logic

The bot simulates moves by:

1. Placing an orb
2. Resolving explosions
3. Evaluating the resulting board
4. Searching future moves
5. Selecting the best move

Explosions propagate to neighboring cells when a cell reaches its critical mass.

---

## Performance Design

The bot is engineered to perform reliably within strict timing limits.

Key performance techniques:

* Reduced board overhead using optimized indexing
* Early pruning of unproductive search branches
* Move prioritization for faster evaluation
* Controlled search depth based on available time
* Efficient queue-based chain reaction handling

---

## Project Structure

```
bot.py
README.md
```

---

## Requirements

* Python 3.x
* No external libraries required

---

## Usage Example

```
move = get_move(state, player_id)
```

The returned move can be directly used by the game engine.

---

## Reliability Measures

The bot includes safeguards to ensure stable execution:

* Time limit protection
* Controlled explosion loops
* Duplicate processing prevention
* Safe move fallback

---

## Notes

This implementation is designed specifically for competitive environments where speed, correctness, and stability are critical. The code is self-contained and requires no additional dependencies.
