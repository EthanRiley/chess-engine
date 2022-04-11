'''
Driver file, handles user input and displays position
'''

from sqlite3 import SQLITE_SELECT
from tkinter.tix import MAX
import chessEngine
import pygame as p
import oreoChess

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize global directory of images
'''
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
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
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    load_images()
    running =True
    sqSelected = () # will keep track of last click of the user
    playerClicks = [] # keeps track of player clicks (two tuples: eg. [(6, 4), [4, 4]])
    gameOver = False
    playerOne = True
    playerTwo = True
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
        
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    gs.checkmate = False
                    gs.stalemate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gs.checkmate = False
                    gs.stalemate = False
                    gameOver = False
        # AI Movefinder
        if not gameOver and not humanTurn:
            AIMove = oreoChess.findRandomMove(validMoves)
            if AIMove is None:
                AIMove = oreoChess.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')

            else:
                drawText(screen, 'White wins by checkmate')

        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Game drawn by stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
        

def drawGameState(screen, gs, validMoves, sqSelected):
    '''
    draws squares on the board
    '''
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color('white'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - textObject.get_width() / 2,
        HEIGHT / 2 - textObject.get_height() / 2,
    )
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))



main()
