from wtforms import StringField, SubmitField, EmailField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', [Length(min=4, max=25), DataRequired()])
    email = EmailField('Email Address', [Length(min=6, max=35), DataRequired(), Email()])
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Register new account")
    
class CommentForm(FlaskForm):
    comment = CKEditorField('Add a comment', validators=[DataRequired()])
    submit = SubmitField("Comment")
    
    
class LoginForm(FlaskForm):
    email = EmailField('Email address', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField("Login")
    