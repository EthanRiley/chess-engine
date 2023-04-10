import copy
import numpy as np
import math
import random as rnd
from oreoZero import *

WHITE = "WHITE"
BLACK = "BLACK"
OreoUtil = OreoZero()

class Edge():
    def __init__(self, move, parent_node): 
        self.parent_node = parent_node 
        self.move = move
        self.N = 0
        self.W = 0 
        self.Q = 0 
        self.P = 0

class Node():
    def __init__(self, board, parent_edge):
        self.board = board
        self.parent_edge = parent_edge
        self.child_edge_node = []

    def expand(self, network):
        moves = self.board.getChessMoves()
        for move in moves:
            child_board = copy.deepcopy(self.board)
            child_board.makeMove(move)
            child_edge = Edge(move, self)
            child_node = Node(child_board, child_edge)
            self.child_edge_node.append((child_edge, child_node))
        prediction_array = network.predict(np.array([OreoUtil.convert_game_state_to_input(self.board)]))
        prob_sum = 0
        for (edge, _) in self.child_edge_node:
            m_indx = self.OreoZero.get_network_output_index(edge.move)
            edge.P = prediction_array[0][0][m_indx] # probability of move
            prob_sum += edge.P
        for (edge, _) in self.child_edge_node:
            edge.P /= prob_sum
        evaluation = prediction_array[1][0][0]
        return evaluation
    
    def is_leaf(self):
        return self.child_edge_node == []
    
class MCTS():
    def __init__(self, network):
        self.network = network
        self.rootNode = None
        self.tau = 1.0
        self.c_puct = 5

    def uct_value(self, edge, parentN):
        return self.c_puct * edge.P * (math.sqrt(parentN) / (1 + edge.N))
    
    def select(self, node):

        if(node.is_leaf()):
            return node
        
        else:
            max_uct_child = None
            max_uct_value = -100000000
            for (edge, child_node) in node.child_edge_node:
                uct_val = self.uct_value(edge, edge.parent_node.parent_edge.N)
                val = edge.Q

                if(edge.parent_node.board.whiteToMove == False):
                    val = -edge.Q

                uct_val_child = val + uct_val
                if(uct_val_child > max_uct_value):
                    max_uct_child = child_node
                    max_uct_value = uct_val_child
            
            all_best_childs = []
            for (edge, child_node) in node.child_edge_node:
                uct_val = self.uct_value(edge, edge.parent_node.parent_edge.N)
                val = edge.Q
                if(edge.parent_node.board.whiteToMove == False):
                    val = -edge.Q
                uct_val_child = val + uct_val
                if(uct_val_child == max_uct_value):
                    all_best_childs.append(child_node)

            if(max_uct_child == None):
                raise ValueError("could not identify child with best uct value")
            else:
                if(len(all_best_childs) > 1):
                    indx = rnd.randint(0, len(all_best_childs)-1)
                    return self.select(all_best_childs[indx])
                else:
                    return self.select(max_uct_child)
    
    def expand_and_evaluate(self, node, max_depth=5, current_depth=0):

        if node.board.checkmate == True:
            terminal = node.board.checkmate
            winner = node.board.winner
            if winner == WHITE:
                v = 1
            elif winner == BLACK:
                v = -1
            self.backpropagate(v, node.parent_edge)
            return
        elif node.board.stalemate == True:
            terminal = node.board.stalemate
            v = 0
            self.backpropagate(v, node.parent_edge)
            return
        elif current_depth == max_depth:
            v = self.network.predict(np.array([OreoUtil.convert_game_state_to_input(node.board)]))[1][0][0]
            return
        v = node.expand(self.network)
        self.backpropagate(v, node.parent_edge)

    def backpropagate(self, v, edge):
        edge.N += 1
        edge.W = edge.W + v
        edge.Q = edge.W / edge.N
        if(edge.parent_node != None):
            if(edge.parent_node.parent_edge != None):
                self.backpropagate(v, edge.parent_node.parent_edge)

    def search(self, root_node):
        self.root_node = root_node
        _ = self.root_node.expand(self.network)
        for i in range(0, 100):
            selected_node = self.select(root_node)
            self.expand_and_evaluate(selected_node)
        N_sum = 0
        move_probs = []
        for (edge, _) in root_node.child_edge_node:
            N_sum += edge.N
        for (edge, node) in root_node.child_edge_node:
            prob = (edge.N ** (1/self.tau)) / ((N_sum) ** (1/self.tau))
            move_probs.append((edge.move, prob, edge.N, edge.Q))
        return move_probs
                
