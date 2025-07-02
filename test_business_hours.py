#!/usr/bin/env python3
"""
Test Business Hours Consistency
"""
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_business_hours():
    print("🕘 Testing Business Hours Consistency...")
    
    try:
        from config.business_hours import BUSINESS_START_HOUR, BUSINESS_END_HOUR, get_business_hours_display
        from backend.calender_service import calendar_service
        from backend.agent.helpers.slot_manager import SlotManager
        
        print(f"✅ Business Hours Config: {BUSINESS_START_HOUR}:00 - {BUSINESS_END_HOUR}:00")
        print(f"✅ Display Format: {get_business_hours_display()}")
        
        # Test calendar service
        tomorrow = datetime.now() + timedelta(days=1)
        slots = calendar_service.get_available_slots(tomorrow)
        print(f"✅ Calendar service returned {len(slots)} slots")
        
        # Check if any slots start before 10:00
        early_slots = [slot for slot in slots if int(slot.get('start_time', '10:00').split(':')[0]) < 10]
        if early_slots:
            print(f"❌ Found {len(early_slots)} slots before 10:00 AM:")
            for slot in early_slots:
                print(f"   - {slot.get('start_time')} - {slot.get('end_time')}")
        else:
            print("✅ No slots before 10:00 AM (correct)")
        
        # Check if any slots start after 18:00
        late_slots = [slot for slot in slots if int(slot.get('start_time', '10:00').split(':')[0]) >= 18]
        if late_slots:
            print(f"❌ Found {len(late_slots)} slots at or after 6:00 PM:")
            for slot in late_slots:
                print(f"   - {slot.get('start_time')} - {slot.get('end_time')}")
        else:
            print("✅ No slots at or after 6:00 PM (correct)")
        
        # Test slot manager validation
        print("\n🧪 Testing SlotManager time validation:")
        test_times = ['09:00', '10:00', '12:00', '18:00', '19:00']
        
        for test_time in test_times:
            availability = SlotManager.check_time_availability(tomorrow, test_time, 60)
            status = "✅ Available" if availability.get('available') else "❌ Not available"
            reason = availability.get('reason', 'No reason given')
            print(f"   {test_time}: {status} - {reason}")
        
        print("\n🎉 Business Hours Consistency Test Complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_business_hours()
