import chess, chess.pgn
import numpy as np
from pgn_aggregation import *
import json

test_pgn = open("oreo_zero/data/lichess_elite_2022-06.pgn")
positions = []
moveProbs = []
outcomes = []
counter = 0
while True:
    game = chess.pgn.read_game(test_pgn)
    counter += 1
    if game is None:
        break
    board = game.board()
    print(counter)
    for move in game.mainline_moves():
        fen = board.fen()
        bitboards = FEN_to_bitboards(fen)
        positions.append(bitboards)
        board.push(move)
        
        moveProb = [0 for x in range(0, 1836)]
        moveProb[move_notation_to_index(move)] = 1
        moveProbs.append(moveProb)

        outcomes.append(result_to_winner(game.headers["Result"]))

np.save("positions", np.array(positions))
np.save("moveProbs", np.array(moveProbs))
np.save("outcomes", np.array(outcomes))