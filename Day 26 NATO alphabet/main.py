import pandas as pd
import os


df = pd.read_csv(os.path.join("Day 26 NATO alphabet",
                 "nato_phonetic_alphabet.csv"))

# TODO 1. Create a dictionary in this format:
NATO_dic = {row['letter']: row['code'] for (_, row) in df.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.
while True:

    name = input("Write your name or 'quit' to exit: ").upper()
    if name == "QUIT":
        break
    NATO = f""
    try:
        for ch in name:
            NATO = NATO + \
                f'{ch} as in {df["code"].loc[df["letter"]==ch].item()}\n'
        print(NATO)
    except KeyError:
        print("Sorry, input should contain alphapets only")
    except ValueError:
        print("Sorry, input should contain alphapets only")
