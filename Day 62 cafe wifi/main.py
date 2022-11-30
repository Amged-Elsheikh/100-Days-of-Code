from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL(False)])
    open_ = StringField('Open time', validators=[DataRequired()])
    close = StringField('Close time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=["✘", "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕" ])
    wifi = SelectField('WiFi Speed', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField('Power plug-in', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = {"Cafe Name": form.cafe.data,
                    "Location": form.location.data,
                    "Open": form.open_.data,
                    "Close": form.close.data,
                    "Coffee": form.coffee.data,
                    "Wifi": form.wifi.data,
                    "Power": form.power.data}
        df = pd.read_csv("Day 62 cafe wifi/cafe-data.csv")
        df = df.append(new_row, ignore_index=True)
        df.to_csv("Day 62 cafe wifi/cafe-data.csv")
        return redirect(url_for("home"))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    df = pd.read_csv("Day 62 cafe wifi/cafe-data.csv")
    return render_template('cafes.html', cafes=df)
        


if __name__ == '__main__':
    app.run(debug=True)
