"""
AI Appointment Assistant Prompts Configuration
Centralized prompt management for better maintainability
"""
from datetime import datetime, timedelta
class AppointmentPrompts:
    """Collection of all AI prompts used in the appointment system"""
    
    # Intent extraction prompt
    INTENT_EXTRACTION = """
    Extract appointment information from this user message: "{user_message}"
    
    IMPORTANT: Return ONLY a valid JSON object, no additional text or explanation.
    
    Format:
    {{
        "intent": "book_appointment|check_availability|cancel_appointment|general_query",
        "date": "tomorrow|today|next monday|etc or null",
        "time": "14:00|2pm|etc or null", 
        "duration_minutes": 60,
        "appointment_type": "meeting|appointment|etc or null",
        "confidence": "high|medium|low"
    }}
    
    Return only the JSON, nothing else.
    """
    
    # Appointment confirmation prompt
    APPOINTMENT_CONFIRMATION = """
    Generate a professional appointment confirmation message.
    
    Appointment Details:
    - Date: {date}
    - Time: {time}
    - Duration: {duration} minutes
    - Type: {appointment_type}
    
    Create a friendly, professional confirmation message that includes:
    1. Confirmation of the appointment
    2. Clear date and time
    3. Next steps if needed
    
    Keep it concise but warm.
    """

    @staticmethod
    def get_intent_prompt(user_message: str) -> str:
        """Enhanced prompt that makes AI do the date parsing work"""
        
        # Get current date info for AI context
        from datetime import datetime
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        day_name = today.strftime('%A')
        
        return f"""
Extract appointment information from: "{user_message}"

CURRENT CONTEXT:
- Today is {today_str} ({day_name})
- Tomorrow is {(today + timedelta(days=1)).strftime('%Y-%m-%d')}
- Day after tomorrow is {(today + timedelta(days=2)).strftime('%Y-%m-%d')}

BUSINESS RULES:
- Business Days: Monday to Friday ONLY (no weekends)
- Business Hours: 10:00 AM to 6:00 PM
- If user requests weekend, suggest next Monday

IMPORTANT: Convert ALL date expressions to YYYY-MM-DD format.

Examples:
- "tomorrow" → "{(today + timedelta(days=1)).strftime('%Y-%m-%d')}"
- "day after tomorrow" → "{(today + timedelta(days=2)).strftime('%Y-%m-%d')}"
- "5 july 2025" → "2025-07-05"
- "july 5" → "2025-07-05" (assume current year)
- "next Monday" → calculate the actual date and return "YYYY-MM-DD"

Return ONLY this JSON:
{{
    "intent": "book_appointment|check_availability|cancel_appointment|general_query",
    "date": "YYYY-MM-DD format or null",
    "time": "HH:MM format (24-hour) or null",
    "duration_minutes": 60,
    "appointment_type": "meeting|appointment|etc or null",
    "confidence": "high|medium|low"
}}

NO explanations, ONLY the JSON.
"""
    
    @classmethod
    def get_confirmation_prompt(cls, **kwargs) -> str:
        """Get formatted confirmation prompt"""
        return cls.APPOINTMENT_CONFIRMATION.format(**kwargs)