"""
Simple Messenger - Notification System Test Script

This script helps test the browser notification functionality.

Run this after starting the messenger server to verify notifications work properly.
"""

import asyncio
import websockets
import json
import time

async def send_test_messages():
    """Send test messages to trigger notifications"""
    
    # Test user credentials
    username = "NotificationBot"
    access_key = "45000"
    
    try:
        # Connect to WebSocket
        ws_url = f"ws://localhost:8000/ws/{username}?lang=en"
        print(f"🔌 Connecting to: {ws_url}")
        
        async with websockets.connect(ws_url) as websocket:
            print("✅ Connected to messenger WebSocket")
            
            # Wait a bit for connection to stabilize
            await asyncio.sleep(2)
            
            # Test 1: Send a regular text message
            print("\n📝 Sending test text message...")
            text_message = {
                "type": "chat",
                "username": username,
                "data": {
                    "username": username,
                    "message": "🔔 This is a test notification message!",
                    "timestamp": time.time()
                }
            }
            await websocket.send(json.dumps(text_message))
            print("✅ Text message sent")
            
            # Wait between messages
            await asyncio.sleep(3)
            
            # Test 2: Send a system message
            print("\n🔧 Sending system notification...")
            system_message = {
                "type": "system",
                "content": f"{username} joined the chat for notification testing"
            }
            await websocket.send(json.dumps(system_message))
            print("✅ System message sent")
            
            # Wait between messages  
            await asyncio.sleep(3)
            
            # Test 3: Simulate file message
            print("\n📁 Sending file notification...")
            file_message = {
                "type": "file",
                "username": username,
                "filename": "test-notification.pdf",
                "file_size": 1024
            }
            await websocket.send(json.dumps(file_message))
            print("✅ File message sent")
            
            # Wait a bit before closing
            await asyncio.sleep(2)
            print("\n🎉 All test notifications sent successfully!")
            print("\n📋 Test Instructions:")
            print("1. Open messenger in browser with a test user")
            print("2. Click the 🔔 bell icon to enable notifications")
            print("3. Switch to another tab or minimize browser")
            print("4. You should see 3 notifications appear")
            print("5. Click a notification to return to the chat")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("- Make sure the messenger server is running (python main.py)")
        print("- Check if localhost:8000 is accessible")
        print("- Verify WebSocket connection is working")

def manual_test_instructions():
    """Print manual testing instructions"""
    print("\n" + "="*60)
    print("🔔 NOTIFICATION SYSTEM - MANUAL TEST GUIDE")
    print("="*60)
    
    print("\n🎯 SETUP:")
    print("1. Start messenger server: python main.py")
    print("2. Open http://localhost:8000 in browser")
    print("3. Enter access key: 45000")
    print("4. Enter username: TestUser1")
    
    print("\n🔔 TEST NOTIFICATIONS:")
    print("1. Look for 🔔 bell icon in header (top right)")
    print("2. Click the bell icon")
    print("3. Grant notification permission when browser asks")
    print("4. Bell icon should disappear")
    print("5. You should see 'Notifications enabled' message")
    
    print("\n📱 TEST MESSAGE NOTIFICATIONS:")
    print("1. Open a second browser tab")
    print("2. Go to messenger with different username: TestUser2")
    print("3. In Tab 2: Send a message")
    print("4. Switch to Tab 1 (make sure it's not active)")
    print("5. You should see notification: 'New message from TestUser2'")
    
    print("\n🎵 TEST VOICE MESSAGE NOTIFICATIONS:")
    print("1. In Tab 2: Click microphone button to record voice")
    print("2. Record a short message and send")
    print("3. Tab 1 should show: 'New voice message from TestUser2'")
    
    print("\n📁 TEST FILE NOTIFICATIONS:")
    print("1. In Tab 2: Click attachment button")
    print("2. Select any file and send")
    print("3. Tab 1 should show: 'New file from TestUser2'")
    
    print("\n✅ EXPECTED BEHAVIORS:")
    print("• Notifications only appear when tab is inactive")
    print("• Notifications auto-close after 5 seconds")
    print("• Clicking notification focuses the messenger tab")
    print("• No notifications when chat tab is active/visible")
    print("• Bell button disappears after permission granted/denied")
    
    print("\n🌍 TEST LANGUAGE SUPPORT:")
    print("1. Change language to Persian (فا)")
    print("2. Repeat notification tests")
    print("3. Notifications should appear in Persian")
    
    print("\n🚫 EXPECTED FAILURES (That's OK):")
    print("• Bell button doesn't appear if notifications already granted")
    print("• Bell button doesn't appear if notifications denied")
    print("• No notifications if browser doesn't support them")
    print("• Notifications blocked if user denied permission")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("❌ No bell button: Check browser notification support")
    print("❌ No notifications: Verify permission was granted")
    print("❌ Always notifications: Check page visibility detection")
    print("❌ Wrong language: Verify language parameter in URL")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("🔔 Simple Messenger - Notification Test Utility")
    print("="*50)
    
    choice = input("\n1️⃣  Run automated test (send test messages)\n2️⃣  Show manual test guide\n\nChoose option (1 or 2): ")
    
    if choice == "1":
        print("\n🤖 Running automated notification test...")
        print("⚠️  Make sure:")
        print("   - Messenger server is running (python main.py)")
        print("   - You have a user connected in browser")
        print("   - Browser tab is inactive to see notifications")
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        try:
            asyncio.run(send_test_messages())
        except KeyboardInterrupt:
            print("\n\n⏹️  Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
    
    elif choice == "2":
        manual_test_instructions()
    
    else:
        print("❌ Invalid choice. Please run again and choose 1 or 2.")
    
    print("\n🎉 Happy testing! Your messenger notifications should work perfectly.")
