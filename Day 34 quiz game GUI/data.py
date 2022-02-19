import requests

def get_questions(amount=20, category=17, difficulty="medium"):
    parameters = {"amount": amount,
                "category": category,
                "difficulty": difficulty,
                "type": "boolean",}

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    questions = response.json()["results"]
    return questions

if __name__ == "__main__":
    print(get_questions()[0])