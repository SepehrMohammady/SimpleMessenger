# Simple Secure Messenger

A modern, secure web-based messenger application with chat and video call capabilities, built with FastAPI and WebRTC.

## Features
- 💬 Real-time chat with WebSocket
- 🎥 Video/Audio calls using WebRTC
- 📁 File sharing with previews (images, PDFs, etc.)
- 🌓 Dark/Light theme with system preference detection
- ⌨️ Typing indicators
- 📜 Message history
- 📱 Responsive design for mobile and desktop
- 👥 User presence notifications

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Start the server:
   ```
   uvicorn main:app --reload
   ```
3. Open your browser and go to `http://localhost:8000`.

## Next Steps
- Add user authentication
- Add message history
- Add WebRTC signaling for calls

---
This project is for personal and family use. For production, add security and privacy features.
