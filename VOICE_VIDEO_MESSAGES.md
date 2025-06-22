# Voice & Video Messages - Feature Documentation

## 🎤 Voice Messages

### Features
- **One-Click Recording**: Press and hold to record voice messages
- **Real-time Visual Feedback**: Recording indicator with pulsing animation
- **Timer Display**: Shows recording duration in real-time
- **Automatic Send**: Voice message is sent when recording stops
- **Custom Audio Player**: Waveform visualization with play/pause controls
- **Duration Display**: Shows message length
- **File Size Limit**: Maximum 5MB per voice message

### How to Use Voice Messages

1. **Starting Recording**:
   - Click the microphone icon (🎤) in the chat input area
   - Grant microphone permission when prompted
   - Recording starts immediately with visual feedback

2. **During Recording**:
   - Red pulsing animation indicates active recording
   - Timer shows current recording duration
   - Click the same button again to stop recording

3. **Playback**:
   - Voice messages appear as compact audio players
   - Click play button to start/pause playback
   - Waveform shows progress visually

### Technical Details
- **Format**: WebM with Opus codec (fallback to WAV)
- **Quality**: Optimized for voice (not music)
- **Browser Support**: Modern browsers with MediaRecorder API
- **Permissions**: Requires microphone access

---

## 📹 Video Messages

### Features
- **Quick Video Recording**: Record short video messages with audio
- **Automatic Thumbnails**: Generates preview thumbnails automatically
- **Duration Tracking**: Shows recording and playback duration
- **Inline Video Player**: Videos play directly in chat
- **Camera Permission**: Requests camera and microphone access
- **File Size Limit**: Maximum 5MB per video message

### How to Use Video Messages

1. **Starting Recording**:
   - Click the video message icon (📹) in the chat input area
   - Grant camera and microphone permissions when prompted
   - Recording starts with visual indicator

2. **During Recording**:
   - Red pulsing animation shows active recording
   - Timer displays current recording duration
   - Click the same button to stop recording

3. **Playback**:
   - Video messages show thumbnail preview
   - Click to play inline with standard video controls
   - Shows message duration

### Technical Details
- **Format**: WebM with VP8 video and Opus audio codecs
- **Resolution**: 640x480 optimized for messaging
- **Thumbnail**: JPEG, 320px wide, generated at 0.5 seconds
- **Browser Support**: Modern browsers with MediaRecorder API
- **Permissions**: Requires camera and microphone access

---

## 🌐 Internationalization Support

### English
- "Record Voice Message" / "Record Video Message"
- "Recording voice/video message..."
- "Stop Recording"
- Error messages for permissions and file size

### Persian (Farsi)
- "ضبط پیام صوتی" / "ضبط پیام ویدیویی"
- "در حال ضبط پیام صوتی/ویدیویی..."
- "توقف ضبط"
- Complete error message translations

---

## 🔧 Technical Implementation

### Backend (Python/FastAPI)
- New message types: `voice_message` and `video_message`
- Base64 encoding for audio/video data transmission
- File size validation (5MB limit)
- WebSocket message broadcasting
- Duration and metadata storage

### Frontend (JavaScript)
- MediaRecorder API for audio/video capture
- Canvas API for video thumbnail generation
- Custom UI components for recording states
- Progress tracking and playback controls
- Responsive design for mobile and desktop

### Browser Compatibility
- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support (iOS 14.3+)
- **Mobile**: Responsive design works on mobile browsers

---

## 🚀 Getting Started

1. **Grant Permissions**: Allow microphone (voice) or camera+microphone (video) access
2. **Start Recording**: Click the respective icon in the chat input
3. **Record Message**: Speak or record your video message
4. **Stop & Send**: Click stop to automatically send the message
5. **Playback**: Recipients can play messages with built-in controls

---

## 📝 Notes

- Messages are sent automatically when recording stops
- No manual "send" button needed for recorded messages
- All recordings respect the 5MB file size limit
- Recorded messages integrate seamlessly with text and file messages
- Works alongside existing video calling feature (video calls are separate)

---

## 🔒 Privacy & Security

- **No Server Storage**: Messages are transmitted and stored in memory only
- **Peer-to-Peer**: Audio/video data is sent through WebSocket directly
- **Permission-Based**: Only works with explicit user permission
- **Local Processing**: Thumbnail generation happens in browser
- **No External Services**: Everything runs on your own server
