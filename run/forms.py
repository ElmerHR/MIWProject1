from flask_wtf import FlaskForm
from wtforms import DecimalRangeField
from wtforms.validators import DataRequired, InputRequired

# Class to create Flask form to retrieve parameters for making lifespan predictions
class getLifespanForm(FlaskForm):
    genetic = DecimalRangeField('genetic', validators=[InputRequired()])
    length = DecimalRangeField('length', validators=[InputRequired()])
    mass = DecimalRangeField('mass', validators=[InputRequired()])
    exercise = DecimalRangeField('exercise', validators=[InputRequired()])
    smoking = DecimalRangeField('smoking', validators=[InputRequired()])
    alcohol = DecimalRangeField('alcohol', validators=[InputRequired()])
    sugar = DecimalRangeField('sugar', validators=[InputRequired()])