from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, Length

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