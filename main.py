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
        self.rect.x = self.x*piece_size + board_offset[0]
        self.rect.y = self.y*piece_size + board_offset[1]

    def mouse_drop(self, mouse_pos):
        self.rect.x = self.x*piece_size + board_offset[0]
        self.rect.y = self.y*piece_size + board_offset[1]
        if board_state[self.x][self.y].piece != Piece.EMPTY:
            px = (mouse_pos[0] - board_offset[0]) // piece_size
            py = (mouse_pos[1] - board_offset[1]) // piece_size
            piece_to = (int(px), int(py)) if px<8 and py<8 and px>=0 and py>=0 else None
            board_update((self.x, self.y), piece_to)

def get_piece(piece):
    return board_state[piece[0]][piece[1]]

def set_piece(piece, state):
    board_state[piece[0]][piece[1]] = copy(state)

def move_piece(piece_from, piece_to):
    set_piece(piece_to, get_piece(piece_from))

def board_update(piece_from, piece_to):
    global check_space, last_move
    if piece_to:
        move_valid = True
        if move_valid:
            last_move = [piece_from, piece_to]
            move_piece(piece_from, piece_to)
            set_piece(piece_from, State(Piece.EMPTY, Color.WHITE))
            for space in Board:
                space.update()
    else:
        check_space = None

# Replace pygame.draw.rect For transparent display
def draw_rect_alpha(surface, color, rect, border_radius=0):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border_radius)
    surface.blit(shape_surf, rect)

board_state = [[State(Piece.EMPTY, Color.WHITE) for _ in range(8)] for _ in range(8)]

init_board_row = (Piece.ROOK,Piece.KNIGHT,Piece.BISHOP,Piece.QUEEN,Piece.KING,Piece.BISHOP,Piece.KNIGHT,Piece.ROOK)
for i, p in enumerate(init_board_row):
    board_state[i][0] = State(p, Color.BLACK)
    board_state[i][1] = State(Piece.PAWN, Color.BLACK)
    board_state[i][6] = State(Piece.PAWN, Color.WHITE)
    board_state[i][7] = State(p, Color.WHITE)

Board = pygame.sprite.Group()
for i in range(8):
    for j in range(8):
        Board.add(Space(i, j))

# Initialize Variables
mouse_down = False
mouse_offset = [0, 0]
mouse_drag_obj = None
# Use coordinate Eg. (0, 2) = a6
check_space = None
last_move = [None, None]

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
        pygame.draw.rect(screen, DARK_RED if (x+y)%2==1 else BRIGHT_RED, (x*piece_size + board_offset[0], y*piece_size + board_offset[1], piece_size+1, piece_size+1))

    # Draw Last Move Indicator
    for pos in last_move:
        if pos:
            x, y = pos
            draw_rect_alpha(screen, DARKER, (int((x+0.1)*piece_size + board_offset[0]), int((y+0.1)*piece_size + board_offset[1]), int(piece_size*0.8), int(piece_size*0.8)), border_radius=int(piece_size*0.2))

    # Draw the pieces
    Board.draw(screen)
    
    clk.tick(FPS)
    pygame.display.update()