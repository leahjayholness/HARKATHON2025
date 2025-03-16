from app.models.account import Account
from app.models.appointment import Appointment
from app.models.report import Report
from app.models.notice import Notice
from app.models.notification import Notification
from app.models.timer import Timer

# Export models for easier imports elsewhere
__all__ = ["Account", "Appointment", "Report", "Notice", "Notification", "Timer"]
