from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    body = CKEditorField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')


class EditPost(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    body = CKEditorField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')


class AddProject(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    about = CKEditorField('Write something')
    tags = StringField('Tags')
    demo_link = StringField('Live Demo Link')
    github_link = StringField('Github Link')
    submit = SubmitField('Submit')
