from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from apps.donor import blueprint
from apps.authentication.util import role_required
from apps.authentication.models import Donor, Food  
from flask_login import login_required, current_user
from apps import db
from apps.donor.forms import DonationForm
from datetime import datetime

@blueprint.route('/donor/profile')
@login_required
@role_required('donor')
def donor_profile():
    # Fetch donor-specific data
    # donor_data = Donations.query.filter_by(donor_id=current_user.id).all()
    return render_template('donor/profile.html', user=current_user) #, donor_data=donor_data)

# TODO edit as required

# @blueprint.route('/donor/donations', methods=['GET', 'POST'])
# @login_required
# @role_required('donor')
# def manage_donations():
#     if request.method == 'POST':
#         # Handle donation updates
#         donation_id = request.form['donation_id']
#         status = request.form['status']
#         # Update the database (example logic)
#         donation = Donations.query.get(donation_id)
#         donation.status = status
#         db.session.commit()
#         return redirect(url_for('donor_blueprint.donations_history'))
    
#     # Fetch donations for the logged-in donor
#     donations = Donations.query.filter_by(donor_id=current_user.id).all()
#     return render_template('donor/donations_history.html', donations=donations)


# donation_bp = Blueprint('donation', __name__)

# @donation_bp.route('/donation/new', methods=['GET', 'POST'])
@blueprint.route('/donor/new_donation', methods=['GET', 'POST'])
@login_required
def new_donation():
    form = DonationForm()
    if form.validate_on_submit():
        # Ensure current user is a donor
        if current_user.role != 'donor':
            flash('Only donors can log donations.', 'danger')
            return redirect(url_for('main.index'))

        # Fetch the donor ID from the donor table
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        if not donor:
            flash('Donor profile not found.', 'danger')
            return redirect(url_for('main.index'))

        # Create a new donation entry
        new_donation = Food(
            donor_id=donor.donor_id,
            quantity=form.quantity.data,
            donation_date=datetime.now().date(),
            expiry_date=form.expiry_date.data,
            food_type=form.food_type.data,
            item_type=form.item_type.data,
            food_name=form.food_name.data,
            food_description=form.food_description.data
        )
        db.session.add(new_donation)
        db.session.commit()
        
        flash('Donation successfully logged!', 'success')
        return redirect(url_for('main.index'))

    return render_template('donor/new_donation.html', form=form)
