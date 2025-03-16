from app import db

class Appointment(db.Model):
    # Appointment model to store scheduling details.
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    washes = db.Column(db.Integer, nullable=False)
    dries = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    account = db.relationship("Account", backref=db.backref("appointments", lazy=True))

    def __repr__(self):
        return f"<Appointment {self.id} for Account {self.account_id}>"