from common.game import Board
import copy
import numpy as np
from minimax import minimax

def getBestMoveRes(board):
    bestMove = None
    bestVal = 100000000
    if(board.turn == board.WHITE):
        bestVal = -100000000
    for m in board.generateMoves():
        tmp = copy.deepcopy(board)
        tmp.applyMove(m)
        mVal = minimax(tmp, 30, tmp.turn == board.WHITE)
        if(board.turn == board.WHITE and mVal > bestVal):
            bestVal = mVal
            bestMove = m
        if(board.turn == board.BLACK and mVal < bestVal):
            bestVal = mVal
            bestMove = m
    return bestMove, bestVal

positions = []
moveProbs = []
outcomes = []

gameStates = {}

def visitNodes(board):
    gameStates[str(board)] = 1
    term, _ = board.isTerminal()
    if(term):
        return
    else:
        bestMove, bestVal = getBestMoveRes(board)
        positions.append(board.toNetworkInput())
        moveProb = [0 for x in range(0, 28)]
        idx = board.getNetworkOutputIndex(bestMove)
        moveProb[idx] = 1
        moveProbs.append(moveProb)
        if(bestVal > 0):
            outcomes.append(1)
        elif(bestVal == 0):
            outcomes.append(0)
        elif(bestVal < 0):
            outcomes.append(-1)
        for m in board.generateMoves():
            next = copy.deepcopy(board)
            next.applyMove(m)
            visitNodes(next)

board = Board()
board.setStartingPosition()
visitNodes(board)
print(f"# of positions: {len(gameStates)}")
np.save("positions", np.array(positions))
np.save("moveProbs", np.array(moveProbs))
np.save("outcomes", np.array(outcomes))