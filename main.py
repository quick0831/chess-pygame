import sys
import pygame
from pygame.locals import QUIT, VIDEORESIZE

import crop_image
from crop_image import Piece, Color, State

size = (820, 820)
title = "Chess"
piece_size = 100
FPS = 60

BLACK = (0, 0, 0)
DARK = (88, 88, 88)
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
        self.resize()
        self.update()
    
    def resize(self):
        self.piece_size = piece_size
        self.pieces = pieces

    def update(self):
        s = board_state[self.x][self.y]
        self.image = pieces[s.color][s.piece]
        self.rect = (self.x*piece_size + board_offset[0], self.y*piece_size + board_offset[1])

board_state = [[State(Piece.EMPTY, Color.WHITE) for _ in range(8)] for _ in range(8)]

board_state[2][3] = State(Piece.BISHOP, Color.BLACK)

Board = pygame.sprite.Group()
for i in range(8):
    for j in range(8):
        Board.add(Space(i, j))

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
                space.resize(piece_size, pieces)
    # ==== End of Event Loop ====
    screen.fill(BLACK)
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, DARK if (i+j)%2==1 else BRIGHT, (i*piece_size + board_offset[0], j*piece_size + board_offset[1], piece_size+1, piece_size+1))
    Board.draw(screen)

    #pygame.draw.rect(screen, DARK_RED, (3*piece_size + board_offset[0], 6*piece_size + board_offset[1], piece_size+1, piece_size+1))
    #screen.blit(pieces[0][0], (3*piece_size + board_offset[0], 6*piece_size + board_offset[1]))
    #pygame.draw.rect(screen, BRIGHT_RED, (4*piece_size + board_offset[0], 6*piece_size + board_offset[1], piece_size+1, piece_size+1))
    #screen.blit(pieces[1][0], (4*piece_size + board_offset[0], 6*piece_size + board_offset[1]))
    clk.tick(FPS)
    pygame.display.update()