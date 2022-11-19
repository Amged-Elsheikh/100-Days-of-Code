from flask import Flask, render_template
from forms import LoginForm
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "rf43er#@r$234vSDQE5778903R12eVRW!590@#C"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"]) 
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if (
            login_form.email.data == "admin@email.com"
            and login_form.password.data == "12345678"
        ):
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
