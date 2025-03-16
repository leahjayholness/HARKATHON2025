from flask import Blueprint, jsonify, request
from app.models.timer import Timer
from app.controllers.authentication_controller import login_required
from app import db

timer_bp = Blueprint("timer", __name__)

@timer_bp.route("/", methods=["GET"])
@login_required
def list_timers():
    timers = Timer.query.all()
    return jsonify([{"id": t.id, "name": t.name, "duration": t.duration} for t in timers])

def create_timer(appointment_id, end_time, appointment):
    new_timer = Timer(appointment_id=appointment_id, end_time=end_time, appointment=appointment)
    db.session.add(new_timer)
    db.session.commit()
    return new_timer