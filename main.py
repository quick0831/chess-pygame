import sys
from copy import deepcopy as copy
import pygame
from pygame.locals import QUIT, VIDEORESIZE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

import crop_image
from crop_image import Piece, Color, State

size = (820, 820)
title = "Chess"
piece_size = 100
FPS = 60

BLACK = (0, 0, 0)
DARK = (88, 88, 88)
DARKER = (50, 50, 50, 100)
BRIGHT = (230, 230, 230)
DARK_RED = (220, 30, 30)
BRIGHT_RED = (249, 58, 56)

pieces = crop_image.main(piece_size)
board_offset = (10,10)

pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption(title)

clk = pygame.time.Clock()

class Space(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.update()

    def update(self):
        s = board_state[self.x][self.y]
        self.image = pieces[s.color][s.piece]
        self.rect = self.image.get_rect()
        self.rect.x =    self.x *piece_size + board_offset[0]
        self.rect.y = (7-self.y)*piece_size + board_offset[1]

    def mouse_drop(self, mouse_pos):
        self.rect.x =    self.x *piece_size + board_offset[0]
        self.rect.y = (7-self.y)*piece_size + board_offset[1]
        if board_state[self.x][self.y].piece != Piece.EMPTY:
            px = (mouse_pos[0] - board_offset[0]) // piece_size
            py = (mouse_pos[1] - board_offset[1]) // piece_size
            piece_to = (int(px), int(7-py)) if px<8 and py<8 and px>=0 and py>=0 else None
            board_update((self.x, self.y), piece_to)

def get_piece(space):
    return board_state[space[0]][space[1]]

def set_piece(space, state):
    board_state[space[0]][space[1]] = copy(state)

def remove_piece(space):
    board_state[space[0]][space[1]] = State(Piece.EMPTY, Color.WHITE)

def move_piece(space_from, space_to):
    set_piece(space_to, get_piece(space_from))

def board_update(space_from, space_to):
    global check_space, last_move
    if space_to:
        # Check if not moved at all (prevent unsafe type)
        if space_from[0] == space_to[0] and space_from[1] == space_to[1]:
            pass
        elif move_valid(space_from, space_to):
            last_move = [space_from, space_to]
            move_piece(space_from, space_to)
            remove_piece(space_from)
            for space in Board:
                space.update()
    else:
        check_space = None

def move_valid(space_from, space_to):
    global en_passant_ok
    piece_from = get_piece(space_from)
    piece_to = get_piece(space_to)
    if piece_from.color == piece_to.color and piece_to.piece != Piece.EMPTY:
        return False # Taking Own Piece
    
    if piece_from.piece == Piece.PAWN:
        return move_valid_pawn(*space_from, *space_to, piece_from.color)
    en_passant_ok = False
    return {
        Piece.KNIGHT : move_valid_knight,
        Piece.BISHOP : move_valid_bishop,
        Piece.ROOK   : move_valid_rook,
        Piece.QUEEN  : move_valid_queen,
        Piece.KING   : move_valid_king
    }[piece_from.piece](*space_from, *space_to)

def move_valid_pawn(x1, y1, x2, y2, color):
    global en_passant_ok
    # Starting Row
    if color == board_side:
        if y1 == 1 and y2 == 3 and x1 == x2:
            en_passant_ok = True
            return True
        if en_passant_ok:
            en_passant_ok = False
            if last_move[0][0] == x2 and abs(x1-x2) == 1:
                if y1 == 4 and y2 == 5:
                    remove_piece(last_move[1])
                    return True
        en_passant_ok = False
        if x1 == x2 and (y1+1) == y2 and get_piece((x2, y2)).piece == Piece.EMPTY:
            return True
        if abs(x1-x2) == 1 and (y1+1) == y2 and get_piece((x2, y2)).piece != Piece.EMPTY:
            return True
    else:
        if y1 == 6 and y2 == 4 and x1 == x2:
            en_passant_ok = True
            return True
        if en_passant_ok:
            en_passant_ok = False
            if last_move[0][0] == x2 and abs(x1-x2) == 1:
                if y1 == 3 and y2 == 2:
                    remove_piece(last_move[1])
                    return True
        en_passant_ok = False
        if x1 == x2 and (y1-1) == y2 and get_piece((x2, y2)).piece == Piece.EMPTY:
            return True
        if abs(x1-x2) == 1 and (y1-1) == y2 and get_piece((x2, y2)).piece != Piece.EMPTY:
            return True
    en_passant_ok = False
    return False

def move_valid_knight(x1, y1, x2, y2):
    return (abs(x1-x2), abs(y1-y2)) in ((1,2),(2,1))

def move_valid_bishop(x1, y1, x2, y2):
    if x1 - x2 == y1 - y2: # Top-Left to Bottom-Right Diagonal
        for i, j in zip(range(x1+1, x2), range(y1+1, y2)):
            if get_piece((i, j)).piece != Piece.EMPTY:
                return False
        for i, j in zip(range(x2+1, x1), range(y2+1, y1)):
            if get_piece((i, j)).piece != Piece.EMPTY:
                return False
        return True
    if x1 - x2 == y2 - y1: # Top-Right to Bottom-Left Diagonal
        for i, j in zip(range(x1+1, x2), range(y1-1, y2, -1)):
            if get_piece((i, j)).piece != Piece.EMPTY:
                return False
        for i, j in zip(range(x2+1, x1), range(y2-1, y1, -1)):
            if get_piece((i, j)).piece != Piece.EMPTY:
                return False
        return True
    return False

def move_valid_rook(x1, y1, x2, y2):
    if x1 == x2:
        for i in range(y1 + 1, y2):
            if get_piece((x1, i)).piece != Piece.EMPTY:
                return False
        for i in range(y2 + 1, y1):
            if get_piece((x1, i)).piece != Piece.EMPTY:
                return False
        return True
    if y1 == y2:
        for i in range(x1 + 1, x2):
            if get_piece((i, y1)).piece != Piece.EMPTY:
                return False
        for i in range(x2 + 1, x1):
            if get_piece((i, y1)).piece != Piece.EMPTY:
                return False
        return True
    return False

def move_valid_queen(*param):
    return move_valid_rook(*param) or move_valid_bishop(*param)

def move_valid_king(x1, y1, x2, y2):
    return True

def flip_board():
    global board_side, board_state, check_space, last_move
    board_state = copy([board_state[7-i][::-1] for i in range(8)])
    board_side = Color.BLACK if board_side == Color.WHITE else Color.WHITE
    if check_space:
        check_space = (7-check_space[0], 7-check_space[1])
    for i in range(len(last_move)):
        if last_move[i]:
            last_move[i] = (7-last_move[i][0], 7-last_move[i][1])
    for space in Board:
        space.update()

# Replace pygame.draw.rect For transparent display
def draw_rect_alpha(surface, color, rect, border_radius=0):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border_radius)
    surface.blit(shape_surf, rect)

