# -*- encoding: utf-8 -*-
"""
Routes for the Volunteer role.
"""

# TODO edit as required

from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from apps.volunteer import blueprint
from apps.authentication.util import role_required
from flask import render_template, jsonify
from datetime import date
import pymysql
import os
from dotenv import load_dotenv
from flask import url_for


load_dotenv()
# Fetch credentials from the environment file
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

def get_db_connection():
    """Establishes a connection to the database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@blueprint.route('/volunteer/profile')
@login_required
@role_required('volunteer')
def volunteer_profile():
    """Volunteer-specific profile page."""
    return render_template('volunteer/profile.html', user=current_user)

@blueprint.route('/deliver')
@login_required
@role_required('volunteer')
def volunteer_tasks():
    """View and manage volunteer tasks."""
    return render_template('volunteer/deliver.html', user=current_user)

@blueprint.route('/history')
@login_required
@role_required('volunteer')
def delivery_history():
    """Displays the volunteer's delivery history."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Query to fetch completed deliveries for the current volunteer
            query = """
            SELECT o.OrderID, f.Name AS FoodName, 
                   d.FirstName AS DonorFirstName, d.LastName AS DonorLastName, 
                   d.ContactNo AS DonorContact, fb.Name AS FoodBankName, 
                   fb.Address AS FoodBankAddress, fb.ContactNo AS FoodBankContact
            FROM orders o
            JOIN food f ON o.FoodID = f.FoodID
            JOIN donor d ON f.DonorID = d.DonorID
            JOIN foodbank fb ON o.FoodBankID = fb.FoodBankID
            WHERE o.Status = 'Received' AND o.VolunteerID = %s
            """
            cursor.execute(query, (current_user.id,))
            deliveries = cursor.fetchall()

        # Render the history page with the deliveries
        return render_template('volunteer/history.html', deliveries=deliveries)

    except Exception as e:
        flash(f"Error retrieving delivery history: {str(e)}", "danger")
        return redirect(url_for('volunteer_blueprint.volunteer_profile'))



@blueprint.route('/volunteer/assign/<int:order_id>', methods=['POST'])
@login_required
@role_required('volunteer')
def assign_order(order_id):
    """Assigns an order to the volunteer."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Update order status and assign the volunteer
            update_query = """
            UPDATE orders
            SET Status = 'VolunteerAssigned', VolunteerID = %s
            WHERE OrderID = %s AND Status = 'Pending'
            """
            cursor.execute(update_query, (current_user.id, order_id))
            connection.commit()

        flash("Order successfully assigned to you.", "success")
    except Exception as e:
        flash(f"Error assigning order: {str(e)}", "danger")

    return redirect(url_for('volunteer_blueprint.volunteer_tasks'))
