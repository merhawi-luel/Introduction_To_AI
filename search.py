import pygame
import sys
from collections import deque

# ── Config ────────────────────────────────────────────────────────────────────
ROWS, COLS = 15, 20
CELL      = 40
WIDTH     = COLS * CELL
HEIGHT    = ROWS * CELL + 80          # extra bar at bottom for controls
FPS       = 1
SPEED     = 1                        # cells explored per frame

# ── Colors ────────────────────────────────────────────────────────────────────
BG         = (15,  23,  42)
WALL       = (55,  65,  81)
EMPTY      = (30,  41,  59)
START_C    = (34, 197,  94)
GOAL_C     = (239, 68,  68)
FRONTIER_C = (59, 130, 246)
EXPLORED_C = (124, 58, 237)
PATH_C     = (251, 191,  36)
TEXT_C     = (226, 232, 240)
BTN_C      = (30,  41,  59)
BTN_HOV    = (51,  65,  85)
BTN_ACT    = (30,  64, 175)

# ── Maze (0=empty, 1=wall) ────────────────────────────────────────────────────
MAZE = [
    [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [0,1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,1,1,0],
    [0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,0],
    [0,0,0,0,1,0,0,0,1,0,0,0,1,1,1,0,1,1,1,0],
    [0,1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,0,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0],
    [0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0],
    [1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0],
    [0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],
    [0,1,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,0],
    [0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
    [0,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,0,0,0],
]
# make sure start and goal are open
MAZE[0][0] = 0
MAZE[ROWS-1][COLS-1] = 0

START = (0, 0)
GOAL  = (ROWS-1, COLS-1)

# ── Search state ──────────────────────────────────────────────────────────────
def make_search(algo):
    """Return initial search state dict."""
    return {
        "algo":     algo,
        "frontier": deque([START]) if algo == "bfs" else [START],
        "explored": set(),
        "parent":   {START: None},
        "path":     [],
        "done":     False,
        "found":    False,
        "steps":    0,
    }

def neighbors(r, c):
    for dr, dc in [(-1,0),(0,1),(1,0),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
            yield (nr, nc)

def step_search(state):
    """Advance search by one node. Mutates state in place."""
    if state["done"]:
        return
    frontier = state["frontier"]
    if not frontier:
        state["done"] = True
        return
    # BFS pops from left (queue), DFS pops from right (stack)
    node = frontier.popleft() if state["algo"] == "bfs" else frontier.pop()
    if node in state["explored"]:
        return
    state["explored"].add(node)
    state["steps"] += 1
    if node == GOAL:
        state["done"] = True
        state["found"] = True
        # reconstruct path
        cur = GOAL
        while cur is not None:
            state["path"].append(cur)
            cur = state["parent"][cur]
        state["path"].reverse()
        return
    for nb in neighbors(*node):
        if nb not in state["explored"] and nb not in state["parent"]:
            state["parent"][nb] = node
            frontier.append(nb)

# ── Drawing ───────────────────────────────────────────────────────────────────
def draw_cell(surface, r, c, color, alpha=255):
    rect = pygame.Rect(c*CELL+2, r*CELL+2, CELL-4, CELL-4)
    if alpha < 255:
        s = pygame.Surface((CELL-4, CELL-4), pygame.SRCALPHA)
        s.fill((*color, alpha))
        surface.blit(s, rect.topleft)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=4)

def draw_text_center(surface, font, text, color, cx, cy):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=(cx, cy)))

