from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Cookie, Query
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List, Dict
import json
import base64
from datetime import datetime
import mimetypes

app = FastAPI()

# Store messages in memory
messages = []
MAX_MESSAGES = 100  # Keep last 100 messages
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Messenger</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            /* Light theme */
            --bg-primary: #ffffff;
            --bg-secondary: #f8f9fa;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --accent-color: #0d6efd;
            --border-color: #dee2e6;
            --chat-bubble-bg: #e9ecef;
            --chat-bubble-own: #cfe2ff;
            --hover-bg: #e9ecef;
            --error-color: #dc3545;
            --success-color: #198754;
        }

        [data-theme="dark"] {
            /* Dark theme */
            --bg-primary: #212529;
            --bg-secondary: #343a40;
            --text-primary: #f8f9fa;
            --text-secondary: #adb5bd;
            --accent-color: #0d6efd;
            --border-color: #495057;
            --chat-bubble-bg: #495057;
            --chat-bubble-own: #084298;
            --hover-bg: #495057;
            --error-color: #dc3545;
            --success-color: #198754;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
            transition: background-color 0.3s ease;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header {
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--bg-secondary);
        }

        .header h1 {
            font-size: 1.5rem;
            margin: 0;
        }

        .theme-toggle {
            background: none;
            border: none;
            color: var(--text-primary);
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .theme-toggle:hover {
            background-color: var(--hover-bg);
        }

        .status { 
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
        }

        .status[data-state="connected"] { color: var(--success-color); }
        .status[data-state="disconnected"] { color: var(--error-color); }

        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 1rem;
            gap: 1rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .chat-container { 
            flex: 1;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            background: var(--bg-secondary);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .message-group {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            max-width: 80%;
        }

        .message-group.own {
            align-self: flex-end;
        }

        .message {
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            background: var(--chat-bubble-bg);
            position: relative;
        }

        .message-group.own .message {
            background: var(--chat-bubble-own);
            color: var(--bg-primary);
        }

        .message .username {
            font-weight: 600;
            font-size: 0.875rem;
            margin-bottom: 0.25rem;
            color: var(--accent-color);
        }

        .message .time {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-left: 0.5rem;
        }

        .message.system {
            background: transparent;
            color: var(--text-secondary);
            font-style: italic;
            text-align: center;
            padding: 0.5rem;
            font-size: 0.875rem;
        }

        .input-container {
            padding: 1rem;
            background: var(--bg-primary);
            border-top: 1px solid var(--border-color);
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .input-container input[type="text"] {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 1.5rem;
            background: var(--bg-secondary);
            color: var(--text-primary);
            font-size: 1rem;
            transition: border-color 0.2s ease;
        }

        .input-container input[type="text"]:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        .file-upload {
            position: relative;
            overflow: hidden;
        }

        .file-upload input[type="file"] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
            width: 100%;
            height: 100%;
        }

        .btn {
            padding: 0.75rem 1rem;
            border: none;
            border-radius: 1.5rem;
            background: var(--accent-color);
            color: white;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: background-color 0.2s ease, transform 0.1s ease;
        }

        .btn:hover {
            background-color: #0b5ed7;
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn.btn-icon {
            padding: 0.75rem;
            border-radius: 50%;
        }

        .btn svg {
            width: 1.25rem;
            height: 1.25rem;
        }

        .file-preview {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .file-preview img {
            max-width: 100px;
            max-height: 100px;
            border-radius: 0.25rem;
        }

        .file-preview .file-info {
            flex: 1;
        }

        .file-preview .remove-file {
            color: var(--error-color);
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.5rem;
        }

        .typing-indicator {
            padding: 0.5rem 1rem;
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-style: italic;
        }

        .video-container {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            padding: 2rem;
        }

        .video-container.active {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }

        .videos {
            display: flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }

        .video-wrapper {
            position: relative;
            width: 320px;
            background: #000;
            border-radius: 0.5rem;
            overflow: hidden;
        }

        .video-wrapper video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .video-wrapper .label {
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            color: white;
            font-size: 0.875rem;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
        }

        .call-controls {
            display: flex;
            gap: 1rem;
        }

        .call-controls button {
            padding: 1rem;
            border-radius: 50%;
            border: none;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }

        .call-controls button:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        .call-controls button.end-call {
            background: var(--error-color);
        }

        .call-controls button.end-call:hover {
            background: #bb2d3b;
        }

        @media (max-width: 640px) {
            .main-container {
                padding: 0.5rem;
            }

            .message-group {
                max-width: 90%;
            }

            .videos {
                flex-direction: column;
            }

            .video-wrapper {
                width: 100%;
            }
        }

        .loading {
            display: inline-block;
            width: 1rem;
            height: 1rem;
            border: 2px solid currentColor;
            border-right-color: transparent;
            border-radius: 50%;
            animation: spin 0.75s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .fade-enter {
            opacity: 0;
            transform: translateY(10px);
        }

        .fade-enter-active {
            opacity: 1;
            transform: translateY(0);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }

        [data-typing="true"] .message-input {
            background-color: var(--hover-bg);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="status" id="status" data-state="connecting">
            <div class="loading"></div>
            Connecting...
        </div>
        <button class="theme-toggle" id="themeToggle" title="Toggle theme">
            <svg viewBox="0 0 24 24" width="24" height="24" class="theme-icon">
                <path fill="currentColor" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.03 0-5.5-2.47-5.5-5.5 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/>
            </svg>
        </button>
    </div>

    <div class="main-container">
        <div class="chat-container">
            <div class="messages" id="chat"></div>
            <div class="typing-indicator" id="typingIndicator"></div>
            <div class="input-container">
                <div class="file-upload">
                    <button type="button" class="btn btn-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M12 5v13M5 12l7-7 7 7" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </button>
                    <input type="file" id="fileInput" onchange="handleFileSelect(event)"/>
                </div>
                <input type="text" id="messageInput" class="message-input" placeholder="Type your message..." autocomplete="off"/>
                <button class="btn" onclick="sendMessage()">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <button class="btn btn-icon" onclick="startCall()" title="Start video call">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M23 7l-7 5 7 5V7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <rect x="1" y="5" width="15" height="14" rx="2" ry="2" stroke-width="2"/>
                    </svg>
                </button>
            </div>
        </div>
        <div id="fileInfo"></div>
    </div>

    <div class="video-container" id="videoContainer">
        <div class="videos">
            <div class="video-wrapper">
                <video id="localVideo" autoplay muted playsinline></video>
                <div class="label">You</div>
            </div>
            <div class="video-wrapper">
                <video id="remoteVideo" autoplay playsinline></video>
                <div class="label">Remote</div>
            </div>
        </div>
        <div class="call-controls">
            <button onclick="toggleMute()" id="muteBtn">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" stroke-width="2"/>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8" stroke-width="2"/>
                </svg>
            </button>
            <button onclick="toggleVideo()" id="videoBtn">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
                    <rect x="2" y="7" width="20" height="10" rx="2" ry="2" stroke-width="2"/>
                    <circle cx="12" cy="12" r="3" stroke-width="2"/>
                </svg>
            </button>
            <button class="end-call" onclick="endCall()">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor">
                    <path d="M22 2L2 22M2 2l20 20" stroke-width="2"/>
                </svg>
            </button>
        </div>
    </div>

    <script type="text/javascript">
        "use strict";
        
        // Global variables
        let ws = null;
        let pc = null;
        let localStream = null;
        let reconnectAttempts = 0;
        let selectedFile = null;
        let isTyping = false;
        let typingTimeout = null;
        let lastTypingNotification = 0;
        let userTyping = new Set();
        const MAX_RECONNECT_ATTEMPTS = 5;
        const TYPING_DEBOUNCE = 1000;
        const TYPING_NOTIFICATION_INTERVAL = 3000;
        const DEFAULT_THEME = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';

        // Initialize everything when the page loads
        (function init() {
            try {
                const username = new URLSearchParams(window.location.search).get('username');
                if (!username) {
                    window.location.href = '/';
                    return;
                }
                initializeWebSocket(username);
                initializeTheme();
                setupEventListeners();
            } catch (error) {
                console.error('Initialization error:', error);
                updateStatus('error', 'Error initializing - Please refresh');
            }
        })();

        function initializeTheme() {
            const theme = localStorage.getItem('theme') || DEFAULT_THEME;
            document.documentElement.setAttribute('data-theme', theme);
            updateThemeIcon(theme);
        }

        function toggleTheme() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        }

        function updateThemeIcon(theme) {
            const icon = document.querySelector('.theme-icon');
            icon.innerHTML = theme === 'dark' 
                ? '<path fill="currentColor" d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-3.03 0-5.5-2.47-5.5-5.5 0-1.82.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1z"/>'
                : '<path fill="currentColor" d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37a.996.996 0 0 0-1.41 0 .996.996 0 0 0 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0a.996.996 0 0 0 0-1.41l-1.06-1.06zm1.06-10.96a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36a.996.996 0 0 0 0-1.41.996.996 0 0 0-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>';
        }

        function updateStatus(state, message) {
            const statusElement = document.getElementById("status");
            statusElement.dataset.state = state;
            statusElement.innerHTML = state === 'connecting' 
                ? '<div class="loading"></div>' + message
                : message;
        }

        // WebSocket Functions
        function initializeWebSocket(username) {
            try {
                if (ws) {
                    ws.close();
                }
                
                ws = new WebSocket(`ws://${location.host}/ws/${encodeURIComponent(username)}`);
                
                ws.onclose = function() {
                    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                        updateStatus('disconnected', `Reconnecting... (${reconnectAttempts + 1}/${MAX_RECONNECT_ATTEMPTS})`);
                        reconnectAttempts++;
                        setTimeout(() => initializeWebSocket(username), 1000);
                    } else {
                        updateStatus('error', 'Connection failed - Please refresh');
                    }
                };

                ws.onopen = function() {
                    updateStatus('connected', 'Connected');
                    console.log("WebSocket connected");
                    reconnectAttempts = 0;
                };
                
                ws.onerror = function(e) {
                    updateStatus('error', 'Connection error');
                    console.error("WebSocket error:", e);
                };

                ws.onmessage = handleWebSocketMessage;
            } catch (error) {
                console.error("WebSocket initialization error:", error);
                updateStatus('error', 'Connection error - Please refresh');
            }
        }

        function setupEventListeners() {
            document.getElementById("themeToggle").addEventListener("click", toggleTheme);
            document.getElementById("messageInput").addEventListener("keypress", handleKeyPress);
            document.getElementById("messageInput").addEventListener("input", handleTyping);
            document.getElementById("messageInput").addEventListener("blur", () => {
                notifyTypingStopped();
                isTyping = false;
            });

            // Add animation to messages
            const observer = new MutationObserver(mutations => {
                mutations.forEach(mutation => {
                    mutation.addedNodes.forEach(node => {
                        if (node.classList && node.classList.contains('message-group')) {
                            node.classList.add('fade-enter');
                            requestAnimationFrame(() => {
                                node.classList.add('fade-enter-active');
                                setTimeout(() => {
                                    node.classList.remove('fade-enter', 'fade-enter-active');
                                }, 300);
                            });
                        }
                    });
                });
            });

            observer.observe(document.getElementById('chat'), { childList: true });
        }

        // Message Handling Functions
        function handleWebSocketMessage(event) {
            try {
                const msg = JSON.parse(event.data);
                if (msg.type === "chat") {
                    handleChatMessage(msg);
                } else if (msg.type === "file") {
                    handleFileMessage(msg);
                } else if (msg.type === "signal") {
                    handleSignaling(msg.data);
                } else if (msg.type === "typing") {
                    handleTypingNotification(msg.data);
                }
            } catch (error) {
                console.error("Message parsing error:", error);
            }
        }

        function handleChatMessage(msg) {
            try {
                const chat = document.getElementById("chat");
                const data = msg.data;

                if (data.system) {
                    const systemMsg = document.createElement("div");
                    systemMsg.className = "message system";
                    systemMsg.textContent = `${data.username} ${data.message}`;
                    chat.appendChild(systemMsg);
                } else {
                    const currentUsername = new URLSearchParams(window.location.search).get('username');
                    const isOwnMessage = data.username === currentUsername;
                    
                    let messageGroup = chat.lastElementChild;
                    const needsNewGroup = !messageGroup || 
                                        !messageGroup.classList.contains('message-group') ||
                                        messageGroup.dataset.username !== data.username;

                    if (needsNewGroup) {
                        messageGroup = document.createElement("div");
                        messageGroup.className = `message-group${isOwnMessage ? ' own' : ''}`;
                        messageGroup.dataset.username = data.username;
                        chat.appendChild(messageGroup);
                    }

                    const messageDiv = document.createElement("div");
                    messageDiv.className = "message";
                    
                    if (needsNewGroup) {
                        messageDiv.innerHTML = `<div class="username">${escapeHtml(data.username)}</div>`;
                    }
                    
                    messageDiv.innerHTML += `
                        <div class="content">${escapeHtml(data.message)}</div>
                        <div class="time">${data.timestamp}</div>
                    `;
                    
                    messageGroup.appendChild(messageDiv);
                }
                
                chat.scrollTop = chat.scrollHeight;
            } catch (error) {
                console.error("Error handling chat message:", error);
            }
        }

        function handleFileMessage(msg) {
            try {
                const chat = document.getElementById("chat");
                const fileData = msg.data;
                const currentUsername = new URLSearchParams(window.location.search).get('username');
                const isOwnMessage = fileData.username === currentUsername;

                const messageGroup = document.createElement("div");
                messageGroup.className = `message-group${isOwnMessage ? ' own' : ''}`;
                messageGroup.dataset.username = fileData.username;

                const messageDiv = document.createElement("div");
                messageDiv.className = "message";

                let content = `
                    <div class="username">${escapeHtml(fileData.username)}</div>
                    ${fileData.message ? `<div class="content">${escapeHtml(fileData.message)}</div>` : ''}
                    <div class="file-content">
                `;

                if (fileData.fileType.startsWith('image/')) {
                    content += `
                        <img src="data:${fileData.fileType};base64,${fileData.data}" 
                             alt="${escapeHtml(fileData.filename)}"
                             loading="lazy"/>
                    `;
                }

                const downloadLink = document.createElement('a');
                downloadLink.className = 'file-download';
                downloadLink.href = `data:${fileData.fileType};base64,${fileData.data}`;
                downloadLink.download = fileData.filename;
                downloadLink.innerHTML = `
                    ${getFileIcon(fileData.fileType)}
                    ${escapeHtml(fileData.filename)} (${formatFileSize(fileData.size)})
                `;

                messageDiv.innerHTML = content;
                messageDiv.querySelector('.file-content').appendChild(downloadLink);
                messageGroup.appendChild(messageDiv);
                chat.appendChild(messageGroup);
                chat.scrollTop = chat.scrollHeight;
            } catch (error) {
                console.error("Error handling file message:", error);
            }
        }

        // Typing Indicator Functions
        function handleTyping() {
            if (!isTyping) {
                isTyping = true;
                notifyTypingStarted();
            }

            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(() => {
                isTyping = false;
                notifyTypingStopped();
            }, TYPING_DEBOUNCE);
        }

        function notifyTypingStarted() {
            if (!ws || ws.readyState !== WebSocket.OPEN) return;
            
            const now = Date.now();
            if (now - lastTypingNotification > TYPING_NOTIFICATION_INTERVAL) {
                ws.send(JSON.stringify({
                    type: "typing",
                    data: { isTyping: true }
                }));
                lastTypingNotification = now;
            }
        }

        function notifyTypingStopped() {
            if (!ws || ws.readyState !== WebSocket.OPEN) return;
            
            ws.send(JSON.stringify({
                type: "typing",
                data: { isTyping: false }
            }));
        }

        function handleTypingNotification(data) {
            const { username, isTyping } = data;
            const currentUsername = new URLSearchParams(window.location.search).get('username');
            if (username === currentUsername) return;

            if (isTyping) {
                userTyping.add(username);
            } else {
                userTyping.delete(username);
            }

            updateTypingIndicator();
        }

        function updateTypingIndicator() {
            const indicator = document.getElementById("typingIndicator");
            if (userTyping.size === 0) {
                indicator.textContent = "";
                return;
            }

            const users = Array.from(userTyping);
            if (users.length === 1) {
                indicator.textContent = `${users[0]} is typing...`;
            } else if (users.length === 2) {
                indicator.textContent = `${users[0]} and ${users[1]} are typing...`;
            } else {
                indicator.textContent = `Several people are typing...`;
            }
        }

        // File Handling Functions
        function handleFileSelect(event) {
            try {
                const file = event.target.files[0];
                if (!file) return;

                const fileInfo = document.getElementById('fileInfo');
                
                if (file.size > 5 * 1024 * 1024) {
                    fileInfo.textContent = 'Error: File size must be less than 5MB';
                    event.target.value = '';
                    selectedFile = null;
                    return;
                }

                selectedFile = file;
                fileInfo.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
                
                if (file.type.startsWith('image/')) {
                    sendFile(file);
                } else {
                    document.getElementById('messageInput').placeholder = 'Add a message with your file (optional)...';
                }
            } catch (error) {
                console.error("Error handling file select:", error);
                document.getElementById('fileInfo').textContent = 'Error processing file';
            }
        }

        async function sendFile(file) {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                document.getElementById("status").textContent = "Not connected - File not sent";
                return;
            }

            try {
                const message = document.getElementById('messageInput').value.trim();
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    try {
                        const base64Data = e.target.result.split(',')[1];
                        const fileData = {
                            type: 'file',
                            data: {
                                filename: file.name,
                                fileType: file.type,
                                size: file.size,
                                data: base64Data,
                                message: message
                            }
                        };
                        
                        ws.send(JSON.stringify(fileData));
                        
                        document.getElementById('fileInput').value = '';
                        document.getElementById('messageInput').value = '';
                        document.getElementById('messageInput').placeholder = 'Type your message...';
                        document.getElementById('fileInfo').textContent = '';
                        selectedFile = null;
                    } catch (error) {
                        console.error("Error preparing file data:", error);
                    }
                };
                
                reader.readAsDataURL(file);
            } catch (error) {
                console.error("Error sending file:", error);
                document.getElementById('fileInfo').textContent = 'Error sending file';
            }
        }

        function getFileIcon(fileType) {
            if (fileType.startsWith('image/')) {
                return `<svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                </svg>`;
            } else if (fileType === 'application/pdf') {
                return `<svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>`;
            }
            return `<svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
            </svg>`;
        }

        // Chat Functions
        function sendMessage() {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                document.getElementById("status").textContent = "Not connected - Message not sent";
                return;
            }

            try {
                if (selectedFile) {
                    sendFile(selectedFile);
                } else {
                    const input = document.getElementById("messageInput");
                    const text = input.value.trim();
                    if (text) {
                        ws.send(JSON.stringify({type: "chat", data: text}));
                        input.value = "";
                    }
                }
            } catch (error) {
                console.error("Error sending message:", error);
            }
        }

        // Utility Functions
        function escapeHtml(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            else return (bytes / 1048576).toFixed(1) + ' MB';
        }

        // WebRTC Functions
        let isAudioMuted = false;
        let isVideoMuted = false;

        function toggleMute() {
            if (!localStream) return;
            
            const audioTracks = localStream.getAudioTracks();
            isAudioMuted = !isAudioMuted;
            
            audioTracks.forEach(track => {
                track.enabled = !isAudioMuted;
            });
            
            const muteBtn = document.getElementById('muteBtn');
            muteBtn.innerHTML = isAudioMuted 
                ? '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"><path d="M1 1l22 22M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/><path d="M17 16.95A7 7 0 0 1 5 12v-2m14 0v2a7 7 0 0 1-.11 1.23M12 19v4M8 23h8"/></svg>'
                : '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8"/></svg>';
        }

        function toggleVideo() {
            if (!localStream) return;
            
            const videoTracks = localStream.getVideoTracks();
            isVideoMuted = !isVideoMuted;
            
            videoTracks.forEach(track => {
                track.enabled = !isVideoMuted;
            });
            
            const videoBtn = document.getElementById('videoBtn');
            videoBtn.innerHTML = isVideoMuted
                ? '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"><path d="M1 1l22 22M9 9v3a3 3 0 0 0 5.12 2.12M15 9.34V4a3 3 0 0 0-5.94-.6"/></svg>'
                : '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"><rect x="2" y="7" width="20" height="10" rx="2" ry="2"/><circle cx="12" cy="12" r="3"/></svg>';
        }

        function endCall() {
            if (localStream) {
                localStream.getTracks().forEach(track => track.stop());
                localStream = null;
            }
            
            if (pc) {
                pc.close();
                pc = null;
            }
            
            document.getElementById('videoContainer').classList.remove('active');
            document.getElementById('localVideo').srcObject = null;
            document.getElementById('remoteVideo').srcObject = null;
        }

        async function startCall() {
            try {
                document.getElementById('videoContainer').classList.add('active');
                
                pc = new RTCPeerConnection();
                localStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
                
                localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
                document.getElementById("localVideo").srcObject = localStream;

                pc.onicecandidate = ({candidate}) => {
                    if (candidate && ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({type: "signal", data: {candidate}}));
                    }
                };

                pc.ontrack = (event) => {
                    document.getElementById("remoteVideo").srcObject = event.streams[0];
                };

                const offer = await pc.createOffer();
                await pc.setLocalDescription(offer);
                
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({type: "signal", data: {offer}}));
                }
            } catch (error) {
                console.error("Error starting call:", error);
                endCall();
            }
        }

        async function handleSignaling(data) {
            try {
                if (data.offer) {
                    if (!pc) {
                        pc = new RTCPeerConnection();
                        pc.onicecandidate = ({candidate}) => {
                            if (candidate) {
                                ws.send(JSON.stringify({type: "signal", data: {candidate}}));
                            }
                        };
                        
                        pc.ontrack = (event) => {
                            document.getElementById("remoteVideo").srcObject = event.streams[0];
                        };

                        localStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
                        localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
                        document.getElementById("localVideo").srcObject = localStream;
                    }
                    await pc.setRemoteDescription(new RTCSessionDescription(data.offer));
                    const answer = await pc.createAnswer();
                    await pc.setLocalDescription(answer);
                    ws.send(JSON.stringify({type: "signal", data: {answer}}));
                } else if (data.answer) {
                    await pc.setRemoteDescription(new RTCSessionDescription(data.answer));
                } else if (data.candidate) {
                    await pc.addIceCandidate(new RTCIceCandidate(data.candidate));
                }
            } catch (error) {
                console.error("Signaling error:", error);
            }
        }

        // Event Listeners
        document.getElementById("messageInput").addEventListener("keypress", (e) => {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Login - Simple Messenger</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0;
            background: #f0f2f5;
        }
        .login-box { 
            text-align: center; 
            padding: 30px; 
            border-radius: 8px; 
            background: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        h2 {
            color: #1a73e8;
            margin-bottom: 20px;
        }
        input { 
            width: 90%;
            margin: 10px 0; 
            padding: 8px; 
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        input:focus {
            outline: none;
            border-color: #1a73e8;
        }
        button { 
            width: 100%;
            padding: 10px; 
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background: #1557b0;
        }
        .error {
            color: #d93025;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Enter Username</h2>
        <form onsubmit="return login(event)">
            <input type="text" id="username" required minlength="3" maxlength="15" 
                   pattern="[A-Za-z0-9]+" placeholder="Choose a username"
                   title="Letters and numbers only, 3-15 characters"/>
            <div id="error" class="error"></div>
            <button type="submit">Join Chat</button>
        </form>
    </div>
    <script>
        function login(event) {
            try {
                event.preventDefault();
                const username = document.getElementById('username').value.trim();
                const error = document.getElementById('error');
                
                if (!username) {
                    error.textContent = 'Please enter a username';
                    error.style.display = 'block';
                    return false;
                }
                
                if (username.length < 3) {
                    error.textContent = 'Username must be at least 3 characters';
                    error.style.display = 'block';
                    return false;
                }
                
                if (username.length > 15) {
                    error.textContent = 'Username must be less than 15 characters';
                    error.style.display = 'block';
                    return false;
                }
                
                if (!/^[A-Za-z0-9]+$/.test(username)) {
                    error.textContent = 'Username can only contain letters and numbers';
                    error.style.display = 'block';
                    return false;
                }
                
                window.location.href = '/?username=' + encodeURIComponent(username);
                return false;
            } catch (error) {
                console.error('Login error:', error);
                return false;
            }
        }
        
        document.getElementById('username').addEventListener('input', function() {
            document.getElementById('error').style.display = 'none';
        });
    </script>
</body>
</html>
"""

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # username -> websocket
        self.user_sessions: Dict[WebSocket, str] = {}  # websocket -> username

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        self.user_sessions[websocket] = username
        # Send connection message
        await self.broadcast_system_message(username, "joined the chat")
        # Send message history
        await self.send_history(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.user_sessions:
            username = self.user_sessions[websocket]
            del self.active_connections[username]
            del self.user_sessions[websocket]
            return username
        return None

    async def send_history(self, websocket: WebSocket):
        for msg in messages:
            await websocket.send_text(json.dumps(msg))

    async def broadcast_system_message(self, username: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg_data = {
            "type": "chat",
            "data": {
                "username": username,
                "message": message,
                "timestamp": timestamp,
                "system": True
            }
        }
        # Store message in history
        messages.append(msg_data)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        # Broadcast to all
        msg_str = json.dumps(msg_data);
        for connection in self.active_connections.values():
            await connection.send_text(msg_str)

    async def broadcast_message(self, username: str, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg_data = {
            "type": "chat",
            "data": {
                "username": username,
                "message": message,
                "timestamp": timestamp
            }
        }
        # Store message in history
        messages.append(msg_data)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        # Broadcast to all
        msg_str = json.dumps(msg_data)
        for connection in self.active_connections.values():
            await connection.send_text(msg_str)

    async def broadcast_typing_notification(self, username: str, is_typing: bool):
        msg_data = {
            "type": "typing",
            "data": {
                "username": username,
                "isTyping": is_typing
            }
        }
        msg_str = json.dumps(msg_data);
        for other_username, connection in self.active_connections.items():
            if other_username != username:
                await connection.send_text(msg_str)

    async def broadcast_file(self, username: str, file_data: dict):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if file_data.get('size', 0) > MAX_FILE_SIZE:
            return False
        
        msg_data = {
            "type": "file",
            "data": {
                **file_data,
                "username": username,
                "timestamp": timestamp
            }
        }
        
        # Store in message history
        messages.append(msg_data)
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
            
        # Broadcast to all
        msg_str = json.dumps(msg_data)
        for connection in self.active_connections.values():
            await connection.send_text(msg_str)
        return True

    async def broadcast_signal(self, username: str, signal_data: dict):
        signal_msg = {
            "type": "signal",
            "data": signal_data,
            "username": username
        }
        signal_str = json.dumps(signal_msg);
        for other_username, connection in self.active_connections.items():
            if other_username != username:
                await connection.send_text(signal_str)

manager = ConnectionManager()

@app.get("/")
async def get(username: str = Query(None)):
    if not username:
        return HTMLResponse(login_html)
    return HTMLResponse(html)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg["type"] == "chat":
                await manager.broadcast_message(username, msg["data"])
            elif msg["type"] == "signal":
                await manager.broadcast_signal(username, msg["data"])
            elif msg["type"] == "file":
                success = await manager.broadcast_file(username, msg["data"])
                if not success:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "data": "File too large. Maximum size is 5MB."
                    }))
            elif msg["type"] == "typing":
                await manager.broadcast_typing_notification(username, msg["data"]["isTyping"])
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast_system_message(username, "left the chat")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
