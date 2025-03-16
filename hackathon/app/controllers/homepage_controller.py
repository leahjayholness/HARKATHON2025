from flask import Blueprint, flash, render_template, request, url_for

from app.controllers.authentication_controller import login_required
from app.controllers.appointment_controller import list_appointments
from app import db

# Create a blueprint for account-related routes
homepage_bp = Blueprint("homepage", __name__)

@homepage_bp.route("/")
@login_required
def index():
    return render_template("schedule.html", appointments=list_appointments())