# Ask the user to enter the year they were born.
# When the user presses enter, print "You are __ years old."
# If the age is greater or equal to 18, print "You can vote."
# Otherwise, print "You cannot vote."

from datetime import date

thisYear = date.today().year

print('What year were you born.')
print('Please enter a year.')
year = input()
year = int(year)
age = thisYear - year
print('You are ' + str(age) + ' years old.')
if age >= 18:
    print("You can vote")
else:
    print("You cannot vote")


# year = 2014
# print('year '+str(year))
# print('year',year)
# print('year: %s' % year)
#print('You have ' + str(NUMBER_OF_GUESSES) + " guesses. Good luck.")

