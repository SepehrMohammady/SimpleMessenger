# Simple Secure Messenger

A modern, secure web-based messenger application with real-time chat, video calls, and enhanced file sharing capabilities, built with FastAPI and WebRTC.

## ✨ Features

### 💬 **Real-time Communication**
- Real-time chat with WebSocket
- Typing indicators with user feedback
- User presence notifications
- Message history (in-memory)

### 🎥 **Video & Audio Calls**
- Video/Audio calls using WebRTC *(2-person limit)*
- Camera and microphone controls
- Mute/unmute functionality
- Full-screen call interface
- **Note**: Video calls work between 2 people only. Multiple users can chat and share files, but video calling is peer-to-peer between any 2 participants.

### 📁 **Enhanced File Sharing**
- **Image Previews**: Inline thumbnails with click-to-expand modal
- **Video Previews**: Inline video player with native controls
- **Audio Previews**: Inline audio player for music/voice files
- **PDF Support**: View PDF in browser or download
- **File Type Detection**: Smart icons for different file types
- **File Size Limits**: 5MB for regular files, 10MB for voice messages, 20MB for video messages

### 🎤 **Voice & Video Messages**
- **Voice Messages**: Record and send audio messages with one-click recording
- **Video Messages**: Record and send short video messages with thumbnails
- **Playback Controls**: Custom audio/video players with progress indicators
- **Duration Display**: Shows recording and playback duration
- **Waveform Visualization**: Visual feedback for voice message playback
- **Auto Thumbnails**: Automatic thumbnail generation for video messages

### 🌐 **User Experience**
- 🌓 Dark/Light theme with automatic detection
- 🌍 **Bilingual Support**: English and Persian (Farsi) with proper RTL layout
- 📱 **Responsive Design**: Works on mobile and desktop
- 🎨 **Modern UI**: Clean interface with smooth animations
- ⚡ **Progressive Web App**: Installable with offline capabilities

### 🔧 **Technical Features**
- Clean, optimized codebase
- Docker support for easy deployment
- Environment variable configuration
- Proper error handling and user feedback
- WebSocket auto-reconnection
- Cross-platform compatibility
- Production-ready CORS and security headers

## 🚀 **Quick Deploy**

> 🎯 **Tested & Working**: Only platforms that work reliably with full functionality

### **🆓 FREE Options:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SepehrMohammady/SimpleMessenger)
*⭐ **BEST FREE OPTION** - Full functionality with WebSockets*

**Fly.io**: CLI deployment (see [DEPLOYMENT.md](DEPLOYMENT.md) for instructions)
*Global edge deployment with excellent performance*

### **Other Deployment Options:**
- **Docker**: Available for VPS/server deployment
- **VPS**: Complete configuration included
- **Local**: Works out of the box with Python 3.8+

### **📊 Platform Comparison:**

| Platform | Cost | WebSockets | Real-time Chat | Recommended |
|----------|------|-----------|----------------|-------------|
| **Render** | Free (750hrs/month) | ✅ Full | ✅ Yes | ⭐ **BEST FREE** |
| **Fly.io** | Generous free tier | ✅ Full | ✅ Yes | ⭐ **EXCELLENT** |

> 📖 **Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🚀 How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Open your browser:**
   - Go to `http://localhost:8000`
   - Enter a username and start chatting!

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Jinja2

## 🎯 Recent Improvements

- ✅ **Enhanced file preview system** with inline media display
- ✅ **Removed "No file chosen" text** for cleaner UI
- ✅ **Added missing i18n translations** for error handling
- ✅ **Improved file type support** (images, videos, audio, PDF)
- ✅ **Cleaned up legacy code** and unused dependencies
- ✅ **Better error handling** for file operations
- ✅ **Fixed GitHub Actions** - removed failing deployment workflows
- ✅ **Voice & Video Messages** - Record and send audio/video messages with playback controls

## 🔮 Future Enhancements

- 🔐 User authentication and authorization
- 💾 Persistent message history with database
- 🔒 End-to-end encryption
- 👥 Multi-room chat support
- � **Group video calls** (3+ participants)
- �📤 Advanced file sharing (larger files, cloud storage)
- 🎬 Screen sharing capabilities
- 📞 Call management (reject, busy status, call queue)

## ⚠️ **Important Limitations**

### **Video Call Capacity**
- **Maximum 2 people** can video call simultaneously
- **Unlimited text chat** - any number of users can join for messaging
- **File sharing works** for all users
- When 3+ people are online:
  - ✅ Everyone can chat and share files
  - ⚠️ Only 2 people can video call at a time
  - 💡 Third person and beyond can see the chat but not join video calls

### **Multi-User Scenarios**
- **2 users**: Full functionality (chat + video calls)
- **3+ users**: Chat and file sharing only, video calls limited to 2 participants
- **Recommendation**: For group video calls, consider using dedicated platforms like Zoom, Google Meet, or Microsoft Teams

---

**Note**: This project is designed for personal and family use. For production deployment, implement proper security measures, user authentication, and data persistence.
