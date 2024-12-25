from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from apps.donor import blueprint
from apps.authentication.util import role_required
from apps.authentication.models import Donor, Food , Order, Volunteer, FoodBank
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


@blueprint.route('/orders', methods=['GET'])
@login_required
@role_required('donor')
def order_history():
    try:
        # Step 1: Fetch the donor record
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        
        if not donor:
            flash('Donor profile not found.', 'danger')
            return render_template('home/home.html')
        
        # Step 2: Fetch food donations by this donor with 'Ordered' status
        donations = Food.query.filter_by(donor_id=donor.donor_id, status='Ordered').all()
        
        if not donations:
            return render_template('donor/order_history.html', orders=[])
        
        # Step 3: Collect all food IDs from these donations
        food_ids = [donation.food_id for donation in donations]
        
        # Step 4: Fetch related orders using these food IDs
        orders = Order.query.filter(Order.food_id.in_(food_ids)).all()
        
        # Step 5: Prepare order details with food, volunteer, and food bank data
        order_details = []
        for order in orders:
            # Fetch related food item
            food = next((d for d in donations if d.food_id == order.food_id), None)
            
            # Fetch food bank details
            food_bank = FoodBank.query.filter_by(foodbank_id=order.foodbank_id).first()
            
            # Fetch volunteer details (if assigned)
            volunteer = Volunteer.query.filter_by(volunteer_id=order.volunteer_id).first() if order.volunteer_id else None
            
            order_details.append({
                'order_id': order.order_id,
                'food_id': food.food_id,
                'food_name': food.food_name,
                'food_description': food.food_description,
                'request_date': order.request_date,  
                'status': order.status,
                'foodbank_name': food_bank.name,
                'foodbank_contact': food_bank.contact_number,
                # 'foodbank_address': food_bank.address if food_bank else 'N/A',
                'volunteer_name': volunteer.first_name if volunteer else 'Not assigned',
                'volunteer_contact': volunteer.contact_number if volunteer else 'Not assigned'
            })
        
        # Step 6: Pass the order details to the template
        return render_template('donor/order_history.html', orders=order_details)
    
    except Exception as e:
        print(f"Error fetching order history: {e}")
        flash('An error occurred while fetching order history.', 'danger')
        return render_template('home/home.html')
