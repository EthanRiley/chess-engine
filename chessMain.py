'''
Driver file, handles user input and displays position
'''

from sqlite3 import SQLITE_SELECT
from tkinter.tix import MAX
import chessEngine
import pygame as p
import oreoChess
from oreoChess import OreoChess
import openingBook

Oreo = OreoChess(depth=2)

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    '''
    Initialize global directory of images
    '''
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    moveLogFont = p.font.SysFont("Times New Roman", 15, False, False)
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    load_images()
    running = True
    options = True
    sqSelected = () # will keep track of last click of the user
    playerClicks = [] # keeps track of player clicks (two tuples: eg. [(6, 4), [4, 4]])
    gameOver = False
    playerOne = True #If a Human is playing white, then this will be True. If an AI is playing, then false.
    playerTwo = True # If a Human is playing black, then this will be True. If an AI is playing, then false.

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: # When mouse is clicked
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # (x, y) location of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: # Clear clicks when the same square is clicked
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col) 
                        playerClicks.append(sqSelected) # Save click into playerClicks list
                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]: # Only make move if it is valid
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
        
            elif e.type == p.KEYDOWN: # Key press handling
                if e.key == p.K_z: # Press Z to undo a move
                    gs.undoMove()
                    moveMade = True
                    gs.checkmate = False
                    gs.stalemate = False
                    gameOver = False
                if e.key == p.K_r: # Press R to reset the game
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gs.checkmate = False
                    gs.stalemate = False
                    gameOver = False
                if options:
                    if e.key == p.K_q:
                        playerOne = True
                        playerTwo = True
                        options = False
                    elif e.key == p.K_w:
                        playerOne = True
                        playerTwo = False
                        options = False
                    elif e.key == p.K_e:
                        playerOne = False
                        playerTwo = True
                        options = False
                    elif e.key == p.K_r:
                        playerOne = False
                        playerTwo = False
                        options = False
        # AI Movefinder
        if not gameOver and not humanTurn:
            AIMove = Oreo.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = Oreo.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)
        if options:
            drawBoard(screen)
            drawOptionsText(screen, text1="Press Q for two player", text2="Press W for White vs AI", text3="Press E for Black vs AI")
        if gs.checkmate or gs.stalemate:
            gameOver = True
            if gs.stalemate:
                text = 'Stalemate'
            else:
                text = 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
            drawEndGameText(screen, text)
        clock.tick(MAX_FPS)
        p.display.flip()
        

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    '''
    draws squares on the board
    '''
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)



def drawBoard(screen):
    '''
    Draws board of squares
    '''
    colors = [p.Color('white'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    '''
    Highlight squares when clicked
    '''
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

def drawPieces(screen, board):
    '''
    Draw pieces from images folder
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('black'), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + "." + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString +=str(moveLog[i + 1]) + "  "
        moveTexts.append(moveString)

    movesPerRow = 3
    padding = 5
    textY = padding
    lineSpacing = 2

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color("White"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


def drawEndGameText(screen, text):
    '''
    Function for drawing checkmate and stalemate text
    '''
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Gray"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - textObject.get_width() / 2,
        BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

def drawOptionsText(screen, text1, text2, text3):
    '''
    Function for drawing options text
    '''
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject1 = font.render(text1, 0, p.Color("Gray"))
    textObject2 = font.render(text2, 0, p.Color("Gray"))
    textObject3 = font.render(text3, 0, p.Color("Gray"))
    textLocation1 = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - textObject1.get_width() / 2,
        BOARD_HEIGHT * .25 - textObject1.get_height() / 2)
    textLocation2 = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - textObject2.get_width() / 2,
        BOARD_HEIGHT * .5 - textObject2.get_height() / 2)
    textLocation3 = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH / 2 - textObject3.get_width() / 2,
        BOARD_HEIGHT * .75 - textObject3.get_height() / 2)
    screen.blit(textObject1, textLocation1)
    textObject1 = font.render(text1, 0, p.Color("Black"))
    screen.blit(textObject1, textLocation1.move(2, 2))
    screen.blit(textObject2, textLocation2)
    textObject2 = font.render(text2, 0, p.Color("Black"))
    screen.blit(textObject2, textLocation2.move(2, 2))
    screen.blit(textObject3, textLocation3)
    textObject3 = font.render(text3, 0, p.Color("Black"))
    screen.blit(textObject3, textLocation3.move(2, 2))

main()
