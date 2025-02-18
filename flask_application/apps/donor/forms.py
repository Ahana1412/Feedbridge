from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length

class DonationForm(FlaskForm):
    food_name = StringField('Food Name', validators=[DataRequired()])
    food_description = TextAreaField('Food Description', validators=[Optional()])
    food_type = SelectField('Food Type', choices=[
        ('', 'Please select'),
        ('Veg', 'Vegetarian'),
        ('NonVeg', 'Non-Vegetarian')
    ], validators=[DataRequired()])
    item_type = SelectField('Item Type', choices=[
        ('', 'Please select'),
        ('Cooked', 'Cooked'),
        ('Grocery', 'Grocery')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])
