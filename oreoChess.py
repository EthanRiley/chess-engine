import random as rnd
from openingBook import Repetoir
from chessEngine import Move
import numpy as np
import tensorflow as tf
from tensorflow import keras
from hexapawn_zero.common.game import Board

class OreoChess:

    def __init__(self, depth=3, repetoir={}):
        self.checkmate = float('inf')
        self.stalemate = 0
        self.depth = depth
        self.repetoir = repetoir
        self.pieceScore = {"K": 0, "Q": 10, "R": 5, "N": 3, "B": 3, "p": 1}
        self.knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], ]

        self.bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4], ]

        self.queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1], ]

        self.rockScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4], ]

        self.whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0], ]

        self.blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8], ]

        self.piecePositionScores = {"N": self.knightScores, "B": self.bishopScores, "Q": self.queenScores, "wp": self.whitePawnScores,
                       "bp": self.blackPawnScores, "R": self.rockScores}

    def findRandomMove(self, validMoves):
        return validMoves[rnd.randint(0, len(validMoves) - 1)]

    def findBestMove(self, gs, validMoves):
        '''
        Helper method to make first recursive call
        '''
        global nextMove, counter
        nextMove = None
        rnd.shuffle(validMoves)
        counter = 0
        board_as_key = Repetoir.pos_to_key(gs.board)
        # findMinMaxMove(gs, validMoves, DEPTH, gs.whiteToMove)
        # findMoveNegamax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
        if board_as_key in self.repetoir:
            return Move(self.repetoir[board_as_key][0][0], self.repetoir[board_as_key][0][1], gs.board, isCastleMove=self.repetoir[board_as_key][1], isEnpassantMove=self.repetoir[board_as_key][2])
        self.findMoveNegamaxAlphaBeta(gs, validMoves, self.depth, -self.checkmate, self.checkmate, 1 if gs.whiteToMove else -1)
        print(counter, currScore)
        return nextMove

    def findMoveNegamaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, counter, currScore
        counter += 1
        if depth == 0:
            return turnMultiplier * scoreBoard(gs)

        # Implementing move ordering later to increase efficiency

        maxScore = -self.checkmate
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = -self.findMoveNegamaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.depth:
                    nextMove = move
            gs.undoMove()
            if maxScore > alpha:  # pruning happens here
                alpha = maxScore
            if alpha >= beta:
                break
        currScore = maxScore
        return maxScore

    def findGreedyMove(self, gs, validMoves):
        '''
        Greedy algorithm
        Simply evaluates the most material it can take on every move and then does so
        '''
        turnMultiplier = 1 if gs.whiteToMove else -1
        opponentMinMaxScore = self.checkmate
        bestResponse = None
        rnd.shuffle(validMoves)
        for playerMove in validMoves:
            gs.makeMove(playerMove)
            opponentsMoves = gs.getValidMoves()
            opponentMaxScore = -self.checkmate
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                if gs.checkmate:
                    score = turnMultiplier * self.checkmate
                elif gs.stalemate:
                    score = self.stalemate
                else:
                    score = -turnMultiplier * OreoChess.scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            if opponentMinMaxScore > opponentMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestResponse = playerMove
            gs.undoMove()
        return bestResponse

    @staticmethod
    def scoreMaterial(board):
        '''
        Board evaluation for greedy. Significantly outclassed by other board evaluation function
        '''
        score = 0
        for row in board:
            for square in row:
                if square[0] == 'w':
                    score += pieceScore[square[1]]
                elif square[0] == 'b':
                    score -= pieceScore[square[1]]

        return score

    def scoreBoard(self, gs):
        """
        # increasing the number of valid moves per piece
        # Giving Bishops more open lanes
        # Queen open lanes
        # Castling (Capturing King safety)
        """
        if gs.checkmate:
            if gs.whiteToMove:
                return -self.checkmate
            else:
                return self.checkmate
        elif gs.stalemate:
            return self.stalemate

        score = 0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                square = gs.board[row][col]
                if square != "--":
                    piecePositionScore = 0
                    if square[1] != "K":
                        if square[1] == "p":
                            piecePositionScore = self.piecePositionScores[square][row][col]
                        else:
                            piecePositionScore = self.piecePositionScores[square[1]][row][col]

                    if square[0] == 'w':
                        score += self.pieceScore[square[1]] + piecePositionScore * 0.1
                    elif square[0] == 'b':
                        score -= self.pieceScore[square[1]] + piecePositionScore * 0.1

        return score




