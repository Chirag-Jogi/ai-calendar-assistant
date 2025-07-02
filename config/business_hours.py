"""
Business Hours Configuration
Centralized business hours definition to ensure consistency
"""

# Business Hours Configuration
BUSINESS_START_HOUR = 10  # 10:00 AM
BUSINESS_END_HOUR = 18    # 6:00 PM (18:00)

# Business Days (Monday=0, Sunday=6)  
BUSINESS_DAYS = [0, 1, 2, 3, 4]  # Monday to Friday

# Helper functions
def get_business_hours_display():
    """Get human-readable business hours"""
    return "10:00 AM - 6:00 PM"

def get_business_days_display():
    """Get human-readable business days"""
    return "Monday to Friday"

def is_business_day(weekday):
    """Check if a weekday (0=Monday, 6=Sunday) is a business day"""
    return weekday in BUSINESS_DAYS

def is_within_business_hours(hour, minute=0):
    """Check if a time is within business hours"""
    time_minutes = hour * 60 + minute
    start_minutes = BUSINESS_START_HOUR * 60
    end_minutes = BUSINESS_END_HOUR * 60
    return start_minutes <= time_minutes < end_minutes
