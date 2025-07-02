import os
from dotenv import load_dotenv

## Load environment variables from .env file
load_dotenv()

class Settings:
    ## Api keys

    GROQ_API_KEY=os.getenv("GROQ_API_KEY")

    # Try file path first, then JSON content
    if os.path.exists(settings.GOOGLE_CREDENTIALS_PATH):
        credentials = Credentials.from_service_account_file(
            settings.GOOGLE_CREDENTIALS_PATH,
            scopes=SCOPES
        )
    else:
        # Use JSON content from environment variable
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if credentials_json:
            credentials_info = json.loads(credentials_json)
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=SCOPES
            )

    ## Google Calendar
    GOOGLE_CREDENTIALS_PATH=os.getenv("GOOGLE_CREDENTIALS_PATH")

    ## Application Settings

    APP_NAME="AI Appointment Assistant"
    DEBUG=True
    HOST="0.0.0.0"
    PORT=8000

    ## Validating required environment variables
    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        if not self.GOOGLE_CREDENTIALS_PATH:
            raise ValueError("GOOGLE_CREDENTIALS_PATH is required")

## Create a global settings instance
settings=Settings()
settings.validate()        
