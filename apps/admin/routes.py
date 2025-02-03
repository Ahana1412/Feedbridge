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
    """Admin-specific user management page."""
    return render_template('admin/orders.html', user=current_user)

@blueprint.route('/donations')
@login_required
@role_required('admin')
def admin_manage_donations():
    """Admin-specific user management page."""
    try:
        # Fetch donations made till now
        donations = Food.query.all()
        
        return render_template('donor/donation_history.html', donations=donations)
    
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
        # Fetch new pending users
        users = Users.query.filter_by(status='PendingApproval').all()
        
        return render_template('admin/approve_users.html', users=users)
    
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
