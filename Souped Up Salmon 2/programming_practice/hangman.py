import random

while True:
    guesses = []
    a = ["egg", "black", "bathtub", "long", "snake", "tree", "funtech", "saxophone", "magic", "bean", "sausage"]

    b = random.choice(a)

    UserGuess = input("Guess a letter...")
    print("You have guessed: " + UserGuess)

    if UserGuess in b:
        print("The letter " + UserGuess + " is in the word")

    elif UserGuess not in b:
        print("The letter " + UserGuess + " is not in the word")

    for UserGuess in b:
        UserGuess in guesses

    print(guesses)


