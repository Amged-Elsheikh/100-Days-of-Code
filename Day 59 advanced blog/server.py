from flask import Flask, render_template
import requests

from blog import Blog


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

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/blog/<int:id>')
def get_blog(id):
    for blog in blogs:
        if blog.id==id:
            return render_template('post.html', blog=blog)


if __name__ == "__main__":
    app.run(debug=True)