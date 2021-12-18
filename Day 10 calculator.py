from os import system


"""Basic calculator code"""

logo = """
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""


def add(num1, num2):
    return num1 + num2


def multiply(num1, num2):
    return num1 * num2


def subtract(num1, num2):
    return num1 - num2


def divide(num1, num2):
    return num1 / num2


operation = {"+": add,
             "-": subtract,
             "*": multiply,
             "/": divide}

# Ask the user to enter to numbers and operation


def calculator():
    try:
        system("cls")
        print(logo)
        num1 = float(input("enter the first number: "))
        num2 = float(input("enter the next number: "))
        op = input("select operation: ")
        ans = operation[op](num1, num2)
        print(f"{num1} {op} {num2} = {ans}")
        flag = True
        while flag:
            check = input(
                "Choose [y]es to continue or [n]ew to start new calclator or anything else to quit: ").lower()
            if check == "y" or check == "yes":
                num2 = float(input("What is the next number? "))
                op = input("select operation: ")
                new_ans = operation[op](ans, num2)
                print(f"{ans} {op} {num2} = {new_ans}")
                ans = new_ans
            elif check == "n" or check == "new":
                flag = False
                calculator()
            else:
                flag = False
                print("close the calculator")
                break
    except KeyboardInterrupt:
        print("\nclose the calculator")
    except:
        print("Wrong input, close the calculator")


calculator()
