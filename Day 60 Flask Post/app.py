from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/success/<username>')
def success(username):
   return f'<h1>welcome {username}</h1>'

@app.route("/login", methods=['GET', 'POST'])
def login_request():
    
    if request.method == 'POST':
        username = request.form['username']
        return f'<h1>welcome {username}</h1>'
    
    return render_template('index.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)