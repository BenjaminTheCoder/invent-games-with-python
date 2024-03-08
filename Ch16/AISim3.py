import random
import sys
import copy
from pprint import pprint
from ramda import *

WIDTH = 8
HEIGHT = 8
NUM_GAMES = 300

def drawBoard(board):
    print('  12345678')
    print(' +--------+')
    for y in range(0, HEIGHT):
        print('%s|'% (y+1), end='')
        for x in range(0, WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoardOrig():
    board = []
    for i in range(0, WIDTH):
        board.append([' ']*8)
    return board

def getNewBoard():
    # For some reason, this did NOT work: return [[' ']*8]*8
    return repeat(repeat(' ', WIDTH), HEIGHT)

def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        while isOnBoard(x,y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if isOnBoard(x,y) and board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip

def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def getBoardWithValidMoves(board, tile):
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        board[x][y] = '.'
    return boardCopy

def getValidMoves(board, tile):
    validMoves = []
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoardOrig(board):
    xscore = 0
    oscore = 0
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def getScoreOfBoard(board):
    countXs = pipe(filter(equals('X')), len)
    countOs = pipe(filter(equals('O')), len)
    getScores = pipe(unnest, lambda b: {'X': countXs(b), 'O': countOs(b)})
    return getScores(board)
    

def enterPlayerTile():
    tile =''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    if tile ==  'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    return random.choice(['computer','player'])

def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    return copy.deepcopy(board)

def isOnCorner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT -1)

def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter the column (1-8) and the row (1-8).')
            print('For example, 81 will move on the top-right corner.')
    return [x, y]

def getCornerBestMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def getWorstMove(board, tile):
    possibleMoves = getValidMoves(board, tile)
    random.shuffle(possibleMoves)

    worstScore = 64
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, tile, x, y)
        score = getScoreOfBoard(boardCopy)[tile]
        if score < worstScore:
            worstMove = [x, y]
            worstScore = score
            
    return worstMove

def getRandomMove(board, tile):
    possibleMoves = getValidMoves(board, tile)
    return random.choice(possibleMoves)

def isOnSide(x, y):
    return x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1

def getCornerSideBestMove(board, tile):
    possibleMoves = getValidMoves(board, tile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    for x, y in possibleMoves:
        if isOnSide(x, y):
            return [x, y]

    return getCornerBestMove(board, tile)

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s points.' % (scores[playerTile],scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn  = whoGoesFirst()
    # print('The ' + turn + ' will go first.')

    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board

        elif turn == 'player':
            if playerValidMoves != []:
##                if showHints:
##                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
##                    drawBoard(validMovesBoard)
##                else:
##                    drawBoard(board)
##                printScore(board, playerTile, computerTile)

                move = getCornerBestMove(board, playerTile)
##                if move == 'quit':
##                    print('Thanks for playing!')
##                    sys.exit()
##                elif move == 'hints':
##                    showHints = not showHints
##                    continue
##                else:
                makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer':
            if computerValidMoves != []:
##                drawBoard(board)
##                printScore(board, playerTile, computerTile)
                # input('Press Enter to see the computer\'s move.')
                move = getCornerSideBestMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'


xWins = oWins = ties = 0
print('Welcome to Othello!')

playerTile, computerTile = ['X', 'O'] # enterPlayerTile()

for i in range(0, NUM_GAMES): # while True:
    finalBoard = playGame(playerTile, computerTile)

    # drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('#%s: X scored %s points. O scored %s points.' % (i+1, scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        xWins += 1 # print('You beat the computer by %s points! Congratulations!' % (scores[playerTile]-scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        oWins += 1 # print('You lost. The computer beat you by %s points.' % (scores[computerTile]-scores[playerTile]))
    else:
        ties += 1 # print('The game is a tie!')

##    print('Do you want to play again? (yes or no)')
##    if not input().lower().startswith('y'):
##        break

print('X wins: %s (%s%%)' % (xWins, round(xWins / NUM_GAMES * 100, 1)))
print('O wins: %s (%s%%)' % (oWins, round(oWins / NUM_GAMES * 100, 1)))
print('Ties:   %s (%s%%)' % (ties, round(ties / NUM_GAMES * 100, 1)))







    
