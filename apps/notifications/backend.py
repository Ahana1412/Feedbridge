from .models import save_notification, get_user_notifications, mark_notification_as_read, clear_all_notifications

def create_notification(user_id, title, message):
    """
    Create and save a new notification.
    """
    notification_id = save_notification(user_id, title, message)
    return notification_id

def fetch_notifications(user_id):
    """
    Retrieve notifications for a user.
    """
    return get_user_notifications(user_id)

def mark_as_read(notification_id):
    """
    Mark a notification as read.
    """
    result = mark_notification_as_read(notification_id)
    return result.modified_count > 0

def clear_notifications(user_id):
    """
    Clear all notifications for a user.
    """
    result = clear_all_notifications(user_id)
    return result.deleted_count
