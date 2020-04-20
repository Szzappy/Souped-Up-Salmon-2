"""
This program is supposed to generate a random number and keep asking the user for a number until the number is guessed
"""

from random import randint

random_number = randint(0, 9)
while True:
    number = input("Enter a number between 0 and 9:")
    if number == random_number:
        print("Well done!")
        break
    else:
        print("Try again!")