board_side = Color.WHITE
board_state = [[State(Piece.EMPTY, Color.WHITE) for _ in range(8)] for _ in range(8)]

init_board_row = (Piece.ROOK,Piece.KNIGHT,Piece.BISHOP,Piece.QUEEN,Piece.KING,Piece.BISHOP,Piece.KNIGHT,Piece.ROOK)
for i, p in enumerate(init_board_row):
    board_state[i][7] = State(p, Color.BLACK)
    board_state[i][6] = State(Piece.PAWN, Color.BLACK)
    board_state[i][1] = State(Piece.PAWN, Color.WHITE)
    board_state[i][0] = State(p, Color.WHITE)

Board = pygame.sprite.Group()
for i in range(8):
    for j in range(8):
        Board.add(Space(i, j))

# Initialize Variables
mouse_down = False
mouse_offset = [0, 0]
mouse_drag_obj = None
# Use coordinate Eg. (0, 2) = a3
check_space = None
last_move = [None, None]
en_passant_ok = False

while True:
    # ====  Event Loop ====
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            w = event.w
            h = event.h
            piece_size = (min(w,h)-20)/8
            board_offset
            pieces = crop_image.main(piece_size)
            for space in Board:
                space.update()
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            # 1=Left 2=Middle 3=Right 4=Up Scroll 5=Down Scroll
            if event.button == 1:
                for space in Board:
                    if space.rect.collidepoint(event.pos):
                        #mouse_offset[0] = space.rect.x - event.pos[0]
                        #mouse_offset[1] = space.rect.y - event.pos[1]
                        mouse_offset[0]=mouse_offset[1]=-piece_size//2
                        mouse_drag_obj = space
        if event.type == MOUSEBUTTONUP:
            if mouse_drag_obj:
                mouse_drag_obj.mouse_drop(event.pos)
            mouse_down = False
            mouse_drag_obj = None
        if event.type == MOUSEMOTION:
            if mouse_down:
                if mouse_drag_obj:
                    mouse_drag_obj.rect.x = mouse_offset[0] + event.pos[0]
                    mouse_drag_obj.rect.y = mouse_offset[1] + event.pos[1]
    # ==== End of Event Loop ====
    screen.fill(BLACK)

    # Draw Game Board
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, DARK if (i+j)%2==1 else BRIGHT, (i*piece_size + board_offset[0], j*piece_size + board_offset[1], piece_size+1, piece_size+1))

    # Draw The Red Checked space
    if check_space:
        x, y = check_space
        pygame.draw.rect(screen, DARK_RED if (x+y)%2==0 else BRIGHT_RED, (x*piece_size + board_offset[0], (7-y)*piece_size + board_offset[1], piece_size+1, piece_size+1))

    # Draw Last Move Indicator
    for pos in last_move:
        if pos:
            x, y = pos
            draw_rect_alpha(screen, DARKER, (int((x+0.1)*piece_size + board_offset[0]), int((7-y+0.1)*piece_size + board_offset[1]), int(piece_size*0.8), int(piece_size*0.8)), border_radius=int(piece_size*0.2))

    # Draw the pieces
    Board.draw(screen)
    # Top the dragged piece by redrawing
    if mouse_drag_obj:
        screen.blit(mouse_drag_obj.image, mouse_drag_obj.rect)
    
    clk.tick(FPS)
    pygame.display.update()