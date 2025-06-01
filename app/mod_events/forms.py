from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired

# form for event creation
class CreateEventForm(FlaskForm):
    applying_event_for = SelectField("Applying event for", choices=[])
    event = StringField(
        "Event",
        validators=[
            InputRequired(),
        ],
    )
    description = StringField(
        "Description",
    )
    event_score = IntegerField(
        "Event score",
        validators=[
            InputRequired(),
        ],
    )
    event_date = DateField(
        "Event Date",
        format="%Y-%m-%d",  # Specify the expected input date format (e.g., YYYY-MM-DD)
        validators=[
            InputRequired(),
        ],
    )
    submit = SubmitField("Create Event")
