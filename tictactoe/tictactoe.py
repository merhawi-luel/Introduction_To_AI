import pygame
import sys
import math
import time

# ── Init ──────────────────────────────────────────────────────────────────────
pygame.init()

W, H     = 520, 620
GRID_OFF = 80          # top offset for grid
CELL     = 120         # cell size
GAP      = 12          # inner padding for X/O

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tic-Tac-Toe  |  You vs AI")
clock  = pygame.time.Clock()

# ── Fonts ─────────────────────────────────────────────────────────────────────
try:
    FONT_BIG   = pygame.font.SysFont("couriernew",  52, bold=True)
    FONT_MED   = pygame.font.SysFont("couriernew",  22, bold=True)
    FONT_SMALL = pygame.font.SysFont("couriernew",  15)
except:
    FONT_BIG   = pygame.font.SysFont(None, 52, bold=True)
    FONT_MED   = pygame.font.SysFont(None, 22, bold=True)
    FONT_SMALL = pygame.font.SysFont(None, 15)

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = (10,  12,  20)
GRID_C    = (40,  46,  70)
X_C       = (80, 180, 255)    # blue — player
O_C       = (255, 80, 110)    # red  — AI
WIN_LINE  = (255, 210,  60)
TEXT_C    = (210, 215, 235)
MUTED     = (90,  96, 130)
BTN_C     = (30,  36,  56)
BTN_HOV   = (50,  58,  88)
BTN_BORD  = (70,  78, 120)

# ── State ─────────────────────────────────────────────────────────────────────
board      = [None] * 9      # None, 'X', 'O'
HUMAN      = 'X'
AI         = 'O'
turn       = HUMAN           # human always goes first
game_over  = False
winner     = None            # 'X', 'O', or 'draw'
win_cells  = None            # list of 3 indices for win line
ai_thinking = False
ai_timer    = 0
score      = {'X': 0, 'O': 0, 'draw': 0}
status_msg = "Your turn  (X)"
anim_cells = {}              # cell_idx: alpha  for fade-in

WINS = [
    (0,1,2),(3,4,5),(6,7,8),   # rows
    (0,3,6),(1,4,7),(2,5,8),   # cols
    (0,4,8),(2,4,6)            # diags
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def cell_rect(idx):
    r, c = divmod(idx, 3)
    x = 40 + c * CELL
    y = GRID_OFF + r * CELL
    return pygame.Rect(x, y, CELL, CELL)

def cell_center(idx):
    rect = cell_rect(idx)
    return rect.centerx, rect.centery

def check_winner(b):
    for a, bb, c in WINS:
        if b[a] and b[a] == b[bb] == b[c]:
            return b[a], [a, bb, c]
    if all(x is not None for x in b):
        return 'draw', None
    return None, None

# ── Minimax ───────────────────────────────────────────────────────────────────
def minimax(b, depth, is_max, alpha=-math.inf, beta=math.inf):
    w, _ = check_winner(b)
    if w == AI:    return 10 - depth
    if w == HUMAN: return depth - 10
    if w == 'draw': return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] is None:
                b[i] = AI
                best = max(best, minimax(b, depth+1, False, alpha, beta))
                b[i] = None
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] is None:
                b[i] = HUMAN
                best = min(best, minimax(b, depth+1, True, alpha, beta))
                b[i] = None
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def best_move(b):
    best_val = -math.inf
    move = None
    for i in range(9):
        if b[i] is None:
            b[i] = AI
            val = minimax(b, 0, False)
            b[i] = None
            if val > best_val:
                best_val = val
                move = i
    return move

# ── Drawing ───────────────────────────────────────────────────────────────────
def draw_bg():
    screen.fill(BG)
    # subtle grid dots
    for row in range(4):
        for col in range(4):
            x = 40 + col * CELL
            y = GRID_OFF + row * CELL
            pygame.draw.circle(screen, GRID_C, (x, y), 3)

def draw_grid():
    for i in range(1, 3):
        # vertical
        x = 40 + i * CELL
        pygame.draw.line(screen, GRID_C, (x, GRID_OFF), (x, GRID_OFF + 3*CELL), 2)
        # horizontal
        y = GRID_OFF + i * CELL
        pygame.draw.line(screen, GRID_C, (40, y), (40 + 3*CELL, y), 2)

def draw_x(idx, alpha=255):
    cx, cy = cell_center(idx)
    pad = GAP + 14
    color = (*X_C, alpha)
    s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
    pygame.draw.line(s, color,
        (pad, pad), (CELL-pad, CELL-pad), 6)
    pygame.draw.line(s, color,
        (CELL-pad, pad), (pad, CELL-pad), 6)
    rect = cell_rect(idx)
    screen.blit(s, rect.topleft)

