"""
Form definitions for creating and managing todos.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateField, SubmitField
from wtforms.validators import InputRequired, Optional


class CreateTodoForm(FlaskForm):
    todo = StringField(
        "Todo",
        validators=[InputRequired(message="Please enter a title for the todo.")],
    )
    description = TextAreaField("Description", validators=[Optional()])
    todo_score = IntegerField(
        "Todo Score",
        validators=[InputRequired(message="Please enter a score for the todo.")],
    )
    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d",
        validators=[InputRequired(message="Please enter a due date.")],
    )
    submit = SubmitField("Create Todo")
