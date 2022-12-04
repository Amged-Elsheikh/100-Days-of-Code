import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, NumberRange
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_api = os.environ.get('THE_MOVIES_DB')
search_base_url = 'https://api.themoviedb.org/3/search/movie'
movie_details_base_url = 'https://api.themoviedb.org/3/movie'
image_base_url = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
Bootstrap(app)

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    year = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(), nullable=False)
    rating = db.Column(db.String(255))
    ranking = db.Column(db.String(255))
    review = db.Column(db.String(255))
    img_url = db.Column(db.String(255))


class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditForm(FlaskForm):
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(0, 10)])
    review = TextAreaField('add your Review')
    submit = SubmitField('Update')


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = MovieForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            params = {'api_key': TMDB_api, "query": form.title.data}
            results = requests.get(search_base_url, params=params).json()[
                'results']
            if results:
                return render_template('select.html', results=results)
    return render_template("add.html", form=form)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    movie_id = request.args.get("id")
    movie_details = requests.get(
        f"{movie_details_base_url}/{movie_id}?api_key={TMDB_api}").json()
    movie_in_db = Movie.query.get(movie_id)
    if not movie_in_db:
        movie_in_db = Movie(id=movie_id, title=movie_details['original_title'],
                            year=movie_details['release_date'][:4],
                            description=movie_details['overview'],
                            img_url=f"{image_base_url}{movie_details['poster_path']}")
        db.session.add(movie_in_db)
        db.session.commit()
    if request.method == 'POST':
        movie_in_db.rating = form.rating.data
        if form.review.data:
            movie_in_db.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("edit.html", movie=movie_in_db, form=form)
    


@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
