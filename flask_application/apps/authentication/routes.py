# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)


from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ResetPasswordForm
from apps.authentication.models import Users, Donor, FoodBank, Volunteer

from apps.authentication.util import verify_pass, hash_pass, role_required


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        user_id = request.form['username']
        password = request.form['password']

        user = Users.find_by_username(user_id) or Users.find_by_email(user_id)

        # Check if new user is approved
        if user and user.status == 'PendingApproval':
            # flash("Your account is pending approval. Please wait for admin approval.", "warning")
            return render_template('accounts/login.html', msg='Your account is pending approval. Please wait for admin approval!', form=login_form)

        if user and verify_pass(password, user.password):
            login_user(user)

            # Redirect based on role
            if user.role == 'donor' or 'food_bank' or 'volunteer' or 'admin':
                return redirect(url_for('home_blueprint.home_page')) 
        
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    return render_template('accounts/login.html', form=login_form)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)

    if 'register' in request.form:

        # Common fields for all roles
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Check if username or email already exists
        if Users.query.filter_by(username=username).first():
            return render_template('accounts/register.html',
                                   msg='Username already registered.',
                                   success=False,
                                   form=create_account_form)

        if Users.query.filter_by(email=email).first():
            return render_template('accounts/register.html',
                                   msg='Email already registered.',
                                   success=False,
                                   form=create_account_form)

        # Insert into Users table
        user = Users(username=username, email=email, password=password, role=role, status='PendingApproval')
        db.session.add(user)
        db.session.flush()  # Get the user's ID for foreign key relationships
        user_id = user.id

        # Role-specific logic
        if role == 'donor':
            name = request.form.get('donor_name')
            donor_type = request.form.get('donor_type')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')

            if not name or not donor_type:
                return render_template('accounts/register.html',
                                       msg='Please fill out all donor-specific fields.',
                                       success=False,
                                       form=create_account_form)
            donor = Donor(user_id=user_id, name=name, donor_type=donor_type, contact_number=contact_number, address=address)
            db.session.add(donor)

        elif role == 'food_bank':
            name = request.form.get('foodbank_name')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            if not name:
                return render_template('accounts/register.html',
                                       msg='Please fill out all food bank-specific fields.',
                                       success=False,
                                       form=create_account_form)
            food_bank = FoodBank(user_id=user_id, name=name, contact_number=contact_number, address=address)
            db.session.add(food_bank)

        elif role == 'volunteer':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            preferred_location = request.form.get('preferred_location')
            availability = request.form.get('availability')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            if not first_name or not last_name:
                return render_template('accounts/register.html',
                                       msg='Please fill out all volunteer-specific fields.',
                                       success=False,
                                       form=create_account_form)
            volunteer = Volunteer(user_id=user_id, first_name=first_name, last_name=last_name,
                                  preferred_location=preferred_location, availability=availability, contact_number=contact_number, address=address)
            db.session.add(volunteer)

        # Commit all changes to the database
        db.session.commit()

        logout_user()
        return render_template('accounts/register.html',
                               msg='User registered successfully!',
                               success=True,
                               form=create_account_form)

    return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login')) 

@blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_password_form = ResetPasswordForm()
    if 'reset' in request.form:
        user_id = request.form['username']
        new_password = request.form['new_password']

        user = Users.find_by_username(user_id) or Users.find_by_email(user_id)

        # Check if new user is approved
        if user and user.status == 'PendingApproval':
            return render_template('accounts/reset_password.html', msg='Your account is pending approval. Please wait for admin approval!', form=reset_password_form)

        else:
            user.password = hash_pass(new_password)
            db.session.commit()
            return render_template('accounts/reset_password.html',
                               msg='Your password has been reset successfully!',
                               success=True,
                               form=reset_password_form)
        
    return render_template('accounts/reset_password.html', form=reset_password_form) 


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
