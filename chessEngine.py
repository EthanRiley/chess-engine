'''
Class responsible for storing information about state of chess game
Determines valid moves at current position and keeps move log
'''
HEXAPAWN = "HEXAPAWN"
CHESS = "Chess"

class GameState():
    def __init__(self, gameMode=CHESS):
        '''
        Board is an 8x8 2 dimensional list
        Each element of the list is 2 characters
        1st character is color
        2nd Character represents piece type
        -- represents empty square
        '''

        self.gameMode = gameMode
        
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        
        self.hexapawnBoard = [
            ['bp', 'bp', 'bp'],
            ['--', '--', '--'],
            ['wp', 'wp', 'wp']]
        
        self.gardnerBoard = [
            ['bR', 'bN', 'bB', 'bQ', 'bK'],
            ['bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK']]

        self.moveFunctions = {
            'p': self.getPawnMoves,
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        '''
        Moves pieces and handles updates of all logical operators
        '''
        self.board[move.startRow][move.startCol] = '--' # Set row where piece moved from to nothing
        self.board[move.endRow][move.endCol] = move.pieceMoved # Set new square equal to piece moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # Update king location if moves
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        # If move is a Pawn Promotion then promote to queen (Need to add selection functionality)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        # If move was an en passant move then need special logic for clearing squares
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
        # More logic on en passant 
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)

        if move.isCastleMove: # Unique logic for castle move
            if move.endCol - move.startCol == 2: # If it is a kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else: # Else it is queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs))

    def undoMove(self):
        '''
        Resets board position based on move log
        '''
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() # Pop most recently added move out of the log
            self.board[move.startRow][move.startCol] = move.pieceMoved # Move piece back
            self.board[move.endRow][move.endCol] = move.pieceCaptured # Move piece that was just captured back
            self.whiteToMove = not self.whiteToMove
            # Update king's position if necessary
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:
                # we make the landing square blank as it was
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False

        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        if move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    def getValidMoves(self):
        '''
        Algorithm for checking moves
        Very slow, first place to make improvements
        '''
        moveFunction = {CHESS: self.getChessMoves,
                        HEXAPAWN: self.getHexapawnMoves,}
        return moveFunction[self.gameMode]()

    
    def getChessMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        # 1) Generate all possible moves
        moves, pieces = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # 3) generate all opponents moves
            # 4) for each of your opponents moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        # 5) if they do attack your king, not a valid move
        if len(moves) == 0 or len(pieces) == 2:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        # to generate castle moves
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
    
    def getHexapawnMoves(self):
        moves, pieces = self.getAllPossibleMoves()
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.undoMove()
        if len(moves) == 0 or len(pieces) == 2:
            self.checkmate = True
        else:
            self.checkmate = False
            self.stalemate = False
        
        # Check if there is a queen on the board
        if self.isQueen():
            self.checkmate = True
        return moves

    def isQueen(self):
        for row in self.board:
            for column in row:
                if column[1] == 'Q':
                    return True
        return False
     
    def inCheck(self):
        '''
        Helper method for determinig if king is in check
        '''
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        '''
        Helper method for determining if a square is under attack
        Used for castling logic
        '''
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()[0]
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        '''
        Determines all possible moves before filtering for whether or not your king will be put in check
        Returns: moves (list), pieces (list)
        '''
        moves = []
        pieces = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '--':
                    pieces.append(self.board[r][c])
                team = self.board[r][c][0]
                if (team == 'w' and self.whiteToMove) or (team == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves, pieces
    

    def getPawnMoves(self, r, c, moves):
        '''
        Logic for pawn moves
        '''
        if self.whiteToMove:  # white pawn move
            if self.board[r - 1][c] == "--":  # the square in front of a pawn is empty
                # startSquare, endSquare, board
                moves.append(Move((r, c), (r - 1, c), self.board))
                # check if it possible to advance to squares in the first move
                if r-2 >= 0:
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # don't go outside the board from the left :)
                if (self.board[r - 1][c - 1][0] == "b"):  # there's an enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= len(self.board[0])-1:  # don't go outside the board from the right :)
                if (self.board[r - 1][c + 1][0] == "b"):  # there's an enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        else:  # black pawn move
            if self.board[r + 1][c] == "--":  # the square in front of a pawn is empty
                # startSquare, endSquare, board
                moves.append(Move((r, c), (r + 1, c), self.board))
                # check if it possible to advance to squares in the first move
                if r+2 <= len(self.board[0])-1:
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # don't go outside the board from the left :)
                if (self.board[r + 1][c - 1][0] == "w"):  # there's an enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c + 1 <= len(self.board[0])-1:  # don't go outside the board from the right :)
                if (self.board[r + 1][c + 1][0] == "w"):  # there's an enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        '''
        Logic for rook moves
        '''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Rooks can move up, down, left, and right
        enemyTeam = 'b' if self.whiteToMove else 'w' # Enemy pieces can be captured so need different logic for enemy pieces and friendly pieces
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # Make sure move doesn't go off the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # If square is empty, then its a legal move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyTeam: # If square has an enemy piece, move can be captured but then must break
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getBishopMoves(self, r, c, moves):
        '''
        Logic for Bishop moves
        Almost identical to Rook moves but directions are different
        '''
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Bishops move diagonally
        enemyTeam = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, len(self.board)):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < len(self.board) and 0 <= endCol < len(self.board):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyTeam:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        '''
        Logic for knight moves
        '''
        jumps = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyTeam = 'w' if self.whiteToMove else 'b'
        for j in jumps:
            endRow = r + j[0]
            endCol = c + j[1]
            if 0 <= endRow < len(self.board[0]) and 0 <= endCol < len(self.board[0]):
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTeam:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getQueenMoves(self, r, c, moves):
        '''
        Queen just moves like a rook and a bishop combined so no need for any unique code
        '''
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        '''
        Logic for king moves
        '''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        allyTeam = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTeam:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        '''
        '''
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if c+2 <= len(self.board[0])-1:
            if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
                if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if c-3 >= 0:
            if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                    not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def toHexapawn(self):
        self.gameMode = HEXAPAWN
        self.board = self.hexapawnBoard

    def toHexapawnNetworkInput(self):
        '''
        Converts the current board to a 1D array of 9 values
        1 for each piece and 0 for empty spaces
        '''
        input = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece == 'wP':
                    input.append(1)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece == 'bP':
                    input.appen(1)
                else:
                    input.append(0)
        for i in range(0, 1):
            if self.whiteToMove:
                input.append(1)
            else:
                input.append(0)
        return input

class Move():
    '''
    Class for handling moves and special move logic like en passant, castling, and promotion are handled here
    '''
    # Dictionaries for mapping row and column numbers to chess notation
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # If a pawn makes it the last rank then it promotes
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == len(board)-1):
            self.isPawnPromotion = True

        # If a move is en passant than piece captured logic must change (it doesn't capture an empty square)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"

        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            # DO THE SAME FOR PAWN PROMOTIONS

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
