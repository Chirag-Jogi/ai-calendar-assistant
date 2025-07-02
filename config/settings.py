
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        # API Keys
        self.GROQ_API_KEY = self._get_secret("GROQ_API_KEY")
        
        # Google Calendar - support both methods
        self.GOOGLE_CREDENTIALS_PATH = self._get_secret("GOOGLE_CREDENTIALS_PATH")
        self.GOOGLE_CREDENTIALS_JSON = self._get_secret("GOOGLE_CREDENTIALS_JSON")
        
        # Application Settings
        self.APP_NAME = "AI Calendar Assistant"
        self.DEBUG = True
        self.HOST = "0.0.0.0"
        self.PORT = 8000
    
    @staticmethod
    def _get_secret(key):
        """Get secret from environment variables or Streamlit secrets"""
        # First try environment variables (most reliable)
        value = os.getenv(key)
        if value:
            return value
            
        # Try Streamlit secrets if available (for cloud deployment)
        try:
            import streamlit as st
            return st.secrets[key]
        except:
            return None
    
    def validate(self):
        """Validate settings - don't crash on missing values"""
        if not self.GROQ_API_KEY:
            print("⚠️ Warning: GROQ_API_KEY not found")
            return False
        
        if not self.GOOGLE_CREDENTIALS_PATH and not self.GOOGLE_CREDENTIALS_JSON:
            print("⚠️ Warning: No Google credentials found")
            return False
            
        return True

# Create settings instance
settings = Settings()
# Don't crash on validation failure
validation_result = settings.validate()