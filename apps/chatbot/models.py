from bson.objectid import ObjectId
from datetime import datetime
from ..config import Config

# Use the MongoDB client and database from the config
mongo_db = Config.mongo_db

def save_interaction(user_id, user_role, query, response):
    """Save chatbot interaction in MongoDB."""
    interaction = {
        'user_id': user_id,
        'user_role': user_role,
        'query': query,
        'response': response,
        'timestamp': datetime.utcnow()
    }
    result = mongo_db.chat_interactions.insert_one(interaction)
    return str(result.inserted_id)  # Return the interaction ID

def get_interactions(user_id):
    """Retrieve all interactions for a specific user."""
    return list(mongo_db.chat_interactions.find({'user_id': user_id}))

def get_interaction_by_id(interaction_id):
    """Retrieve a specific interaction by its ID."""
    return mongo_db.chat_interactions.find_one({'_id': ObjectId(interaction_id)})






