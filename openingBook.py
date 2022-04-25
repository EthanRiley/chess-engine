from chessEngine import Move
class Repetoir:
    def __init__(self, startMove=('e2', 'e4'), e4Response=('e7', 'e5')):
        self.myRepetoir = {}
        self.startPos = self.pos_to_key([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']])
        
    @staticmethod
    def pos_to_key(pos):
        board_string = ''
        for x in pos:
            for y in x:
                board_string += y

        return board_string


    @staticmethod
    def chessToComputer(startSq, endSq):
        ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, 
                    '5': 3, '6': 2, '7': 1, '8': 0}
        filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                    'e': 4, 'f': 5, 'g': 6, 'h':7}
        return ((ranksToRows[startSq[1]], filesToCols[startSq[0]]), (ranksToRows[endSq[1]], filesToCols[endSq[0]]))

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
    
    def add_position_response(self, board, move_tuple, isCastleMove=False, isEnPassantMove=False):
        self.myRepetoir[Repetoir.pos_to_key(board)] = (Repetoir.chessToComputer(move_tuple[0], move_tuple[1]), isCastleMove, isEnPassantMove)

e4 = Repetoir()
e4.add_position_response(e4.startPos, (('e2'), ('e4')))
print(e4.myRepetoir)

'''
repetoirItalian = {# 1. e4
            [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]: [(6, 4), (4, 4)],

            # 1) e4 e5 Nf3
            [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', '--', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'bp', '--', '--', '--'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]: [(7, 6), (5, 5)],

            # e4 c5
            [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', '--', 'bp', 'bP', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', 'bp', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]: [(7, 6), (5, 5)],

            # e4 c6
            [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', '--', 'bp', 'bP', 'bp', 'bp', 'bp'],
            ['--', '--', 'bp', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]: [(6, 3), (4, 3)],


            # e4 e5 Nf3 Nc6 Bc4 
            [
            ['bR', '--', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', '--', 'bp', 'bp', 'bp'],
            ['--', '--', 'bN', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', 'bp', '--', '--', '--'],
            ['--', '--', '--', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', 'wN', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', '--', 'wR']]: [(7, 5), (4, 2)],

            #1) e4 e5 nf3 nf6 Bc4 Bc5 b4
            [
            ['bR', '--', 'bB', 'bQ', 'bK', '--', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', '--', 'bp', 'bp', 'bp'],
            ['--', '--', 'bN', '--', '--', '--', '--', '--'],
            ['--', '--', 'bB', '--', 'bp', '--', '--', '--'],
            ['--', '--', 'wB', '--', 'wp', '--', '--', '--'],
            ['--', '--', '--', '--', '--', 'wN', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', '--', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', '--', '--', 'wR']]: [(6, 1), (4, 1)]
}

repetoirItalian = {}
'''