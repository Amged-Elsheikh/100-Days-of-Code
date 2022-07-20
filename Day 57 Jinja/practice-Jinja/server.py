import requests
from flask import Flask, render_template
from datetime import datetime as dt


class GenderAge():
    def __init__(self, name):
        self.name = name
        self.__gender_guess()
        self.__age_guess()

    def __gender_guess(self):
        url = 'https://api.genderize.io'
        response = requests.get(url, params={'name': self.name})
        response.raise_for_status()
        self.gender = response.json()['gender']

    def __age_guess(self):
        url = 'https://api.agify.io'
        response = requests.get(url, params={'name': self.name})
        response.raise_for_status()
        self.age = response.json()['age']


current_year = dt.now().year

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', year=current_year)


@app.route('/guess/<string:name>')
def guess_game(name):
    user = GenderAge(name)
    return render_template('guess.html', name=user.name, 
                           gender=user.gender,
                           age=user.age,
                           year=current_year)


if __name__ == '__main__':
    app.run(debug=True)
