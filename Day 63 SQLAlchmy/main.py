from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = "rf43er#@r$234vSDQE5778903R12eVRW!590@#C"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class BookForm(FlaskForm):
    book_name = StringField(label="Book name", validators=[DataRequired()])
    author = StringField(label="Author", validators=[DataRequired()])
    rating = StringField(label="Rating", validators=[DataRequired()])
    add_book = SubmitField(label="add book")
    

class BooksDB(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.FLOAT, nullable=False)

@app.route('/')
def home():
    all_books = db.session.query(BooksDB).all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    book_form = BookForm()
    if request.method == 'POST':
        if book_form.validate_on_submit:
            new_book = BooksDB(book_name = book_form.book_name.data,
                               author = book_form.author.data,
                               rating = book_form.rating.data)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html', form=book_form)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RECORD
        book_id = int(request.form["id"])
        print(f"{book_id} {50*'*'}")
        book_to_update = BooksDB.query.get(book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    
    book_id = request.args.get('id')
    book_selected = BooksDB.query.get(book_id)
    return render_template("edit.html", book=book_selected)



@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = BooksDB.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
