from .chatbot_logic import match_intent, knowledge_base, tokenizer, model
from .models import save_interaction

from .chatbot_logic import generate_response
from .models import save_interaction

def process_chat(user_id, user_role, query):
    """
    Process the chatbot query and generate a response.
    Save the interaction in MongoDB.
    """
    response = generate_response(query)

    # Save the interaction in MongoDB
    interaction_id = save_interaction(user_id, user_role, query, response)

    return response, interaction_id




