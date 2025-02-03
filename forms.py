from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class chPWForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Change Password")


class createPostForm(FlaskForm):
    developer = StringField("Developer", validators=[DataRequired()])
    project = StringField("Project", validators=[DataRequired()])
    start_time = StringField("Start Time", validators=[DataRequired()])
    end_time = StringField("End Time", validators=[DataRequired()])
    diary_time = StringField("Diary Time", validators=[DataRequired()])
    time_worked = StringField("Time Worked", validators=[DataRequired()])
    repo = StringField("Repo", validators=[DataRequired()])
    dev_notes = StringField("Developer Notes", validators=[DataRequired()])
    submit = SubmitField("Create Post")
