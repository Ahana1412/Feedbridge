# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import Email, DataRequired, Optional, Length
from wtforms import ValidationError

# login and registration     

class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])
    
# Registration form with role-specific fields
class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                           id='username_create',
                           validators=[DataRequired()])
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    role = SelectField('Role',
                       id='role_selector',
                       choices=[
                           ('', 'Please select'),
                           ('donor', 'Restaurant or Grocery Store'),
                           ('food_bank', 'Food Bank or NGO'),
                           ('volunteer', 'Volunteer')
                       ],
                       validators=[DataRequired()])   
    contact_number = StringField('Contact Number',
                                  validators=[DataRequired(), Length(max=15)])
    address = TextAreaField('Address', validators=[DataRequired()])
    
    # Donor-specific fields
    donor_name = StringField('Donor Name',
                           id='donor_name',
                           validators=[DataRequired()])
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
    foodbank_name = StringField('Food Bank Name',
                           id='foodbank_name',
                           validators=[DataRequired()])
