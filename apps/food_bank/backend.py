from flask import render_template, request, jsonify
from sqlalchemy import asc, desc
import requests

import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
# Fetch credentials from the environment file
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
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

def fetch_food_items():
    """
    Fetches available food items and their details from the database.
    """
    query = """
        SELECT 
            food.Name AS food_name,
            food.Quantity,
            food.FoodType,
            food.ItemType,
            food.ExpiryDate,
            donor.Name AS donor_name,
            donor.Address AS donor_address,
            donor.ContactNo AS donor_contact
        FROM food
        JOIN donor ON food.DonorID = donor.DonorID
    """
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()


def get_available_food_items():
    # Query the database for available food items
    query = """SELECT d.Name as donor_name, f.Quantity, f.FoodType, d.Address, d.ContactNo
               FROM food f
               JOIN donor d ON f.DonorID = d.DonorID
               WHERE f.Quantity > 0"""
    # Use your database connection to fetch this data
    return db.execute(query).fetchall()

def calculate_distances(donors, user_location):
    api_key = "your api key"
    origins = f"{user_location[0]},{user_location[1]}"
    destinations = "|".join([donor['Address'] for donor in donors])

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origins}&destinations={destinations}&key={api_key}"
    response = requests.get(url).json()

    for i, donor in enumerate(donors):
        donor['distance'] = response['rows'][0]['elements'][i]['distance']['value']
    return donors
