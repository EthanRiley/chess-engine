def getAllPossibleMoves(self):
    moves = []
    for r in range(len(self.board)):
        for c in range(len(self.board[r])):
            team = self.board[r][c][0]
            if (team == 'w' and self.whiteToMove) or (team == 'b' and not self.whiteToMove):
                piece = self.board[r][c][1]
                if piece == 'p':
                    self.getPawnMoves(r, c, moves)
                    print(len(moves))
                elif piece == 'R':
                    self.getRookMoves(r, c, moves)
                    print(len(moves))
                elif piece == 'B':
                    self.getBishopMoves(r, c, moves)
                elif piece == 'N':
                    self.getKnightMoves(r, c, moves)
                elif piece == 'Q':
                    self.getQueenMoves(r, c, moves)
                elif piece == 'K':
                    self.getKingMoves(r, c, moves)
    return moves

def getValidMoves(self):
    moves = []
    self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
    if self.whiteToMove:
        kingRow = self.whiteKingLocation[0]
        kingCol = self.whiteKingLocation[1]
    else:
        kingRow = self.blackKingLocation[0]
        kingCol = self.blackKingLocation[1]
    if self.inCheck:
        if len(self.checks) == 1:
            moves = self.getAllPossibleMoves()
            # To block a check you must move a piece onto one of the squares between the piece and the king
            check = self.checks[0]
            checkRow = check[0]
            checkCol = check[1]
            pieceChecking = self.board[checkRow][checkCol]
            validSquares = []
            if pieceChecking[1] == 'N':
                validSquares = [(checkRow, checkCol)]
            else:
                for i in range(1, 8):
                    validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                    validSquares.append(validSquare)
                    if validSquare[0] == checkRow and validSquare[1] == checkCol:
                        break
            for i in range(len(moves) - 1, -1, -1):
                if moves[i].pieceMoved[1] != 'K':
                    if not (moves[i].endRow, moves[i].endCol) in validSquares:
                        moves.remove(moves[i])
        else: # Double check so king has to move
            self.getKingMoves(kingRow, kingCol, moves)
    else: # Not in check so all moves are fine
        moves = self.getAllPossibleMoves()

    return moves

def getPawnMoves(self, r, c, moves):
    piecePinned = False
    pinDirection = ()
    for i in range(len(self.pins)-1, -1, -1):
        if self.pins[i][0] == r and self.pins[i][1] == c:
            piecePinned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[1])
            break

    if self.whiteToMove:
        if self.board[r-1][c] == "--":
            if not piecePinned or pinDirection == (-1, 0):
                moves.append(Move((r, c), (r-1, c), self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r, c), (r-2, c), self.board))

        if c-1 >= 0: 
            if self.board[r-1][c-1][0] == 'b':
                if not piecePinned or pinDirection == (-1, -1):
                    moves.append(Move((r, c), (r-1, c-1), self.board))
        if c+1 <= 7:
            if self.board[r-1][c+1][0] == 'b':
                if not piecePinned or pinDirection == (-1, 1):
                    moves.append(Move((r, c), (r-1, c+1), self.board))

    else:
        if self.board[r+1][c] == "--":
            if not piecePinned or pinDirection == (1, 0):
                moves.append(Move((r, c), (r+1, c), self.board))
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r, c), (r+2, c), self.board))

        if c-1 >= 0: 
            if self.board[r+1][c-1][0] == 'w':
                if not piecePinned or pinDirection == (1, -1):
                    moves.append(Move((r, c), (r+1, c-1), self.board))
        if c+1 <= 7:
            if self.board[r+1][c+1][0] == 'w':
                if not piecePinned or pinDirection == (1, 1):
                    moves.append(Move((r, c), (r+1, c+1), self.board))

def getRookMoves(self, r, c, moves):
    piecePinned = False
    pinDirection = ()
    for i in range(len(self.pins)-1, -1, -1):
        if self.pins[i][0] == r and self.pins[i][1] == c:
            piecePinned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            if self.board[r][c][1] != 'Q':
                self.pins.remove(self.pins[i])
            break
    
    directions = ((-1, 0), (0, -1), (1, 0), (0,1))
    enemyColor = 'b' if self.whiteToMove else 'w'
    for d in directions:
        for i in range(1, 8):
            endRow = r + d[0] * i
            endCol = c + d[1] * i
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
            else: break

def getBishopMoves(self, r, c, moves):
    piecePinned = False
    pinDirection = ()
    for i in range(len(self.pins)-1, -1, -1):
        if self.pins[i][0] == r and self.pins[i][1] == c:
            piecePinned = True
            pinDirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break
    directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    enemyTeam = 'b' if self.whiteToMove else 'w'
    for d in directions:
        for i in range(1, 8):
            endRow = r + d[0] * i
            endCol = c + d[1] * i
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyTeam:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
            else: break

def getKnightMoves(self, r, c, moves):
    piecePinned = False
    for i in range(len(self.pins)-1, -1, -1):
        if self.pins[i][0] == r and self.pins[i][1] == c:
            piecePinned = True
            self.pins.remove(self.pins[i])
            break
    knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    allyColor = 'w' if self.whiteToMove else 'b'
    for m in knightMoves:
        endRow = r + m[0]
        endCol = r + m[1]
        if 0 <= endRow < 8 and 0<= endCol < 8:
            if not piecePinned:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endCol, endCol), self.board))

def getKingMoves(self, r, c, moves):
    rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
    colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
    allyTeam = 'w' if self.whiteToMove else 'b'
    for i in range(8):
        endRow = r + rowMoves[i]
        endCol = c + colMoves[i]
        if 0 <= endRow < 8 and 0 <= endCol < 8:
            endPiece = self.board[endRow][endCol]
            if endPiece[0] != allyTeam:
                if allyTeam == 'w':
                    self.whiteKingLocation = (endRow, endCol)
                else:
                    self.blackKingLocation = (endRow, endCol)
                inCheck, pins, checks = self.checkForPinsAndChecks()
                if not inCheck:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                if allyTeam == 'w':
                    self.whiteKingLocation = (r, c)
                else:
                    self.blackKingLocation = (r, c)