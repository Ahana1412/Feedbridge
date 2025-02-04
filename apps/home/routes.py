# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from flask import render_template, jsonify
from apps.home import blueprint
from flask_login import login_required
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch credentials from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')


def get_db_connection():
    """Establish a connection to the database."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@blueprint.route('/home', methods=['GET'])
@login_required
def home_page():
    connection = None
    try:
        # Establish database connection
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Fetch weekly donations for charts
            cursor.execute("""
                SELECT WEEK(DonationDate) AS Week,
                       COUNT(*) AS TotalDonations
                FROM food
                WHERE DonationDate >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                GROUP BY WEEK(DonationDate);
            """)
            weekly_donations = cursor.fetchall()

            # Fetch top food items by donation count
            cursor.execute("""
                SELECT 
                    Name, 
                    COUNT(*) AS TotalDonations
                FROM food
                GROUP BY Name
                ORDER BY TotalDonations DESC
                LIMIT 5;
            """)
            top_food_items = cursor.fetchall()

            # Fetch top donor locations by donation count
            cursor.execute("""
                SELECT 
                    Address, 
                    COUNT(*) AS DonationCount
                FROM donor
                GROUP BY Address
                ORDER BY DonationCount DESC
                LIMIT 5;
            """)
            top_locations = cursor.fetchall()

            # Fetch monthly volunteer deliveries data (volunteer delivered an order if status is 'Received')
            cursor.execute("""
                SELECT MONTH(o.RequestDate) AS Month,
                       COUNT(DISTINCT o.VolunteerID) AS TotalDeliveries
                FROM orders o
                WHERE o.Status = 'Received'
                GROUP BY MONTH(o.RequestDate);
            """)
            monthly_deliveries = cursor.fetchall()

        # Pass data to the template
        return render_template(
            'home/home.html',
            weekly_donations=weekly_donations,
            top_food_items=top_food_items,
            top_locations=top_locations,
            monthly_deliveries=monthly_deliveries  # Pass the new data to the template
        )

    except Exception as e:
        # Log the error and return an error response
        print(f"Error fetching data for home page: {str(e)}")
        return jsonify({"error": "An error occurred while fetching data"}), 500

    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use


