from bson.objectid import ObjectId
from datetime import datetime
from ..config import Config

# Use the MongoDB client and database from the config
mongo_db = Config.mongo_db

def save_notification(user_id, title, message, status="unread"):
    """
    Save a notification in MongoDB.
    :param user_id: The integer ID of the user (from MySQL).
    """
    notification = {
        'user_id': int(user_id),  # Ensure it's stored as an integer
        'title': title,
        'message': message,
        'status': status,
        'timestamp': datetime.utcnow()
    }
    result = mongo_db.notifications.insert_one(notification)
    return str(result.inserted_id)


def get_user_notifications(user_id):
    """
    Retrieve all notifications for a specific user.
    """
    return list(mongo_db.notifications.find({'user_id': int(user_id)}).sort('timestamp', -1))



def mark_notification_as_read(notification_id):
    """
    Mark a specific notification as read.
    """
    return mongo_db.notifications.update_one(
        {'_id': ObjectId(notification_id)},
        {'$set': {'status': 'read'}}
    )

def clear_all_notifications(user_id):
    """
    Delete all notifications for a specific user.
    """
    return mongo_db.notifications.delete_many({'user_id': user_id})
