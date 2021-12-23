"""
This is a simple encryption method. It receives a message and then shifts all the alphabets by a specific value.
"""
from string import ascii_lowercase


def caesar():
    while True:
        message = input("Type your message: ").lower()

        shift = int(input("Type the shift number: "))
        while shift > len(alphabets_list)-1:
            shift -= len(alphabets_list)

        direction = input(
            "Do you want to 'encrypt' or 'decrypt' the message: ").lower()
        if direction == 'decrypt':
            shift *= -1

        ceaser_message = ""
        for ch in message:
            ceaser_message += shift_character(ch, shift)
        print(f"Your message is:\n{ceaser_message}")
        i = input(f"Do you want to continue {direction}ing [y/n]? ")
        if i == "n":
            break
        elif i == "y":
            pass
        else:
            print(f"Unknown choice, assume finish {direction}ing")
            break


def shift_character(ch, shift):
    if ch in alphabets_list:
        # The character is the key to the dictionary.
        ch_id = alphabets[ch] + shift
        # confirm the index is not exceeding the number of alphabets while encrypting.
        if ch_id >= len(alphabets_list):
            return alphabets_list[ch_id-(len(alphabets_list))]
        elif ch_id < 0:  # confirm the index is not negative while decrypting.
            return alphabets_list[ch_id+(len(alphabets_list))]
        else:
            return(alphabets_list[ch_id])
    else:
        return ch  # In case of symbols or space, no change.


if __name__ == '__main__':
    alphabets_list = list(ascii_lowercase)
    alphabets = dict(zip(alphabets_list, list(
        range(len(alphabets_list)))))  # ch:number
    caesar()
