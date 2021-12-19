"""
This is a basic Blackjack game.
"""
import random


def sum_cards(player):
    """
    player is a list contains the cards which the player have
    """
    sum = 0  # To hold the score
    ace = 0  # Count the number of aces in player hand
    for card in board[player]:
        if card in "jqk":
            sum += 10
        elif card == "a":
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
        ace = -1
    return sum


def is_bust(sum):
    if sum > 21:
        return True
    return False


def draw_card(player):
    board[player].append(random.choice(deck))


def both_draw():
    draw_card("player")
    draw_card("dealer")


def dealer_hand(dealer):
    dealer_sum = sum_cards(board[dealer])
    while dealer_sum < 17:
        draw_card(board[dealer])
        dealer_sum = sum_cards(board[dealer])
    return dealer_sum


def is_blackjack_hand(player):
    if len(board[player]) == 2 and sum_cards(player) == 21:
        return True
    else:
        False


if __name__ == "__main__":
    deck = ("a", 2, 3, 4, 5, 6, 7, 8, 9, 10, "j", "q", "k")
    # initialize the player and the dealer
    board = {"player": [], "dealer": []}
    # Everyone draw 2 cards and show it
    print("Now evryone will get two cards, dealer 1st card will be shown, all players card will be shown")
    both_draw()
    both_draw()
    print(f"Dealer first card is: {board['dealer'][0]}")
    print(f"player 1 first card is: {board['player'][0]}")
    print(f"player 1 second card is: {board['player'][1]}")
    # #cHECK PLAYER AND DEALER SUM
    player_sum = sum_cards('player')
    dealer_sum = sum_cards("dealer")
    # Check for Blackjack
    if is_blackjack_hand("dealer") and not is_blackjack_hand("player"):
        print(f"dealer second card is {board['dealer'][0]}. Dealer got Blackjack. You LOST!")
    elif not is_blackjack_hand("dealer") and is_blackjack_hand("player"):
        print(f"You got Blackjack. You WON!")
    elif is_blackjack_hand("dealer") and is_blackjack_hand("player"):
        print(f"dealer second card is {board['dealer'][0]}. both got Blackjack. DRAW!")
    else: # if no one got blackjack
        print(f"Your cards sum is {player_sum}. ", end="")
        draw = True
        while draw:
            if input("Do you want to draw a new card? [y/n]").lower() == "y":
                draw_card("player")
                player_sum = sum_cards("player")
                if is_bust(player_sum):
                    print(f"Your score is {player_sum}. BUST! You LOST!")
                    break
            else:
                draw = False
        # Check dealer hand
    
    
