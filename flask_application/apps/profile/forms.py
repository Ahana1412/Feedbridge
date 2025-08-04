from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, Optional, Length
from wtforms import IntegerField, BooleanField

class ProfileUpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=13)])
    address = TextAreaField('Address', validators=[DataRequired()])

    # Donor-specific fields
    donor_name = StringField('Donor Name', validators=[DataRequired(), Length(max=100)])
    donor_type = SelectField('Donor Type',
                             choices=[
                                 ('', 'Please select'),
                                 ('Individual', 'Individual'),
                                 ('Restaurant', 'Restaurant'),
                                 ('GroceryStore', 'Grocery Store'),
                                 ('Others', 'Others')
                             ],
                             validators=[DataRequired()])

    # Volunteer-specific fields
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    preferred_location = StringField('Preferred Location', validators=[Optional(), Length(max=100)])
    availability = SelectField('Availability',
                               choices=[
                                   ('', 'Please select'),
                                   ('Weekdays', 'Weekdays'),
                                   ('Weekends', 'Weekends'),
                                   ('FullTime', 'Full-Time'),
                                   ('PartTime', 'Part-Time')
                               ],
                               validators=[Optional()])

    # Food Bank-specific fields
    foodbank_name = StringField('Food Bank Name', validators=[DataRequired(), Length(max=100)])
    capacity = IntegerField('Capacity', validators=[Optional()])
    accepts_non_veg = BooleanField('Accepts Non-Veg Food')
