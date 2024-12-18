from flask import Blueprint, render_template, request
from .models import Task, VolunteerHistory

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/volunteer/home')
def home():
    tasks = Task.query.filter_by(status='Pending').all()
    return render_template('volunteer/home.html', tasks=tasks)

@volunteer_bp.route('/volunteer/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        # Chatbot logic here
        pass
    return render_template('volunteer/chatbot.html')

@volunteer_bp.route('/volunteer/history')
def history():
    # Fetch completed tasks
    pass

@volunteer_bp.route('/volunteer/profile')
def profile():
    # Fetch and update volunteer profile
    pass

@volunteer_bp.route('/volunteer/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        # Assign or update tasks
        pass
    return render_template('volunteer/tasks.html')
