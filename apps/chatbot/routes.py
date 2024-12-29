from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user  # Import for session management
from .backend import process_chat

chatbot_blueprint = Blueprint('chatbot', __name__)

@chatbot_blueprint.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        data = request.get_json()

        # Use current_user to fetch user_id and user_role dynamically
        user_id = current_user.id
        user_role = current_user.role

        # Extract the query from the POST request
        query = data.get('query')

        # Process the query
        response, interaction_id = process_chat(user_id, user_role, query)

        # Return the response as JSON
        return jsonify({'response': response, 'interaction_id': interaction_id})

    return render_template('chatbot.html')  # Render the chatbot page for GET request
