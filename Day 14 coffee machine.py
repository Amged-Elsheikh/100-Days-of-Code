from os import system
"""The coffe machine can take orders, check for payment and resources, deliver the coffee and return exchange, virtually.

If I returned to this project in the future, I will add a method to show the user available drinks only and reject if exchange is not possible (this is rear but can happen only if user keep giving 1000¥ notes)
"""

logo = '''
                                            o$$$$$$oo
                                        o$"        "$oo
                                        $   o""""$o  "$o
                                        "$  o  "o  "o   $
                                        "$   $o $   $   o$
                                        "$       o$"$  o$
                                        "$ooooo$$  $  o$
                                o$ """ $     " $$$   "  $
                            o$        $o    $$"   "   "
                            $$  $ " $   $$$o"$    o  o$"
                            $"  o "" $   $" "   o"  $$
                            $o  " "  $  o$"   o"  o$"
                            "$o    $$  $   o"  o$$"
                            ""o$o"$"  $oo"  o$"
                                o$$ $   $$$  o$$
                                o" o oo""  "" "$o
                            o$o" ""          $
                            $" " o"   " " "   "o
                            $$ "  "  o$ o$o "   $
                            o$ $  $  o$$ "  "   ""
                            o  $ $"  " "o      o$
                            $ o         $o$oo$""
                        $o $   o  o  o"$$
                        $o  o  $  $    "$o
                        $o  $   o  $  $ "o
                            $  $   "o  $  "o"$o
                            $   "   o   $   o $$
                    $o$o$o$o$$o$$$o$$o$o$$o$$o$$$o$o$o$o$o$o$o$o$o$ooo
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   " $$$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$      "$$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     o$$$$"
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ooooo$$$$
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""""
                    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        "$o$o$o$o$o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"""
            """""""""""""""""""""""""""""""""""""""""""""""""""""
                '''


def print_logo():
    system("cls")
    print(logo)


class CoffeeMachine:
    def __init__(self):
        # Turn On the machine
        self.working = False
        # Initialize resopurces
        self.__water = 7000
        self.__milk = 5000
        self.__coffee = 1000
        # Initialize coins count and profit
        self.__profit = 0
        self.__thousand_yen = 0
        self.__five_hundred_yen = 20
        self.__hundred_yen = 100
        self.__fifty_yen = 200
        self.__ten_yen = 500
        self.__orders_counter = {"Espresso": 0, "Latte": 0, "Cappuccino": 0}

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

    def turn_on(self):
        if not self.working:
            self.working = True
        else:
            print("Machine already ON")

    def get_report(self):
        self.__report()

    def take_order(self):
        if not self.working:
            if input("Machine is off. Do you want to turn it on? [y/n]").lower() == "y":
                self.working = True
            else:
                print("Machine is off.")
                return
        if self.working:
            screen = f"""Hello. How can I help you?
            [E]spresso: {self.__espresso['cost']}¥.
            [L]atte: {self.__latte['cost']}¥.
            [C]appuccino: {self.__cappuccino['cost']}¥
            turn off: to turn off the machine
            """
            print(screen)
            try:
                order = input(
                    "Enter the first character of the order only. If you want to take other action write it as it is. ").lower()
            except:
                order = "Nothing"
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
        elif order == "turn off":
            self.working = False
            print("Machine is closed")
            return
        else:
            print(
                "Sorry. Wrong order, I can't help you. This is your money back as it is.")
            input("Press Enter to to return to menu...")
            return
        total_payment, money_list = self.__take_money()
        print(f"You're paying {total_payment}¥")
        if total_payment < self.menu[order]["cost"]:
            print(
                f"Sorry you do not have enough money for {order}, it cost {self.menu[order]['cost']}. Here is your money back")
            input("Press Enter to continue.....")
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
                self.__return_change(
                    total_payment, self.menu[order]["cost"])
                # Count profit and update record history
                self.__profit += self.menu[order]["cost"]
                self.__orders_counter[order.title()] += 1
                input("Press Enter to continue.....")

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
        self.__money_counter["100 yen"] += money_list[2]
        self.__money_counter["50 yen"] += money_list[3]
        self.__money_counter["10 yen"] += money_list[4]

    def __return_change(self, total_payment, order_cost):
        change = total_payment - order_cost
        self.__total_money -= change
        print(f"Here is your {change}¥ change. Don't forget it please")
        returned_1000 = change // 1000
        change -= returned_1000*1000

        returned_500 = change // 500
        change -= returned_500*500

        returned_100 = change // 100
        change -= returned_100*100

        returned_50 = change // 50
        change -= returned_50*50

        returned_10 = change // 10
        change -= returned_10*10

        self.__money_counter["notes"] -= returned_1000
        self.__money_counter["500 yen"] -= returned_500
        self.__money_counter["100 yen"] -= returned_100
        self.__money_counter["50 yen"] -= returned_50
        self.__money_counter["10 yen"] -= returned_10

    def __report(self) -> str:
        report = f"""
        Available Resources:
                        Water: {self.__water} ml.
                        milk : {self.__milk} ml.
                        coffe: {self.__coffee} g.
        Money Status:
                        1000 notes: {self.__thousand_yen}.
                        500 yen coins: {self.__five_hundred_yen}.
                        100 yen coins: {self.__hundred_yen}.
                        50 yen coins: {self.__fifty_yen}.
                        10 yen coins: {self.__ten_yen}.
                        Total: {self.__total_money}¥
                        Total profit: {self.__profit}¥
        Orders Count:
                        Espresso: {self.__orders_counter["Espresso"]} order.
                        "Latte": {self.__orders_counter["Latte"]} order.
                        "Cappuccino": {self.__orders_counter["Cappuccino"]} order.

        #################### Report END ####################\n\n
        """
        print(report)


if __name__ == '__main__':
    machine_1 = CoffeeMachine()
    machine_1.turn_on()
    while machine_1.working:
        print_logo()
        machine_1.take_order()
    machine_1.get_report()
