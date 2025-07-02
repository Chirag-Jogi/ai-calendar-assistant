#!/usr/bin/env python3
"""
Flow Validation Test
Tests the complete data flow from user input to response
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    try:
        from backend.agent.ai_assistant import ai_assistant
        from backend.calender_service import calendar_service
        from backend.agent.helpers.response_builder import ResponseBuilder
        from backend.agent.helpers.slot_manager import SlotManager
        from backend.agent.helpers.date_parser import DateParser
        
        print("✅ All imports successful")
        print(f"✅ AI Assistant: {type(ai_assistant)}")
        print(f"✅ Calendar Service: {type(calendar_service)}")
        print(f"✅ Calendar Available: {calendar_service.is_available if calendar_service else 'None'}")
        
        return ai_assistant, calendar_service
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None

def test_calendar_service(calendar_service):
    """Test calendar service methods"""
    print("\n🔍 Testing Calendar Service...")
    
    if not calendar_service or not calendar_service.is_available:
        print("❌ Calendar service not available")
        return False
    
    try:
        # Test get_available_slots
        tomorrow = datetime.now() + timedelta(days=1)
        print(f"📅 Testing get_available_slots for: {tomorrow.strftime('%Y-%m-%d')}")
        
        slots = calendar_service.get_available_slots(tomorrow)
        print(f"✅ Got {len(slots)} slots")
        
        if slots:
            first_slot = slots[0]
            print(f"✅ First slot structure: {list(first_slot.keys())}")
            print(f"✅ First slot: {first_slot}")
        
        return True
        
    except Exception as e:
        print(f"❌ Calendar service error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_slot_manager():
    """Test SlotManager methods"""
    print("\n🔍 Testing SlotManager...")
    
    try:
        from backend.agent.helpers.slot_manager import SlotManager
        
        tomorrow = datetime.now() + timedelta(days=1)
        print(f"📅 Testing get_available_slots_with_details for: {tomorrow.strftime('%Y-%m-%d')}")
        
        slots_data = SlotManager.get_available_slots_with_details(tomorrow)
        print(f"✅ Slots data keys: {list(slots_data.keys())}")
        print(f"✅ Total slots: {slots_data.get('total_slots', 0)}")
        
        # Test time availability check
        print("\n🔍 Testing check_time_availability...")
        availability = SlotManager.check_time_availability(tomorrow, "14:00", 60)
        print(f"✅ Availability check: {availability}")
        
        return True
        
    except Exception as e:
        print(f"❌ SlotManager error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_assistant_flow(ai_assistant):
    """Test AI assistant complete flow"""
    print("\n🔍 Testing AI Assistant Flow...")
    
    if not ai_assistant:
        print("❌ AI Assistant not available")
        return False
    
    try:
        # Test availability check
        print("📞 Testing: 'give me available slots for tomorrow'")
        response = ai_assistant.process_message("give me available slots for tomorrow")
        print(f"✅ Response keys: {list(response.keys())}")
        print(f"✅ Response: {response.get('response', 'No response')[:100]}...")
        
        # Test booking flow
        print("\n📞 Testing: 'Book appointment tomorrow at 2 PM'")
        response = ai_assistant.process_message("Book appointment tomorrow at 2 PM")
        print(f"✅ Response keys: {list(response.keys())}")
        print(f"✅ Response: {response.get('response', 'No response')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Assistant error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all validation tests"""
    print("🚀 Starting Flow Validation Tests...")
    print("=" * 50)
    
    # Test 1: Imports
    ai_assistant, calendar_service = test_imports()
    if not ai_assistant:
        return
    
    # Test 2: Calendar Service
    calendar_ok = test_calendar_service(calendar_service)
    
    # Test 3: Slot Manager
    slot_manager_ok = test_slot_manager()
    
    # Test 4: AI Assistant Flow
    ai_ok = test_ai_assistant_flow(ai_assistant)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY:")
    print(f"✅ Imports: ✓")
    print(f"✅ Calendar Service: {'✓' if calendar_ok else '❌'}")
    print(f"✅ Slot Manager: {'✓' if slot_manager_ok else '❌'}")
    print(f"✅ AI Assistant: {'✓' if ai_ok else '❌'}")
    
    if calendar_ok and slot_manager_ok and ai_ok:
        print("\n🎉 ALL TESTS PASSED! Flow is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
