"""
Response Building and Message Formatting
Clean, consistent response formatting for better UX
"""
from datetime import datetime
from typing import Dict, List, Optional
from config.business_hours import get_business_hours_display

class ResponseBuilder:
    """Utility class for building consistent, user-friendly responses"""
    
    @staticmethod
    def build_success_response(message: str, **kwargs) -> Dict:
        """Build a successful operation response"""
        response = {
            'response': message,
            'success': True,
            **kwargs
        }
        return response
    
    @staticmethod
    def build_error_response(message: str, error: Optional[str] = None, **kwargs) -> Dict:
        """Build an error response with fallback options"""
        response = {
            'response': message,
            'success': False,
            'error': True,
            **kwargs
        }
        if error:
            response['error_details'] = error
        return response
    
    @staticmethod
    def build_clarification_response(message: str, missing_info: List[str], **kwargs) -> Dict:
        """Build response when more information is needed"""
        return {
            'response': message,
            'needs_clarification': True,
            'missing_info': missing_info,
            **kwargs
        }
    
    @staticmethod
    def build_appointment_confirmation(appointment_details: Dict) -> Dict:
        """Build appointment confirmation response"""
        details = appointment_details
        
        confirmation_message = f"""✅ Perfect! Your appointment has been successfully booked!

📅 **Date**: {details.get('date')}
⏰ **Time**: {details.get('start_time')} - {details.get('end_time')}
📝 **Title**: {details.get('title')}
🔗 **Calendar Link**: Available in your Google Calendar

You can view and manage this appointment in your Google Calendar."""
        
        return {
            'response': confirmation_message,
            'appointment_created': True,
            'appointment_details': details,
            'action': 'appointment_confirmed'
        }
    
    @staticmethod
    def build_availability_response(slots_data: Dict) -> Dict:
        """Build response showing available slots"""
        if slots_data['total_slots'] == 0:
            return {
                'response': f"No available slots found for {slots_data['display_date']}. Let me suggest some alternative dates.",
                'available_slots': [],
                'action': 'no_availability'
            }
        
        message = f"""📅 Available slots for {slots_data['display_date']} ({slots_data['day_name']}):

Found {slots_data['total_slots']} available time slots."""
        
        if slots_data.get('has_morning_slots') and slots_data.get('has_afternoon_slots'):
            message += "\n\n🌅 Morning and afternoon slots available!"
        elif slots_data.get('has_morning_slots'):
            message += "\n\n🌅 Morning slots available!"
        elif slots_data.get('has_afternoon_slots'):
            message += "\n\n🌇 Afternoon slots available!"
        
        return {
            'response': message,
            'available_slots': slots_data['slots'],
            'date': slots_data['date'],
            'action': 'show_slots',
            'slot_summary': {
                'total': slots_data['total_slots'],
                'earliest': slots_data.get('earliest_slot'),
                'latest': slots_data.get('latest_slot')
            }
        }
    
    @staticmethod
    def build_alternatives_response(alternatives: List[Dict], original_date: str) -> Dict:
        """Build response with alternative date suggestions"""
        if not alternatives:
            message = f"Unfortunately, I couldn't find any available slots in the next week. Please try a different time period."
            return ResponseBuilder.build_error_response(message)
        
        message = f"Here are some alternative dates with availability:\n\n"
        
        for i, alt in enumerate(alternatives, 1):
            message += f"{i}. **{alt['display_date']}** ({alt['day_name']}) - {alt['slots_count']} slots available\n"
        
        message += "\nWhich date would you prefer?"
        
        return {
            'response': message,
            'suggested_dates': alternatives,
            'original_date': original_date,
            'action': 'choose_alternative_date'
        }
    
    @staticmethod
    def build_help_response() -> Dict:
        """Build comprehensive help response"""
        help_message = """👋 Hello! I'm your AI Appointment Assistant. Here's what I can help you with:

📅 **BOOK APPOINTMENTS**
• "Book appointment tomorrow at 2 PM"
• "Schedule a meeting for next Monday at 10 AM"
• "I need a doctor appointment this Friday"

🔍 **CHECK AVAILABILITY**
• "Show me available slots for tomorrow"
• "What times are free on Monday?"
• "Check availability for next week"

❓ **GET HELP**
• "What can you do?"
• "How do I book an appointment?"
• "Help me schedule a meeting"

💡 **TIPS**
• Be specific with dates and times for best results
• I understand natural language like "tomorrow", "next Monday"
• I can suggest alternatives if your preferred time isn't available

What would you like to do today?"""
        
        return {
            'response': help_message,
            'action': 'general_help',
            'available_commands': [
                'Book appointment for [date] at [time]',
                'Show available slots for [date]',
                'Check my schedule for [date]',
                'Help with appointments'
            ]
        }
    
    @staticmethod
    def build_time_conflict_response(requested_time: str, alternatives: List[Dict]) -> Dict:
        """Build response when requested time is not available"""
        message = f"Unfortunately, {requested_time} is not available. Here are some nearby alternatives:"
        
        return {
            'response': message,
            'requested_time': requested_time,
            'available_slots': alternatives[:3],  # Show 3 best alternatives
            'action': 'show_alternatives'
        }
    
    @staticmethod
    def build_business_hours_error(requested_time: str, suggested_times: list) -> Dict:
        """Build response for times outside business hours"""
        
        suggestions = ", ".join(suggested_times) if suggested_times else "10:00, 11:00, 14:00, 15:00"
        
        return {
            'response': f"""⚠️ Sorry, {requested_time} is outside our business hours.

🕘 **Business Hours**: {get_business_hours_display()} (Monday to Friday)

✅ **Available times today**: {suggestions}

Please choose a time within business hours for your appointment.""",
            'action': 'business_hours_violation',
            'suggested_times': suggested_times,
            'business_hours': get_business_hours_display(),
            'success': False,
            'error': True
        }
    
    @staticmethod
    def build_weekend_error(requested_date: str, day_name: str, suggested_dates: list) -> Dict:
        """Build response for weekend booking attempts"""
        
        if suggested_dates and isinstance(suggested_dates[0], dict):
            # If suggested_dates is already in proper format
            suggestions = ", ".join([
                f"{date['display_date']} ({date['day_name']})" 
                for date in suggested_dates[:3]
            ])
        else:
            # Fallback for string format
            suggestions = "next Monday, Tuesday, Wednesday"
        
        return {
            'response': f"""⚠️ Sorry, we don't operate on {day_name}.

🗓️ **Business Days**: Monday to Friday only
🕘 **Business Hours**: {get_business_hours_display()}

✅ **Next available business days**: {suggestions}

Please choose a weekday for your appointment.""",
            'action': 'weekend_violation',
            'suggested_dates': suggested_dates,
            'business_days': 'Monday to Friday',
            'success': False,
            'error': True
        }
    
    @staticmethod
    def format_slot_list(slots: List[Dict], max_display: int = 5) -> str:
        """Format list of slots for display"""
        if not slots:
            return "No slots available"
        
        display_slots = slots[:max_display]
        formatted = []
        
        for i, slot in enumerate(display_slots, 1):
            formatted.append(f"{i}. {slot['start_time']} - {slot['end_time']}")
        
        result = "\n".join(formatted)
        
        if len(slots) > max_display:
            result += f"\n... and {len(slots) - max_display} more slots"
        
        return result