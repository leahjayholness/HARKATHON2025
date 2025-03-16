from datetime import datetime

def format_date(value):
    """Formats a date for templates."""
    return value.strftime("%Y-%m-%d") if value else "N/A"

def format_time(value):
    """Formats a time for templates."""
    return value.strftime("%H:%M:%S") if value else "N/A"
