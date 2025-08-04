import pandas as pd
import joblib
import os

# Load model only once
model_path =  model_path = r'D:\FeedBridge1\flask_application\apps\utils\donor_ngo_match_model.pkl'
model = joblib.load(model_path)

def predict_match(food, foodbank, distance_km):
    """
    Given a food donation and a foodbank, return prediction and confidence score.
    """
    input_data = {
        "distance_km": distance_km,
        "food_quantity": food.quantity,
        "ngo_capacity": foodbank.capacity,
        "food_type": food.food_type.lower(),
        "food_category": food.item_type.lower(),
        "accepts_nonveg": foodbank.accepts_non_veg,
        "time_until_expiry_hrs": food.expiry_hours
    }

    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    confidence = model.predict_proba(df)[0][1]  # Confidence for class 1 (match)

    return int(prediction), float(confidence)
