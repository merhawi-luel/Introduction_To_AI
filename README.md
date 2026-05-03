# BFS & DFS Search Visualizer

A Python + Pygame visualization of two foundational AI search algorithms — **Breadth-First Search (BFS)** and **Depth-First Search (DFS)** — running on an interactive maze grid. Inspired by Harvard's CS50 Introduction to AI course.

---

## What it looks like

| Color | Meaning |
|---|---|
| 🟢 Green | Start node (S) |
| 🔴 Red | Goal node (G) |
| 🔵 Blue | Frontier — cells queued to explore next |
| 🟣 Purple | Explored — already visited cells |
| 🟡 Yellow | Solution path found |
| ⬛ Dark gray | Wall / obstacle |

---

## How it works

Both algorithms share the same structure — the only difference is the data structure used for the **frontier**:

```
BFS → uses a Queue (FIFO) → explores level by level → guarantees shortest path
DFS → uses a Stack (LIFO) → dives deep first      → faster but not optimal
```

Every node tracks its **parent** — when the goal is found, the algorithm walks back through parents to reconstruct the solution path (the yellow trail).

---

## Requirements

- Python 3.7+
- pygame

Install pygame with:

```bash
pip install pygame
```

---

## Running the visualizer

```bash
python search.py
```

A window will open with the maze. Use the buttons at the bottom to control the search.

---

## Controls

| Button | Action |
|---|---|
| **BFS** | Switch to Breadth-First Search |
| **DFS** | Switch to Depth-First Search |
| **Step** | Explore one step at a time |
| **Auto** | Run the search automatically |
| **Pause** | Pause auto-run |
| **Reset** | Clear the search and start over |
| **Click a cell** | Toggle a wall on or off |

---

## Adjusting the speed

At the top of `search.py`, two values control how fast the visualization runs:

```python
FPS   = 10   # frames per second — lower is slower overall
SPEED = 1    # cells explored per frame — 1 is easiest to follow
```

Recommended settings for different paces:

| Feel | FPS | SPEED |
|---|---|---|
| Fast (default) | 30 | 8 |
| Comfortable | 15 | 2 |
| One step at a time | 10 | 1 |
| Very slow | 6 | 1 |

---

## Project structure

```
bfs-dfs-visualizer/
│
├── search.py       # main file — maze, search logic, and pygame rendering
└── README.md       # this file
```

---

## Key concepts illustrated

**State** — each cell `(row, col)` is a state in the search space.

**Frontier** — the collection of states waiting to be explored. BFS uses a queue, DFS uses a stack.

**Explored set** — states already visited, so the algorithm never revisits them.

**Parent tracking** — each state remembers where it came from. Used to trace the solution path back from goal to start once the goal is found.

**Path reconstruction** — once the goal is reached, the algorithm follows parent pointers back to the start and reverses the list to get the full solution path.

---

## Concepts from CS50 AI

This project is built on the ideas taught in Harvard's [CS50 Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/). Specifically:

- Search problems (states, actions, transitions, goal test)
- Uninformed search (BFS and DFS)
- Node and frontier data structures
- Path reconstruction via parent pointers

---

## License

MIT — free to use, modify, and share.
