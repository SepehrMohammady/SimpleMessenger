#!/usr/bin/env python3
"""
Test script for Simple Messenger voice and video message features
"""

import asyncio
import json
import websockets
import base64
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_voice_message():
    """Test voice message functionality"""
    print("Testing voice message functionality...")
    
    # Create a simple audio blob (simulated)
    audio_data = b"fake_audio_data_for_testing_purposes"
    audio_base64 = f"data:audio/webm;base64,{base64.b64encode(audio_data).decode()}"
    
    voice_message = {
        "type": "voice_message",
        "data": {
            "content": audio_base64,
            "duration": 5
        }
    }
    
    try:
        async with websockets.connect("ws://localhost:8000/ws/test_user") as websocket:
            await websocket.send(json.dumps(voice_message))
            print("✅ Voice message sent successfully")
            
            # Wait for confirmation
            response = await websocket.recv()
            print(f"📨 Response: {response}")
            
    except Exception as e:
        print(f"❌ Voice message test failed: {e}")

async def test_video_message():
    """Test video message functionality"""
    print("Testing video message functionality...")
    
    # Create a simple video blob (simulated)
    video_data = b"fake_video_data_for_testing_purposes"
    video_base64 = f"data:video/webm;base64,{base64.b64encode(video_data).decode()}"
    
    video_message = {
        "type": "video_message",
        "data": {
            "content": video_base64,
            "duration": 10,
            "thumbnail": "data:image/jpeg;base64,fake_thumbnail"
        }
    }
    
    try:
        async with websockets.connect("ws://localhost:8000/ws/test_user2") as websocket:
            await websocket.send(json.dumps(video_message))
            print("✅ Video message sent successfully")
            
            # Wait for confirmation
            response = await websocket.recv()
            print(f"📨 Response: {response}")
            
    except Exception as e:
        print(f"❌ Video message test failed: {e}")

async def main():
    """Main test function"""
    print("🎤 Testing Simple Messenger Voice & Video Messages")
    print("=" * 50)
    
    await test_voice_message()
    print()
    await test_video_message()
    
    print("\n✨ Testing completed!")

if __name__ == "__main__":
    # Check if server is running
    import requests
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running, starting tests...")
            asyncio.run(main())
        else:
            print("❌ Server returned non-200 status")
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first with: python main.py")
