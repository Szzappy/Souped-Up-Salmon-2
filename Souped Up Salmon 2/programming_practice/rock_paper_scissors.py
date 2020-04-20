import random
import time
while True:
    score = 0

    rock = 1
    paper = 2
    scissors = 3

    a = int(input("Rock (1), paper (2) or scissors (3)"))

    if a == 1:
        x = "rock"

    if a == 2:
        x = "paper"

    if a == 3:
        x = "scissors"

    b = random.randint(1, 3)

    if b == 1:
        y = "rock"

    if b == 2:
        y = "paper"

    if b == 3:
        y = "scissors"

    print("You have put: " + x)

    print("The other player has put: ")
    time.sleep(1)
    print(y)

    if a == b:
        print("Draw")
        print("")

    elif a == 2 and b == 1:
        print("You win!!")
        score += 1
        print("")

    elif a == 1 and b == 3:
        print("You win!!")
        score += 1
        print("")

    elif a == 2 and b == 1:
        print("You win!!")
        score += 1
        print("")

    elif a == 2 and b == 3:
        print("You lose!!")
        print("You got a score of " + str(score))
        print("")

    elif a == 3 and b == 1:
        print("You lose!!")
        print("You got a score of " + str(score))
        print("")

    elif a == 1 and b == 2:
        print("You lose!!")
        print("You got a score of " + str(score))
        print("")






