"""
This program should ask the for their age. If it is less than 0 (an age that shouldn't exist), it outputs an error message.
"""

age = input("Please enter an age: ")
if age > 0:
    print("That age doesn't exist!")
else:
    print("That's all good!")
