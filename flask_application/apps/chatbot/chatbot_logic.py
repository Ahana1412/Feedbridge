
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from fuzzywuzzy import fuzz

# Load pre-trained conversational model (DialoGPT)
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Knowledge Base
knowledge_base = {
    "donate_food": "You can donate food by visiting the 'Donate' page. Fill in the required details like food type, description, quantity, and expiry date.",
    "order_food": "To order food for your food bank, go to the 'Order' page in the app and submit your request.",
    "volunteer": "Volunteers can sign up for helping in deliveries. You can also check available deliveries and your volunteering history.",
    "donation_items": "Items you can donate include packed goods, dry food, fruits, vegetables and cooked food in good condition",
    "how_to_help": "You can help by donating food, volunteering, or sharing our app with others. Visit donate page for donations and signup as volunteer to get involved in volunteering",
    "general_greeting": "Hello! How can I assist you today?",
    "thanking": "You're welcome! Let me know if there's anything else I can assist you with.",
    "profile_update": "You can update your personal details by visiting the 'Profile' page on the app.",
    "volunteer_history": "Volunteers can check their delivery history on the 'History' page.",
    "volunteer_delivery": "To know where to deliver, visit your 'History' page to see the food bank and donor address and contact details.",
    "foodbank_contact": "You can find donor information, addresses, and contact details on their 'Orders History' page.",
    "donor_contact": "You can track volunteer and donor/food bank details in the 'History' section. You can also check the notifications",
    "foodbank_history": "You can check your order history and other donor/volunteer and food details on the 'History' page.",
    "default": "I'm sorry, I didn't understand that. Could you please rephrase your question or ask about donating, ordering, volunteering, or profile updates?"
}


# Define intents and associated keywords
intents = {
    "donate_food": ["donate food", "how to donate food", "food donation", "fruits", "vegetables", "give food", "can I donate", "where to donate"],
    "order_food": ["order food", "order items", "food banks", "ordering for food banks", "receive"],
    "volunteer": ["deliver food", "help out", "get involved", "sign up as volunteer"],
    "donation_items": ["what can I donate", "items to donate", "acceptable donations", "what donations can i give", "list to donate", "what food to donate"],
    "how_to_help": ["how can I help", "help options", "ways to help", "what to do", "What to help with"],
    "general_greeting": ["how are you", "hello", "hi", "hey", "what's up"],
    "thanking": ["thanks", "thank you", "thank you so much", "okay", "bye"],
    "profile_update": ["update profile", "change details", "edit profile", "change number", "change email", "change name", "can i update profile"],
    "volunteer_history": ["check history", "volunteer history", "my deliveries"],
    "volunteer_delivery": ["where to deliver", "delivery location", "volunteer task location", "pick up location", "where to collect", "where to deliver to"],
    "foodbank_contact": ["donor contact", "where is donor address", "donor name", "donor address"],
    "donor_contact": ["who is volunteer", "who will take up the order", "contact foodbank", "which volunteer", "which foodbank", "who is delivering my order"],
    "foodbank_history": ["order status", "order history", "Where to check previous orders", "Order information"]
}

# Function to match user input to an intent
def match_intent(user_input):
    for intent, keywords in intents.items():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword, user_input.lower()) > 80:  # Threshold for similarity
                return intent
    return "default"

# Function to generate chatbot response
def generate_response(user_input):
    matched_intent = match_intent(user_input)
    if matched_intent in knowledge_base:
        # Respond from knowledge base
        return knowledge_base[matched_intent]
    else:
        # Generate response using DialoGPT
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        response_ids = model.generate(new_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        return tokenizer.decode(response_ids[0], skip_special_tokens=True)
