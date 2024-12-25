from flask import Blueprint, request, jsonify, render_template
from .backend import process_chat
from ..config import Config

chatbot_blueprint = Blueprint('chatbot', __name__)

@chatbot_blueprint.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()  # Handle incoming JSON data
        
        # Extract data from the POST request
        user_id = data.get('user_id')
        user_role = data.get('user_role')
        query = data.get('query')

        # Process the query using your backend logic
        response, interaction_id = process_chat(user_id, user_role, query)

        # Return the response as JSON to be handled in the frontend
        return jsonify({'response': response, 'interaction_id': interaction_id})

    # For GET request, render the chatbot page
    return render_template('chatbot.html')  # Your main chat page
