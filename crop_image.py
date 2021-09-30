import os
import pygame

CHESS_PATH = os.path.join(".","chess_piece_200x200.png")

img = pygame.image.load(CHESS_PATH)

class Piece():
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5
    EMPTY = 6

class Color():
    WHITE = 0
    BLACK = 1

class State:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color

def main(piece_size):
    piece_size = int(piece_size)
    pieces = [[0]*7]*2
    for i in range(2):
        p = []
        for j in range(6):
            p.append(pygame.transform.smoothscale(img.subsurface((j*200, i*200, 200, 200)), (piece_size, piece_size)))
        
        s = pygame.Surface((piece_size, piece_size))
        s.set_colorkey((0,0,0))
        p.append(s)
        pieces[i] = p
    
    return pieces
