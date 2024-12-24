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

def fetch_food_items():
    """Fetches available food items and their details from the database."""
    query = """
        SELECT
            food.FoodID,  
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
        WHERE food.Status = 'Available'  -- Only select available food items
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        # Log the error and raise an exception
        print(f"Error fetching food items: {str(e)}")
        raise Exception(f"Error fetching food items: {str(e)}")
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use


def get_available_food_items():
    """Fetches only available food items from the database."""
    query = """SELECT 
                    d.Name AS donor_name, 
                    f.Quantity, 
                    f.FoodType, 
                    f.ItemType, 
                    d.Address, 
                    d.ContactNo
               FROM food f
               JOIN donor d ON f.DonorID = d.DonorID
               WHERE f.Status = 'Available'  -- Only available food items
               AND f.Quantity > 0"""  # Ensure the quantity is more than 0
    # Use your database connection to fetch this data
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    except Exception as e:
        # Log the error and raise an exception
        print(f"Error fetching available food items: {str(e)}")
        raise Exception(f"Error fetching available food items: {str(e)}")
    finally:
        if connection:
            connection.close()  # Ensure the connection is closed after use






def calculate_distances(donors, user_location):
    api_key = "your api key"
    origins = f"{user_location[0]},{user_location[1]}"
    destinations = "|".join([donor['Address'] for donor in donors])

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origins}&destinations={destinations}&key={api_key}"
    response = requests.get(url).json()

    for i, donor in enumerate(donors):
        donor['distance'] = response['rows'][0]['elements'][i]['distance']['value']
    return donors 

