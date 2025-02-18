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
from apps.notifications.backend import create_notification

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

from flask import flash, redirect, url_for

@blueprint.route('/deliver')
@login_required
@role_required('volunteer')
def volunteer_tasks():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = """
            SELECT o.OrderID, f.Name AS FoodName, 
                   fb.Name AS FoodBankName, fb.ContactNo AS FoodBankContact, fb.Address AS FoodBankAddress,
                   d.Name AS DonorName, 
                   d.ContactNo AS DonorContact, d.Address AS DonorAddress
            FROM orders o
            JOIN food f ON o.FoodID = f.FoodID
            JOIN donor d ON f.DonorID = d.DonorID
            JOIN foodbank fb ON o.FoodBankID = fb.FoodBankID
            WHERE o.Status = 'Pending' 
            """
            cursor.execute(query)
            tasks = cursor.fetchall()

        return render_template('volunteer/deliver.html', user=current_user, tasks=tasks)

    except Exception as e:
        flash("Failed to fetch delivery tasks. Please try again later.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('home_blueprint.home_page'))






@blueprint.route('/history')
@login_required
@role_required('volunteer')
def delivery_history():
    try:
        # Fetch the VolunteerID using current_user.id (which is the UserID in the users table)
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT VolunteerID FROM volunteer WHERE UserID = %s", (current_user.id,))
            volunteer = cursor.fetchone()

            if volunteer is None:
                flash('Volunteer profile not found.', 'error')
                return render_template('volunteer/history.html', deliveries=[])

            volunteer_id = volunteer['VolunteerID']

        # Fetch deliveries for the logged-in Volunteer user using VolunteerID
        query = """
        SELECT o.OrderID, f.Name AS FoodName, 
               d.Name AS DonorName, 
               d.ContactNo AS DonorContact, fb.Name AS FoodBankName, 
               fb.Address AS FoodBankAddress, fb.ContactNo AS FoodBankContact
        FROM orders o
        JOIN food f ON o.FoodID = f.FoodID
        JOIN donor d ON f.DonorID = d.DonorID
        JOIN foodbank fb ON o.FoodBankID = fb.FoodBankID
        WHERE o.Status = 'Received' AND o.VolunteerID = %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, (volunteer_id,))
            deliveries = cursor.fetchall()

        # Return the deliveries in the template
        return render_template('volunteer/history.html', deliveries=deliveries)

    except Exception as e:
        flash(f"Error retrieving delivery history: {str(e)}", "danger")
        return redirect(url_for('volunteer_blueprint.volunteer_profile'))

@blueprint.route('/volunteer/assign/<int:order_id>', methods=['POST'])
@login_required
@role_required('volunteer')
def assign_order(order_id):
    """Assigns an order to the volunteer and sends notifications."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch the VolunteerID, Name, and Contact for the current user
            volunteer_query = "SELECT VolunteerID, FirstName, LastName, ContactNo FROM volunteer WHERE UserID = %s"
            cursor.execute(volunteer_query, (current_user.id,))
            volunteer = cursor.fetchone()

            if not volunteer:
                flash("You are not a registered volunteer.", "danger")
                return redirect(url_for('volunteer_blueprint.volunteer_tasks'))

            volunteer_id = volunteer['VolunteerID']
            volunteer_name = f"{volunteer['FirstName']} {volunteer['LastName']}"
            volunteer_contact = volunteer['ContactNo']

            # Update order status and assign the VolunteerID
            update_query = """
            UPDATE orders
            SET Status = 'VolunteerAssigned', VolunteerID = %s
            WHERE OrderID = %s AND Status = 'Pending'
            """
            cursor.execute(update_query, (volunteer_id, order_id))
            connection.commit()

            # Fetch the related Food Bank and Donor information
            details_query = """
            SELECT 
                fb.Name AS FoodBankName, fb.ContactNo AS FoodBankContact, fb.UserID AS FoodBankUserID,
                d.Name AS DonorName, d.ContactNo AS DonorContact, d.UserID AS DonorUserID
            FROM orders o
            JOIN foodbank fb ON o.FoodBankID = fb.FoodBankID
            JOIN food f ON o.FoodID = f.FoodID
            JOIN donor d ON f.DonorID = d.DonorID
            WHERE o.OrderID = %s
            """
            cursor.execute(details_query, (order_id,))
            details = cursor.fetchone()

            if not details:
                flash("Order details could not be found.", "danger")
                return redirect(url_for('volunteer_blueprint.volunteer_tasks'))

            # Send notification to the Food Bank
            food_bank_message = (
                f"Volunteer {volunteer_name} has taken up your delivery task. "
                f"Contact: {volunteer_contact}"
            )
            create_notification(details['FoodBankUserID'], "Volunteer Assigned", food_bank_message)

            # Send notification to the Donor
            donor_message = (
                f"Volunteer {volunteer_name} is delivering the food you donated. "
                f"Contact: {volunteer_contact}"
            )
            create_notification(details['DonorUserID'], "Volunteer Assigned", donor_message)

        flash("Order successfully assigned to you, and notifications have been sent.", "success")
        return redirect(url_for('volunteer_blueprint.thank'))

    except Exception as e:
        flash(f"Error assigning order: {str(e)}", "danger")
        return redirect(url_for('volunteer_blueprint.volunteer_tasks'))





@blueprint.route('/volunteer/thank')
@login_required
@role_required('volunteer')
def thank():
    return render_template('volunteer/thank.html')

