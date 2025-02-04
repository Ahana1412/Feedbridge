# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from sqlalchemy.orm import relationship
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from apps import db, login_manager
from apps.authentication.util import hash_pass
from sqlalchemy.exc import SQLAlchemyError


class InvalidUsage(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(100), unique=True)
    email         = db.Column(db.String(100), unique=True)
    password      = db.Column('password_hash', db.LargeBinary)
    role          = db.Column(ENUM('donor', 'food_bank', 'volunteer', 'admin'), nullable=False)
    status        = db.Column(ENUM('PendingApproval', 'Approved'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)

            setattr(self, property, value)

    def has_role(self, role):
        """Check if user has a specific role."""
        return self.role == role

    def __repr__(self):
        return str(self.username)

    @classmethod
    def find_by_email(cls, email: str) -> "Users":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username: str) -> "Users":
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id: int) -> "Users":
        return cls.query.filter_by(id=_id).first()
   
    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
          
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
    
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class Donor(db.Model):
    __tablename__ = 'donor'
    donor_id = db.Column('DonorID', db.Integer, primary_key=True)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column('Name', db.String(100), nullable=False)
    donor_type = db.Column('DonorType', db.Enum('Individual', 'Restaurant', 'GroceryStore', 'Others'), nullable=False)
    contact_number = db.Column('ContactNo', db.String(15), nullable=False)
    address = db.Column('Address', db.Text, nullable=False)

    user = db.relationship('Users', backref='donor', lazy=True) # to access email use - donor.user.email 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class FoodBank(db.Model):
    __tablename__ = 'foodbank'
    foodbank_id = db.Column('FoodBankID', db.Integer, primary_key=True)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column('Name', db.String(100), nullable=False)
    address = db.Column('Address', db.Text, nullable=False)
    contact_number = db.Column('ContactNo', db.String(15), nullable=False)

    user = db.relationship('Users', backref='foodbanks', lazy=True) 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class Volunteer(db.Model):
    __tablename__ = 'volunteer'
    volunteer_id = db.Column('VolunteerID', db.Integer, primary_key=True)
    user_id = db.Column('UserID', db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column('FirstName', db.String(50), nullable=False)
    last_name = db.Column('LastName', db.String(50), nullable=False)
    contact_number = db.Column('ContactNo', db.String(15), nullable=False)
    preferred_location = db.Column('PreferredLocation', db.String(100), nullable=True)
    availability = db.Column(db.Enum('Weekdays', 'Weekends', 'FullTime', 'PartTime'), nullable=False)
    address = db.Column('Address', db.Text, nullable=False)

    user = db.relationship('Users', backref='volunteers', lazy=True)

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class Food(db.Model):
    __tablename__ = 'food'
    food_id = db.Column('FoodID', db.Integer, primary_key=True)
    donor_id = db.Column('DonorID', db.Integer, db.ForeignKey('donor.DonorID'), nullable=False)
    food_name = db.Column('Name', db.String(100), nullable=False)  
    food_description = db.Column('Description', db.String(255), nullable=True) 
    quantity = db.Column('Quantity', db.Integer)
    donation_date = db.Column('DonationDate', db.Date, nullable=False)
    expiry_date = db.Column('ExpiryDate', db.Date, nullable=False)
    food_type = db.Column('FoodType', db.Enum('Veg', 'NonVeg'), nullable=False)
    item_type = db.Column('ItemType', db.Enum('Cooked', 'Grocery'), nullable=False)
    status = db.Column('Status', db.Enum('Available', 'Ordered'), nullable=False)  # Will be auto-calculated in MySQL

    # RemainingShelfLife is automatically calculated in the database.
    __mapper_args__ = {
        "exclude_properties": ["RemainingShelfLife"]
    }

    # Relationship with Donor (optional)
    # donor = db.relationship('donor', backref='food', lazy=True)

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column('OrderID', db.Integer, primary_key=True)
    food_id = db.Column('FoodID', db.Integer, db.ForeignKey('food.FoodID'), nullable=False)
    foodbank_id = db.Column('FoodBankID', db.Integer, db.ForeignKey('foodbank.FoodBankID'), nullable=False)
    volunteer_id = db.Column('VolunteerID', db.Integer, db.ForeignKey('volunteer.VolunteerID'), nullable=False)
    request_date = db.Column('RequestDate', db.Date, nullable=False)
    status = db.Column('Status', db.Enum('Pending', 'VolunteerAssigned', 'Completed'), nullable=False)

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        
    def delete_from_db(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return

    # Optional Relationship fields
    # food = db.relationship('Food', backref='orders', lazy=True)
    # foodbank = db.relationship('FoodBank', backref='orders', lazy=True)


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
