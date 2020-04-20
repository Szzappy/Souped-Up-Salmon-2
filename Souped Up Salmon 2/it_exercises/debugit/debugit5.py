"""
This program is supposed to ask user for two numbers and output a grid of asterisks with O at user's position
e. g. User input is 2 and 1
Output should be:
******
**O***
******
******
******
******
"""
x_pos = int(input("Enter width, a number from 0 to 5: "))
y_pos = int(input("Enter height, a number from 0 to 5: "))

for y in range(0, 6):
    for x in range(0, 6):
        if x != x_pos and y != y_pos:
            print("*", end='')
        else:
            print("O", end='')
    print("")
