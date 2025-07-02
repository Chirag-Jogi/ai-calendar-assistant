#!/usr/bin/env python3
"""
Quick Direct Test for Specific Issues
"""
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_specific_issue():
    """Test the specific 'start_time' error"""
    print("🔍 Testing specific start_time error...")
    
    try:
        from backend.calender_service import calendar_service
        from backend.agent.helpers.slot_manager import SlotManager
        
        if not calendar_service or not calendar_service.is_available:
            print("❌ Calendar service not available")
            return
        
        tomorrow = datetime.now() + timedelta(days=1)
        print(f"📅 Testing for date: {tomorrow.strftime('%Y-%m-%d')}")
        
        # Test 1: Direct calendar service call
        print("\n🧪 Test 1: calendar_service.get_available_slots()")
        slots = calendar_service.get_available_slots(tomorrow)
        print(f"✅ Got {len(slots)} slots from calendar service")
        
        if slots:
            print(f"✅ First slot keys: {list(slots[0].keys())}")
            print(f"✅ First slot content: {slots[0]}")
        
        # Test 2: SlotManager call
        print("\n🧪 Test 2: SlotManager.get_available_slots_with_details()")
        slots_data = SlotManager.get_available_slots_with_details(tomorrow)
        print(f"✅ Slots data keys: {list(slots_data.keys())}")
        print(f"✅ Total slots: {slots_data.get('total_slots', 0)}")
        
        # Test 3: Time availability check
        print("\n🧪 Test 3: SlotManager.check_time_availability()")
        availability = SlotManager.check_time_availability(tomorrow, "14:00", 60)
        print(f"✅ Availability result keys: {list(availability.keys())}")
        print(f"✅ Available: {availability.get('available', False)}")
        
        if availability.get('available'):
            print(f"✅ Start time: {availability.get('start_time')}")
            print(f"✅ End time: {availability.get('end_time')}")
        else:
            print(f"ℹ️ Reason: {availability.get('reason', 'Unknown')}")
        
        print("\n🎉 All specific tests passed!")
        
    except Exception as e:
        print(f"❌ Error in specific test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specific_issue()
