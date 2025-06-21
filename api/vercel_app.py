import sys
import os

# Add the parent directory to sys.path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from typing import List, Dict
import json
import base64
from datetime import datetime
import mimetypes

# Create a new FastAPI app specifically for Vercel
app = FastAPI()

# CORS configuration
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Store messages in memory (for production, consider using Redis or database)
messages = []
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "100"))
MAX_FILE_SIZE = int(os.environ.get("MAX_FILE_SIZE", str(5 * 1024 * 1024)))

# Template directory - need to adjust path for Vercel
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")

templates = Jinja2Templates(directory=template_dir)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
except:
    pass  # Static files might not be available in serverless environment

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Messenger - Vercel</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
                .container { text-align: center; }
                input, button { padding: 10px; margin: 10px; font-size: 16px; }
                button { background-color: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background-color: #005a8b; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Simple Messenger</h1>
                <p><strong>Note:</strong> This is running on Vercel's serverless platform.</p>
                <p>WebSocket real-time chat is not available on Vercel due to serverless limitations.</p>
                <p>For full functionality including real-time WebSocket chat, please deploy on:</p>
                <ul style="text-align: left;">
                    <li><a href="https://railway.app/template/https://github.com/SepehrMohammady/SimpleMessenger" target="_blank">Railway (Recommended)</a></li>
                    <li><a href="https://render.com/deploy?repo=https://github.com/SepehrMohammady/SimpleMessenger" target="_blank">Render</a></li>
                    <li>VPS or dedicated server</li>
                </ul>
                
                <form action="/chat" method="post">
                    <input type="text" name="username" placeholder="Enter your username" required>
                    <br>
                    <select name="lang">
                        <option value="en">English</option>
                        <option value="fa">فارسی</option>
                    </select>
                    <br>
                    <button type="submit">Join Chat (Polling Mode)</button>
                </form>
            </div>
        </body>
        </html>
        """)

@app.post("/chat", response_class=HTMLResponse)
async def chat_page(request: Request, username: str = Form(...), lang: str = Form("en")):
    try:
        return templates.TemplateResponse("chat.html", {
            "request": request, 
            "username": username, 
            "lang": lang,
            "is_vercel": True  # Flag to enable polling mode in frontend
        })
    except:
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simple Messenger - Chat</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }}
                .messages {{ height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; margin: 20px 0; }}
                .message {{ margin: 10px 0; padding: 5px; }}
                .system {{ color: #666; font-style: italic; }}
                input[type="text"] {{ width: 70%; padding: 10px; }}
                button {{ padding: 10px; background-color: #007cba; color: white; border: none; border-radius: 5px; cursor: pointer; }}
                .warning {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>Simple Messenger - {username}</h1>
            <div class="warning">
                <strong>⚠️ Limited Functionality:</strong> You're using the Vercel version which has limited real-time capabilities.
                For full WebSocket chat, deploy on Railway or Render using the links in the README.
            </div>
            <div id="messages" class="messages"></div>
            <input type="text" id="messageInput" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
            
            <script>
                const username = "{username}";
                let lastMessageId = 0;
                
                function loadMessages() {{
                    fetch('/api/messages?since=' + lastMessageId)
                        .then(response => response.json())
                        .then(data => {{
                            const messagesDiv = document.getElementById('messages');
                            data.messages.forEach(msg => {{
                                const messageDiv = document.createElement('div');
                                messageDiv.className = 'message ' + (msg.type || '');
                                if (msg.type === 'system') {{
                                    messageDiv.innerHTML = `<span class="system">${{msg.content}}</span>`;
                                }} else {{
                                    messageDiv.innerHTML = `<strong>${{msg.username}}:</strong> ${{msg.content}}`;
                                }}
                                messagesDiv.appendChild(messageDiv);
                            }});
                            if (data.messages.length > 0) {{
                                lastMessageId = data.lastId;
                                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                            }}
                        }});
                }}
                
                function sendMessage() {{
                    const input = document.getElementById('messageInput');
                    const message = input.value.trim();
                    if (message) {{
                        fetch('/api/send', {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{username: username, message: message}})
                        }});
                        input.value = '';
                    }}
                }}
                
                document.getElementById('messageInput').addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        sendMessage();
                    }}
                }});
                
                // Poll for new messages every 2 seconds
                setInterval(loadMessages, 2000);
                loadMessages(); // Initial load
            </script>
        </body>
        </html>
        """)

@app.get("/api/messages")
async def get_messages(since: int = 0):
    """Get messages since a specific ID (for polling)"""
    new_messages = messages[since:]
    return {
        "messages": new_messages,
        "lastId": len(messages)
    }

@app.post("/api/send")
async def send_message(request: Request):
    """Send a message via REST API (for polling mode)"""
    try:
        data = await request.json()
        username = data.get("username", "Anonymous")
        message = data.get("message", "")
        
        if message.strip():
            msg_data = {
                "type": "message",
                "username": username,
                "content": message,
                "timestamp": datetime.now().isoformat()
            }
            messages.append(msg_data)
            if len(messages) > MAX_MESSAGES:
                messages.pop(0)
            
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "platform": "vercel", "mode": "polling"}

# Static file fallbacks for Vercel
@app.get("/favicon.ico")
async def favicon():
    try:
        return FileResponse(os.path.join(static_dir, "favicon.ico"))
    except:
        return JSONResponse({"error": "File not found"}, status_code=404)

@app.get("/manifest.json")
async def manifest():
    try:
        return FileResponse(os.path.join(static_dir, "manifest.json"))
    except:
        return JSONResponse({
            "name": "Simple Messenger",
            "short_name": "Messenger",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#007cba"
        })
