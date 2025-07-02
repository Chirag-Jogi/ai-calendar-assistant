import json
import os
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import streamlit as st

# Google Calendar API Configuration
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_credentials():
    """Get Google Calendar credentials for Streamlit Cloud"""
    
    # Method 1: Try Streamlit secrets (for cloud deployment)
    try:
        google_creds_json = st.secrets["GOOGLE_CREDENTIALS_JSON"]
        if isinstance(google_creds_json, str):
            credentials_info = json.loads(google_creds_json)
        else:
            credentials_info = google_creds_json
        
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES
        )
        print("✅ Using credentials from Streamlit secrets")
        return credentials
        
    except Exception as e:
        print(f"❌ Streamlit secrets failed: {str(e)}")
    
    # Method 2: Try environment variable (backup)
    try:
        google_creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if google_creds_json:
            credentials_info = json.loads(google_creds_json)
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=SCOPES
            )
            print("✅ Using credentials from environment variable")
            return credentials
    except Exception as e:
        print(f"❌ Environment variable failed: {str(e)}")
    
    # Method 3: Try file path (for local development only)
    try:
        credentials_path = st.secrets.get("GOOGLE_CREDENTIALS_PATH") or os.getenv("GOOGLE_CREDENTIALS_PATH")
        if credentials_path and os.path.exists(credentials_path):
            credentials = Credentials.from_service_account_file(
                credentials_path,
                scopes=SCOPES
            )
            print("✅ Using credentials from file")
            return credentials
    except Exception as e:
        print(f"❌ File path failed: {str(e)}")
    
    raise ValueError("❌ No valid Google credentials found. Please check your Streamlit secrets configuration.")

class CalendarService:
    def __init__(self):
        self.credentials = get_calendar_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)
        print("✅ Google Calendar service initialized")

    def get_calendar_list(self):
        """Get list of available calendars"""
        try:
            calendars_result = self.service.calendarList().list().execute()
            calendars = calendars_result.get('items', [])
            
            print("📅 Available calendars:")
            for calendar in calendars:
                print(f"  - {calendar['summary']} ({calendar['id']})")
            
            return calendars
        except Exception as e:
            print(f"❌ Error getting calendars: {str(e)}")
            return []

    def create_event(self, title: str, start_time: datetime, end_time: datetime, description: str = "") -> dict:
        """Create a calendar event"""
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
            
            # Use primary calendar
            result = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"✅ Event created: {result.get('htmlLink')}")
            
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
            return {
                'success': False,
                'error': str(e)
            }

    def check_for_conflicts(self, start_time: datetime, end_time: datetime) -> list:
        """Check for conflicting events in the specified time range"""
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

# Create global instance
calendar_service = CalendarService()