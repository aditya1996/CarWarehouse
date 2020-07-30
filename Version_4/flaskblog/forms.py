from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class CarRegistrationForm(FlaskForm):

    make = StringField('Car Maker', validators=[DataRequired(), Length(min=2,max=30)])
    fueltype = StringField('Fuel Type', validators=[DataRequired(), Length(min=2,max=30)])
    bodystyle = StringField('Body Type', validators=[DataRequired(), Length(min=2,max=30)])
    horsepower = IntegerField('HorsePower', validators=[DataRequired()])
    citympg = IntegerField('City Mileage', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])

    submit = SubmitField('Add Entry')

class DeleteCar(FlaskForm):

    make = StringField('Car Maker', validators=[DataRequired(), Length(min=2,max=30)])
    price = IntegerField('Price', validators=[DataRequired()])

    submit = SubmitField('Delete this Car')