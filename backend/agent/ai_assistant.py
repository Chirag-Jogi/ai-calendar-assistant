"""
Main AI Assistant - Direct HTTP API Approach
Clean, reliable, and dependency-free
"""
import os
import json
import httpx
from datetime import datetime, timedelta
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

from backend.prompts.appointment_prompts import AppointmentPrompts
from backend.calender_service import calendar_service

# Import our clean helper modules
from .helpers.date_parser import DateParser
from .helpers.slot_manager import SlotManager
from .helpers.response_builder import ResponseBuilder

class AIAssistant:
    """AI Assistant with Direct HTTP API - Clean and Reliable"""
    
    def __init__(self):
        """Initialize AI Assistant with Direct HTTP API"""
        print("🤖 AIAssistant initializing...")
        
        # Direct API configuration
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-8b-8192"
        
        # HTTP headers
        self.headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        # System personality
        self.system_prompt = """You are a professional AI Appointment Assistant. You help users:
        - Schedule appointments in their Google Calendar
        - Check availability for meetings
        - Provide clear, helpful responses
        
        Always be polite, professional, and efficient."""
        
        print("✅ AIAssistant ready to help!")
    
    def process_message(self, user_message: str) -> Dict:
        """Main method to process user messages and handle requests"""
        try:
            print(f"🤖 Processing: {user_message}")
            
            # Step 1: Extract intent from user message
            intent_data = self._extract_intent(user_message)
            print(f"🔍 Intent detected: {intent_data.get('intent', 'unknown')}")
            
            # Step 2: Route to appropriate handler based on intent
            if intent_data['intent'] == 'book_appointment':
                return self._handle_booking(user_message, intent_data)
            elif intent_data['intent'] == 'check_availability':
                return self._handle_availability(intent_data)
            elif intent_data['intent'] == 'cancel_appointment':
                return self._handle_cancellation(intent_data)
            else:
                return ResponseBuilder.build_help_response()
                
        except Exception as e:
            print(f"❌ Error processing message: {str(e)}")
            return ResponseBuilder.build_error_response(
                'I apologize, but I encountered an error. Please try again.',
                error=str(e)
            )
    
    def _extract_intent(self, user_message: str) -> Dict:
        """Extract intent using Direct HTTP API to Groq with better JSON parsing"""
        try:
            print(f"🔍 Analyzing intent for: {user_message}")
            
            # Get specialized prompt from our prompts file
            prompt = AppointmentPrompts.get_intent_prompt(user_message)
            
            # Create payload for Groq API
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 500,
                "stream":False
            }
            
            # Make direct HTTP request to Groq
            response = httpx.post(self.groq_url, headers=self.headers, json=payload , timeout=15.0)
            
            # Check if request was successful
            if response.status_code == 200:
                ai_content = response.json()["choices"][0]["message"]["content"]
                print(f"🤖 AI Raw Response: {ai_content}")
                
                # Better JSON extraction - find JSON block
                try:
                    # Method 1: Extract JSON using string manipulation
                    json_start = ai_content.find('{')
                    json_end = ai_content.rfind('}') + 1
                    
                    if json_start != -1 and json_end > json_start:
                        json_str = ai_content[json_start:json_end]
                        intent_data = json.loads(json_str)
                        
                        # Add validation for empty or incomplete JSON
                        if not intent_data or 'intent' not in intent_data:
                            print("⚠️ Empty or invalid JSON, using fallback")
                            return self._simple_intent_fallback(user_message)
                            
                        print(f"✅ Parsed Intent: {intent_data}")
                        return intent_data
                    else:
                        print("⚠️ No JSON found, using fallback")
                        return self._simple_intent_fallback(user_message)
                        
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed: {str(e)}, using fallback")
                    return self._simple_intent_fallback(user_message)
            else:
                print(f"❌ API request failed: {response.status_code}")
                return self._simple_intent_fallback(user_message)
                
        except Exception as e:
            print(f"❌ AI intent extraction failed: {str(e)}")
            return self._simple_intent_fallback(user_message)
    
    def _simple_intent_fallback(self, message: str) -> Dict:
        """Simple keyword-based intent extraction when AI fails"""
        print(f"🔄 Using fallback method for: {message}")
        
        message_lower = message.lower()
        
        # Intent detection using simple keywords
        if any(word in message_lower for word in ['book', 'schedule', 'appointment', 'create', 'make']):
            intent = 'book_appointment'
        elif any(word in message_lower for word in ['available', 'free', 'slots', 'show', 'check']):
            intent = 'check_availability'
        elif any(word in message_lower for word in ['cancel', 'delete', 'remove']):
            intent = 'cancel_appointment'
        else:
            intent = 'general_query'
        
        # Simple date extraction
        date = None
        if 'tomorrow' in message_lower:
            date = 'tomorrow'
        elif 'today' in message_lower:
            date = 'today'
        elif 'monday' in message_lower:
            date = 'next monday'
        elif 'tuesday' in message_lower:
            date = 'next tuesday'
        elif 'friday' in message_lower:
            date = 'next friday'
        
        # Simple time extraction
        time = None
        if '2pm' in message_lower or '2 pm' in message_lower:
            time = '2pm'
        elif '10am' in message_lower or '10 am' in message_lower:
            time = '10am'
        elif '3pm' in message_lower or '3 pm' in message_lower:
            time = '3pm'
        elif '9am' in message_lower or '9 am' in message_lower:
            time = '9am'
        
        return {
            'intent': intent,
            'date': date,
            'time': time,
            'duration_minutes': 60,
            'appointment_type': 'appointment',
            'confidence': 'low'
        }
    
    def _handle_booking(self, user_message: str, intent_data: Dict) -> Dict:
        """Handle appointment booking requests with clean helper methods"""
        print(f"📅 Handling booking request...")
        
        # Check if we have minimum required information
        if not intent_data.get('date'):
            return ResponseBuilder.build_clarification_response(
                "I'd be happy to help you book an appointment! When would you like to schedule it? For example: 'tomorrow at 2 PM' or 'next Monday morning'",
                missing_info=['date']
            )
        
        try:
            # Parse date using helper
            target_date = DateParser.parse_date(intent_data['date'])
            
            # Get available slots using helper
            slots_data = SlotManager.get_available_slots_with_details(target_date)
            
            # Check if any slots are available
            if slots_data['total_slots'] == 0:
                alternatives = SlotManager.suggest_alternative_dates(target_date)
                return ResponseBuilder.build_alternatives_response(alternatives, target_date.strftime('%Y-%m-%d'))
            
            # If user specified a time, try to book that specific slot
            if intent_data.get('time'):
                return self._book_specific_time(target_date, intent_data, user_message)
            else:
                # Show available options for user to choose
                return ResponseBuilder.build_availability_response(slots_data)
                
        except Exception as e:
            print(f"❌ Booking error: {str(e)}")
            return ResponseBuilder.build_error_response(
                "I encountered an issue while checking availability. Could you please try rephrasing your request?",
                error=str(e)
            )
    
    def _book_specific_time(self, date: datetime, intent_data: Dict, original_message: str) -> Dict:
        """Book appointment at specific requested time using helpers"""
        print(f"⏰ Booking specific time: {intent_data.get('time')}")
        
        # Check time availability using helper (now includes business hours validation)
        availability = SlotManager.check_time_availability(
            date, 
            intent_data.get('time', '14:00'),
            intent_data.get('duration_minutes', 60)
        )
        
        if availability.get('available'):
            # Create appointment using helper
            appointment_title = f"AI Scheduled - {intent_data.get('appointment_type', 'Appointment')}"
            
            result = SlotManager.create_appointment_with_validation(
                title=appointment_title,
                start_time=availability['start_time'],
                end_time=availability['end_time'],
                description=f"Scheduled via AI Assistant. Original request: {original_message}"
            )
            
            if result['success']:
                return ResponseBuilder.build_appointment_confirmation(result['appointment_details'])
            else:
                return ResponseBuilder.build_error_response(result.get('message', 'Failed to create appointment'))
        else:
            # Handle business hours violation
            if availability.get('business_hours_violation'):
                return ResponseBuilder.build_business_hours_error(
                    intent_data.get('time'), 
                    availability.get('suggested_times', [])
                )
            # Handle weekend violation
            elif availability.get('weekend_violation'):
                day_name = date.strftime('%A')
                return ResponseBuilder.build_weekend_error(
                    date.strftime('%Y-%m-%d'),
                    day_name,
                    availability.get('suggested_dates', [])
                )
            else:
                # Time conflicts with existing appointments or other issues
                slots_data = SlotManager.get_available_slots_with_details(date)
                return ResponseBuilder.build_time_conflict_response(
                    intent_data.get('time'), 
                    slots_data['slots'][:3]
                )
    
    def _handle_availability(self, intent_data: Dict) -> Dict:
        """Handle requests to check available time slots using helpers"""
        print(f"🔍 Checking availability...")
        
        # Parse date
        date_str = intent_data.get('date', 'tomorrow')
        target_date = DateParser.parse_date(date_str)
        
        # Get availability data using helper
        slots_data = SlotManager.get_available_slots_with_details(target_date)
        
        if slots_data['total_slots'] > 0:
            return ResponseBuilder.build_availability_response(slots_data)
        else:
            alternatives = SlotManager.suggest_alternative_dates(target_date)
            return ResponseBuilder.build_alternatives_response(alternatives, target_date.strftime('%Y-%m-%d'))
    
    def _handle_cancellation(self, intent_data: Dict) -> Dict:
        """Handle appointment cancellation requests"""
        return {
            'response': 'Appointment cancellation feature is coming soon! For now, please cancel appointments directly in your Google Calendar.',
            'action': 'cancellation_not_available',
            'help_text': 'You can access your calendar at calendar.google.com'
        }

# Create global AI Assistant instance
ai_assistant = AIAssistant()