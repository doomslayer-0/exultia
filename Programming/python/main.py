import random
import sys

def guessGame():
    guessAmount = 5
    secretNum = random.randrange(1,25)
    while guessAmount > 0:
        print("Input your guess:")
        guessNum = int(input())
        print("Your guess is {}".format(guessNum))
        if guessNum == secretNum:
            print("You win!")
            break
        elif guessNum != secretNum:
            if guessNum < secretNum:
                guessAmount = guessAmount - 1
                print("Too small!")
                continue
            elif guessNum > secretNum:
                print("Too big!")
                guessAmount = guessAmount - 1
                continue
    else:
        print("You lose!")
    print("Do you want to play again?")
    answer = input()
    if answer == "y" or answer == "Y":
        guessGame()
    else:
        exit()

guessGame()
