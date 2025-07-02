
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file (local development)
load_dotenv()

class Settings:
    def __init__(self):
        # API Keys
        self.GROQ_API_KEY = self._get_secret("GROQ_API_KEY")
        
        # Google Calendar - support both methods
        self.GOOGLE_CREDENTIALS_PATH = self._get_secret("GOOGLE_CREDENTIALS_PATH")
        self.GOOGLE_CREDENTIALS_JSON = self._get_secret("GOOGLE_CREDENTIALS_JSON")
        
        # Application Settings
        self.APP_NAME = "AI Appointment Assistant"
        self.DEBUG = True
        self.HOST = "0.0.0.0"
        self.PORT = 8000
    
    @staticmethod
    def _get_secret(key):
        """Get secret from Streamlit secrets or environment variables"""
        # Try Streamlit secrets first (for cloud deployment)
        try:
            return st.secrets[key]
        except:
            # Fallback to environment variables (for local development)
            return os.getenv(key)
    
    # Validating required environment variables
    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        
        # Accept either credentials method
        if not self.GOOGLE_CREDENTIALS_PATH and not self.GOOGLE_CREDENTIALS_JSON:
            raise ValueError("Either GOOGLE_CREDENTIALS_PATH or GOOGLE_CREDENTIALS_JSON is required")

# Create a global settings instance
settings = Settings()
settings.validate()