import random
HANGMAN_PICS =['''
  +---+
      |
      |
      |
     ===''','''  
  +---+
  O   |
      |
      |
     ===''','''
  +---+
  O   |
  |   |
      |
     ===''','''
  +---+
  O   |
 /|   |
      |
     ===''','''
  +---+
  O   |
 /|\  |
      |
     ===''','''
 +---+
  O  |
 /|\ |
 /   |
    ===''','''
 +---+
  O  |
 /|\ |
 / \ |
    ===''','''
 +---+
 [O  |
 /|\ |
 / \ |
    ===''','''
 +---+
 [O] |
 /|\ |
 / \ |
    ===''']

words = {'Colors':'red orange yellow green blue indigo violet white black brown pink'.split(),
         'Shapes':'square triangle rectangle circle ellipse rhombus trapezoid chevron pentagon hexagon septagon octagon'.split(),
         'Fruits':'apple orange lemon lime pear watermelon grape grapefruit cherry banana cantaloupe mango strawberry tomato'.split(),
         'Animals': '''ant baboon badger bat bear beaver camel cat clam cobra cougar
coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk
lion lizard llama mole monkey moose mouse mule newt otter owl panda
parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep
skunk sloth snake spider stork swan tiger toad trout turkey turtle
weasel whale wolf wombat zebra'''.split()}

def getRandomWord(wordDict):
    secretSet = random.choice(list(wordDict.keys()))
    secretWord = random.choice(list(wordDict[secretSet]))
    return [secretWord, secretSet]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMAN_PICS[len(missedLetters)])
    print()

    print ('Missed letters:', end=' ')
    for letter in missedLetters:
        print(letter, end=' ')
    print()

    blanks = '_' * len (secretWord)

    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print()


def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in alreadyGuessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess 

def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


print('H A N G M A N')

difficulty = 'X'
while difficulty not in ['E','M','H']:
    print('Enter difficulty: E - Easy, M - Medium, H - Hard')
    difficulty = input().upper()
if difficulty == 'M':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
if difficulty == 'H':
    del HANGMAN_PICS[8]
    del HANGMAN_PICS[7]
    del HANGMAN_PICS[5]
    del HANGMAN_PICS[3]

missedLetters = ''
correctLetters = ''
secretWord, secretSet = getRandomWord(words)
gameIsDone = False

while True:
    print('The secret word is in the set: ' + secretSet)
    displayBoard(missedLetters, correctLetters, secretWord)


    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters += guess


        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            print('Yes! the secret word is "' + secretWord + '"!  You have won!')
            gameIsDone = True
    else:
        missedLetters += guess

        if len(missedLetters) == len(HANGMAN_PICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('You have run out of guesses!\nAfter ' +
                  str(len(missedLetters)) + ' missed guesses and ' +
                  str(len(correctLetters)) + ' correct guesses, the word was "' +
                  secretWord + '"')
            gameIsDone = True

    if gameIsDone:
        if playAgain() == True:
            print('H A N G M A N')
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord, secretSet = getRandomWord(words)
        else:
            print('See you next time!')
            break 
