import sys
import pygame
from pygame.locals import QUIT, VIDEORESIZE

import crop_image

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
    # ==== End of Event Loop ====
    screen.fill(BLACK)
    for i in range(8):
        for j in range(8):
            pygame.draw.rect(screen, DARK if (i+j)%2==1 else BRIGHT, (i*piece_size + board_offset[0], j*piece_size + board_offset[1], piece_size+1, piece_size+1))
    for i in range(2):
        for j in range(6):
            screen.blit(pieces[i][j], (j*piece_size + board_offset[0],  i   *piece_size + board_offset[1]))
            screen.blit(pieces[i][j], (j*piece_size + board_offset[0], (i+3)*piece_size + board_offset[1]))
    
    pygame.draw.rect(screen, DARK_RED, (3*piece_size + board_offset[0], 6*piece_size + board_offset[1], piece_size+1, piece_size+1))
    screen.blit(pieces[0][0], (3*piece_size + board_offset[0], 6*piece_size + board_offset[1]))
    pygame.draw.rect(screen, BRIGHT_RED, (4*piece_size + board_offset[0], 6*piece_size + board_offset[1], piece_size+1, piece_size+1))
    screen.blit(pieces[1][0], (4*piece_size + board_offset[0], 6*piece_size + board_offset[1]))
    clk.tick(FPS)
    pygame.display.update()