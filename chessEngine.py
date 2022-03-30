'''
Class responsible for storing information about state of chess game
Determines valid moves at current position and keeps move log
'''
class GameState():
    def __init__(self):
        '''
        Board is an 8x8 2 dimensional list
        Each element of the list is 2 characters
        1st character is color
        2nd Character represents piece type
        -- represents empty square
        '''
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.whiteToMove = True
        self.moveLog = []