def draw_button(surface, font, label, rect, active=False, hovered=False):
    color = BTN_ACT if active else (BTN_HOV if hovered else BTN_C)
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (71,85,105), rect, width=1, border_radius=6)
    draw_text_center(surface, font, label, TEXT_C, rect.centerx, rect.centery)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BFS vs DFS Visualizer")
    clock  = pygame.time.Clock()
    font   = pygame.font.SysFont("monospace", 13)
    sfont  = pygame.font.SysFont("monospace", 11)

    # Button rects (bottom bar)
    BAR_Y = ROWS * CELL + 10
    btn_bfs   = pygame.Rect(10,  BAR_Y, 80, 30)
    btn_dfs   = pygame.Rect(100, BAR_Y, 80, 30)
    btn_step  = pygame.Rect(200, BAR_Y, 80, 30)
    btn_auto  = pygame.Rect(290, BAR_Y, 90, 30)
    btn_reset = pygame.Rect(390, BAR_Y, 80, 30)

    algo    = "bfs"
    state   = make_search(algo)
    auto    = False
    running = True

    while running:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()

        # ── events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_bfs.collidepoint(mx, my):
                    algo = "bfs"; state = make_search(algo); auto = False
                elif btn_dfs.collidepoint(mx, my):
                    algo = "dfs"; state = make_search(algo); auto = False
                elif btn_step.collidepoint(mx, my):
                    auto = False
                    for _ in range(SPEED):
                        step_search(state)
                elif btn_auto.collidepoint(mx, my):
                    auto = not auto
                elif btn_reset.collidepoint(mx, my):
                    state = make_search(algo); auto = False
                else:
                    # toggle wall on click
                    if my < ROWS * CELL:
                        r, c = my // CELL, mx // CELL
                        if (r, c) != START and (r, c) != GOAL:
                            MAZE[r][c] = 0 if MAZE[r][c] == 1 else 1
                            state = make_search(algo); auto = False

        # ── auto-step ─────────────────────────────────────────────────────────
        if auto and not state["done"]:
            for _ in range(SPEED):
                step_search(state)

        # ── draw background ───────────────────────────────────────────────────
        screen.fill(BG)

        # frontier set for fast lookup
        frontier_set = set(state["frontier"])

        # ── draw cells ────────────────────────────────────────────────────────
        for r in range(ROWS):
            for c in range(COLS):
                pos = (r, c)
                if MAZE[r][c] == 1:
                    color = WALL
                elif pos == START:
                    color = START_C
                elif pos == GOAL:
                    color = GOAL_C
                elif state["found"] and pos in state["path"]:
                    color = PATH_C
                elif pos in state["explored"]:
                    color = EXPLORED_C
                elif pos in frontier_set:
                    color = FRONTIER_C
                else:
                    color = EMPTY
                draw_cell(screen, r, c, color)

        # labels on start / goal
        draw_text_center(screen, font, "S", (255,255,255), CELL//2, CELL//2)
        draw_text_center(screen, font, "G", (255,255,255),
                         (COLS-1)*CELL + CELL//2, (ROWS-1)*CELL + CELL//2)

        # ── status bar ────────────────────────────────────────────────────────
        hov = lambda r: r.collidepoint(mx, my)
        draw_button(screen, font, "BFS",   btn_bfs,   active=(algo=="bfs"),  hovered=hov(btn_bfs))
        draw_button(screen, font, "DFS",   btn_dfs,   active=(algo=="dfs"),  hovered=hov(btn_dfs))
        draw_button(screen, font, "Step",  btn_step,  hovered=hov(btn_step))
        draw_button(screen, font, "Auto" if not auto else "Pause", btn_auto, hovered=hov(btn_auto))
        draw_button(screen, font, "Reset", btn_reset, hovered=hov(btn_reset))

        # stats
        fsize  = len(state["frontier"])
        esize  = len(state["explored"])
        psize  = len(state["path"])
        status = (f"Path: {psize} steps" if state["found"]
                  else ("No path!" if state["done"] else
                        f"Frontier: {fsize}  Explored: {esize}"))
        algo_label = f"{algo.upper()} ({'Queue' if algo=='bfs' else 'Stack'})"
        draw_text_center(screen, sfont, f"{algo_label}   |   {status}",
                         TEXT_C, WIDTH//2 + 100, BAR_Y + 44)

        # legend
        legend = [("Start", START_C), ("Goal", GOAL_C),
                  ("Frontier", FRONTIER_C), ("Explored", EXPLORED_C), ("Path", PATH_C)]
        lx = 10
        for label, col in legend:
            pygame.draw.rect(screen, col, (lx, BAR_Y+48, 12, 12), border_radius=2)
            ts = sfont.render(label, True, TEXT_C)
            screen.blit(ts, (lx+16, BAR_Y+47))
            lx += ts.get_width() + 32

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
