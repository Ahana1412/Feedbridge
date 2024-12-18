from flask import Blueprint, render_template, request, redirect, url_for
from .models import FoodItem, Order, Chat

foodbank_bp = Blueprint('foodbank', __name__)

@foodbank_bp.route('/foodbank/home')
def home():
    food_items = FoodItem.query.all()
    return render_template('foodbank/home.html', food_items=food_items)

@foodbank_bp.route('/foodbank/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Logic to place an order
        pass
    return render_template('foodbank/order.html')

@foodbank_bp.route('/foodbank/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        # Chatbot logic here
        pass
    return render_template('foodbank/chatbot.html')

@foodbank_bp.route('/foodbank/history')
def history():
    # Fetch past orders
    pass

@foodbank_bp.route('/foodbank/profile')
def profile():
    # Fetch and update foodbank profile
    pass

def get_donors():
    sort_by = request.args.get('sort_by', 'quantity')  # Default to quantity if not provided
    if sort_by == 'quantity':
        donors = Donor.query.order_by(Donor.quantity.desc()).all()
    elif sort_by == 'distance':
        donors = Donor.query.order_by(Donor.distance).all()  # Assuming distance is calculated in your database
    else:
        donors = Donor.query.all()
    return donors
