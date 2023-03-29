'''
First 25 values is the location of the white pawns
Next 25 values is the location of the white knights
Next 25 values is the location of the white bishops
Next 25 values is the location of the white rooks
Next 25 values is the location of the white queens
Next 25 values is the location of the white king
Next 25 values is the location of the black pawns
Next 25 values is the location of the black knights
Next 25 values is the location of the black bishops
Next 25 values is the location of the black rooks
Next 25 values is the location of the black queens
Next 25 values is the location of the black king
Final 3 values is whos turn (1,1,1) if white to play (0, 0, 0) if black to play

5 layers in between (maybe? check book for reasoning)

policyHead that gives the probabilities for each move
Moves are generated assuming that there is a "superpiece" on each square
A superpiece is piece that can move like a queen and a knight
Need the promotion moves
Pawn on the final rank disappears and a queen appears in each respective vector
Need for the pawn push and capture in each direction

'''

mock_board = ['--', '--', '--', '--', '--',
              '--', '--', '--', '--', '--',
              '--', '--', '--', '--', '--',
              '--', '--', '--', '--', '--',
              '--', '--', '--', '--', '--']