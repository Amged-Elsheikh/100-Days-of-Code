from random import randint
from art import logo, vs
from data import data
from os import system


def print_logo():
    system("cls")
    print(logo)


# Select random A and B from data and make sure A and B do not equal
def get_data(A=None, B=None):
    """Get a random dic from the data and take case A and B to make sure you do not get the same past cases or equal cases."""
    case = data[randint(0, len(data) - 1)]
    while case == A or case == B:
        case = data[randint(0, len(data) - 1)]
    return case


def show_card(A, holder="A"):
    print(f"{holder} is {A['name'], A['description']} from {A['country']}.")


def show_battle(A, B):
    show_card(A, "A")
    print(vs)
    show_card(B, "B")


def highest_followers(A, B):
    return max(A["follower_count"], B["follower_count"])


def play_higher_lower():
    print_logo()
    # Initialize score
    score = 0
    # Initialize case A and case B
    A = B = None
    A = get_data()
    B = get_data(A=A)

    accounts = {"A": A, "B": B}
    # Let the user Choose which have more followers
    play = True
    while play:
        show_battle(accounts["A"], accounts["B"])
        user_choice = input(f"Which has more followers? [A] or [B] ").upper()
        if accounts[user_choice]["follower_count"] == highest_followers(A, B):
            print_logo()
            score += 1
            print(f"\nRight choice, you score is {score} point[s].\n")
            # make the write choice "A" and get new B
            if user_choice == "A":
                accounts["B"] = get_data(A, B)

            elif user_choice == "B":
                new_data = get_data(A, B)
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
