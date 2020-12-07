from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models import Tag


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')




class AddProject(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    about = CKEditorField('Write something')
    demo_link = StringField('Live Demo Link')
    github_link = StringField('Github Link')
    tags = SelectField('Tags', coerce=int)

    submit = SubmitField('Submit')

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

# class TagForm(FlaskForm):
#     choices = MultiCheckboxField('Routes', coerce=int)
#     submit = SubmitField("Set User Choices")

