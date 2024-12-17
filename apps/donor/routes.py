from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from apps.donor import blueprint
from apps.authentication.util import role_required
# from apps.models import Donations  # Example database model

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
