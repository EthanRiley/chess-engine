import copy
class Edge:
    def __init__(self, move, parentNode):
        self.N = self.W = self.Q = self.P = 0
        self.move = move
        self.parentNode = parentNode

class Node:
    def __init__(self, board, parentEdge):
        self.board = board
        self.parentEdge = parentEdge
        self.childEdgeNode = []

    def expand(self, network):
        moves = self.board.generateMoves()
        for m in moves:
            child_board = copy.deepcopy(self.board)
            child_board.applyMove(m)
    