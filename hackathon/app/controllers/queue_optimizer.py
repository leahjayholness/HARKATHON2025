import datetime
from sqlalchemy import func
from app import db  
from app.models.appointment import Appointment 
from app.models.waitlist import Waitlist     
from app.notifications import notify_user      

class QueueOptimizer:
    def __init__(self):
        pass

    def score_waitlist_entry(self, waitlist_entry):
        urgency = getattr(waitlist_entry, 'urgency', 1)
        wait_time = (datetime.datetime.utcnow() - waitlist_entry.timestamp).total_seconds() / 60  
        score = urgency * 10 + wait_time
        return score

    def get_best_candidate(self):
        waitlist_entries = db.session.query(Waitlist).all()
        if not waitlist_entries:
            return None
        best_entry = max(waitlist_entries, key=self.score_waitlist_entry)
        return best_entry

    def fill_cancellation(self, appointment_id):
        # Retrieve the cancelled appointment. We assume 'status' is set to 'cancelled'
        appointment = db.session.query(Appointment).filter_by(id=appointment_id, status='cancelled').first()
        if not appointment:
            print(f"Appointment {appointment_id} not found or not marked as cancelled.")
            return

        candidate = self.get_best_candidate()
        if candidate is None:
            print("No candidates available on the waitlist to fill the slot.")
            return

        # Reassign the appointment slot:
        appointment.user_id = candidate.user_id
        appointment.status = 'reassigned'
        # Optionally, update the assigned_time or other relevant fields
        appointment.assigned_time = datetime.datetime.utcnow()

        # Remove the candidate from the waitlist
        db.session.delete(candidate)
        db.session.commit()

        # Notify the candidate that their waitlist entry has been fulfilled
        notify_msg = (f"Your waitlist request has been fulfilled. Your appointment is now scheduled "
                      f"for {appointment.time_slot}.")
        notify_user(candidate.user_id, notify_msg)
        print(f"Filled cancelled appointment {appointment_id} with waitlist candidate user {candidate.user_id}.")

    def predict_cancellation_probability(self, appointment):
        base_probability = 0.1  # 10% base cancellation probability
        if hasattr(appointment, 'priority') and appointment.priority > 0:
            probability = base_probability / appointment.priority
        else:
            probability = base_probability
        return probability

    def adjust_availability(self):
        scheduled_appointments = db.session.query(Appointment).filter_by(status='scheduled').all()
        for appointment in scheduled_appointments:
            cancellation_prob = self.predict_cancellation_probability(appointment)
            # Example threshold: if cancellation probability is over 50%, flag the slot.
            if cancellation_prob > 0.5:
                print(f"High cancellation probability ({cancellation_prob:.2f}) for appointment {appointment.id}.")
               
if __name__ == "__main__":
    optimizer = QueueOptimizer()
    optimizer.fill_cancellation(appointment_id=123)