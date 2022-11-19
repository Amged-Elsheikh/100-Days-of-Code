from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField(label="username", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="password",
        validators=[DataRequired(),
                    Length(message="Password should contain 8 to 24 characters", 
                    min=8, max=24)])
    submit = SubmitField(label="submit")
