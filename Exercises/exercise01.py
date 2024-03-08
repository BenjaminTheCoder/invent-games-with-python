# Ask the user to enter the year they were born.
# When the user presses enter, print "You are __ years old."

from datetime import date

thisYear = date.today().year

print('What year were you born.')
print('Please enter a year.')
year = input()
year = int(year)
age = thisYear - year
print('You are ' + str(age) + ' years old.')

# year = 2014
# print('year '+str(year))
# print('year',year)
# print('year: %s' % year)
#print('You have ' + str(NUMBER_OF_GUESSES) + " guesses. Good luck.")

