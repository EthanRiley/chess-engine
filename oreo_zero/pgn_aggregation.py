import chess.pgn
import chess
import numpy as np
import json
#import Move class

integers = ['1', '2', '3', '4', '5', '6', '7', '8']

ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                '5': 3, '6': 2, '7': 1, '8': 0}

filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                'e': 4, 'f': 5, 'g': 6, 'h': 7}

with open("move_indeces.json", "r") as f:
    move_indeces = json.load(f)

move_indeces = dict(move_indeces)

def reformat_FEN(fen):
    new_fen = ""
    for char in fen:
        if char in integers:
            for i in range(int(char)):
                new_fen += "-"
        else:
            new_fen += char
    return new_fen

def FEN_to_bitboards(fen):
    fen_info = fen.split(' ')
    board = fen_info[0]
    turn = fen_info[1]
    castling = fen_info[2]
    en_passant = fen_info[3]
    halfmove_clock = fen_info[4]
    fullmove_number = fen_info[5]
    board = reformat_FEN(board)
    bitboards = []
    create_piece_bitboard(board, bitboards, "P")
    create_piece_bitboard(board, bitboards, "N")
    create_piece_bitboard(board, bitboards, "B")
    create_piece_bitboard(board, bitboards, "R")
    create_piece_bitboard(board, bitboards, "Q")
    create_piece_bitboard(board, bitboards, "K")
    create_piece_bitboard(board, bitboards, "p")
    create_piece_bitboard(board, bitboards, "n")
    create_piece_bitboard(board, bitboards, "b")
    create_piece_bitboard(board, bitboards, "r")
    create_piece_bitboard(board, bitboards, "q")
    create_piece_bitboard(board, bitboards, "k")
    create_turn_bitboard(turn, bitboards)
    create_castling_bitboard(castling, bitboards)
    create_en_passant_bitboard(en_passant, bitboards)
    return bitboards

def create_piece_bitboard(fen, bitboards, char):
    board = np.zeros((8, 8))
    rows = fen.split('/')
    for row in range(len(rows)):
        for col in range(len(rows[row])):
            if rows[row][col] == char:
                board[row][col] = 1
            else:
                pass 
    bitboards.append(board)

def create_turn_bitboard(turn, bitboards):
    if turn == "w":
        bitboards.append(np.ones((8, 8)))
    else:
        bitboards.append(np.zeros((8, 8)))

def create_castling_bitboard(castling, bitboards):
    castling_keys = ["K", "Q", "k", "q"]
    if castling_keys == "-":
        for i in range(4):
            bitboards.append(np.zeros((8, 8)))
    else:
        for key in castling_keys:
            if key in castling:
                bitboards.append(np.ones((8, 8)))
            else:
                bitboards.append(np.zeros((8, 8)))

def create_en_passant_bitboard(en_passant, bitboards):
    if en_passant == "-":
        bitboards.append(np.zeros((8, 8)))
    else:
        board = np.zeros((8, 8))
        board[ranksToRows[en_passant[1]]][filesToCols[en_passant[0]]] = 1
        bitboards.append(board)


def move_notation_to_index(move):
    move = str(move)
    index = ''
    for char in move:
        if char in ranksToRows:
            index += str(ranksToRows[char])
        elif char in filesToCols:
            index += str(filesToCols[char])
        else:
            index += char
    actual_index = index[1]+index[0]+index[3]+index[2]
    if len(index) == 5:
        actual_index += "Q"
    return move_indeces[actual_index]

def result_to_winner(result):
    if result == "1-0":
        return 1
    elif result == "0-1":
        return -1
    else:
        return 0