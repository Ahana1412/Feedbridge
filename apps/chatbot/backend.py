from .chatbot_logic import match_intent, knowledge_base, tokenizer, model
from .models import save_interaction

def process_chat(user_id, user_role, query):
    """
    Process the chatbot query and generate a response.
    Save the interaction in MongoDB.
    """
    # Match the user query to an intent
    matched_intent = match_intent(query)

    if matched_intent in knowledge_base:
        # Provide a response from the knowledge base if intent matches
        response = knowledge_base[matched_intent]
    else:
        # Generate a response using DialoGPT
        new_input_ids = tokenizer.encode(query + tokenizer.eos_token, return_tensors="pt")
        response_ids = model.generate(new_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

    # Save the interaction in MongoDB
    interaction_id = save_interaction(user_id, user_role, query, response)

    return response, interaction_id



