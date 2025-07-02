import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config.settings import settings
import json

# Google Calendar API Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_credentials():
    """Get Google Calendar credentials from file or environment variable"""
    
    # Method 1: Try file path first (for local development)
    if settings.GOOGLE_CREDENTIALS_PATH and os.path.exists(settings.GOOGLE_CREDENTIALS_PATH):
        credentials = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_PATH,
            scopes=SCOPES
        )
        print("✅ Using credentials from file")
        return credentials
    
    # Method 2: Use JSON content from environment variable (for Railway deployment)
    elif settings.GOOGLE_CREDENTIALS_JSON:
        try:
            credentials_info = json.loads(settings.GOOGLE_CREDENTIALS_JSON)
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=SCOPES
            )
            print("✅ Using credentials from environment variable")
            return credentials
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid GOOGLE_CREDENTIALS_JSON format: {str(e)}")
    
    else:
        raise ValueError("No valid Google credentials found. Please set GOOGLE_CREDENTIALS_PATH or GOOGLE_CREDENTIALS_JSON")
    

class CalendarService:
    def __init__(self):
        "Initialize Google Calendar service with account credentials"
        self.credentials = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API using service account"""
        try:
            # Define required scopes for calendar access
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            
            # Load credentials from service account file
            self.credentials = Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                scopes=SCOPES
            )
            
            # Build the calendar service
            self.service = build('calendar', 'v3', credentials=self.credentials)
            print("✅ Google Calendar authentication successful")
            
        except Exception as e:
            print(f"Google Calendar authentication failed: {str(e)}")
            raise



    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if a time slot is available in the calendar"""
        try:
            # Query calendar for events in the specified time range
            events_result = self.service.events().list(
                calendarId='chiragjogi97@gmail.com',   # Use 'primary' for the primary calendar
                timeMin=start_time.isoformat() + 'Z', # 'Z' indicates UTC time
                timeMax=end_time.isoformat() + 'Z',   
                singleEvents=True,   # Return single events instead of recurring ones
                orderBy='startTime'    # Order events by start time
            ).execute()
            
            events = events_result.get('items', [])  # Get list of events
            
            # If no events found, slot is available
            return len(events) == 0
            
        except HttpError as error:
            print(f"Error checking availability: {error}")
            return False
        


    def get_available_slots(self, date: datetime, duration_minutes: int = 60) -> List[Dict]:
        """Get available time slots for a specific date"""
        available_slots = []
        
        # Define working hours (9 AM to 5 PM)
        start_hour = 9
        end_hour = 17
        
        # Create time slots for the day
        current_time = date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        
        while current_time < end_of_day:
            slot_end = current_time + timedelta(minutes=duration_minutes)
            
            # Check if this slot is available
            if self.check_availability(current_time, slot_end):
                available_slots.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': slot_end.strftime('%H:%M'),
                    'datetime': current_time
                })
            
            # Move to next hour
            current_time += timedelta(hours=1)
        
        return available_slots


    # ...existing code...

    def create_appointment(self, title: str, start_time: datetime, 
                          end_time: datetime, description: str = "") -> Dict:
        """Create a new appointment in the calendar"""
        try:
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',  # Use appropriate timezone
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Asia/Kolkata',
                },
            }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId='chiragjogi97@gmail.com',
                body=event
            ).execute()
            
            print(f"✅ Appointment created: {created_event.get('htmlLink')}")
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink'),
                'message': f"Appointment '{title}' created successfully"
            }
            
        except HttpError as error:
            print(f"Error creating appointment: {error}")
            return {
                'success': False,
                'error': str(error),
                'message': "Failed to create appointment"
            }

# Create global calendar service instance
calendar_service = CalendarService() 