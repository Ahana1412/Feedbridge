from flask import Blueprint, request, jsonify
from flask_login import current_user
from .backend import create_notification, fetch_notifications, mark_as_read, clear_notifications

notifications_blueprint = Blueprint('notifications', __name__)

@notifications_blueprint.route('/get', methods=['GET'])


def get_notifications():
    if not current_user.is_authenticated:
        return jsonify({'error': 'User not authenticated'}), 401

    print(f"Current User ID: {current_user.id}")  # Ensure this prints an integer
    user_id = current_user.id
    notifications = fetch_notifications(user_id)

    for notification in notifications:
        notification['_id'] = str(notification['_id'])

    return jsonify({'notifications': notifications})







@notifications_blueprint.route('/mark-as-read/<notification_id>', methods=['POST'])
def mark_notification(notification_id):
    """
    Mark a specific notification as read.
    """
    success = mark_as_read(notification_id)
    return jsonify({'success': success})

@notifications_blueprint.route('/clear', methods=['POST'])
def clear_all():
    """
    Clear all notifications for the current user.
    """
    user_id = current_user.id
    count = clear_notifications(user_id)
    return jsonify({'cleared_count': count})

@notifications_blueprint.route('/create', methods=['POST'])
def create_new_notification():
    """
    Create a new notification. (For testing or future admin functionalities)
    """
    data = request.get_json()
    
    # Always use the logged-in user's ID unless explicitly provided
    user_id = data.get('user_id', current_user.id)
    
    # Ensure the user_id is an integer (MySQL User ID)
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID format. User ID must be an integer.'}), 400

    title = data.get('title')
    message = data.get('message')

    notification_id = create_notification(user_id, title, message)
    return jsonify({'notification_id': notification_id})

