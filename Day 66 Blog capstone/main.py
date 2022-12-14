from functools import wraps
from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar

from forms import *


basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "posts.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

##CONFIGURE TABLE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comments", back_populates="commented_author")
    
    
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author = relationship("User", back_populates="posts")
    comments = relationship('Comments', back_populates='post')
    
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
    comment = db.Column(db.Text, nullable=False)
    post = relationship("BlogPost", back_populates='comments')
    commented_author = relationship("User", back_populates='comments')
    date = db.Column(db.String(250), nullable=False)

    
with app.app_context():
    db.create_all()
    
    
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)        
    return decorated_function


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)

@app.route("/post/<int:index>",  methods=['GET', 'POST'])
def show_post(index):
    requested_post = BlogPost.query.filter_by(id=index).first()
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        
        new_comment = Comments(comment=form.comment.data,
                               date=datetime.now().strftime("%B %d, %Y, %H:%m"),
                               commented_author=current_user,
                               post=requested_post)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', index=index))
    return render_template("post.html", post=requested_post, form=form)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/edit', methods=['POST', 'GET'])
@admin_only
def edit_post():
    post_id = request.args.get('post_id')
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(title=post.title, subtitle=post.subtitle,
                          body=post.body, author=post.author,
                          img_url=post.img_url)
        
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.body = edit_form.body.data
        post.author = edit_form.author.data
        post.img_url = edit_form.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', index=post_id))
    return render_template('make-post.html', form=edit_form, is_new=False)
    

@app.route('/new_post', methods=['GET', 'POST'])
@admin_only
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        db.session.add(BlogPost(title=form.title.data, subtitle=form.subtitle.data,
                                date = datetime.now().strftime("%B %d, %Y"),
                                body=form.body.data, author_id=current_user.id,
                                img_url=form.img_url.data))
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, is_new=True)

@app.route('/delete/<id>')
@admin_only
def delete_post(id):
    post = db.session.get(BlogPost, id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash("User Already exists")
            return render_template('register.html', form=form)
        else:
            username = form.username.data
            password = generate_password_hash(form.password.data)
            user = User(username=username, password=password,
                        email=email)
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template('register.html', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Wrong email address or password. Please try again")
            return render_template('login.html', form=form)
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)