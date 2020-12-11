import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField, widgets, SelectField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, InputRequired, Length
from app.models import Tag, Post

class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            # Display tags as comma-seperated list.
            return ', '.join([tag.name for tag in self.data])
        return ''
    
    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        #filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        #query the database and tretrieve any tags we have already saved
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        #determin which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        #create list of unsaved Tag instances for new tags.
        new_tags = [Tag(name=name) for name in new_names]

        #return all existing tags + all new, unsaved tags
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired(), Length(max=100)])
    body = CKEditorField('Write something',
        validators=[DataRequired()])
    tags = TagField('Tags')
    submit = SubmitField('Submit')

