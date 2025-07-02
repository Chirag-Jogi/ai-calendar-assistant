import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Google Calendar - support both methods
    GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH")
    GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    # Application Settings
    APP_NAME = "AI Appointment Assistant"
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 8000
    
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