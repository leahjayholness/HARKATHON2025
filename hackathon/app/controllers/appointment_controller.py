from datetime import time, datetime, timedelta

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)
from sqlalchemy import exc
from app.models.appointment import Appointment
from app.controllers.authentication_controller import login_required
from app import db
from app import scheduler

appointment_bp = Blueprint("appointment", __name__)

@appointment_bp.route("/", methods=("GET", "POST"))
@login_required
def create_appointment():
    if request.method == "POST":
        _account_id = session.get('user_id')
        _start_time = request.form.get('start_time')
        _washes = request.form.get('washes')
        _dries = request.form.get('dries')
        error = None

        if not _start_time or not _washes or not _dries:
            error = "All fields are required."
        else:
            try:
                # Parse start time
                _start_time = datetime.strptime(_start_time, "%H:%M").time()
                
                # Calculate end time
                wash_duration = int(_washes) * 40  # in minutes
                dry_duration = int(_dries) * 45  # in minutes
                total_duration = wash_duration + dry_duration
                
                start_time = datetime.combine(datetime.today(), _start_time)
                end_time = start_time + timedelta(minutes=total_duration)
                
                # Check for overlapping appointments
                overlapping_appointments = Appointment.query.filter(
                    Appointment.start_time < end_time,
                    Appointment.end_time > start_time
                ).all()

                if overlapping_appointments:
                    error = "This time slot is already booked."
            except ValueError:
                error = "Invalid start time format."

        if error is None:
            new_appointment = Appointment(
                account_id=_account_id,
                start_time=start_time,
                end_time=end_time,
                washes=int(_washes),
                dries=int(_dries)
            )
            db.session.add(new_appointment)
            db.session.commit()
            return redirect(url_for("index"))
        
        flash(error)
        
    return render_template("appointment/create.html")

@appointment_bp.route("/<int:id>/edit", methods=("GET", "POST"))
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get(id)
    if appointment.account_id != session.get('user_id'):
        flash("You are not authorized to edit this appointment.")
        return redirect(url_for("index"))

    if request.method == "POST":
        _start_time = request.form.get('start_time')
        _washes = request.form.get('washes')
        _dries = request.form.get('dries')
        error = None

        try:
            # Parse start time
            _start_time = datetime.strptime(_start_time, "%H:%M").time()
                
            # Calculate end time
            wash_duration = int(_washes) * 40  # in minutes
            dry_duration = int(_dries) * 45  # in minutes
            total_duration = wash_duration + dry_duration
                
            start_time = datetime.combine(datetime.today(), _start_time)
            end_time = start_time + timedelta(minutes=total_duration)

            overlapping_appointments = Appointment.query.filter(
                Appointment.start_time < end_time,
                Appointment.end_time > start_time,
                Appointment.id != appointment.id  # Exclude current appointment
            ).all()

            if overlapping_appointments:
                error = "This time slot is already booked."
        except ValueError:
            error = "Invalid time format."

        if error is None:
            appointment.start_time = start_time
            appointment.end_time = end_time
            appointment.washes = int(_washes)
            appointment.dries = int(_dries)
            db.session.commit()
            flash("Appointment updated successfully!")
            return redirect(url_for("index"))

        flash(error)

    return render_template("appointment/edit.html", appointment=appointment)

@appointment_bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if appointment.account_id != session.get('user_id'):
        flash("You are not authorized to delete this appointment.")
        return redirect(url_for("index"))

    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted successfully!")
    return redirect(url_for("index"))

def list_appointments():
    appointments = Appointment.query.all()
    return sorted(appointments, key = lambda appointment: appointment.start_time)

# Task to mark appointments as completed
def mark_completed():
    with scheduler.app.app_context():
        now = datetime.now()
        appointments = Appointment.query.filter_by(completed=False).all()
        for appointment in appointments:
            if appointment.end_time <= now:
                appointment.completed = True
                db.session.commit()

# Task to remove all appointments at midnight
def delete_appointments():
    with scheduler.app.app_context():
        db.session.query(Appointment).delete()  # Delete all appointments
        db.session.commit()
        print("All appointments have been removed.")  # Log confirmation


scheduler.add_job(
    func=mark_completed,
    trigger="interval",
    seconds=10,
    id="mark_completed",
    name="mark_completed",
    replace_existing=True,
)

scheduler.add_job(
    func=delete_appointments,
    trigger="cron",
    hour=0,
    minute=0,
    id="delete_appointments",
    name="delete_appointments",
    replace_existing=True,
)