def draw_o(idx, alpha=255):
    cx, cy = cell_center(idx)
    pad = GAP + 14
    color = (*O_C, alpha)
    s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
    pygame.draw.circle(s, color, (CELL//2, CELL//2), CELL//2 - pad, 6)
    rect = cell_rect(idx)
    screen.blit(s, rect.topleft)

def draw_pieces():
    for idx, val in enumerate(board):
        if val is None:
            continue
        alpha = int(anim_cells.get(idx, 255))
        if val == HUMAN:
            draw_x(idx, alpha)
        else:
            draw_o(idx, alpha)

def draw_win_line():
    if win_cells is None:
        return
    a, b, c = win_cells
    x1, y1 = cell_center(a)
    x2, y2 = cell_center(c)
    pygame.draw.line(screen, WIN_LINE, (x1, y1), (x2, y2), 5)

def draw_hover(mx, my):
    if game_over or turn != HUMAN:
        return
    for idx in range(9):
        if board[idx] is None and cell_rect(idx).collidepoint(mx, my):
            s = pygame.Surface((CELL-4, CELL-4), pygame.SRCALPHA)
            s.fill((255, 255, 255, 18))
            r = cell_rect(idx)
            screen.blit(s, (r.x+2, r.y+2))

def draw_header():
    title = FONT_MED.render("TIC-TAC-TOE", True, TEXT_C)
    screen.blit(title, (W//2 - title.get_width()//2, 18))

    # score
    xs = FONT_SMALL.render(f"YOU  {score['X']}", True, X_C)
    ds = FONT_SMALL.render(f"DRAW  {score['draw']}", True, MUTED)
    os = FONT_SMALL.render(f"AI  {score['O']}", True, O_C)
    screen.blit(xs, (44, 46))
    screen.blit(ds, (W//2 - ds.get_width()//2, 46))
    screen.blit(os, (W - 44 - os.get_width(), 46))

def draw_status():
    col = TEXT_C
    if winner == HUMAN:   col = X_C
    elif winner == AI:    col = O_C
    elif winner == 'draw': col = WIN_LINE

    surf = FONT_MED.render(status_msg, True, col)
    screen.blit(surf, (W//2 - surf.get_width()//2, GRID_OFF + 3*CELL + 20))

def draw_button(label, rect, hovered):
    color = BTN_HOV if hovered else BTN_C
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, BTN_BORD, rect, width=1, border_radius=8)
    t = FONT_SMALL.render(label, True, TEXT_C)
    screen.blit(t, (rect.centerx - t.get_width()//2,
                    rect.centery - t.get_height()//2))

def draw_ai_dots():
    if not ai_thinking:
        return
    t = time.time()
    dots = "." * (int(t * 3) % 4)
    surf = FONT_SMALL.render("AI thinking" + dots, True, O_C)
    screen.blit(surf, (W//2 - surf.get_width()//2,
                       GRID_OFF + 3*CELL + 50))

# ── Game logic ─────────────────────────────────────────────────────────────────
def make_move(idx):
    global board, turn, game_over, winner, win_cells, status_msg
    if board[idx] is not None or game_over:
        return
    board[idx] = turn
    anim_cells[idx] = 0    # start fade-in

    w, wc = check_winner(board)
    if w:
        game_over = True
        winner    = w
        win_cells = wc
        score[w]  = score.get(w, 0) + 1
        if w == HUMAN:
            status_msg = "You win!  Well done."
        elif w == AI:
            status_msg = "AI wins!  Better luck."
        else:
            status_msg = "It's a draw!"
        return

    turn = AI if turn == HUMAN else HUMAN
    status_msg = "AI thinking..." if turn == AI else "Your turn  (X)"

def reset_game():
    global board, turn, game_over, winner, win_cells, ai_thinking, ai_timer, status_msg
    board       = [None] * 9
    turn        = HUMAN
    game_over   = False
    winner      = None
    win_cells   = None
    ai_thinking = False
    ai_timer    = 0
    status_msg  = "Your turn  (X)"
    anim_cells.clear()

# ── Button rects ──────────────────────────────────────────────────────────────
BTN_RESET = pygame.Rect(W//2 - 70, GRID_OFF + 3*CELL + 70, 140, 34)

# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    global ai_thinking, ai_timer, status_msg

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()

        # ── events ────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if BTN_RESET.collidepoint(mx, my):
                    reset_game()
                elif not game_over and turn == HUMAN:
                    for idx in range(9):
                        if cell_rect(idx).collidepoint(mx, my):
                            make_move(idx)
                            # schedule AI
                            if not game_over and turn == AI:
                                ai_thinking = True
                                ai_timer    = pygame.time.get_ticks() + 500
                            break

        # ── AI move (with delay so it feels natural) ──────────────────────────
        if ai_thinking and pygame.time.get_ticks() >= ai_timer:
            ai_thinking = False
            mv = best_move(board)
            if mv is not None:
                make_move(mv)

        # ── animate fade-in ───────────────────────────────────────────────────
        for idx in list(anim_cells.keys()):
            anim_cells[idx] = min(255, anim_cells[idx] + 18)
            if anim_cells[idx] >= 255:
                anim_cells[idx] = 255

        # ── draw ──────────────────────────────────────────────────────────────
        draw_bg()
        draw_header()
        draw_grid()
        draw_hover(mx, my)
        draw_pieces()
        if game_over and winner != 'draw':
            draw_win_line()
        draw_status()
        draw_ai_dots()

        hov_btn = BTN_RESET.collidepoint(mx, my)
        draw_button("New Game  (R)", BTN_RESET, hov_btn)

        pygame.display.flip()

if __name__ == "__main__":
    main()
