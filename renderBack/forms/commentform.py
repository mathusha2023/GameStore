from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class ReviewForm(FlaskForm):
    review = TextAreaField('Отзыв', validators=[InputRequired()])
    rating = IntegerField('Оценка', validators=[InputRequired(), NumberRange(min=0, max=5)])
