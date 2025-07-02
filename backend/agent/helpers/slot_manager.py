"""
Slot Management and Availability Logic
Handles calendar slots, availability checks, and suggestions
"""
from datetime import datetime, timedelta
from typing import List, Dict
from backend.calender_service import calendar_service

class SlotManager:
    """Utility class for managing appointment slots and availability"""
    
    @staticmethod
    def suggest_alternative_dates(original_date: datetime, max_suggestions: int = 3) -> List[Dict]:
        """Suggest alternative dates when original date has no availability"""
        print(f"💡 Suggesting alternatives for: {original_date.strftime('%Y-%m-%d')}")
        
        alternatives = []
        current_date = original_date + timedelta(days=1)  # Start from next day
        
        # Check up to 7 days ahead
        for i in range(7):
            check_date = current_date + timedelta(days=i)
            slots = calendar_service.get_available_slots(check_date)
            
            if slots:  # If this date has available slots
                # Safely get first slot time
                first_slot_time = None
                if slots:
                    first_slot = slots[0]
                    if 'start_time' in first_slot:
                        first_slot_time = first_slot['start_time']
                    elif 'start' in first_slot:
                        if isinstance(first_slot['start'], str):
                            first_slot_time = first_slot['start']
                        else:
                            first_slot_time = first_slot['start'].strftime('%H:%M')
                
                alternatives.append({
                    'date': check_date.strftime('%Y-%m-%d'),
                    'display_date': check_date.strftime('%B %d, %Y'),
                    'day_name': check_date.strftime('%A'),
                    'slots_count': len(slots),
                    'first_slot': first_slot_time
                })
                
                # Stop after finding required suggestions
                if len(alternatives) >= max_suggestions:
                    break
        
        print(f"💡 Found {len(alternatives)} alternative dates")
        return alternatives
    
    @staticmethod
    def check_time_availability(target_date: datetime, time_str: str, duration_minutes: int = 60) -> Dict:
        """Check if specific time slot is available with business hours validation"""
        from .date_parser import DateParser
        from datetime import time
        
        try:
            # Parse the requested time
            hour, minute = DateParser.parse_time(time_str)
            start_time = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            # **BUSINESS DAYS VALIDATION (Monday=0, Sunday=6)**
            weekday = target_date.weekday()
            if weekday >= 5:  # Saturday=5, Sunday=6
                day_name = target_date.strftime('%A')
                return {
                    'available': False,
                    'reason': f'Cannot schedule appointments on {day_name}. We only operate Monday to Friday.',
                    'suggested_dates': SlotManager._get_next_business_days(target_date, 3),
                    'weekend_violation': True
                }
            
            # **BUSINESS HOURS VALIDATION**
            business_start = time(10, 0)  # 10:00 AM
            business_end = time(18, 0)    # 6:00 PM
            
            requested_time_obj = start_time.time()
            
            # Check if requested time is before business hours
            if requested_time_obj < business_start:
                return {
                    'available': False,
                    'reason': f'Requested time {time_str} is before business hours (10:00 AM - 6:00 PM)',
                    'suggested_times': ['10:00', '11:00', '12:00', '14:00'],
                    'business_hours_violation': True
                }
            
            # Check if requested time is after business hours
            if requested_time_obj >= business_end:
                return {
                    'available': False,
                    'reason': f'Requested time {time_str} is after business hours (10:00 AM - 6:00 PM)',
                    'suggested_times': ['14:00', '15:00', '16:00', '17:00'],
                    'business_hours_violation': True
                }
            
            # Check if appointment would end after business hours
            if end_time.time() > business_end:
                return {
                    'available': False,
                    'reason': f'Appointment would end at {end_time.strftime("%H:%M")}, which is after business hours',
                    'suggested_times': ['10:00', '11:00', '14:00', '15:00'],
                    'business_hours_violation': True
                }
            
            # Check calendar availability
            is_available = calendar_service.check_availability(start_time, end_time)
            
            if not is_available:
                return {
                    'available': False,
                    'reason': 'Time slot conflicts with existing appointment',
                    'start_time': start_time,
                    'end_time': end_time,
                    'conflict': True
                }
            
            # Time is available!
            return {
                'available': True,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration_minutes,
                'formatted_time': start_time.strftime('%I:%M %p')
            }
            
        except Exception as e:
            print(f"❌ Error checking time availability: {str(e)}")
            return {
                'available': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_available_slots_with_details(target_date: datetime) -> Dict:
        """Get available slots with additional metadata"""
        try:
            slots = calendar_service.get_available_slots(target_date)
            
            # Handle case where slots might be empty or have different formats
            if not slots:
                return {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'display_date': target_date.strftime('%B %d, %Y'),
                    'day_name': target_date.strftime('%A'),
                    'slots': [],
                    'total_slots': 0,
                    'has_morning_slots': False,
                    'has_afternoon_slots': False,
                    'earliest_slot': None,
                    'latest_slot': None
                }
            
            # Helper function to safely get time string from slot
            def get_time_string(slot):
                if 'start_time' in slot:
                    return slot['start_time']
                elif 'start' in slot:
                    if isinstance(slot['start'], str):
                        return slot['start']
                    else:
                        return slot['start'].strftime('%H:%M')
                return '00:00'
            
            # Safely parse times for morning/afternoon checks
            def is_morning_slot(slot):
                try:
                    time_str = get_time_string(slot)
                    hour = int(time_str.split(':')[0])
                    return hour < 12
                except:
                    return False
            
            def is_afternoon_slot(slot):
                try:
                    time_str = get_time_string(slot)
                    hour = int(time_str.split(':')[0])
                    return hour >= 12
                except:
                    return False
            
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'display_date': target_date.strftime('%B %d, %Y'),
                'day_name': target_date.strftime('%A'),
                'slots': slots,
                'total_slots': len(slots),
                'has_morning_slots': any(is_morning_slot(slot) for slot in slots),
                'has_afternoon_slots': any(is_afternoon_slot(slot) for slot in slots),
                'earliest_slot': get_time_string(slots[0]) if slots else None,
                'latest_slot': get_time_string(slots[-1]) if slots else None
            }
        except Exception as e:
            print(f"❌ Error in get_available_slots_with_details: {str(e)}")
            return {
                'date': target_date.strftime('%Y-%m-%d'),
                'display_date': target_date.strftime('%B %d, %Y'),
                'day_name': target_date.strftime('%A'),
                'slots': [],
                'total_slots': 0,
                'has_morning_slots': False,
                'has_afternoon_slots': False,
                'earliest_slot': None,
                'latest_slot': None
            }
    
    @staticmethod
    def create_appointment_with_validation(title: str, start_time: datetime, 
                                         end_time: datetime, description: str = "") -> Dict:
        """Create appointment with pre-validation"""
        try:
            # Double-check availability before creating
            if not calendar_service.check_availability(start_time, end_time):
                return {
                    'success': False,
                    'error': 'Time slot is no longer available',
                    'message': 'Someone else may have booked this time. Please choose another slot.'
                }
            
            # Create the appointment
            result = calendar_service.create_event(title, start_time, end_time, description)
            
            if result['success']:
                return {
                    'success': True,
                    'appointment_details': {
                        'title': title,
                        'date': start_time.strftime('%Y-%m-%d'),
                        'start_time': start_time.strftime('%H:%M'),
                        'end_time': end_time.strftime('%H:%M'),
                        'duration_minutes': int((end_time - start_time).total_seconds() / 60),
                        'event_link': result.get('html_link'),
                        'event_id': result.get('event_id')
                    },
                    'message': f"Appointment created successfully for {start_time.strftime('%B %d, %Y at %I:%M %p')}"
                }
            else:
                return result
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create appointment due to technical error'
            }
    
    @staticmethod
    def _get_next_business_days(start_date: datetime, count: int = 3) -> List[Dict]:
        """Get next business days (Monday-Friday) from start_date"""
        business_days = []
        current_date = start_date
        days_checked = 0
        
        while len(business_days) < count and days_checked < 14:  # Max 2 weeks ahead
            current_date += timedelta(days=1)
            days_checked += 1
            
            # Check if it's a weekday (Monday=0 to Friday=4)
            if current_date.weekday() < 5:
                business_days.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'display_date': current_date.strftime('%B %d, %Y'),
                    'day_name': current_date.strftime('%A'),
                    'slots_count': 8  # Assume 8 slots available (business hours)
                })
        
        return business_days