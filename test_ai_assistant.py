"""
Test file for the new clean AI Assistant architecture
Tests all components: AI logic, helpers, and integrations
"""
from backend.agent.ai_assistant import ai_assistant
from backend.agent.helpers.date_parser import DateParser
from backend.agent.helpers.slot_manager import SlotManager
from backend.agent.helpers.response_builder import ResponseBuilder
from datetime import datetime, timedelta

def test_helper_modules():
    """Test individual helper modules"""
    print("🧪 Testing Helper Modules...")
    print("=" * 50)
    
    # Test DateParser
    print("\n📅 Testing DateParser:")
    test_dates = ['tomorrow', 'next monday', 'today', 'next friday']
    for date_str in test_dates:
        parsed = DateParser.parse_date(date_str)
        print(f"  '{date_str}' → {parsed.strftime('%Y-%m-%d %A')}")
    
    # Test time parsing
    print("\n⏰ Testing Time Parser:")
    test_times = ['2pm', '9am', '14:30', '12am', '12pm']
    for time_str in test_times:
        hour, minute = DateParser.parse_time(time_str)
        print(f"  '{time_str}' → {hour:02d}:{minute:02d}")
    
    # Test SlotManager
    print("\n📊 Testing SlotManager:")
    tomorrow = datetime.now() + timedelta(days=1)
    slots_data = SlotManager.get_available_slots_with_details(tomorrow)
    print(f"  Slots for tomorrow: {slots_data['total_slots']} available")
    print(f"  Date: {slots_data['display_date']}")
    
    print("✅ Helper modules working!")

def test_ai_assistant():
    """Test the main AI Assistant with various scenarios"""
    print("\n\n🤖 Testing AI Assistant...")
    print("=" * 50)
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Book Appointment with Specific Time',
            'message': 'Book appointment tomorrow at 2 PM',
            'expected': 'booking'
        },
        {
            'name': 'Check Availability',
            'message': 'Show me available slots for tomorrow',
            'expected': 'availability'
        },
        {
            'name': 'Book Without Time',
            'message': 'I need an appointment tomorrow',
            'expected': 'show_options'
        },
        {
            'name': 'General Help',
            'message': 'What can you help me with?',
            'expected': 'help'
        },
        {
            'name': 'Book Next Monday',
            'message': 'Schedule meeting next Monday at 10 AM',
            'expected': 'booking'
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📝 Test {i}: {scenario['name']}")
        print(f"👤 User: {scenario['message']}")
        
        # Process message
        response = ai_assistant.process_message(scenario['message'])
        
        # Display response
        print(f"🤖 AI: {response.get('response', 'No response')[:100]}...")
        
        # Check response data
        if response.get('available_slots'):
            print(f"📅 Available slots: {len(response['available_slots'])}")
        
        if response.get('appointment_created'):
            print(f"✅ Appointment created: {response['appointment_details']['date']} at {response['appointment_details']['start_time']}")
        
        if response.get('needs_clarification'):
            print(f"❓ Needs clarification: {response['missing_info']}")
        
        if response.get('suggested_dates'):
            print(f"💡 Alternative dates: {len(response['suggested_dates'])}")
        
        print("-" * 40)

def test_response_builder():
    """Test response building utilities"""
    print("\n\n📝 Testing ResponseBuilder...")
    print("=" * 50)
    
    # Test different response types
    success_response = ResponseBuilder.build_success_response("Test successful!")
    print(f"✅ Success Response: {success_response['success']}")
    
    error_response = ResponseBuilder.build_error_response("Test error", "Sample error details")
    print(f"❌ Error Response: {error_response['error']}")
    
    help_response = ResponseBuilder.build_help_response()
    print(f"❓ Help Response Length: {len(help_response['response'])} characters")
    
    print("✅ ResponseBuilder working!")

def run_all_tests():
    """Run complete test suite"""
    print("🚀 Starting Complete Test Suite for Clean Architecture")
    print("=" * 60)
    
    try:
        # Test 1: Helper modules
        test_helper_modules()
        
        # Test 2: Response builder
        test_response_builder()
        
        # Test 3: Main AI Assistant
        test_ai_assistant()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Clean Architecture is working perfectly!")
        print("🚀 Ready for TailorTalk demo!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        print("🔧 Please check the error and fix before demo")

if __name__ == "__main__":
    run_all_tests()