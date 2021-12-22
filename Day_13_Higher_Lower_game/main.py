from random import choice
from art import logo, vs
from data import data
from os import system


def print_logo():
    system("cls")
    print(logo)


def show_card(account):
    name = account["name"]
    description = account["description"]
    country = account["country"]
    return f" is {name}, {description} from {country}."


def show_battle(account_a, account_b):
    print("Account A" + show_card(account_a))
    print(vs)
    print("Account B" + show_card(account_b))


def get_data(account_a=None, account_b=None):
    """Get a random dic from the data and take case A and B to make sure you do not get the same past cases or equal cases."""
    case = choice(data)
    while case == account_a or case == account_b:
        case = choice(data)
    return case


def most_famous(account_a, account_b):
    """Winner is the one with the highest score"""
    return max(account_a["follower_count"], account_b["follower_count"])
    # highest_followers


def play_higher_lower():
    print_logo()
    # Initialize score
    score = 0
    # Initialize case A and case B
    account_a = account_b = None
    account_a = get_data()
    account_b = get_data(account_a=account_a)

    accounts = {"A": account_a, "B": account_b}
    # Let the user Choose which have more followers
    play = True
    while play:
        show_battle(accounts["A"], accounts["B"])
        user_choice = input(f"Which has more followers? [A] or [B] ").upper()
        if accounts[user_choice]["follower_count"] == most_famous(account_a, account_b):
            print_logo()
            score += 1
            print(f"\nRight choice, you score is {score} point[s].\n")
            # make the write choice "A" and get new B
            if user_choice == "A":
                accounts["B"] = get_data(account_a, account_b)


# TODO 

            elif user_choice == "B":
                new_data = get_data(account_a, account_b)
                accounts["A"] = accounts["B"]
                accounts["B"] = new_data

        else:
            print(f"Wrong choice. You Lost with {score} point[s].")
            play = False

            if input("Do you want to play again? [y/n] ").lower() == "y":
                play_higher_lower()
            else:
                break


if __name__ == "__main__":
    play_higher_lower()
