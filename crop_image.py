import os
import pygame

CHESS_PATH = os.path.join(".","chess_piece_200x200.png")

img = pygame.image.load(CHESS_PATH)

def main(piece_size):
    piece_size = int(piece_size)
    pieces = [[pygame.transform.smoothscale(img.subsurface((j*200, i*200, 200, 200)), (piece_size, piece_size)) for j in range(6)] for i in range(2)]
    
    return pieces
