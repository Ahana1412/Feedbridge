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

        order_details = []
        for order in orders:
            food = Food.query.filter_by(food_id=order.food_id).first()
            food_bank = FoodBank.query.filter_by(foodbank_id=order.foodbank_id).first()
            donor = Donor.query.filter_by(donor_id=food.donor_id).first()
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
                'donor_name': donor.name,
                'donor_contact': donor.contact_number,
                'volunteer_name': volunteer.first_name if volunteer else 'Not assigned',
                'volunteer_contact': volunteer.contact_number if volunteer else 'Not assigned'
            })
        
        return render_template('admin/orders.html', orders=order_details)
    
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
        food_items = Food.query.all()

        donation_details = []
        for food in food_items:
            donor = Donor.query.filter_by(donor_id=food.donor_id).first()
            
            donation_details.append({
                'food_id': food.food_id,
                'donor_id': food.donor_id,
                'donor_name': donor.name,
                'donor_type': donor.donor_type,
                'food_name': food.food_name,
                'food_description': food.food_description,
                'donation_date': food.donation_date,  
                'expiry_date': food.expiry_date,
                'food_type': food.food_type,
                'item_type': food.item_type,
                'status': food.status,
                'donor_contact': donor.contact_number
            })
        
        return render_template('admin/donations.html', donations=donation_details)
    
    except Exception as e:
        print(f"Error fetching donation history: {e}")
        flash('An error occurred while fetching donation history.', 'danger')
        return render_template('home/home.html')


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
        return render_template('admin/approve_users.html', 
                            msg='There is some glitch. Try again later!',
                            success=False)

@blueprint.route('/reject_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def reject_user(user_id):
    """Reject and delete a new user."""
    try:
        user = Users.query.get(user_id)
        if not user:
            flash("User not found.", "danger")
            return render_template('admin/confirm_user_rejection.html', 
                            msg='User not found.',
                            success=False)
        
        # Delete role-specific record first
        if user.role == "donor":
            Donor.query.filter_by(user_id=user.id).delete()
        elif user.role == "volunteer":
            Volunteer.query.filter_by(user_id=user.id).delete()
        elif user.role == "food_bank":
            FoodBank.query.filter_by(user_id=user.id).delete()
        
        # Delete the user record
        Users.query.filter_by(id=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        flash("User rejected and removed successfully!", "success")
        return render_template('admin/confirm_user_rejection.html', 
                            msg='The user has been rejected successfully!',
                            success=True)
    
    except Exception as e:
        print(f"Error rejecting user: {e}")
        db.session.rollback()
        flash("An error occurred while rejecting the user.", "danger")
        return render_template('admin/approve_users.html', 
                            msg='There is some glitch. Try again later!',
                            success=False)
