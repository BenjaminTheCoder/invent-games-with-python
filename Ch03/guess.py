# This is a Guess the Number game.
# Remember: Don't Repeat Yourself (DRY)
import random
from math import log2, ceil

HIGH_NUMBER = 100
EXTRA_GUESSES = 3
NUMBER_OF_GUESSES = int(ceil(log2(HIGH_NUMBER))) + EXTRA_GUESSES

guessesTaken = 0

print('Hello! What is your name?')
myName = input()

number = random.randint(1,HIGH_NUMBER)
print('Well, ' + myName + ', I am thinking of a number between 1 and ' + str(HIGH_NUMBER) + ".")
print('You have ' + str(NUMBER_OF_GUESSES) + " guesses. Good luck.")

for guessesTaken in range(NUMBER_OF_GUESSES):
    print('Take a guess.')
    guess = input()
    guess = int(guess)

    if guess < number:
        print('Your guess is too low.')

    if guess > number:
        print('Your guess is too high.')

    if guess == number:
        break

if guess == number:
    guessesTaken =str(guessesTaken + 1)
    print('Good job, '   + myName + '! You guessed my number in ' + guessesTaken +' guesses!')

if guess != number:
    number = str(number)
    print('Nope. The number I was thinking of was ' + number + '.')
