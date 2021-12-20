from random import randint
from os import system
from time import sleep

logo = """

███╗░░██╗██╗░░░██╗███╗░░░███╗██████╗░███████╗██████╗░  ░██████╗░██╗░░░██╗███████╗░██████╗░██████╗██╗███╗░░██╗░██████╗░
████╗░██║██║░░░██║████╗░████║██╔══██╗██╔════╝██╔══██╗  ██╔════╝░██║░░░██║██╔════╝██╔════╝██╔════╝██║████╗░██║██╔════╝░
██╔██╗██║██║░░░██║██╔████╔██║██████╦╝█████╗░░██████╔╝  ██║░░██╗░██║░░░██║█████╗░░╚█████╗░╚█████╗░██║██╔██╗██║██║░░██╗░
██║╚████║██║░░░██║██║╚██╔╝██║██╔══██╗██╔══╝░░██╔══██╗  ██║░░╚██╗██║░░░██║██╔══╝░░░╚═══██╗░╚═══██╗██║██║╚████║██║░░╚██╗
██║░╚███║╚██████╔╝██║░╚═╝░██║██████╦╝███████╗██║░░██║  ╚██████╔╝╚██████╔╝███████╗██████╔╝██████╔╝██║██║░╚███║╚██████╔╝
╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝  ░╚═════╝░░╚═════╝░╚══════╝╚═════╝░╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░
"""


def print_logo():
    system("cls")
    print(logo)


def check_guess(num, target):
    if num == target:
        return True
    elif num > target:
        print(f"{num} is greater than the target number. Try a smaller number.")
    elif num < target:
        print(f"{num} is lower than the target number. Try a bigger number")
    return False

def guessing_game():
    # Create a list of numbers from which a random number will be choosen and get the random number
    print_logo()
    GAME_LAST_NUMBER = int(
        input("Select the maximum possible number for target. *It can't be less than 50*: ")
    )  # The last number in the range
    if GAME_LAST_NUMBER < 50:
        print(f"{GAME_LAST_NUMBER} is less than 50, value set to 50")
        GAME_LAST_NUMBER = 50
    target = randint(1,100)

    LEVEL = input("Choose the level from [e]asy or [h]ard: ").lower()
    if LEVEL == "e":
        life = 10
    elif LEVEL == "h":
        life = 5

    while life > 0:  # Play as long as you have lifes left
        print(f"You have {life} guess[es]")
        num = int(input(f"try to guess the number between [1, {GAME_LAST_NUMBER}]: "))
        if check_guess(num, target):
            print(f"AWESOME! you guessed the right number which was {target}. You WON!")
            break
        else:
            life -= 1
        if life == 0:
            print(f"Sorry, you LOST. the number was {target}")
    if input("\n\nDo you want to play again? [y/n]: ").lower() == "y":
        print("New game will start after 2 seconds")
        sleep(3)
        guessing_game()
    else:
        print("\n\nThanks for playing. Please come back again!")

if __name__=='__main__':
    guessing_game()