'''
Defunct engine functionality maintained here
'''

pieceScore = {"K": 0, "Q": 10, "R": 5, "N": 3, "B": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], ]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4], ]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1], ]

rockScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4], ]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0], ]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8], ]

piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores, "wp": whitePawnScores,
                       "bp": blackPawnScores, "R": rockScores}


CHECKMATE = float('inf')
STALEMATE = 0
DEPTH = 2

# Min max without recursion
def findGreedyMove(self, gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = self.checkmate
    bestResponse = None
    rnd.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentMove in opponentsMoves:
            gs.makeMove(opponentMove)
            if gs.checkmate:
                score = turnMultiplier * CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMinMaxScore > opponentMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestResponse = playerMove
        gs.undoMove()
    return bestResponse


def findBestMove(gs, validMoves):
    '''
    Helper method to make first recursive call
    '''
    global nextMove, counter
    nextMove = None
    rnd.shuffle(validMoves)
    counter = 0
    # findMinMaxMove(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegamax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegamaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter, currScore)
    return nextMove


def findMinMaxMove(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMinMaxMove(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegamax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegamax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


def findMoveNegamaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter, currScore
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Implementing move ordering later to increase efficiency

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegamaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happens here
            alpha = maxScore
        if alpha >= beta:
            break
    currScore = maxScore
    return maxScore


def scoreBoard(gs):
    """
    # increasing the number of valid moves per piece
    # Giving Bishops more open lanes
    # Queen open lanes
    # Castling (Capturing King safety)
    """
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * 0.1

    return score


'''
Score the board based on material
'''


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score

class HexaOreo():
    def __init__(self):
        self.model = keras.models.load_model('hexapawn_zero/supervised_model.keras')
        self.outputIndex = {}
        self.outputIndex["(6, 3)"] = 0
        self.outputIndex["(7, 4)"] = 1
        self.outputIndex["(8, 5)"] = 2
        self.outputIndex["(3, 0)"] = 3
        self.outputIndex["(4, 1)"] = 4
        self.outputIndex["(5, 2)"] = 5

        # black forward moves
        self.outputIndex["(0, 3)"] = 6
        self.outputIndex["(1, 4)"] = 7
        self.outputIndex["(2, 5)"] = 8
        self.outputIndex["(3, 6)"] = 9
        self.outputIndex["(4, 7)"] = 10
        self.outputIndex["(5, 8)"] = 11

        # white capture moves
        self.outputIndex["(6, 4)"] = 12
        self.outputIndex["(7, 3)"] = 13
        self.outputIndex["(7, 5)"] = 14
        self.outputIndex["(8, 4)"] = 15
        self.outputIndex["(3, 1)"] = 16
        self.outputIndex["(4, 0)"] = 17
        self.outputIndex["(4, 2)"] = 18
        self.outputIndex["(5, 1)"] = 19

        # black capture moves
        self.outputIndex["(0, 4)"] = 20
        self.outputIndex["(1, 3)"] = 21
        self.outputIndex["(1, 5)"] = 22
        self.outputIndex["(2, 4)"] = 23
        self.outputIndex["(3, 7)"] = 24
        self.outputIndex["(4, 6)"] = 25
        self.outputIndex["(4, 8)"] = 26
        self.outputIndex["(5, 7)"] = 27

    def squareToIndex(self, r, c):
        return r*3 + c
    
    def getNetworkOutputIndex(self, move):
        move_key = (self.squareToIndex(move.startRow, move.startCol), self.squareToIndex(move.endRow, move.endCol))
        return self.outputIndex[str(move_key)]

    def findBestMove(self, gs):
        network_output = self.model.predict(np.array([gs.toHexapawnNetworkInput()]))
        masked_output = [0 for x in range(0, 28)]
        moves = gs.getHexapawnMoves()
        for move in moves:
            moveIndex = self.getNetworkOutputIndex(move)
            masked_output[moveIndex] = network_output[0][0][moveIndex]
        bestIdx = np.argmax(masked_output)
        for move in moves:
            if self.getNetworkOutputIndex(move) == bestIdx:
                return move


