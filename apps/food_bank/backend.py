from flask import render_template, request, jsonify
from sqlalchemy import asc, desc
import requests

@app.route('/food-bank', methods=['GET'])
def food_bank():
    sort_option = request.args.get('sort', 'quantity')  # Default sort by quantity
    donors = get_available_food_items()

    # Sorting logic
    if sort_option == 'distance':
        user_location = (user_lat, user_lng)  # Replace with actual user's lat/lng
        donors = calculate_distances(donors, user_location)
        donors = sorted(donors, key=lambda x: x['distance'])
    elif sort_option == 'quantity':
        donors = sorted(donors, key=lambda x: x['quantity'], reverse=True)

    return render_template('food_bank.html', donors=donors)

def get_available_food_items():
    # Query the database for available food items
    query = """SELECT d.Name as donor_name, f.Quantity, f.FoodType, d.Address, d.ContactNo
               FROM food f
               JOIN donor d ON f.DonorID = d.DonorID
               WHERE f.Quantity > 0"""
    # Use your database connection to fetch this data
    return db.execute(query).fetchall()

def calculate_distances(donors, user_location):
    api_key = "YOUR_API_KEY"
    origins = f"{user_location[0]},{user_location[1]}"
    destinations = "|".join([donor['Address'] for donor in donors])

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origins}&destinations={destinations}&key={api_key}"
    response = requests.get(url).json()

    for i, donor in enumerate(donors):
        donor['distance'] = response['rows'][0]['elements'][i]['distance']['value']
    return donors
