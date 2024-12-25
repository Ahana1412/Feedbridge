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
    "foodbank_contact": "Food banks can find donor information, addresses, and contact details on their 'Orders History' page.",
    "donor_contact": "Donors can track volunteer and food bank details in the 'History' section after placing a donation.",
    "default": "I'm sorry, I didn't understand that. Could you please rephrase your question or ask about donating, ordering, volunteering, or profile updates?"
}

# Define intents and associated keywords
intents = {
    "donate_food": ["donate food", "how to donate", "food donation", "donate", "fruits", "vegetables", "give food", "can I donate", "where to donate"],
    "order_food": ["order food", "order", "food banks", "ordering for food banks", "receive"],
    "volunteer": ["volunteer", "help out", "get involved", "sign up"],
    "donation_items": ["what can I donate", "items to donate", "acceptable donations", "donations", "list to donate", "what to donate"],
    "how_to_help": ["how can I help", "help options", "ways to help", "what to do"],
    "general_greeting": ["how are you", "hello", "hi", "hey", "what's up"],
    "thanking": ["thanks", "thank you", "thank you so much", "okay"],
    "profile_update": ["update profile", "change details", "edit profile", "change number", "change email"],
    "volunteer_history": ["check history", "volunteer history", "my deliveries"],
    "volunteer_delivery": ["where to deliver", "delivery location", "volunteer task location", "pick up location", "where to collect", "where to deliver to"],
    "foodbank_contact": ["food bank contact", "food bank details", "contact food bank", "donor address"],
    "donor_contact": ["donor contact", "donor address", "contact donor", "which volunteer", "which foodbank"]
}

# Function to match user input to an intent
def match_intent(user_input):
    for intent, keywords in intents.items():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword, user_input.lower()) > 80:  # Threshold for similarity
                return intent
    return "default"

# Start a conversation
chat_history = ""

print("Bot: Welcome to the Food Bank Assistant! How can I help you today? (Type 'exit' to quit)")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye! Have a great day!")
        break

    # Match the user input to an intent
    matched_intent = match_intent(user_input)

    if matched_intent in knowledge_base:
        # Provide a response from the knowledge base if intent matches
        response = knowledge_base[matched_intent]
    else:
        # Otherwise, generate a response using DialoGPT
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
        bot_input_ids = new_input_ids if chat_history == "" else torch.cat([chat_history, new_input_ids], dim=-1)

        chat_history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    print(f"Bot: {response}") 