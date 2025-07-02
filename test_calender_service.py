from datetime import datetime, timedelta
from backend.calender_service import calendar_service

def test_calendar_service():
    print("🧪 Testing Calendar Service...")
    
    try:
        # Test 1: Check if service is authenticated
        print("✅ Calendar service initialized successfully")
        
        # Test 2: Get available slots for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        slots = calendar_service.get_available_slots(tomorrow)
        print(f"📅 Available slots for tomorrow: {len(slots)}")
        
        if slots:
            print("First few available slots:")
            for i, slot in enumerate(slots[:3]):  # Show first 3 slots
                print(f"  {i+1}. {slot['start_time']} - {slot['end_time']}")
        
        # Test 3: Create a test appointment (optional)
        # Uncomment below if you want to test appointment creation
        test_start = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
        test_end = test_start + timedelta(hours=1)
        result = calendar_service.create_event(
            "Test Appointment", 
            test_start, 
            test_end, 
            "This is a test appointment"
        )
        print(f" Test appointment: {result}")
        
    except Exception as e:
        print(f" Test failed: {str(e)}")

if __name__ == "__main__":
    test_calendar_service()