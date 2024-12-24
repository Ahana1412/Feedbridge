# -*- encoding: utf-8 -*-
"""
Routes for the Food Bank role.
"""

# TODO edit as required

from flask import render_template, request, flash
from flask_login import login_required, current_user
from apps.food_bank import blueprint
from apps.authentication.util import role_required
from flask import render_template, jsonify
from apps.food_bank.backend import fetch_food_items
from datetime import date

@blueprint.route('/food_bank/profile')
@login_required
@role_required('food_bank')
def food_bank_profile():
    """Food Bank-specific profile page."""
    return render_template('food_bank/profile.html', user=current_user)
'''
@blueprint.route('/food_bank/order')
@login_required
@role_required('food_bank')
def food_bank_requests():
    """View and manage food requests."""
    return render_template('food_bank/order.html', user=current_user)
'''
@blueprint.route('/food_bank/order')
@login_required
@role_required('food_bank')
def food_bank_requests():
    """View and manage food requests."""
    try:
        donors = fetch_food_items()
        return render_template('food_bank/order.html', user=current_user, donors=donors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@blueprint.route('/thank', methods=['POST'])
@login_required
@role_required('food_bank')
def place_order():
    """Handles placing an order and recording it in the database."""
    try:
        # Retrieve form data
        food_id = request.form.get('donor_id')  # FoodID from the form
        food_bank_id = current_user.id           # Current FoodBank User ID

        # Insert the order into the database using backend function
        add_order(food_id, food_bank_id, date.today(), 'Pending')

        # Redirect to thank-you page
        flash('Order placed successfully!')
        return render_template('food_bank/thank.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@blueprint.route('/food_bank/history')
@login_required
@role_required('food_bank')
def order_history():
    """Displays the order history for the food bank."""
    try:
        food_bank_id = current_user.id  # Current FoodBank User ID

        # Fetch orders for the logged-in FoodBank user
        query = """
        SELECT o.OrderID, o.RequestDate, o.Status, f.FoodName, f.Description
        FROM orders o
        JOIN food f ON o.FoodID = f.FoodID
        WHERE o.FoodBankID = :food_bank_id
        """
        orders = db.session.execute(query, {'food_bank_id': food_bank_id}).fetchall()

        return render_template('food_bank/history.html', orders=orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500