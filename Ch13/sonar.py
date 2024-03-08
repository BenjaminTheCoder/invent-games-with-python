import random
import sys
import math

BOARD_WIDTH = 60
TENS = int(BOARD_WIDTH / 10.0)
BOARD_HEIGHT = 15
NUM_SONARS = 20
NUM_CHESTS = 3




def getNewBoard():

    board = []
    for x in range(BOARD_WIDTH):
        board.append([])
        for y in range(BOARD_HEIGHT):
            wave = random.choice(['~','='])
            board[x].append(wave)

    return board


def drawBoard(board):
    tensDigitsLine = '    '
    for i in range(1, TENS):
        tensDigitsLine += (' ' * 9) + str(i)

    print(tensDigitsLine)
    print('   ' + ('0123456789' * TENS))
    print()

    for row in range(BOARD_HEIGHT):
        if row < 10:
            extraSpace = ' '
        else:
            extraSpace = ''

        boardRow = ''
        for column in range(BOARD_WIDTH):
            boardRow += board[column][row]

        print('%s%s %s %s' % (extraSpace, row, boardRow, row))
        
    print()
    print('   ' + ('0123456789' * TENS))
    print(tensDigitsLine)

def getRandomChests(numChests):
    chests = []
    while len(chests) < numChests:
        newChest = [random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1)]
        if newChest not in chests:
            chests.append(newChest)
    return chests

def isOnBoard(x, y):
    return x >= 0 and x <= BOARD_WIDTH - 1 and y >= 0 and y <= BOARD_HEIGHT - 1

def makeMove(board, chests, x, y):
    smallestDistance = 1000
    for cx, cy in chests:
        distance = math.hypot(cx - x, cy - y)

        if distance < smallestDistance:            
            smallestDistance = distance
    smallestDistance = round(smallestDistance)

    if smallestDistance == 0:
        chests.remove([x, y])
        return 'You have found a sunken treasure chest!'
    else:
        if smallestDistance <= 9: # This has to be single character number (0-9) or it will mess up the board
            board[x][y] = str(smallestDistance)
            return 'Treasure chest detected at a distance of %s from the sonar device.' % smallestDistance
        else:
            board[x][y] = 'X'
            return 'Sonar did not detect anything. All treasure chests out of range.'

def enterPlayerMove(previousMoves):
    print('Where do you want to drop the next sonar device? (0-%s 0-%s) (or type quit)' % (BOARD_WIDTH-1, BOARD_HEIGHT-1))
    while True:
        move = input()
        if move.lower() == 'quit':
            print('Thanks for playing!')
            sys.exit()

        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]),int(move[1])):
            if [int(move[0]),int(move[1])] in previousMoves:
                print('You already moved there.')
                continue
            return [int(move[0]),int(move[1])]

        print('Enter a number from 0-%s, a space, then a number from 0-%s.' % (BOARD_WIDTH-1, BOARD_HEIGHT-1))

def showInstructions():
    print('''Instructions:
You are the captain of the Simon, a treasure-hunting ship. Your current mission
is to use sonar devices to find three sunken treasure chests at the bottom of
the ocean. But you only have cheap sonar that finds distance, not direction.

Enter the coordinates to drop a sonar device. The ocean map will be marked with
how far away the nearest chest is, or an X if it is beyond the sonar device's
range. For example, the C marks are where chests are. The sonar device shows a
3 because the closest chest is 3 spaces away.

1 2 3
012345678901234567890123456789012

0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
2 `~`C``3`~~~~`C`~~~~`````~~``~~~`` 2
3 ````````~~~`````~~~`~`````~`~``~` 3
4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

012345678901234567890123456789012
1 2 3
(In the real game, the chests are not visible in the ocean.)

Press enter to continue...''')
    input()

    print('''When you drop a sonar device directly on a chest, you retrieve it and the other
sonar devices update to show how far away the next nearest chest is. The chests
are beyond the range of the sonar device on the left, so it shows an X.

1 2 3
012345678901234567890123456789012

0 ~~~~`~```~`~``~~~``~`~~``~~~``~`~ 0
1 ~`~`~``~~`~```~~~```~~`~`~~~`~~~~ 1
2 `~`X``7`~~~~`C`~~~~`````~~``~~~`` 2
3 ````````~~~`````~~~`~`````~`~``~` 3
4 ~`~~~~`~~`~~`C`~``~~`~~~`~```~``~ 4

012345678901234567890123456789012
1 2 3

The treasure chests don't move around. Sonar devices can detect treasure chests
up to a distance of 9 spaces. Try to collect all 3 chests before running out of
sonar devices. Good luck!

Press enter to continue...''')
    input()


# main
print('S O N A R !')
print()
print('Would you like to view the instructions? (yes/no)')
if input().lower().startswith('y'):
    showInstructions()

while True:
    sonarDevices = NUM_SONARS
    theBoard = getNewBoard()
    theChests = getRandomChests(NUM_CHESTS)
    drawBoard(theBoard)
    previousMoves = []

    while sonarDevices > 0:
        print('You have %s sonar devices left. %s treasure chests remaining.' % (sonarDevices, len(theChests)))

        x, y = enterPlayerMove(previousMoves)
        previousMoves.append([x, y])

        moveResult = makeMove(theBoard, theChests, x, y)
        if moveResult == False:
            continue
        else:
            if moveResult == 'You have found a sunken treasure chest!':
                for x, y in previousMoves:
                    makeMove(theBoard, theChests, x, y)
            drawBoard(theBoard)
            print(moveResult)

        if len(theChests) == 0:
            print('You have found all the sunken treasure chests! Congratualtions and good game!')
            break

        sonarDevices -= 1

    if sonarDevices == 0:
        print('We\'ve run out of sonar devices!')
        print('Now we have to turn the ship around and head for home with treasure chests still out there!')
        print('Game over!')
        print('    The remaining chests were here:')
        for x, y in theChests:
            print('    %s %s ' % (x, y))

    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        sys.exit()
            

        
                
                
    







        































        

    
        










































            
