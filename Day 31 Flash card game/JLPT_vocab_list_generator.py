import requests  # pip install requests
from bs4 import BeautifulSoup as bs  # pip install beautifulsoup4
import re
import pandas as pd
import os


def get_url(N: int):
    url = f"https://en.wiktionary.org/wiki/Appendix:JLPT/N{N}"
    if N in range(2, 6):
        pass
    elif N == 1:
        hiragana = ["あ", "か", "さ", "た", "な", "は", "ま", "や", "ら", "わ"]
        url = [f"{url}/{x}行" for x in hiragana]
    else:
        raise "JLPT exams are numbered from 1-5"
    return url


def get_jlpt_vocab(url: str):
    # Load the webpage content
    r = requests.get(url)
    # Convert to a beautiful soup object
    soup = bs(r.content)
    df = pd.DataFrame(columns=["Kanji", "Furigana", "translation"])
    pattern = "[a-zA-Z{}|\-]"

    items_list = soup.body.select("div.mw-parser-output li")
    for item in items_list:
        txt_ = item.text.split(" -")
        en = txt_.pop(-1)
        en.replace(",", ", ")
        txt_ = txt_[0].split(", ")
        if len(txt_) == 1:
            txt_.insert(0, "")
        for i in range(len(txt_)):
            txt_[i-1] = re.sub(pattern, '', txt_[i-1])
            txt_[i-1] = txt_[i-1].strip()
        new_row = {"Kanji": txt_[0], "Furigana": txt_[1], "translation": en}
        df = df.append(new_row, ignore_index=True)
    return df


if __name__ == '__main__':
    day = "31"
    if day not in os.getcwd():
        sub_folder = list(filter(lambda x: day in x, os.listdir()))
        if sub_folder:
            os.chdir(os.path.join(os.getcwd(), sub_folder[0]))
    for N in range(1, 6):
        url = get_url(N)
        if type(url) == str:
            df = get_jlpt_vocab(url)
        else:
            df = pd.DataFrame(columns=["Kanji", "Furigana", "translation"])
            for page in url:
                temp_df = get_jlpt_vocab(page)
                df = pd.concat([df, temp_df])
        df.to_csv(f"jp_words/JLPT N{N} vocab-list.csv", index=False)
        df.to_csv(f"N{N} to learn.csv", index=False)
