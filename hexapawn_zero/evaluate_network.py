from common.game import Board
import random as rnd
import numpy as np


def fst(a):
    return a[0]

def rand_vs_net(board, model):
    record = []
    while(not fst(board.isTerminal())):
        if(board.turn == Board.WHITE):
            moves = board.generateMoves()
            m = moves[rnd.randint(0, len(moves)-1)]
            board.applyMove(m)
            record.append(m)
            continue
        else:
            q = model.predict(np.array([board.toNetworkInput()]))
            masked_output = [0 for x in range(0, 28)]
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                masked_output[m_idx] = q[0][0][m_idx]
            best_idx = np.argmax(masked_output)
            sel_move = None
            for m in board.generateMoves():
                m_idx = board.getNetworkOutputIndex(m)
                if(best_idx == m_idx):
                    sel_move = m
            board.applyMove(sel_move)
            record.append(sel_move)
            continue
    terminal, winner = board.isTerminal()
    return winner

def rand_vs_rand(board):
    while(not fst(board.isTerminal())):
        moves = board.generateMoves()
        m = moves[rnd.randint(0, len(moves)-1)]
        board.applyMove(m)
        continue
    terminal, winner = board.isTerminal()
    return winner
    