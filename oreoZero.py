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
        self.model = keras.models.load_model('oreo_zero/oreo_zero_v2.keras')
        self.move_indeces = move_indeces
        self.depth = depth

    def findBestMove(self, gs, dummy):
        '''
        Finds the best move for the given GameState object.
        '''
        network_output = self.model.predict(np.array([self.convert_game_state_to_input(gs)]))
        masked_output = [0 for x in range(0, 1836)]
        moves = gs.getChessMoves()
        for move in moves:
            move_index = self.get_network_output_index(move)
            masked_output[move_index] = network_output[0][0][move_index]
        best_move_index = np.argmax(masked_output)
        for move in moves:
            if self.get_network_output_index(move) == best_move_index:
                return move

    @staticmethod
    def convert_game_state_to_input(gs):
        '''
        Converts a GameState object into a numpy array that can be fed into the neural network.
        '''
        board = gs.board
        bitboards = []
        OreoZero.make_piece_input_layer(board, 'wp', bitboards)
        OreoZero.make_piece_input_layer(board, 'wN', bitboards)
        OreoZero.make_piece_input_layer(board, 'wB', bitboards)
        OreoZero.make_piece_input_layer(board, 'wR', bitboards)
        OreoZero.make_piece_input_layer(board, 'wQ', bitboards)
        OreoZero.make_piece_input_layer(board, 'wK', bitboards)
        OreoZero.make_piece_input_layer(board, 'bp', bitboards)
        OreoZero.make_piece_input_layer(board, 'bN', bitboards)
        OreoZero.make_piece_input_layer(board, 'bB', bitboards)
        OreoZero.make_piece_input_layer(board, 'bR', bitboards)
        OreoZero.make_piece_input_layer(board, 'bQ', bitboards)
        OreoZero.make_piece_input_layer(board, 'bK', bitboards)
        OreoZero.make_turn_input_layer(gs, bitboards)
        OreoZero.make_castling_input_layer(gs, bitboards)
        OreoZero.make_enpassant_input_layer(gs, bitboards)
        return np.array(bitboards)

    @staticmethod
    def make_piece_input_layer(board, piece, bitboards):
        '''
        Makes a layer of the neural network that represents a certain type of piece.
        '''
        piece_input_layer = np.zeros((8, 8))
        for r in range(len(board)):
            for c in range(len(board[r])):
                if board[r][c] == piece:
                    piece_input_layer[r][c] = 1
        bitboards.append(piece_input_layer)

    @staticmethod
    def make_turn_input_layer(gs, bitboards):
        '''
        Makes a layer of the neural network that represents whose turn it is.
        '''
        if gs.whiteToMove:
            turn_input_layer = np.ones((8, 8))
        else:
            turn_input_layer = np.zeros((8, 8))
        bitboards.append(turn_input_layer)

    @staticmethod
    def make_castling_input_layer(gs, bitboards):
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
    
    @staticmethod
    def make_enpassant_input_layer(gs, bitboards):
        '''
        Makes a layer of the neural network that represents which squares are en passant squares.
        '''
        enpassant_input_layer = np.zeros((8, 8))
        if gs.enpassantPossible != ():
            enpassant_input_layer[gs.enpassantPossible[0]][gs.enpassantPossible[1]] = 1
        bitboards.append(enpassant_input_layer)
    
    def get_move_probs(self, gs):
        '''
        Returns a list of probabilities for each move in the given position.
        '''
        network_input = self.convert_game_state_to_input(gs)
        network_input = np.array([network_input])
        move_probs = self.model.predict(network_input)[0]
        return move_probs
    
    def get_network_output_index(self, move):
        '''
        Returns the index of the move in the neural network's output.
        '''
        index = f"{move.startRow}{move.startCol}{move.endRow}{move.endCol}"
        if move.isPawnPromotion:
            index += "Q"
        return self.move_indeces[index]
    
    
    


