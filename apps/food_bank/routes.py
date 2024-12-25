# -*- encoding: utf-8 -*-
"""
Routes for the Food Bank role.
"""

# TODO edit as required

from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from apps.food_bank import blueprint
from apps.authentication.util import role_required
from flask import render_template, jsonify
from apps.food_bank.backend import fetch_food_items
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

@blueprint.route('/food_bank/profile')
@login_required
@role_required('food_bank')
def food_bank_profile():
    """Food Bank-specific profile page."""
    return render_template('food_bank/profile.html', user=current_user)

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
        food_id = request.form.get('food_id')  # FoodID from the form
        user_id = current_user.id              # Current User ID

        # 1. Retrieve the corresponding FoodBankID for the logged-in User
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT FoodBankID FROM foodbank WHERE UserID = %s", (user_id,))
            food_bank = cursor.fetchone()

            if not food_bank:
                raise Exception(f"No food bank found for user ID {user_id}")

            food_bank_id = food_bank['FoodBankID']

            # 2. Insert the order into the orders table
            order_query = """
            INSERT INTO orders (FoodID, FoodBankID, RequestDate, Status)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(order_query, (food_id, food_bank_id, date.today(), 'Pending'))
            connection.commit()

            # 3. Update the status of the food item to "Ordered"
            update_food_query = """
            UPDATE food
            SET Status = 'Ordered'
            WHERE FoodID = %s
            """
            cursor.execute(update_food_query, (food_id,))
            connection.commit()

        # Close the connection
        connection.close()

        # Flash success message and redirect to thank-you page
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
        # Step 1: Fetch the FoodBankID using current_user.id (which is the UserID in the users table)
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT FoodBankID FROM foodbank WHERE UserID = %s", (current_user.id,))
            food_bank = cursor.fetchone()

            if food_bank is None:
                flash('Food Bank profile not found.', 'error')
                return render_template('food_bank/history.html', orders=[])

            food_bank_id = food_bank['FoodBankID']

        # Step 2: Fetch orders for the logged-in FoodBank user using FoodBankID
        query = """
        SELECT o.OrderID, o.RequestDate, o.Status, 
               f.Name AS FoodName, f.Description, 
               d.Name AS DonorName, d.Address AS DonorAddress, d.ContactNo AS DonorContact,
               CONCAT(v.FirstName, ' ', v.LastName) AS VolunteerName, v.ContactNo AS VolunteerContact
        FROM orders o
        JOIN food f ON o.FoodID = f.FoodID
        LEFT JOIN donor d ON f.DonorID = d.DonorID
        LEFT JOIN volunteer v ON o.VolunteerID = v.VolunteerID
        WHERE o.FoodBankID = %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, (food_bank_id,))
            orders = cursor.fetchall()

        # Return the orders in the template
        return render_template('food_bank/history.html', orders=orders)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@blueprint.route('/food_bank/history/change_status/<int:order_id>', methods=['POST'])
@login_required
@role_required('food_bank')
def change_status(order_id):
    """Handles changing the order status to 'Received'."""
    try:
        user_id = current_user.id  # Current User ID
        
        # Establish a connection to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Verify if the order belongs to the current food bank
            cursor.execute("""
                SELECT o.OrderID 
                FROM orders o
                JOIN foodbank fb ON o.FoodBankID = fb.FoodBankID
                WHERE o.OrderID = %s AND fb.UserID = %s
            """, (order_id, user_id))
            order = cursor.fetchone()

            if not order:
                raise Exception("Order not found or unauthorized access.")

            # Update the status to 'Received'
            cursor.execute("""
                UPDATE orders 
                SET Status = 'Received' 
                WHERE OrderID = %s
            """, (order_id,))
            connection.commit()

        # Close the connection
        connection.close()

        # Flash success message and redirect to the order history page
        flash('Order status updated to "Received".', 'success')
        return redirect(url_for('food_bank_blueprint.order_history'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    

