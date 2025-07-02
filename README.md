# 🤖 AI Calendar Assistant

A production-ready, AI-powered appointment booking system that integrates with Google Calendar through natural language chat. Built with enterprise-grade security and deployment readiness.

## ✨ Features

- 🗣️ **Natural Language Booking** - Book appointments through conversational AI
- 📅 **Google Calendar Integration** - Seamless calendar management with service account
- ⏰ **Business Rules Enforcement** - Automatic validation of business hours (10 AM - 6 PM, weekdays only)
- 🔒 **Production Security** - All sensitive data properly protected and gitignored
- 🚀 **Deployment Ready** - Ready for cloud deployment
- 💬 **Interactive Chat UI** - Beautiful Streamlit interface for demos and real use

## 🛠️ Quick Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd AI-Appointment-Assistant
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy the template
cp .env.example .env

# Edit .env with your actual values
# Get Groq API key from: https://console.groq.com
GROQ_API_KEY="your_actual_groq_api_key"
```

### 3. Google Calendar Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Calendar API
4. Create a Service Account
5. Download the JSON credentials file
6. Place it at: `config/credentials/service_account.json`
7. Share your Google Calendar with the service account email

### 4. Run the Application
```bash
streamlit run streamlit_app.py
```

## 🚀 Deployment

Ready for deployment on multiple cloud platforms. The project includes a `Procfile` for easy deployment.

### Local Development
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
AI-Appointment-Assistant/
├── .env                          # Environment variables (hidden from Git)
├── .env.example                  # Template for environment setup
├── .gitignore                    # Comprehensive security ignore file
├── requirements.txt              # Production dependencies
├── streamlit_app.py              # Main Streamlit application
├── README.md                     # This file
│
├── backend/
│   ├── agent/
│   │   ├── ai_assistant.py       # Main AI logic with direct API calls
│   │   └── helpers/
│   │       ├── date_parser.py    # Smart date parsing
│   │       ├── slot_manager.py   # Availability & business rules
│   │       └── response_builder.py # User-friendly responses
│   ├── prompts/
│   │   └── appointment_prompts.py # AI prompts & instructions
│   └── calender_service.py       # Google Calendar integration
│
├── config/
│   ├── settings.py               # Application configuration
│   └── credentials/
│       └── service_account.json  # Google service account (hidden)
│
└── test_*.py                     # Test files for development
```

## 🔒 Security Features

- ✅ All sensitive files properly gitignored
- ✅ Service account credentials never committed
- ✅ API keys stored in environment variables
- ✅ Production-ready credential management
- ✅ Comprehensive `.gitignore` for all sensitive data

## 🎯 Business Rules

- **Business Hours**: 10:00 AM - 6:00 PM
- **Working Days**: Monday - Friday only
- **Time Zones**: Configurable (default UTC)
- **Slot Duration**: 1-hour appointments
- **Conflict Detection**: Automatic overlap prevention

## 🧪 Testing

```bash
# Test AI Assistant
python test_ai_assistant.py

# Test Calendar Service
python test_calender_service.py
```

## 📝 Usage Examples

### Chat Interface
- "Book an appointment tomorrow at 2 PM"
- "What slots are available this week?"
- "Schedule a meeting for next Monday morning"
- "Check my calendar for Friday"

### Response Handling
The system provides intelligent responses for:
- ✅ Successful bookings
- ❌ Business hours violations
- ⚠️ Weekend booking attempts
- 📅 Alternative time suggestions
- 🔍 Availability queries

## 🆘 Troubleshooting

### Common Issues

**"Google Calendar access denied"**
- Share your Google Calendar with the service account email: `appointment-bot@mythic-fulcrum-464610-n2.iam.gserviceaccount.com`
- Check that Google Calendar API is enabled in your Google Cloud Console
- Verify credentials are properly configured

**"Groq API error"**
- Verify `GROQ_API_KEY` environment variable is set correctly
- Check Groq console for quota/billing status
- Ensure API key has proper permissions

**"Module not found errors"**
- Install dependencies: `pip install -r requirements.txt`
- Check Python path if running from subdirectories

## 🔧 Development

### Adding New Features
1. Business rule changes: Edit `slot_manager.py`
2. AI behavior: Modify `appointment_prompts.py`
3. UI improvements: Update `streamlit_app.py`
4. Response formatting: Customize `response_builder.py`

### Environment Management
- Development: Use `.env` file
- Production: Set environment variables on hosting platform
- Never commit sensitive files to Git!


---

## 🚀 Ready for Demo?

1. ✅ Security: All sensitive data hidden
2. ✅ Deployment: Ready for cloud deployment
3. ✅ Business Rules: Professional appointment management
4. ✅ UI: Beautiful chat interface
5. ✅ Integration: Google Calendar fully connected

**Perfect for professional appointment management and business demos!**
