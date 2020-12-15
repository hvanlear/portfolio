import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models import Tag

from app.blog.forms import TagField

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    about = CKEditorField('Write something')
    demo_link = StringField('Live Demo Link')
    github_link = StringField('Github Link')
    tags = TagField('Tags')

    submit = SubmitField('Submit')