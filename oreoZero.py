from chessEngine import GameState, Move
import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
from oreo_zero.pgn_aggregation import move_indeces

'''
OreoZero is a neural network trained from online master games to try and play the best move in a given position.
'''

class OreoZero:
    def __init__(self, depth=3):
        self.model = keras.models.load_model('oreo_zero/oreo_zero_v1.keras')
        self.move_indeces = move_indeces
        self.depth = depth

    def convert_game_state_to_input(self, gs):
        '''
        Converts a GameState object into a numpy array that can be fed into the neural network.
        '''
        board = gs.board
        bitboards = []
        self.make_piece_input_layer(board, 'wp')
        self.make_piece_input_layer(board, 'wN')
        self.make_piece_input_layer(board, 'wB')
        self.make_piece_input_layer(board, 'wR')
        self.make_piece_input_layer(board, 'wQ')
        self.make_piece_input_layer(board, 'wK')
        self.make_piece_input_layer(board, 'bp')
        self.make_piece_input_layer(board, 'bN')
        self.make_piece_input_layer(board, 'bB')
        self.make_piece_input_layer(board, 'bR')
        self.make_piece_input_layer(board, 'bQ')
        self.make_piece_input_layer(board, 'bK')

    def make_piece_input_layer(self, board, piece, bitboards):
        '''
        Makes a layer of the neural network that represents a certain type of piece.
        '''
        piece_input_layer = np.zeros((8, 8))
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == piece:
                    piece_input_layer[r][c] = 1
        bitboards.append(piece_input_layer)

    def make_turn_input_layer(self, gs, bitboards):
        '''
        Makes a layer of the neural network that represents whose turn it is.
        '''
        if gs.whiteToMove:
            turn_input_layer = np.ones((8, 8))
        else:
            turn_input_layer = np.zeros((8, 8))
        bitboards.append(turn_input_layer)

    def make_castling_input_layer(self, gs, bitboards):
        '''
        Makes a layer of the neural network that represents which castling rights are available.
        '''
        if gs.currentCastlingRight.wks:
            wks_input_layer = np.ones((8, 8))
        else:
            wks_input_layer = np.zeros((8, 8))
        bitboards.append(wks_input_layer)
        if gs.currentCastlingRight.wqs:
            wqs_input_layer = np.ones((8, 8))
        else:
            wqs_input_layer = np.zeros((8, 8))
        bitboards.append(wqs_input_layer)
        if gs.currentCastlingRight.bks:
            bks_input_layer = np.ones((8, 8))
        else:
            bks_input_layer = np.zeros((8, 8))
        bitboards.append(bks_input_layer)
        if gs.currentCastlingRight.bqs:
            bqs_input_layer = np.ones((8, 8))
        else:
            bqs_input_layer = np.zeros((8, 8))
        bitboards.append(bqs_input_layer)
    
    def make_enpassant_input_layer(self, gs, bitboards):
        '''
        Makes a layer of the neural network that represents which squares are en passant squares.
        '''
        enpassant_input_layer = np.zeros((8, 8))
        if gs.enpassantPossible != ():
            enpassant_input_layer[gs.enpassantPossible[0]][gs.enpassantPossible[1]] = 1
        bitboards.append(enpassant_input_layer)
    

