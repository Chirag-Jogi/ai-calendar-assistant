#!/usr/bin/env python3
"""
Minimal AI Assistant Test
"""
import sys
import os

# Add project root to path  
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def minimal_test():
    print("🚀 Minimal AI Assistant Test")
    
    try:
        from backend.agent.ai_assistant import ai_assistant
        print("✅ AI Assistant imported successfully")
        
        # Test simple availability check
        print("\n📞 Testing: 'Show me available slots for tomorrow'")
        response = ai_assistant.process_message("Show me available slots for tomorrow")
        
        print(f"✅ Response type: {type(response)}")
        print(f"✅ Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
        
        if 'response' in response:
            print(f"✅ Response message: {response['response'][:200]}...")
        
        if 'error' in response:
            print(f"❌ Error in response: {response.get('error')}")
        
        print("\n🎉 Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_test()
