from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from wtforms import ValidationError, TextAreaField
from database import db

class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('Comment',validators=[Length(min=1)])

    submit = SubmitField('Add Comment')

class PlayerForm(FlaskForm):
    class Meta:
        csrf = False

    player = TextAreaField('Player',validators=[Length(min=1)])

    submit = SubmitField('Add Player')

class TopicForm(FlaskForm):
    class Meta:
        csrf = False

    topic = TextAreaField('Topic',validators=[Length(min=1)])

    submit = SubmitField('Add Topic')

class BRNoteForm(FlaskForm):
    class Meta:
        csrf = False

    note = TextAreaField('Note',validators=[Length(min=1)])

    submit = SubmitField('Submit')

class BRCommForm(FlaskForm):
    class Meta:
        csrf = False

    comm = TextAreaField('Comment',validators=[Length(min=1)])

    submit = SubmitField('Submit')