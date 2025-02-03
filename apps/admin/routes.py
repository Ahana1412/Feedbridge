# -*- encoding: utf-8 -*-
"""
Routes for the Admin role.
"""

from flask import render_template, flash
from flask_login import login_required, current_user
from apps.admin import blueprint
from apps.authentication.util import role_required
from apps.authentication.models import Users, Donor, Food , Order, Volunteer, FoodBank
from apps import db



@blueprint.route('/donors')
@login_required
@role_required('admin')
def admin_manage_donors():
    """Admin-specific profile page."""
    return render_template('admin/donors.html', user=current_user)

@blueprint.route('/food_banks')
@login_required
@role_required('admin')
def admin_manage_food_banks():
    """Admin-specific user management page."""
    return render_template('admin/food_banks.html', user=current_user)

@blueprint.route('/volunteers')
@login_required
@role_required('admin')
def admin_manage_volunteers():
    """Admin-specific user management page."""
    return render_template('admin/volunteers.html', user=current_user)

@blueprint.route('/orders')
@login_required
@role_required('admin')
def admin_manage_orders():
    """Admin-specific order management page."""
    try:
        # Fetch orders made till now
        orders = Order.query.all()
        
        return render_template('admin/orders.html', orders=orders)
    
    except Exception as e:
        print(f"Error fetching order history: {e}")
        flash('An error occurred while fetching order history.', 'danger')
        return render_template('home/home.html')
    
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
            food = next((d for d in donations if d.food_id == order.food_id), None)
            food_bank = FoodBank.query.filter_by(foodbank_id=order.foodbank_id).first()
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
        
        return render_template('donor/order_history.html', orders=order_details)
    
    except Exception as e:
        print(f"Error fetching order history: {e}")
        flash('An error occurred while fetching order history.', 'danger')
        return render_template('home/home.html')
    


@blueprint.route('/donations')
@login_required
@role_required('admin')
def admin_manage_donations():
    """Admin-specific donor management page."""
    try:
        # Fetch donations made till now
        donations = Food.query.all()
        
        return render_template('admin/donations.html', donations=donations)
    
    except Exception as e:
        print(f"Error fetching donation history: {e}")
        flash('An error occurred while fetching donation history.', 'danger')
        return render_template('home/home.html')


# @blueprint.route('/new_users')
# @login_required
# @role_required('admin')
# def new_pending_users():
#     """Admin-specific new user approval page."""
#     try:
#         # Fetch new pending users
#         users = Users.query.filter_by(status='PendingApproval').all()
        
#         return render_template('admin/approve_users.html', users=users)
    
#     except Exception as e:
#         print(f"Error fetching new users: {e}")
#         flash('An error occurred while fetching new users.', 'danger')
#         return render_template('home/home.html')

@blueprint.route('/new_users')
@login_required
@role_required('admin')
def new_pending_users():
    """Admin-specific new user approval page."""
    try:
        # Fetch pending users
        users = Users.query.filter_by(status='PendingApproval').all()
        
        # Categorize users based on role
        donors, volunteers, foodbanks = [], [], []
        
        for user in users:
            if user.role == "donor":
                donor = Donor.query.filter_by(user_id=user.id).first()
                if donor:
                    donors.append({**user.__dict__, **donor.__dict__})

            elif user.role == "volunteer":
                volunteer = Volunteer.query.filter_by(user_id=user.id).first()
                if volunteer:
                    volunteers.append({**user.__dict__, **volunteer.__dict__})

            elif user.role == "food_bank":
                foodbank = FoodBank.query.filter_by(user_id=user.id).first()
                if foodbank:
                    foodbanks.append({**user.__dict__, **foodbank.__dict__})

        return render_template('admin/approve_users.html', 
                               donors=donors, 
                               volunteers=volunteers, 
                               foodbanks=foodbanks)

    except Exception as e:
        print(f"Error fetching new users: {e}")
        flash('An error occurred while fetching new users.', 'danger')
        return render_template('home/home.html')



@blueprint.route('/approve_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def approve_user(user_id):
    """Approve a new user."""
    try:
        user = Users.query.get(user_id)
        if user:
            user.status = 'Approved'
            db.session.commit()
            flash("User approved successfully!", "success")
            return render_template('admin/confirm_user_approval.html', 
                            msg='The user has been approved successfully!',
                            success=True)
        else:
            flash("User not found.", "danger")
            return render_template('admin/confirm_user_approval.html', 
                            msg='User not found!',
                            success=False)
        
    except Exception as e:
        print(f"Error approving user: {e}")
        db.session.rollback()  # Rollback in case of failure
        flash("An error occurred while approving the user.", "danger")
        return render_template('admin/confirm_user_approval.html', 
                            msg='There is some glitch. Try again later!',
                            success=False)
