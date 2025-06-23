from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie, Query, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import List, Dict
import json
import base64
from datetime import datetime
import mimetypes
import os
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# CORS configuration - can be customized via environment variable
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

# Enable CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Can be configured via CORS_ORIGINS env var
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Store messages in memory (for production, consider using Redis or database)
messages = []
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "100"))  # Keep last N messages
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", str(5 * 1024 * 1024)))  # Default 5MB for files
MAX_VOICE_SIZE = int(os.environ.get("MAX_VOICE_SIZE", str(10 * 1024 * 1024)))  # 10MB for voice messages
MAX_VIDEO_SIZE = int(os.environ.get("MAX_VIDEO_SIZE", str(20 * 1024 * 1024)))  # 20MB for video messages

# Access control
ACCESS_KEY = os.environ.get("ACCESS_KEY", "45000")  # Can be overridden via environment variable

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # username -> websocket
        self.user_sessions: Dict[WebSocket, str] = {}  # websocket -> username
        self.user_languages: Dict[str, str] = {}  # username -> language

    async def connect(self, websocket: WebSocket, username: str, lang: str = "en"):
        await websocket.accept()
        self.active_connections[username] = websocket
        self.user_sessions[websocket] = username
        self.user_languages[username] = lang
        await self.broadcast_system_message(f"{username} joined the chat")

    def disconnect(self, websocket: WebSocket):
        username = self.user_sessions.get(websocket)
        if username:
            self.active_connections.pop(username, None)
            self.user_sessions.pop(websocket, None)
            self.user_languages.pop(username, None)
        return username

    async def broadcast_system_message(self, content: str):
        msg_data = {
            "type": "system",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        messages.append(msg_data)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        await self._broadcast_to_all(msg_data)

    async def broadcast_message(self, username: str, content: str):
        msg_data = {
            "type": "message",
            "username": username,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        messages.append(msg_data)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        await self._broadcast_to_all(msg_data)

    async def broadcast_file(self, username: str, file_data: dict) -> bool:
        try:
            file_size = len(base64.b64decode(file_data["content"].split(",")[1]))
            if file_size > MAX_FILE_SIZE:
                return False
                
            msg_data = {
                "type": "file",
                "username": username,
                "content": file_data["content"],
                "filename": file_data["filename"],
                "mimetype": file_data["type"],
                "timestamp": datetime.now().isoformat()            }
            await self._broadcast_to_all(msg_data)
            return True
        except Exception as e:
            print(f"Error broadcasting file: {e}")
            return False

    async def broadcast_voice_message(self, username: str, audio_data: dict) -> bool:
        try:
            # Extract base64 data and add padding if needed
            content = audio_data["content"]
            if "," in content:
                base64_data = content.split(",")[1]
            else:
                base64_data = content
            
            # Add padding if necessary for base64 decoding
            missing_padding = len(base64_data) % 4
            if missing_padding:
                base64_data += '=' * (4 - missing_padding)
            
            file_size = len(base64.b64decode(base64_data))
            if file_size > MAX_VOICE_SIZE:
                return False
                
            msg_data = {
                "type": "voice_message",
                "username": username,
                "content": audio_data["content"],
                "duration": audio_data.get("duration", 0),
                "timestamp": datetime.now().isoformat()
            }
            messages.append(msg_data)
            if len(messages) > MAX_MESSAGES:
                messages.pop(0)
            await self._broadcast_to_all(msg_data)
            return True
        except Exception as e:
            print(f"Error broadcasting voice message: {e}")
            return False

    async def broadcast_video_message(self, username: str, video_data: dict) -> str:
        """
        Returns: 'success', 'too_large', 'invalid_data', or 'error'
        """
        try:
            # Extract base64 data and add padding if needed
            content = video_data["content"]
            if "," in content:
                # Remove data URL prefix (e.g., "data:video/webm;base64,")
                base64_data = content.split(",")[1]
            else:
                base64_data = content
              # Clean the base64 string - remove any whitespace or invalid characters
            import re
            # Keep only valid base64 characters: A-Z, a-z, 0-9, +, /, =
            base64_data = re.sub(r'[^A-Za-z0-9+/=]', '', base64_data)
            
            # Add padding if necessary for base64 decoding
            missing_padding = len(base64_data) % 4
            if missing_padding:
                base64_data += '=' * (4 - missing_padding)
            
            # Validate base64 and get file size
            try:
                decoded_data = base64.b64decode(base64_data, validate=True)
                file_size = len(decoded_data)
            except Exception as decode_error:
                print(f"Base64 decode error in video message: {decode_error}")
                return 'invalid_data'
            
            if file_size > MAX_VIDEO_SIZE:
                print(f"Video message too large: {file_size} bytes (max {MAX_VIDEO_SIZE})")
                return 'too_large'
                
            msg_data = {
                "type": "video_message",
                "username": username,
                "content": video_data["content"],
                "duration": video_data.get("duration", 0),
                "thumbnail": video_data.get("thumbnail", ""),
                "timestamp": datetime.now().isoformat()
            }
            messages.append(msg_data)
            if len(messages) > MAX_MESSAGES:
                messages.pop(0)
            await self._broadcast_to_all(msg_data)
            return 'success'
        except Exception as e:
            print(f"Error broadcasting video message: {e}")
            return 'error'

    async def broadcast_typing_notification(self, username: str, is_typing: bool):
        msg_data = {
            "type": "typing",
            "username": username,
            "isTyping": is_typing
        }
        await self._broadcast_to_all(msg_data)

    async def broadcast_signal(self, username: str, signal_data: dict):
        msg_data = {
            "type": "signal",
            "username": username,
            "data": signal_data
        }
        await self._broadcast_to_all(msg_data)

    async def _broadcast_to_all(self, msg_data: dict):
        if not self.active_connections:
            return
            
        msg_str = json.dumps(msg_data)
        disconnected_users = []
        
        for username, connection in list(self.active_connections.items()):
            try:
                await connection.send_text(msg_str)
            except Exception as e:
                print(f"Error sending message to {username}: {e}")
                disconnected_users.append(username)
        
        # Clean up disconnected connections
        for user in disconnected_users:
            self.active_connections.pop(user, None)
            self.user_languages.pop(user, None)

    async def send_message_history(self, websocket: WebSocket):
        """Send recent message history to newly connected user"""
        try:
            for msg in messages[-20:]:  # Send last 20 messages
                await websocket.send_text(json.dumps(msg))
        except Exception as e:
            print(f"Error sending message history: {e}")

    async def disconnect_user(self, username: str):
        """Disconnect a specific user"""
        if username in self.active_connections:
            try:
                websocket = self.active_connections[username]
                await websocket.close()
                self.disconnect(websocket)
            except Exception as e:
                print(f"Error disconnecting user {username}: {e}")

manager = ConnectionManager()

@app.get("/")
async def get_login(request: Request, lang: str = Query("en"), error: str = Query(None)):
    # Ensure lang is valid
    if lang not in ["en", "fa"]:
        lang = "en"
      # i18n data
    i18n_data = {
        "en": {
            "login": {
                "title": "Simple Messenger",
                "access_key_placeholder": "Enter access key",
                "username_placeholder": "Enter your username", 
                "join_button": "Join Chat",
                "validation": {
                    "required": "Username is required",
                    "access_key_required": "Access key is required",
                    "invalid_access_key": "Invalid access key",
                    "min_length": "Username must be at least 3 characters",
                    "max_length": "Username must be less than 15 characters",
                    "invalid_chars": "Username can only contain letters and numbers"
                }
            },
            "pwa": {
                "install": "Install App"
            }
        },
        "fa": {
            "login": {
                "title": "پیام‌رسان ساده",
                "access_key_placeholder": "کد دسترسی را وارد کنید",
                "username_placeholder": "نام کاربری خود را وارد کنید",
                "join_button": "ورود به چت",
                "validation": {
                    "required": "نام کاربری الزامی است",
                    "access_key_required": "کد دسترسی الزامی است",
                    "invalid_access_key": "کد دسترسی نامعتبر است",
                    "min_length": "نام کاربری باید حداقل ۳ کاراکتر باشد",
                    "max_length": "نام کاربری باید کمتر از ۱۵ کاراکتر باشد",
                    "invalid_chars": "نام کاربری فقط می‌تواند شامل حروف و اعداد باشد"
                }
            },
            "pwa": {
                "install": "نصب اپلیکیشن"
            }
        }
    }
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "i18n": i18n_data[lang],
        "lang": lang,
        "error": error
    })

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/chat")
async def get_chat(request: Request, username: str = Query(...), access_key: str = Query(...), lang: str = Query("en")):
    # Validate access key first
    if access_key != ACCESS_KEY:
        # Redirect back to login with error
        error_msg = "invalid_access_key" if lang == "en" else "invalid_access_key"
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": error_msg,
            "lang": lang,
            "i18n": {
                "en": {
                    "login": {
                        "title": "Simple Messenger",
                        "access_key_placeholder": "Enter access key",
                        "username_placeholder": "Enter your username", 
                        "join_button": "Join Chat",
                        "validation": {
                            "required": "Username is required",
                            "access_key_required": "Access key is required",
                            "invalid_access_key": "Invalid access key",
                            "min_length": "Username must be at least 3 characters",
                            "max_length": "Username must be less than 15 characters",
                            "invalid_chars": "Username can only contain letters and numbers"
                        }
                    },
                    "pwa": {
                        "install": "Install App"
                    }
                },
                "fa": {
                    "login": {
                        "title": "پیام‌رسان ساده",
                        "access_key_placeholder": "کد دسترسی را وارد کنید",
                        "username_placeholder": "نام کاربری خود را وارد کنید",
                        "join_button": "ورود به چت",
                        "validation": {
                            "required": "نام کاربری الزامی است",
                            "access_key_required": "کد دسترسی الزامی است",
                            "invalid_access_key": "کد دسترسی نامعتبر است",
                            "min_length": "نام کاربری باید حداقل ۳ کاراکتر باشد",
                            "max_length": "نام کاربری باید کمتر از ۱۵ کاراکتر باشد",
                            "invalid_chars": "نام کاربری فقط می‌تواند شامل حروف و اعداد باشد"
                        }
                    },
                    "pwa": {
                        "install": "نصب اپلیکیشن"
                    }
                }
            }[lang]
        })
    
    if lang not in ["en", "fa"]:
        lang = "en"# i18n data for chat
    i18n_data = {
        "en": {
            "chat": {
                "title": "Simple Messenger",
                "message_placeholder": "Type your message...",                "send_button": "Send",
                "file_button": "Choose File",
                "call_button": "Start Video Call",                "attach_button": "Attach File",
                "voice_button": "Record Voice Message",
                "video_message_button": "Record Video Message",
                "video_call_button": "Start Video Call",
                "end_call_button": "End Call",
                "typing": "is typing...",
                "file_too_large": "File too large (max 5MB)",                "files": {
                    "no_file_chosen": "No file chosen",
                    "upload_success": "File uploaded successfully",
                    "upload_error": "Error uploading file",
                    "send_error": "Error sending file",
                    "read_error": "Error reading file",
                    "download": "Download",
                    "too_large": "File too large (max 5MB)",
                    "file_selected": "File selected"
                },
                "voice": {
                    "recording": "Recording voice message...",
                    "stop_recording": "Stop Recording",
                    "start_recording": "Start Recording",
                    "play": "Play",
                    "pause": "Pause",
                    "permission_error": "Microphone permission is required for voice messages",
                    "record_error": "Error recording voice message",
                    "too_large": "Voice message too large (max 10MB)"
                },
                "video_message": {
                    "recording": "Recording video message...",
                    "stop_recording": "Stop Recording",
                    "start_recording": "Start Recording",
                    "play": "Play",
                    "pause": "Pause",
                    "permission_error": "Camera and microphone permissions are required for video messages",
                    "record_error": "Error recording video message",
                    "too_large": "Video message too large (max 20MB)"
                },
                "video": {
                    "you": "You",
                    "remote": "Remote",
                    "remote_user": "Remote User",
                    "starting_call": "Starting video call...",
                    "call_ended": "Call ended",
                    "connecting": "Connecting...",
                    "failed": "Call failed"
                },
                "call": {
                    "permission_error": "Camera and microphone permissions are required for video calls",
                    "start_error": "Failed to start video call",
                    "connection_error": "Connection failed"
                },                "status": {
                    "connecting": "Connecting...",
                    "connected": "Connected",
                    "disconnected": "Disconnected",
                    "reconnecting": "Reconnecting...",
                    "reconnecting_attempt": "Reconnecting...",
                    "connection_error": "Connection Error",
                    "error": "Error"
                },"typing": {
                    "single": "{username} is typing...",
                    "multiple": "{usernames} are typing..."
                },
                "notifications": {
                    "permission_request": "Enable notifications to get alerts when you receive messages",
                    "permission_denied": "Notifications are disabled. You can enable them in your browser settings.",
                    "new_message": "New message from {username}",
                    "new_voice_message": "New voice message from {username}",
                    "new_video_message": "New video message from {username}",
                    "new_file": "New file from {username}",
                    "user_joined": "{username} joined the chat",
                    "user_left": "{username} left the chat",
                    "enable_button": "Enable Notifications",
                    "enabled": "Notifications enabled",
                    "not_supported": "Notifications are not supported in this browser"
                }
            },
            "theme": {
                "toggle": "Toggle theme"
            },
            "pwa": {
                "install": "Install App"
            }
        },
        "fa": {
            "chat": {
                "title": "پیام‌رسان ساده",
                "message_placeholder": "پیام خود را تایپ کنید...",                "send_button": "ارسال",
                "file_button": "انتخاب فایل",
                "call_button": "شروع تماس ویدیویی",                "attach_button": "پیوست فایل",
                "voice_button": "ضبط پیام صوتی",
                "video_message_button": "ضبط پیام ویدیویی",
                "video_call_button": "شروع تماس ویدیویی",
                "end_call_button": "پایان تماس",
                "typing": "در حال تایپ...",
                "file_too_large": "فایل خیلی بزرگ است (حداکثر ۵ مگابایت)",                "files": {
                    "no_file_chosen": "فایلی انتخاب نشده",
                    "upload_success": "فایل با موفقیت آپلود شد",
                    "upload_error": "خطا در آپلود فایل",
                    "send_error": "خطا در ارسال فایل",
                    "read_error": "خطا در خواندن فایل",
                    "download": "دانلود",
                    "too_large": "فایل خیلی بزرگ است (حداکثر ۵ مگابایت)",                    "file_selected": "فایل انتخاب شده"
                },
                "voice": {
                    "recording": "در حال ضبط پیام صوتی...",
                    "stop_recording": "توقف ضبط",
                    "start_recording": "شروع ضبط",
                    "play": "پخش",
                    "pause": "مکث",
                    "permission_error": "برای پیام صوتی نیاز به دسترسی میکروفون است",
                    "record_error": "خطا در ضبط پیام صوتی",
                    "too_large": "پیام صوتی خیلی بزرگ است (حداکثر ۱۰ مگابایت)"
                },
                "video_message": {
                    "recording": "در حال ضبط پیام ویدیویی...",
                    "stop_recording": "توقف ضبط",
                    "start_recording": "شروع ضبط",
                    "play": "پخش",
                    "pause": "مکث",
                    "permission_error": "برای پیام ویدیویی نیاز به دسترسی دوربین و میکروفون است",
                    "record_error": "خطا در ضبط پیام ویدیویی",
                    "too_large": "پیام ویدیویی خیلی بزرگ است (حداکثر ۲۰ مگابایت)"
                },
                "video": {
                    "you": "شما",
                    "remote": "طرف مقابل",
                    "remote_user": "کاربر طرف مقابل",
                    "starting_call": "در حال شروع تماس ویدیویی...",
                    "call_ended": "تماس پایان یافت",
                    "connecting": "در حال اتصال...",
                    "failed": "تماس ناموفق"
                },
                "call": {
                    "permission_error": "برای تماس ویدیویی نیاز به دسترسی دوربین و میکروفون است",
                    "start_error": "خطا در شروع تماس ویدیویی",                    "connection_error": "خطا در اتصال"
                },                "status": {
                    "connecting": "در حال اتصال...",
                    "connected": "متصل",
                    "disconnected": "قطع شده",
                    "reconnecting": "در حال اتصال مجدد...",
                    "reconnecting_attempt": "در حال اتصال مجدد...",
                    "connection_error": "خطای اتصال",
                    "error": "خطا"
                },"typing": {
                    "single": "{username} در حال تایپ است...",
                    "multiple": "{usernames} در حال تایپ هستند..."
                },
                "notifications": {
                    "permission_request": "اعلان‌ها را فعال کنید تا هنگام دریافت پیام آگاه شوید",
                    "permission_denied": "اعلان‌ها غیرفعال هستند. می‌توانید آنها را در تنظیمات مرورگر فعال کنید.",
                    "new_message": "پیام جدید از {username}",
                    "new_voice_message": "پیام صوتی جدید از {username}",
                    "new_video_message": "پیام ویدیویی جدید از {username}",
                    "new_file": "فایل جدید از {username}",
                    "user_joined": "{username} وارد چت شد",
                    "user_left": "{username} چت را ترک کرد",
                    "enable_button": "فعال‌سازی اعلان‌ها",
                    "enabled": "اعلان‌ها فعال شدند",
                    "not_supported": "اعلان‌ها در این مرورگر پشتیبانی نمی‌شوند"
                }
            },
            "theme": {
                "toggle": "تغییر تم"
            },
            "pwa": {
                "install": "نصب اپلیکیشن"
            }
        }
    }
    
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "username": username,
        "lang": lang,
        "i18n": i18n_data[lang]
    })

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, lang: str = Query("en")):
    await manager.connect(websocket, username, lang)
    
    # Send message history to the newly connected user
    await manager.send_message_history(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                msg_type = msg.get("type")
                
                if msg_type == "message":
                    content = msg.get("content", "")
                    if content.strip():
                        await manager.broadcast_message(username, content)
                        
                elif msg_type == "file":
                    file_data = msg.get("data", {})
                    success = await manager.broadcast_file(username, file_data)
                    if not success:
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "File too large (max 5MB)"
                        }))
                        
                elif msg_type == "voice_message":
                    audio_data = msg.get("data", {})
                    success = await manager.broadcast_voice_message(username, audio_data)
                    if not success:                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Voice message too large (max 10MB)"
                        }))
                        
                elif msg_type == "video_message":
                    video_data = msg.get("data", {})
                    result = await manager.broadcast_video_message(username, video_data)
                    if result != 'success':
                        if result == 'too_large':
                            error_msg = "Video message too large (max 20MB)"
                        elif result == 'invalid_data':
                            error_msg = "Invalid video data. Please try recording again."
                        else:
                            error_msg = "Error processing video message. Please try again."
                        
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": error_msg
                        }))
                        
                elif msg_type == "typing":
                    is_typing = msg.get("isTyping", False)
                    await manager.broadcast_typing_notification(username, is_typing)
                    
                elif msg_type == "signal":
                    signal_data = msg.get("data", {})
                    await manager.broadcast_signal(username, signal_data)
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error from {username}: {e}")
            except Exception as e:
                print(f"Error processing message from {username}: {e}")
                
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast_system_message(f"{username} left the chat")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=False)
