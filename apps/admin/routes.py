# -*- encoding: utf-8 -*-
"""
Routes for the Admin role.
"""
# TODO edit as required

from flask import render_template
from flask_login import login_required, current_user
from apps.admin import blueprint
from apps.authentication.util import role_required

@blueprint.route('/admin/donors')
@login_required
@role_required('admin')
def admin_manage_donors():
    """Admin-specific profile page."""
    return render_template('admin/donors.html', user=current_user)

@blueprint.route('/admin/food_banks')
@login_required
@role_required('admin')
def admin_manage_food_banks():
    """Admin-specific user management page."""
    return render_template('admin/food_banks.html', user=current_user)

@blueprint.route('/admin/orders')
@login_required
@role_required('admin')
def admin_manage_orders():
    """Admin-specific user management page."""
    return render_template('admin/orders.html', user=current_user)

@blueprint.route('/admin/food_items')
@login_required
@role_required('admin')
def admin_manage_food_items():
    """Admin-specific user management page."""
    return render_template('admin/food_items.html', user=current_user)
