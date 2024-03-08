from ramda import *

# Helpers
@curry
def trace(message, x):
    print(message, repr(x))
    return x


grid = curry(lambda w, h, x: repeat(repeat(x, w), h))


# Program
new_board = grid(8, 8)

print(new_board(" "))
