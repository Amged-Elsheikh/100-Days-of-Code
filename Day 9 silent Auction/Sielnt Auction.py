from os import system

logo = '''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''


def make_logo():
    system("cls")
    print(logo)


def auctioneers_respond():
    auction = input("Are there any other bidders? [y/n]? ")
    while auction not in "yn":
        print("Unknown input, we will ask again.")
        auction = input("Are there any other bidders? [y/n]? ")
    return auction


def do_auction(Auctioneers, top_bidder):
    name = input("What is your name? ").title()
    bid = int(input("What's your bid? $"))
    Auctioneers[name] = bid
    if bid > Auctioneers[top_bidder]:
        top_bidder = name
    elif bid == Auctioneers[top_bidder]:
        print(f"Someone already bided {bid}$. priorty for the first bidder")
    return Auctioneers, top_bidder


if __name__ == "__main__":
    make_logo()
    initial_bid = int(input("Please enter the initial value for the bid: $"))
    top_bidder = "Initial Value"
    Auctioneers = {
        top_bidder: initial_bid
    }  # A dictionary that contains the name of the participans and their bid value

    make_logo()
    print(f"Welcome to the Secret Auction.")
    # #Initial bidder is essintial
    Auctioneers, top_bidder = do_auction(Auctioneers, top_bidder)

    auction = auctioneers_respond()
    make_logo()
    while True:
        if auction == "y":
            Auctioneers, top_bidder = do_auction(Auctioneers, top_bidder)
            auction = auctioneers_respond()
            make_logo()
        elif auction == "n":
            break

    if initial_bid >= Auctioneers[top_bidder]:
        print(f"item won't be sold since no one is bidding higher than {initial_bid}$")
    else:
        print(f"Auction closed at {Auctioneers[top_bidder]}$ for {top_bidder}")
