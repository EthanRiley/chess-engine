from chessEngine import GameState, Move
import json

gs = GameState()
gs.board = gs.emptyBoard

move_indeces = {}
counter = 0
for r in range(0, 8):
    for c in range(0, 8):
        moves = []
        gs.getQueenMoves(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}'
            move_indeces[index] = counter
            counter += 1
for r in range(0, 8):
    for c in range(0, 8):
        moves = []
        gs.getKnightMoves(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}'
            move_indeces[index] = counter
            counter += 1
# Handle all promotion moves

start_rows = [1, 6]
def get_left_promotion(start_row, start_col, moves):
    if start_col - 1 >= 0:
        if start_row == 6:
            moves.append(Move((start_row, start_col), (start_row+1, start_col-1), gs.board, True))
        if start_row == 1:
            moves.append(Move((start_row, start_col), (start_row-1, start_col-1), gs.board, True))

def get_right_promotion(start_row, start_col, moves):
    if start_col + 1 < len(gs.board[0]):
        if start_row == 6:
            moves.append(Move((start_row, start_col), (start_row+1, start_col+1), gs.board, True))
        if start_row == 1:
            moves.append(Move((start_row, start_col), (start_row-1, start_col+1), gs.board, True))

def get_forward_promotion(start_row, start_col, moves):
    if start_row == 6:
        moves.append(Move((start_row, start_col), (start_row+1, start_col), gs.board, True))
    if start_row == 1:
        moves.append(Move((start_row, start_col), (start_row-1, start_col), gs.board, True))

for r in range(len(gs.board)):
    for c in range(len(gs.board[r])):
        moves = []
        get_left_promotion(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}Q'
            move_indeces[index] = counter
            counter += 1
for r in range(len(gs.board)):
    for c in range(len(gs.board[r])):
        moves = []
        get_right_promotion(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}Q'
            move_indeces[index] = counter
            counter += 1
for r in range(0, 8):
    for c in range(0, 8):
        moves = []
        get_forward_promotion(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}Q'
            move_indeces[index] = counter
            counter += 1

"""
def get_enpassant_move(start_row, start_col, moves):
    if start_row == 3:
        if start_col - 1 >= 0:
            moves.append(Move((start_row, start_col), (start_row+1, start_col-1), gs.board))
        if start_col + 1 < len(gs.board[0]):
            moves.append(Move((start_row, start_col), (start_row+1, start_col+1), gs.board))
    if start_row == 4:
        if start_col - 1 >= 0:
            moves.append(Move((start_row, start_col), (start_row-1, start_col-1), gs.board))
        if start_col + 1 < len(gs.board[0]):
            moves.append(Move((start_row, start_col), (start_row-1, start_col+1), gs.board))

for r in range(len(gs.board)):
    for c in range(len(gs.board[r])):
        moves = []
        get_enpassant_move(r, c, moves)
        for m in moves:
            index = f'{r}{c}{m.endRow}{m.endCol}eP'
            move_indeces[index] = counter
            counter += 1
"""
"""
castle_moves = ['O-O', 'O-O-O']
for move in castle_moves:
    index = f'{move}w'
    move_indeces[index] = counter
    counter += 1
    index2 = f'{move}b'
    move_indeces[index2] = counter
    counter += 1
"""



with open("move_indeces.json", "w") as f:
    json.dump(move_indeces, f)

print(move_indeces)