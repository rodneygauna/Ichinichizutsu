'''
Forms for the core pages of the application
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from src.dict import TODOS_STATUS


class TodoForm(FlaskForm):
    '''Form for the Todo page'''
    title = StringField('Title', validators=[
                        DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=TODOS_STATUS,
                         validators=[DataRequired()])
    submit = SubmitField('Submit')
