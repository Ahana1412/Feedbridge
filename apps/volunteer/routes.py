# -*- encoding: utf-8 -*-
"""
Routes for the Volunteer role.
"""

# TODO edit as required

from flask import render_template
from flask_login import login_required, current_user
from apps.volunteer import blueprint
from apps.authentication.util import role_required

@blueprint.route('/volunteer/profile')
@login_required
@role_required('volunteer')
def volunteer_profile():
    """Volunteer-specific profile page."""
    return render_template('volunteer/profile.html', user=current_user)

@blueprint.route('/volunteer/tasks')
@login_required
@role_required('volunteer')
def volunteer_tasks():
    """View and manage volunteer tasks."""
    return render_template('volunteer/tasks.html', user=current_user)
