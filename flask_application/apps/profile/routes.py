from flask import render_template, request, flash
from flask_login import login_required, current_user
from apps.profile import blueprint
from apps.authentication.models import Users, Donor, FoodBank, Volunteer
from apps import db
from apps.profile.forms import ProfileUpdateForm  


from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.profile import blueprint
from apps.authentication.models import Users, Donor, FoodBank, Volunteer
from apps import db
from apps.profile.forms import ProfileUpdateForm  # Import the form

@blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
def user_profile():
    """Fetch user role-specific details and update profile."""

    # Fetch the current logged-in user from the Users table
    user = Users.query.filter_by(id=current_user.id).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("profile_blueprint.user_profile"))

    form = ProfileUpdateForm()

    # Fetch role-specific details
    role_data = None
    if user.role == "donor":
        role_data = Donor.query.filter_by(user_id=user.id).first()
    elif user.role == "food_bank":
        role_data = FoodBank.query.filter_by(user_id=user.id).first()
    elif user.role == "volunteer":
        role_data = Volunteer.query.filter_by(user_id=user.id).first()

    # Pre-fill form with current user data
    if request.method == "GET" and role_data:
        form.email.data = user.email
        form.contact_number.data = role_data.contact_number
        form.address.data = role_data.address

        if user.role == "donor":
            form.donor_name.data = role_data.name
            form.donor_type.data = role_data.donor_type
        elif user.role == "food_bank":
            form.foodbank_name.data = role_data.name
        elif user.role == "volunteer":
            form.first_name.data = role_data.first_name
            form.last_name.data = role_data.last_name
            form.availability.data = role_data.availability
            form.preferred_location.data = role_data.preferred_location

    if 'update' in request.form:
        # if form.validate_on_submit():
            try:
                # **Update Users table**
                user.email = form.email.data

                # Ensure role-specific data exists before updating
                if role_data:
                    # **Update Donor table**
                    if user.role == "donor":
                        role_data.name = form.donor_name.data
                        role_data.donor_type = form.donor_type.data

                    # **Update FoodBank table**
                    elif user.role == "food_bank":
                        role_data.name = form.foodbank_name.data

                    # **Update Volunteer table**
                    elif user.role == "volunteer":
                        role_data.first_name = form.first_name.data
                        role_data.last_name = form.last_name.data
                        role_data.availability = form.availability.data
                        role_data.preferred_location = form.preferred_location.data

                    # **Common fields for all roles**
                    role_data.contact_number = form.contact_number.data
                    role_data.address = form.address.data

                    # **Commit changes**

                    print(db.session.dirty)  # Shows which objects are pending updates

                    db.session.commit()
                    flash("Profile updated successfully!", "success")
                    return render_template('profile.html', user=user, form=form, role_data=role_data)
                else:
                    flash("No associated role data found. Please contact admin.", "danger")

            except Exception as e:
                db.session.rollback()
                flash("An error occurred while updating your profile.", "danger")
                print(str(e))  # Debugging - Check error in logs

    return render_template('profile.html', user=user, form=form, role_data=role_data)


# @blueprint.route('/edit', methods=['GET', 'POST'])
# @login_required
# def user_profile():
#     """Fetch user role-specific details and update profile."""
    
#     user = Users.query.get(current_user.id)
#     form = ProfileUpdateForm()

#     # Fetch role-specific details
#     role_data = None
#     if user.role == "donor":
#         role_data = Donor.query.filter_by(user_id=user.id).first()
#     elif user.role == "food_bank":
#         role_data = FoodBank.query.filter_by(user_id=user.id).first()
#     elif user.role == "volunteer":
#         role_data = Volunteer.query.filter_by(user_id=user.id).first()

#     # Pre-fill form with current user data
#     if request.method == "GET" and role_data:
#         form.email.data = user.email
#         form.contact_number.data = role_data.contact_number
#         form.address.data = role_data.address

#         if user.role == "donor":
#             form.donor_name.data = role_data.name
#             form.donor_type.data = role_data.donor_type
#         elif user.role == "food_bank":
#             form.foodbank_name.data = role_data.name
#         elif user.role == "volunteer":
#             form.first_name.data = role_data.first_name
#             form.last_name.data = role_data.last_name
#             form.availability.data = role_data.availability
#             form.preferred_location.data = role_data.preferred_location

#     if form.validate_on_submit():
#         try:
#             # Update common fields
#             user.email = form.email.data
#             role_data.contact_number = form.contact_number.data
#             role_data.address = form.address.data

#             # Update role-specific fields
#             if user.role == "donor":
#                 role_data.name = form.donor_name.data
#                 role_data.donor_type = form.donor_type.data
#             elif user.role == "food_bank":
#                 role_data.name = form.foodbank_name.data
#             elif user.role == "volunteer":
#                 role_data.first_name = form.first_name.data
#                 role_data.last_name = form.last_name.data
#                 role_data.availability = form.availability.data
#                 role_data.preferred_location = form.preferred_location.data

#             db.session.commit()
#             # goto new page confirming update
#             flash("Profile updated successfully!", "success")
#             return render_template('profile.html', user=user, form=form, role_data=role_data)

#         except Exception as e:
#             db.session.rollback()
#             flash("An error occurred while updating your profile.", "danger")

#     return render_template('profile.html', user=user, form=form, role_data=role_data)



# @blueprint.route('/edit', methods=['GET', 'POST'])
# @login_required
# def user_profile():
#     """Fetch user role-specific details and allow profile updates."""
    
#     user = Users.query.get(current_user.id)
#     role_data = {}

#     # Fetch role-specific details
#     if user.role == "donor":
#         role_data = Donor.query.filter_by(user_id=user.id).first()
#     elif user.role == "food_bank":
#         role_data = FoodBank.query.filter_by(user_id=user.id).first()
#     elif user.role == "volunteer":
#         role_data = Volunteer.query.filter_by(user_id=user.id).first()

#     if request.method == "POST":
#         try:
#             # Update common fields
#             user.email = request.form.get("email", user.email)

#             # Update role-specific fields
#             if user.role == "donor":
#                 role_data.name = request.form.get("name", role_data.name)
#                 role_data.donor_type = request.form.get("donor_type", role_data.donor_type)
#                 role_data.contact_number = request.form.get("contact_no", role_data.contact_number)
#                 role_data.address = request.form.get("address", role_data.address)

#             elif user.role == "food_bank":
#                 role_data.name = request.form.get("name", role_data.name)
#                 role_data.contact_number = request.form.get("contact_no", role_data.contact_number)
#                 role_data.address = request.form.get("address", role_data.address)

#             elif user.role == "volunteer":
#                 role_data.first_name = request.form.get("first_name", role_data.first_name)
#                 role_data.last_name = request.form.get("last_name", role_data.last_name)
#                 role_data.contact_number = request.form.get("contact_no", role_data.contact_number)
#                 role_data.address = request.form.get("address", role_data.address)
#                 role_data.availability = request.form.get("availability", role_data.availability)
#                 role_data.preferred_location = request.form.get("preferred_location", role_data.preferred_location)

#             db.session.commit()
#             flash("Profile updated successfully!", "success")
#             # goto new page confirming update
#             return render_template('profile.html', user=user, role_data=role_data)

#         except Exception as e:
#             db.session.rollback()
#             print(f"Error updating profile: {e}")
#             flash("An error occurred while updating your profile.", "danger")

#     return render_template('profile.html', user=user, role_data=role_data)
