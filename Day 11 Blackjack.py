"""
This is a basic Blackjack game.
"""
import random
from os import system

logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

deck = ("ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k")


def print_logo():
    system("cls")
    print(logo)


def sum_cards(player):
    """
    player is a list contains the cards which the player/dealer have
    """
    sum = 0  # To hold the score
    ace = 0  # Count the number of aces in player hand
    for card in player:
        if str(card) in "jqk":
            sum += 10
        elif card == "ace":
            ace += 1
        else:
            sum += card
    sum = handle_ace(sum, ace)
    return sum


def handle_ace(sum, ace):
    while ace != 0:
        if sum + 11 <= 21:
            sum += 11
        else:
            sum += 1
        ace -= 1
    return sum


def is_bust(sum):
    if sum > 21:
        return True
    return False


def draw_card(player):
    """
    player is a list contains the cards which the player/dealer have
    """
    player.append(random.choice(deck))


def initial_draw(player, dealer):
    """
    player is a list contains the cards which the player/dealer have
    """
    for _ in range(2):
        draw_card(player)
        draw_card(dealer)


def dealer_hand(dealer):
    """
    dealer is a list contains the cards which the dealer have
    """
    dealer_sum = sum_cards(dealer)
    print(f"Dealer cards are {dealer}.\nDealer sum is {dealer_sum}")
    while dealer_sum < 16:
        draw_card(dealer)
        dealer_sum = sum_cards(dealer)
        print(f"Dealer new card is {dealer[-1]}. Dealer cards are: {dealer}.\nDealer sum is {dealer_sum}")
    return dealer_sum


def is_blackjack_hand(player):
    if len(player) == 2 and sum_cards(player) == 21:
        return True
    else:
        False


def Blackjack():
    print_logo()
    # initialize the player and the dealer
    board = {"player": [], "dealer": []}
    # Everyone draw 2 cards and show it
    print(
        "Now evryone will get two cards, dealer 1st card will be shown, all players card will be shown"
    )
    initial_draw((board["player"]), (board["dealer"]))
    print(f"Dealer cards are: [{board['dealer'][0]}, *]")
    print(f"player 1 cards are: {board['player']}")
    # #cHECK PLAYER AND DEALER SUM
    player_sum = sum_cards(board["player"])
    dealer_sum = sum_cards(board["dealer"])
    # Check for Blackjack
    if is_blackjack_hand(board["dealer"]) and not is_blackjack_hand(board["player"]):
        print(
            f"dealer second card is {board['dealer'][0]}. Dealer got Blackjack. You LOST!"
        )

    elif not is_blackjack_hand(board["dealer"]) and is_blackjack_hand(board["player"]):
        print(f"You got Blackjack. You WON!")

    elif is_blackjack_hand(board["dealer"]) and is_blackjack_hand(board["player"]):
        print(f"dealer second card is {board['dealer'][0]}. both got Blackjack. DRAW!")

    else:  # if no one got blackjack
        print(f"Your cards sum is {player_sum}.")
        draw = True
        while draw:
            if input("Do you want to draw a new card? [y/n]: ").lower() == "y":
                draw_card(board["player"])
                print(
                    f"You draw {board['player'][-1]}. Your cards are: {board['player']}"
                )
                player_sum = sum_cards(board["player"])
                print(f"Your score is {player_sum}")
                if is_bust(player_sum):
                    draw = False
                    print(f"BUST! You LOST!")
                    print(
                        f"Dealer cards are {board['dealer']}.\nDealer sum is {dealer_sum}"
                    )
            else:
                draw = False
                # Check dealer hand
                dealer_sum = dealer_hand(board["dealer"])

                if is_bust(dealer_sum):
                    print("Dealer bust. You WON!")
                elif dealer_sum > player_sum:
                    print("You LOST!")
                elif dealer_sum < player_sum:
                    print("You WON!")
                elif dealer_sum == player_sum:
                    print("Draw")
    if input("Game end.\nDo you want to play again? [y/n]: ").lower() == "y":
        Blackjack()


Blackjack()
