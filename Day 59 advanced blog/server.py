import os
from flask import Flask, render_template, request
import requests
import smtplib
import dotenv

from blog import Blog
dotenv.load_dotenv()


app = Flask(__name__)

response = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
response.raise_for_status()
blogs = [Blog(x) for x in response.json()]


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        name = data['name']
        email = data['email']
        phone = data['phone']
        message = request.form['message']
        
        msg = f'Subject: New message from {name}\n\nName: {name}.\nEmail: {email}\nPhone: {phone}\n\n{message}'
        send_email(msg)
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


@app.route('/blog/<int:id>')
def get_blog(id):
    for blog in blogs:
        if blog.id == id:
            return render_template('post.html', blog=blog)


def send_email(msg: str) -> None:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Secure the connection
        connection.starttls()
        connection.login(user=os.getenv('MY_EMAIL'),
                         password=os.getenv('MY_PASSWORD'))
        connection.sendmail(from_addr=os.getenv('MY_EMAIL'),
                            to_addrs=os.getenv('MY_EMAIL'),
                            msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
