from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError
from wtforms.validators import Required,Email
from .. models import User, Blog, Comment

class BlogForm(FlaskForm):
    title = StringField('Blog title', validators = [Required()])
    content = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = StringField("", validators = [Required()])
    submit = SubmitField('Submit')