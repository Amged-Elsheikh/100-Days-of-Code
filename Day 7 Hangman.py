"""
Hangman is a simple game for guessing something, in this case fruits
"""
import random
from os import system

system("cls")
stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']  # A visualization tool for the number of lifes

logo = ''' 
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/    '''

print(f'{logo}\n\n')


def create_hidden_word(target):
    current_word = list("-" * len(target))
    for i, ch in enumerate(target):
        if ch == " ":  # Space should be given
            current_word[i] = ch
    return current_word


def add_charcter_to_current(current_word, target, ch):
    for i, letter in enumerate(target):
        if ch == letter:
            current_word[i] = ch
    return current_word


def status(current_word, life):
    print(f"current word {''.join(current_word).title()}")
    print(f"You have {life} life(s) left\n")


def lost(life):
    if life <= 0:
        print(
            f"You've lost 🤕\nThe corrrect guess was {''.join(target).title()}\n"
        )
        return True
    else:
        status(current_word, life)
        return False


fruits = ["apple", "orange", "banana", "kiwi", "strawberry"]
cities = ["new york", "tokyo", "kyoto", "london", "paris", "khartoum"]

# Let user choose what they want to guess
source_dic = {"fruits": fruits, "cities": cities}

attr = input("Please select 'cities' or 'fruits': ")
if attr not in source_dic.keys():
    attr = random.choice(list(source_dic.keys()))
    print(f'You have written wrong input, you should guess from {attr}')

# Computer will choose the random word from the selected attribute
target = list(random.choice(source_dic[attr]).lower())
life = len(stages)-1  # The number of mistakes user can made
selected_ch = []  # a list  to handle repeated input from users
flag = False  # Flag to warn users not to continue enter same character again

current_word = create_hidden_word(target)
print("".join(current_word))
while True:
    ch = input("Please select a character: ").lower()
    system("cls")
    if ch not in selected_ch:  # Check if we used this character before
        selected_ch.append(ch)
    else:
        if not flag:  # No penelty for first repeat
            print(
                f"You have selected {ch.upper()}/{ch.lower()} before, from next time I will draw the hinge"
            )
            status(current_word, life)
            flag = True
            print(stages[life])
            continue
        else:
            print(
                f"You have selected {ch.upper()}/{ch.lower()} before, life reduced\n"
            )
            ch = None

    if ch in target:  # If the ch in the target word
        current_word = add_charcter_to_current(current_word, target, ch)
        if current_word == target:  # If all charcters were found
            print("YOU WON 🤠!!!!!!")
            print(f"The correct guess is: {''.join(current_word).title()}\n\n")
            break
        else:
            status(current_word, life)

    else:
        life -= 1
        print(stages[life])
        if lost(life):
            break
