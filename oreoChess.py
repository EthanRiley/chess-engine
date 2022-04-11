import random as rnd

pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "p": 1}
CHECKMATE = float('inf')
STALEMATE = 0


class OreoChess:


    def findRandomMove(self, validMoves):
        return validMoves[rnd.randint(0, len(validMoves)-1)]

    def findBestMove(validMoves):
        pass

def findRandomMove(validMoves):
    return validMoves[rnd.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove

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

