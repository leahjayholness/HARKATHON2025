from app import db

class Timer(db.Model):
    # Timer model for managing timed events.
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    appointment = db.relationship("Appointment", backref=db.backref("timers", lazy=True))

    def __repr__(self):
        return f"<Timer {self.name} ({self.duration}s)>"