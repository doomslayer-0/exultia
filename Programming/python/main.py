import random
import sys


def guessGame():
    secretNum = random.randrange(1, 25)
    print("How many guesses do you want to have at your disposal?")
    guessAmount = int(input())
    while guessAmount > 0:
        print("Input your guess:")
        guessNum = int(input())
        print("Your guess is {}\n".format(guessNum))
        if guessNum == secretNum:
            print("You win!")
            break
        if guessNum != secretNum:
            if guessNum < secretNum:
                guessAmount -= 1
                print("Too small!\n")
                print("You have {} guesses left!\n".format(guessAmount))
                continue
            if guessNum > secretNum:
                guessAmount -= 1
                print("Too big!\n")
                print("You have {} guesses left!\n".format(guessAmount))
                continue
    else:
        print("You lose!")
    print("Do you want to play again?")
    answer = input()
    if answer in ('y', 'Y'):
        guessGame()
    else:
        sys.exit()


guessGame()
