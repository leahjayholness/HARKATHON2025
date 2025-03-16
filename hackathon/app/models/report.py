from app import db

class Report(db.Model):
    # Report model for generating and tracking reports.
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    account = db.relationship("Account", backref=db.backref("reports", lazy=True))

    def __repr__(self):
        return f"<Report {self.id} for Account {self.account_id}>"