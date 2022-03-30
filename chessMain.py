'''
Driver file, handles user input and displays position
'''

from tkinter.tix import MAX
import pygame as p
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize global directory of images
'''
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wL', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bL']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

'''
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = chessEngine.GameState()
    load_images()
    running =True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT():
                running = False
            clock.tick(MAX_FPS)
            p.display.flip()

def drawGameState(screen, gs):
    '''
    draws squares on the board
    '''
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(scren):
    colors = [p.Color('white'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
