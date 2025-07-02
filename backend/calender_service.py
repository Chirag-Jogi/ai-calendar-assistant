import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False
    print("⚠️ Google API libraries not available")

from config.settings import settings
from config.business_hours import BUSINESS_START_HOUR, BUSINESS_END_HOUR

# Google Calendar API Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_credentials():
    """Get Google Calendar credentials with fallback handling"""
    if not GOOGLE_LIBS_AVAILABLE:
        raise ImportError("Google API libraries not installed")
    
    # Method 1: Try file path first (for local development)
    if settings.GOOGLE_CREDENTIALS_PATH and os.path.exists(settings.GOOGLE_CREDENTIALS_PATH):
        try:
            credentials = Credentials.from_service_account_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                scopes=SCOPES
            )
            print("✅ Using credentials from file")
            return credentials
        except Exception as e:
            print(f"❌ File credentials failed: {str(e)}")
    
    # Method 2: Use JSON content from environment variable
    elif settings.GOOGLE_CREDENTIALS_JSON:
        try:
            if isinstance(settings.GOOGLE_CREDENTIALS_JSON, str):
                credentials_info = json.loads(settings.GOOGLE_CREDENTIALS_JSON)
            else:
                credentials_info = settings.GOOGLE_CREDENTIALS_JSON
                
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=SCOPES
            )
            print("✅ Using credentials from environment variable")
            return credentials
        except Exception as e:
            print(f"❌ JSON credentials failed: {str(e)}")
    
    raise ValueError("No valid Google credentials found")

class CalendarService:
    def __init__(self):
        """Initialize Google Calendar service with robust error handling"""
        self.credentials = None
        self.service = None
        self.is_available = False
        
        try:
            if GOOGLE_LIBS_AVAILABLE:
                self._authenticate()
                self.is_available = True
            else:
                print("❌ Google API libraries not available")
        except Exception as e:
            print(f"❌ Calendar service initialization failed: {str(e)}")
            self.is_available = False

    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        try:
            self.credentials = get_calendar_credentials()
            self.service = build('calendar', 'v3', credentials=self.credentials)
            print("✅ Google Calendar authentication successful")
        except Exception as e:
            print(f"❌ Google Calendar authentication failed: {str(e)}")
            raise



    def get_available_slots(self, date: datetime, duration_hours: int = 1) -> List[Dict]:
        """Get available time slots for a given date"""
        if not self.is_available:
            print("❌ Calendar service not available")
            return []
            
        try:
            print(f"📅 Getting available slots for: {date.strftime('%Y-%m-%d')}")
            
            # Define business hours using centralized config
            start_hour = BUSINESS_START_HOUR
            end_hour = BUSINESS_END_HOUR
            
            # Create start and end times for the day
            day_start = date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            day_end = date.replace(hour=end_hour, minute=0, second=0, microsecond=0)
            
            print(f"🕘 Business hours: {day_start.strftime('%H:%M')} - {day_end.strftime('%H:%M')}")
            
            # Get existing events for the day
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=day_start.isoformat() + 'Z',
                timeMax=day_end.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            print(f"📋 Found {len(events)} existing events")
            
            # Find available slots
            available_slots = []
            current_time = day_start
            
            for event in events:
                try:
                    event_start = datetime.fromisoformat(
                        event['start'].get('dateTime', event['start'].get('date')).replace('Z', '+00:00')
                    ).replace(tzinfo=None)
                    event_end = datetime.fromisoformat(
                        event['end'].get('dateTime', event['end'].get('date')).replace('Z', '+00:00')
                    ).replace(tzinfo=None)
                    
                    print(f"📅 Event: {event_start.strftime('%H:%M')} - {event_end.strftime('%H:%M')}")
                    
                    # Check if there's a gap before this event
                    if (event_start - current_time).total_seconds() >= duration_hours * 3600:
                        slot_end = min(event_start, current_time + timedelta(hours=duration_hours))
                        if slot_end > current_time:
                            available_slots.append({
                                'start_time': current_time.strftime('%H:%M'),
                                'end_time': slot_end.strftime('%H:%M'),
                                'start': current_time,
                                'end': slot_end,
                                'duration': str(duration_hours) + ' hour(s)'
                            })
                            print(f"✅ Added slot: {current_time.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}")
                    
                    current_time = max(current_time, event_end)
                except Exception as e:
                    print(f"⚠️ Error parsing event: {str(e)}")
                    continue
            
            # Check if there's time left at the end of the day
            if (day_end - current_time).total_seconds() >= duration_hours * 3600:
                end_slot_time = current_time + timedelta(hours=duration_hours)
                available_slots.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': end_slot_time.strftime('%H:%M'),
                    'start': current_time,
                    'end': end_slot_time,
                    'duration': str(duration_hours) + ' hour(s)'
                })
                print(f"✅ Added end-of-day slot: {current_time.strftime('%H:%M')} - {end_slot_time.strftime('%H:%M')}")
            
            print(f"📊 Total available slots: {len(available_slots)}")
            return available_slots
            
        except Exception as e:
            print(f"❌ Error getting available slots: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        """Check if a time slot is available"""
        if not self.is_available:
            return False
            
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_time.isoformat() + 'Z',
                timeMax=end_time.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return len(events) == 0
            
        except Exception as e:
            print(f"❌ Error checking availability: {str(e)}")
            return False

    def get_calendar_list(self):
        """Get list of available calendars"""
        if not self.is_available:
            return []
            
        try:
            calendars_result = self.service.calendarList().list().execute()
            return calendars_result.get('items', [])
        except Exception as e:
            print(f"❌ Error getting calendars: {str(e)}")
            return []

    def create_event(self, title: str, start_time: datetime, end_time: datetime, description: str = "") -> dict:
        """Create a calendar event"""
        if not self.is_available:
            return {'success': False, 'error': 'Calendar service not available'}
            
        try:
            event = {
                'summary': title,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            result = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                'success': True,
                'event_id': result.get('id'),
                'html_link': result.get('htmlLink'),
                'event_details': {
                    'title': title,
                    'start_time': start_time.strftime('%Y-%m-%d %H:%M'),
                    'end_time': end_time.strftime('%Y-%m-%d %H:%M'),
                    'description': description
                }
            }
            
        except Exception as e:
            print(f"❌ Error creating event: {str(e)}")
            return {'success': False, 'error': str(e)}

    def check_for_conflicts(self, start_time: datetime, end_time: datetime) -> list:
        """Check for conflicting events"""
        if not self.is_available:
            return []
            
        try:
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            conflicts = []
            
            for event in events:
                conflicts.append({
                    'title': event.get('summary', 'No title'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date'))
                })
            
            return conflicts
            
        except Exception as e:
            print(f"❌ Error checking conflicts: {str(e)}")
            return []

# Create global instance with error handling
try:
    calendar_service = CalendarService()
except Exception as e:
    print(f"❌ Failed to create calendar service: {str(e)}")
    calendar_service = None