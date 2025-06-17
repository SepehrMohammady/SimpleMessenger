# Simple Messenger - Deployment Guide

## 🚀 Production Deployment

Your modernized bilingual messenger is ready for deployment! Here's how to deploy it:

### Local Development (Current Setup)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py

# Access at: http://localhost:8000
```

### Production Deployment Options

#### 1. Cloud Platform Deployment (Recommended)

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy to Heroku
git add .
git commit -m "Ready for production"
heroku create your-messenger-app
git push heroku main
```

**Railway/Render:**
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 2. VPS/Server Deployment

**With Nginx + Gunicorn:**
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Configure Nginx reverse proxy for SSL and static files
```

### Environment Configuration

**Environment Variables:**
```bash
# Optional: Set custom port
export PORT=8000

# Optional: Set custom host
export HOST=0.0.0.0
```

**Update main.py for production (optional):**
```python
import os
# Add to main.py if needed
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
```

### SSL/HTTPS Setup

For production, enable HTTPS:
```bash
# Using Let's Encrypt with Certbot
sudo certbot --nginx -d yourdomain.com
```

### Performance Optimization

**For high traffic:**
```bash
# Use multiple workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Enable Gzip compression in Nginx
gzip on;
gzip_types text/css application/javascript application/json;
```

### Monitoring & Logging

**Add logging to main.py:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 📱 PWA Installation

Users can install your messenger as a PWA:
1. Visit the website in Chrome/Edge
2. Click the install button in the address bar
3. Or use "Add to Home Screen" on mobile

## 🌐 Features Summary

✅ **Bilingual**: English/Farsi with RTL support
✅ **Real-time Chat**: Stable WebSocket connections  
✅ **File Sharing**: Upload/download with previews
✅ **PWA**: Installable web app
✅ **Modern UI**: Responsive design with accessibility
✅ **Production Ready**: Error handling and clean code

## 🔧 Customization

**To customize further:**
- Update `static/manifest.json` for branding
- Modify CSS in templates for styling
- Add more languages to i18n dictionaries
- Implement user authentication
- Add message persistence/database

Your messenger is now ready for users! 🎉
