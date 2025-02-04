from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from apps.donor import blueprint
from apps.authentication.util import role_required
from apps.authentication.models import Donor, Food , Order, Volunteer, FoodBank
from flask_login import login_required, current_user
from apps import db
from apps.donor.forms import DonationForm
from datetime import datetime
from flask import current_app
from io import BytesIO
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image


@blueprint.route('/profile')
@login_required
@role_required('donor')
def donor_profile():
    # Fetch donor-specific data
    # donor_data = Donations.query.filter_by(donor_id=current_user.id).all()
    return render_template('donor/profile.html', user=current_user) #, donor_data=donor_data)


@blueprint.route('/new_donation', methods=['GET', 'POST'])
@login_required
@role_required('donor')
def new_donation():
    form = DonationForm()

    if 'new_donation' in request.form:
        # Ensure current user is a donor
        if current_user.role != 'donor':
            return render_template('donor/new_donation.html',
                                   msg='Only donors can log donations.',
                                   success=False,
                                   form=form)

        # Fetch the donor ID from the donor table
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        if not donor:
            return render_template('donor/new_donation.html',
                                   msg='Donor profile not found.',
                                   success=False,
                                   form=form)

        # Handle the image upload and classification
        if form.item_type.data == 'Grocery':
            uploaded_file = request.files['food_image']
            if uploaded_file:
                # Read image into memory as a byte stream
                img_bytes = uploaded_file.read()
                # Call the detect_food_spoilage function with the image in-memory
                spoilage_status = detect_food_spoilage(img_bytes)
                if spoilage_status == 'rotten':
                    return render_template('donor/confirmation.html',
                                        msg='Unfortunately, your donation was rejected because the food is not fresh. Rotten food is not accepted.',
                                        success=False)

        # If food is fresh, proceed to create a new donation entry
        try:
            new_donation = Food(
                donor_id=donor.donor_id,
                quantity=form.quantity.data,
                donation_date=datetime.now().date(),
                expiry_date=form.expiry_date.data,
                food_type=form.food_type.data,
                item_type=form.item_type.data,
                food_name=form.food_name.data,
                food_description=form.food_description.data,
                status='Available'
            )
            db.session.add(new_donation)
            db.session.commit()

            # Return the success page
            return render_template('donor/confirmation.html',
                                   msg='Donation successfully logged!',
                                   success=True)

        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")
            flash('An error occurred while saving the donation.', 'danger')

    return render_template('donor/new_donation.html', form=form)


def preprocess_image(img_bytes, target_size=(224, 224)):
    """Preprocess the image to be used for model inference."""

    img = Image.open(BytesIO(img_bytes))
    img = img.resize(target_size)    
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)    
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    
    return img_array


def detect_food_spoilage(image_bytes):
    """Function to detect spoilage based on the uploaded image using the pre-trained model."""
    try:
        img_array = preprocess_image(image_bytes)

        model = tf.keras.models.load_model(os.getenv('MODEL_PATH'))
        predictions = model.predict(img_array)

        predicted_class = np.argmax(predictions, axis=1)
        confidence_scores = predictions[0]

        class_labels = ['fresh', 'rotten']
        predicted_label = class_labels[predicted_class[0]]
        confidence_score = confidence_scores[predicted_class[0]]

        # Log prediction details for debugging
        print(f"Predicted class index: {predicted_class[0]}")
        print(f"Predicted label: {predicted_label}")
        print(f"Confidence score: {confidence_score:.4f}")

        return predicted_label

    except Exception as e:
        print(f"Error in spoilage detection: {e}")
        return 'error'


@blueprint.route('/donations', methods=['GET'])
@login_required
@role_required('donor')
def donation_history():
    try:
        # Fetch the donor ID from the donor table
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        
        if not donor:
            flash('Donor profile not found.', 'danger')
            return render_template('home/home.html')

        # Fetch donations made by this donor
        donations = Food.query.filter_by(donor_id=donor.donor_id).all()
        
        return render_template('donor/donation_history.html', donations=donations)
    
    except Exception as e:
        print(f"Error fetching donation history: {e}")
        flash('An error occurred while fetching donation history.', 'danger')
        return render_template('home/home.html')


@blueprint.route('/orders', methods=['GET'])
@login_required
@role_required('donor')
def order_history():
    try:
        # Step 1: Fetch the donor record
        donor = Donor.query.filter_by(user_id=current_user.id).first()
        
        if not donor:
            flash('Donor profile not found.', 'danger')
            return render_template('home/home.html')
        
        # Step 2: Fetch food donations by this donor with 'Ordered' status
        donations = Food.query.filter_by(donor_id=donor.donor_id, status='Ordered').all()
        
        if not donations:
            return render_template('donor/order_history.html', orders=[])
        
        # Step 3: Collect all food IDs from these donations
        food_ids = [donation.food_id for donation in donations]
        
        # Step 4: Fetch related orders using these food IDs
        orders = Order.query.filter(Order.food_id.in_(food_ids)).all()
        
        # Step 5: Prepare order details with food, volunteer, and food bank data
        order_details = []
        for order in orders:
            food = next((d for d in donations if d.food_id == order.food_id), None)
            food_bank = FoodBank.query.filter_by(foodbank_id=order.foodbank_id).first()
            volunteer = Volunteer.query.filter_by(volunteer_id=order.volunteer_id).first() if order.volunteer_id else None
            
            order_details.append({
                'order_id': order.order_id,
                'food_id': food.food_id,
                'food_name': food.food_name,
                'food_description': food.food_description,
                'request_date': order.request_date,  
                'status': order.status,
                'foodbank_name': food_bank.name,
                'foodbank_contact': food_bank.contact_number,
                # 'foodbank_address': food_bank.address if food_bank else 'N/A',
                'volunteer_name': volunteer.first_name if volunteer else 'Not assigned',
                'volunteer_contact': volunteer.contact_number if volunteer else 'Not assigned'
            })
        
        return render_template('donor/order_history.html', orders=order_details)
    
    except Exception as e:
        print(f"Error fetching order history: {e}")
        flash('An error occurred while fetching order history.', 'danger')
        return render_template('home/home.html')
    

# @blueprint.route('/test_mongo', methods=['POST', 'GET'])
# def test_mongo():
#     mongo_db = current_app.config['mongo_db']
#     if mongo_db:
#         mongo_db.notifications.insert_one({"message": "MongoDB connection works!"})
#         return "MongoDB Test Successful"
#     return "MongoDB Not Configured Properly"
