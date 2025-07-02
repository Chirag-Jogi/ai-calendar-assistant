import streamlit as st

# MUST be the very first Streamlit command - DO NOT MOVE OR CHANGE THIS
st.set_page_config(
    page_title="🤖 AI Calendar Assistant",
    page_icon="📅",
    layout="wide"
)

# Now import everything else - ORDER MATTERS!
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def safe_import():
    """Safely import modules with error handling"""
    try:
        from backend.agent.ai_assistant import ai_assistant
        from backend.calender_service import calendar_service
        return ai_assistant, calendar_service, None
    except Exception as e:
        return None, None, str(e)

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background-color: #f8f9fa;
        border-left-color: #667eea;
        color: #2c3e50;  /* Dark text for better contrast */
    }
    
    .ai-message {
        background-color: #e3f2fd;
        border-left-color: #4CAF50;
        color: #1565c0;  /* Dark blue text for better contrast */
    }
    
    .success-message {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #f5c6cb;
    }
    
    .info-box {
        background-color: #fff3cd;
        border-color: #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #ffeaa7;
    }
    
    /* Fix Streamlit default text colors */
    .stMarkdown p {
        color: #2c3e50 !important;
    }
    
    /* Fix button text visibility */
    .stButton > button {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #5a6fd8;
        color: white;
    }
    
    /* Fix chat input visibility */
    .stChatInput > div > div > input {
        background-color: white;
        color: #2c3e50;
        border: 2px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'appointments_created' not in st.session_state:
        st.session_state.appointments_created = []

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Appointment Assistant</h1>
        <p>Your intelligent scheduling companion powered by advanced AI</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with features and statistics"""
    with st.sidebar:
        st.markdown("## 🚀 Features")
        
        st.markdown("""
        **✅ Natural Language Booking**
        - "Book appointment tomorrow at 2 PM"
        - "Schedule meeting next Monday"
        
        **✅ Smart Availability Check**
        - "Show me free slots for Friday"
        - "What times are available?"
        
        **✅ Google Calendar Integration**
        - Real calendar appointments
        - Automatic conflict detection
        
        **✅ AI-Powered Understanding**
        - Groq LLaMA 3 AI model
        - Intent recognition
        - Smart fallback system
        """)
        
        st.markdown("---")
        
        # Statistics
        st.markdown("## 📊 Session Stats")
        total_messages = len(st.session_state.chat_history)
        total_appointments = len(st.session_state.appointments_created)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", total_messages)
        with col2:
            st.metric("Appointments", total_appointments)
        
        if st.session_state.appointments_created:
            st.markdown("### 📅 Recent Appointments")
            for apt in st.session_state.appointments_created[-3:]:
                st.markdown(f"- {apt['date']} at {apt['time']}")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("## ⚡ Quick Actions")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
            
        if st.button("📋 Show Available Slots"):
            st.session_state.quick_action = "show_slots"

def display_appointment_confirmation(appointment_details):
    """Display appointment confirmation with success styling"""
    if not appointment_details:
        return
        
    st.markdown(f"""
    <div class="success-message">
        <h4>✅ Appointment Successfully Created!</h4>
        <p><strong>📅 Date:</strong> {appointment_details.get('date')}</p>
        <p><strong>⏰ Time:</strong> {appointment_details.get('start_time')} - {appointment_details.get('end_time')}</p>
        <p><strong>📝 Title:</strong> {appointment_details.get('title')}</p>
        <p><strong>🔗 Calendar:</strong> <a href="{appointment_details.get('event_link', '#')}" target="_blank">View in Google Calendar</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add to session appointments
    st.session_state.appointments_created.append({
        'date': appointment_details.get('date'),
        'time': appointment_details.get('start_time'),
        'title': appointment_details.get('title')
    })

def display_chat_interface():
    """Display the main chat interface"""
    st.markdown("## 💬 Chat with AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {user_msg}
            </div>
            """, unsafe_allow_html=True)
            
            # AI response
            response_text = ai_response.get('response', 'No response')
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>🤖 AI Assistant:</strong> {response_text}
            </div>
            """, unsafe_allow_html=True)
            
            # Display additional info based on response type
            if ai_response.get('available_slots'):
                display_available_slots(ai_response['available_slots'], chat_index=i)
            
            if ai_response.get('appointment_created'):
               display_appointment_confirmation(ai_response['appointment_details'])
            
            if ai_response.get('suggested_dates'):
                display_alternative_dates(ai_response['suggested_dates'], chat_index=i)

def display_available_slots(slots, chat_index=0):
    """Display available time slots in a nice format"""
    if not slots:
        return
    
    st.markdown("### 📅 Available Time Slots")
    
    # Create columns for better layout
    cols = st.columns(3)
    
    for i, slot in enumerate(slots[:9]):  # Show max 9 slots
        col_index = i % 3
        with cols[col_index]:
            # Use chat_index to make keys unique across chat history
            unique_key = f"slot_{chat_index}_{i}"
            if st.button(f"🕐 {slot['start_time']} - {slot['end_time']}", key=unique_key):
                st.session_state.selected_slot = slot
                st.success(f"Selected slot: {slot['start_time']} - {slot['end_time']}")

def display_alternative_dates(suggested_dates, chat_index=0):
    """Display alternative date suggestions"""
    if not suggested_dates:
        return
    
    st.markdown("### 💡 Alternative Dates Available")
    
    for i, date_option in enumerate(suggested_dates):
        # Handle both dictionary and string formats
        if isinstance(date_option, dict):
            display_date = date_option.get('display_date', 'Unknown Date')
            day_name = date_option.get('day_name', 'Unknown Day')
            slots_count = date_option.get('slots_count', 0)
            date_str = date_option.get('date', '')
        else:
            # Fallback for string format
            try:
                from datetime import datetime
                date_obj = datetime.strptime(str(date_option), '%Y-%m-%d')
                display_date = date_obj.strftime('%B %d, %Y')
                day_name = date_obj.strftime('%A')
                slots_count = 8  # Default
                date_str = str(date_option)
            except:
                continue  # Skip invalid entries
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{display_date}** ({day_name})")
        
        with col2:
            st.markdown(f"{slots_count} slots")
        
        with col3:
            unique_key = f"alt_date_{chat_index}_{i}"
            if st.button(f"Select", key=unique_key):
                # Trigger availability check for this date
                process_user_input(f"Show available slots for {date_str}")

def process_user_input(user_input):
    """Process user input and get AI response"""
    try:
        # Get AI assistant and calendar service
        ai_assistant, calendar_service, error = safe_import()
        
        if error:
            st.error(f"❌ Import error: {error}")
            return
            
        if not ai_assistant:
            st.error("❌ AI Assistant not available")
            return
        
        # Show thinking indicator
        with st.spinner("🤖 AI is thinking..."):
            # Get AI response
            ai_response = ai_assistant.process_message(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append((user_input, ai_response))
        
        # Show success/error indicators
        if ai_response.get('success') == False:
            st.error("❌ " + ai_response.get('response', 'Something went wrong'))
        elif ai_response.get('appointment_created'):
            st.success("✅ Appointment created successfully!")
        
        # Rerun to update the interface
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.markdown("""
        <div class="error-message">
            <strong>Error occurred:</strong> Please try again or contact support.
        </div>
        """, unsafe_allow_html=True)

def display_demo_examples():
    """Display example commands for demo purposes"""
    st.markdown("## 🎯 Try These Examples")
    
    examples = [
        "Book appointment tomorrow at 2 PM",
        "Show me available slots for next Monday", 
        "I need a meeting this Friday at 10 AM",
        "Check availability for next week",
        "Schedule doctor appointment tomorrow morning"
    ]
    
    cols = st.columns(2)
    
    for i, example in enumerate(examples):
        col_index = i % 2
        with cols[col_index]:
            if st.button(f"📝 {example}", key=f"example_{i}"):
                process_user_input(example)

def main():
    """Main application function"""
    # Apply custom styling first
    apply_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Display sidebar
    display_sidebar()
    
    # Main chat interface - NOT inside columns
    display_chat_interface()
    
    # Input area - OUTSIDE of any containers
    st.markdown("---")
    user_input = st.chat_input("Type your message here... (e.g., 'Book appointment tomorrow at 2 PM')")
    
    if user_input:
        process_user_input(user_input)
    
    # Demo examples if no chat history
    if not st.session_state.chat_history:
        st.markdown("---")
        display_demo_examples()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by AI | Built for TailorTalk Demo | Google Calendar Integration</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()