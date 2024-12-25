from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from apps.donor import blueprint
from apps.authentication.util import role_required
from apps.authentication.models import Donor, Food  
from flask_login import login_required, current_user
from apps import db
from apps.donor.forms import DonationForm
from datetime import datetime

# @blueprint.route('/donor')
# def route_default():
#     return redirect(url_for('home_blueprint.home_page'))


@blueprint.route('/profile')
@login_required
@role_required('donor')
def donor_profile():
    # Fetch donor-specific data
    # donor_data = Donations.query.filter_by(donor_id=current_user.id).all()
    return render_template('donor/profile.html', user=current_user) #, donor_data=donor_data)


@blueprint.route('/new_donation', methods=['GET', 'POST'])
@login_required
@role_required('donor')
def new_donation():
    form = DonationForm()

    if 'new_donation' in request.form:
        # Ensure current user is a donor
        if current_user.role != 'donor':
            return render_template('donor/new_donation.html',
                                       msg='Only donors can log donations.',
                                       success=False,
                                       form=form)

        # Fetch the donor ID from the donor table
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        if not donor:
            return render_template('donor/new_donation.html',
                                       msg='Donor profile not found.',
                                       success=False,
                                       form=form)

        # Create a new donation entry
        try:
            new_donation = Food(
                donor_id=donor.donor_id,
                quantity=form.quantity.data,
                donation_date=datetime.now().date(),
                expiry_date=form.expiry_date.data,
                food_type=form.food_type.data,
                item_type=form.item_type.data,
                food_name=form.food_name.data,
                food_description=form.food_description.data,
                status='Available'
            )
            db.session.add(new_donation)
            db.session.commit()
            return render_template('donor/thank.html',
                                       msg='Donation successfully logged!',
                                       success=True,
                                       form=form)
            # flash('Donation successfully logged!', 'success')

        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")
            flash('An error occurred while saving the donation.', 'danger')

    # print("Form submitted:", request.method)
    # print("Form valid:", form.validate_on_submit())
    # print("Form errors:", form.errors)

    return render_template('donor/new_donation.html', form=form)


@blueprint.route('/donations', methods=['GET'])
@login_required
@role_required('donor')
def donation_history():
    try:
        # Fetch the donor ID from the donor table
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        
        if not donor:
            flash('Donor profile not found.', 'danger')
            return render_template('home/home.html')

        # Fetch donations made by this donor
        donations = Food.query.filter_by(donor_id=donor.donor_id).all()
        
        return render_template('donor/donation_history.html', donations=donations)
    
    except Exception as e:
        print(f"Error fetching donation history: {e}")
        flash('An error occurred while fetching donation history.', 'danger')
        return render_template('home/home.html')

