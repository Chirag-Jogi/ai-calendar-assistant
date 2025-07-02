"""
Date and Time Parsing Utilities
Clean, reusable date/time handling functions
"""
from datetime import datetime, timedelta
from typing import Tuple

class DateParser:
    """Utility class for parsing dates and times from natural language"""
    
    @staticmethod
    def parse_date(date_string: str) -> datetime:
        """Parse AI-provided date strings (should be YYYY-MM-DD format)"""
        print(f"📅 Parsing date: {date_string}")
        
        if not date_string:
            result = datetime.now() + timedelta(days=1)
            print(f"✅ Parsed date: {result.strftime('%Y-%m-%d')}")
            return result
        
        date_string = date_string.strip()
        
        try:
            # First, try to parse as YYYY-MM-DD (what AI should provide)
            if len(date_string) == 10 and date_string.count('-') == 2:
                result = datetime.strptime(date_string, '%Y-%m-%d')
                print(f"✅ Parsed date: {result.strftime('%Y-%m-%d')}")
                return result
            
            # Fallback for natural language (shouldn't happen with good prompt)
            date_string_lower = date_string.lower()
            base_date = datetime.now()
            
            if date_string_lower in ['today']:
                result = base_date
            elif date_string_lower in ['tomorrow']:
                result = base_date + timedelta(days=1)
            elif date_string_lower in ['day after tomorrow', 'overmorrow']:
                result = base_date + timedelta(days=2)
            else:
                print(f"⚠️ Unknown date format '{date_string}', defaulting to tomorrow")
                result = base_date + timedelta(days=1)
            
            print(f"✅ Parsed date: {result.strftime('%Y-%m-%d')}")
            return result
            
        except Exception as e:
            print(f"❌ Date parsing error: {str(e)}, defaulting to tomorrow")
            result = datetime.now() + timedelta(days=1)
            print(f"✅ Parsed date: {result.strftime('%Y-%m-%d')}")
            return result
    
    @staticmethod
    def _get_next_weekday(current_date: datetime, target_weekday: int) -> datetime:
        """Get next occurrence of target weekday (0=Monday, 6=Sunday)"""
        days_ahead = target_weekday - current_date.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    
    @staticmethod
    def parse_time(time_str: str) -> Tuple[int, int]:
        """Parse time string to (hour, minute) tuple"""
        print(f"⏰ Parsing time: {time_str}")
        
        try:
            # Handle different time formats
            if ':' in time_str:
                # Format: "14:30" or "2:30"
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                
            elif 'pm' in time_str.lower():
                # Format: "2pm" or "2 pm"
                hour_part = time_str.lower().replace('pm', '').strip()
                hour = int(hour_part)
                if hour != 12:
                    hour += 12
                minute = 0
                
            elif 'am' in time_str.lower():
                # Format: "9am" or "9 am"
                hour_part = time_str.lower().replace('am', '').strip()
                hour = int(hour_part)
                if hour == 12:
                    hour = 0
                minute = 0
                
            else:
                # Default: assume 24-hour format
                hour = int(time_str)
                minute = 0
            
            # Validate hour and minute
            if not (0 <= hour <= 23):
                hour = 14  # Default to 2 PM
            if not (0 <= minute <= 59):
                minute = 0
                
            print(f"✅ Parsed time: {hour:02d}:{minute:02d}")
            return hour, minute
            
        except Exception as e:
            print(f"⚠️ Time parsing failed: {str(e)}, defaulting to 2 PM")
            return 14, 0  # Default to 2:00 PM
    
    @staticmethod
    def format_display_date(date: datetime) -> str:
        """Format datetime for user-friendly display"""
        return date.strftime('%B %d, %Y')
    
    @staticmethod
    def format_display_time(date: datetime) -> str:
        """Format datetime for user-friendly time display"""
        return date.strftime('%I:%M %p')