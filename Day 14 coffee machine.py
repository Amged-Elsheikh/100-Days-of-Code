from os import system
"""The coffe machine can take orders, check for payment and resources, deliver the coffee and return exchange, virtually."""

system("cls")


class CoffeeMachine:
    def __init__(self):
        # Initialize resopurces
        self.__water = 70
        self.__milk = 50
        self.__coffee = 500
        # Initialize coins count
        self.__thousand_yen = 0
        self.__five_hundred_yen = 20
        self.__hundred_yen = 100
        self.__fifty_yen = 200
        self.__ten_yen = 500

        self.__total_money = self.__thousand_yen*1000 + self.__five_hundred_yen * 500 +\
            self.__hundred_yen*100 + self.__fifty_yen*50 + self.__ten_yen*10

        self.__money_counter = {"10 yen": self.__ten_yen, "50 yen": self.__fifty_yen,
                                "100 yen": self.__hundred_yen, "500 yen": self.__five_hundred_yen,
                                "notes": self.__thousand_yen}
        # initialize menu prices. All prices in JPY
        self.__espresso = {"ingredients": {"water": 50, "milk": 0, "coffee": 18},
                           "cost": 200}
        self.__latte = {"ingredients": {"water": 200, "milk": 150, "coffee": 24},
                        "cost": 400}
        self.__cappuccino = {"ingredients": {"water": 250, "milk": 100, "coffee": 24},
                             "cost": 500}
        self.menu = {"espresso": self.__espresso,
                     "latte": self.__latte, "cappuccino": self.__cappuccino}

    def take_order(self):
        print("Hello. How can I help you?")
        print(
            f"[E]spresso: {self.__espresso['cost']}¥.\n[L]atte: {self.__latte['cost']}¥.\n[C]appuccino: {self.__cappuccino['cost']}¥")
        order = input(
            "I can only understand the first character :). Select please: ").lower()
        self.__fullfil_order(order)

    def __fullfil_order(self, order):
        if order[0] == "e":
            order = "espresso"
        elif order[0] == "l":
            order = "latte"
        elif order[0] == "c":
            order = "cappuccino"
        elif order == "report":
            self.__report()
            return
        else:
            print(
                "Sorry. Wrong order, I can't help you. This is your money back as it is.")
            return
        total_payment, money_list = self.__take_money()
        print(f"You're paying {total_payment}¥")
        if total_payment < self.menu[order]["cost"]:
            print(
                f"Sorry you do not have enough money for {order}, it cost {self.menu[order]['cost']}. Here is your money back")
        else:
            if self.__confirm_enough_resources(order):
                # deduct resources
                self.__water -= self.menu[order]["ingredients"]["water"]
                self.__milk -= self.menu[order]["ingredients"]["milk"]
                self.__coffee -= self.menu[order]["ingredients"]["coffee"]
                print(
                    f"Your {order} is ready. Please enjoy it! and come back again")
                # Add money first to make sure you have enough money for return
                self.__add_money(total_payment, money_list)
                self.__return_exchange(total_payment, self.menu[order]["cost"])

    def __take_money(self):
        thousnds = int(input("How many 1000 yen notes you want to insert? "))
        five_hundred = int(input("How many 500 yen coin you want to insert? "))
        hundred = int(input("How many 100 yen coin you want to insert? "))
        fifty = int(input("How many 50 yen coin you want to insert? "))
        ten = int(input("How many 10 yen coin you want to insert? "))
        total_payment = thousnds*1000 + five_hundred * 500 +\
            hundred*100 + fifty*50 + ten*10
        money_list = [thousnds, five_hundred, hundred, fifty, ten]
        return total_payment, money_list

    def __confirm_enough_resources(self, order: str):
        possible = True
        drink_needs = self.menu[order]["ingredients"]
        if self.__water < drink_needs["water"]:
            print("Sorry I do not have enough water.")
            possible = False
        if self.__milk < drink_needs["milk"]:
            print("Sorry I do not have enough milk")
            possible = False
        if self.__coffee < drink_needs["coffee"]:
            print("Sorry I do not have enough coffee")
            possible = False
        return possible

    def __add_money(self, total_payment, money_list):
        self.__total_money += total_payment
        self.__money_counter["notes"] += money_list[0]
        self.__money_counter["500 yen"] += money_list[1]
        self.__money_counter["100"] += money_list[2]
        self.__money_counter["50 yen"] += money_list[3]
        self.__money_counter["10 yen"] += money_list[4]

    def __return_exchange(self, total_payment, order_cost):
        exchange = total_payment - order_cost
        self.__total_money -= exchange
        print(f"Here is your {exchange}¥ exchange. Don't forget it please")
        returned_1000 = exchange // 1000
        exchange -= returned_1000*1000

        returned_500 = exchange // 500
        exchange -= returned_500*500

        returned_100 = exchange // 100
        exchange -= returned_100*100

        returned_50 = exchange // 50
        exchange -= returned_50*50

        returned_10 = exchange // 10
        exchange -= returned_10*10

        self.__money_counter["notes"] -= returned_1000
        self.__money_counter["500 yen"] -= returned_500
        self.__money_counter["100 yen"] -= returned_100
        self.__money_counter["50 yen"] -= returned_50
        self.__money_counter["10 yen"] -= returned_10
        assert(exchange == 0.0), f"Exchange is {exchange} Yen"

    def __report(self) -> str:
        print(
            f"Water: {self.__water} ml.\nmilk : {self.__milk} ml.\ncoffe: {self.__coffee} g.")
        print(
            f"1000 notes: {self.__thousand_yen}.\n500 yen coins: {self.__five_hundred_yen}.")
        print(
            f"100 yen coins: {self.__hundred_yen}.\n50 yen coins: {self.__fifty_yen}.")
        print(f"10 yen coins: {self.__ten_yen}.\nTotal: {self.__total_money}¥")
        print("Report End.\n\n")


if __name__ == '__main__':
    machine_1 = CoffeeMachine()

    machine_1.take_order()
    machine_1.take_order()
    machine_1.take_order()
    machine_1.take_order()
    machine_1.take_order()
    machine_1.take_order()
