# 🚀 Simple Messenger - Deployment Guide

This project is ready for web deployment! Choose from multiple hosting options below.

> ⚠️ **Important Update**: Heroku discontinued their free tier in November 2022. We recommend **Railway** or **Render** for free hosting.

## 📋 Quick Deploy Options

### 🎯 **One-Click Deploy** (Recommended for beginners)

**🆓 FREE Options:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https://github.com/SepehrMohammady/SimpleMessenger)
*Railway: $5 free credit monthly*
> 💡 **If button fails:** Visit [Railway.app](https://railway.app) → New Project → Deploy from GitHub repo → Select "SimpleMessenger"

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SepehrMohammady/SimpleMessenger)
*Render: 750 hours free per month*

**💰 Paid Option:**

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/SepehrMohammady/SimpleMessenger)
*Heroku: Starting at $5/month (no free tier)*

### 📁 **Configuration Files Included**

This project includes platform-specific configuration files for easy deployment:

- **`railway.json`** & **`railway.toml`**: Railway deployment configuration
- **`nixpacks.toml`**: Railway build configuration (Nixpacks)
- **`render.yaml`**: Render service configuration  
- **`app.json`**: Heroku app configuration
- **`Procfile`**: Process file for Heroku and similar platforms
- **`Dockerfile`** & **`docker-compose.yml`**: Container deployment
- **`.env.example`**: Environment variables template

---

## 🆓 **Recommended FREE Alternatives to Heroku**

### **Railway** (Best overall free option)
- **Free Tier**: $5 monthly credit (sufficient for most small apps)
- **Features**: Auto-deployments, custom domains, databases
- **Deploy**: One-click from GitHub

### **Render** (Most reliable free tier)
- **Free Tier**: 750 hours/month, auto-sleep after 15min inactivity
- **Features**: Free SSL, auto-deployments, custom domains
- **Deploy**: Connect GitHub repo directly

### **Vercel** (Best for frontend-focused apps)
- **Free Tier**: Generous limits for hobby projects
- **⚠️ Limitation**: WebSockets not supported (uses polling mode instead)
- **Features**: Edge network, instant deployments
- **Deploy**: `npx vercel` or GitHub integration

## 🛠️ **Manual Deployment Instructions**

### 1. **Heroku** (Paid plans starting from $5/month)

> ⚠️ **Note**: Heroku discontinued their free tier. The cheapest option is now "Eco" dyno at $5/month.

```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-messenger-app-name

# Deploy
git push heroku main

# Scale to Eco dyno (minimum paid plan)
heroku ps:scale web=1 --type=eco

# Open your app
heroku open
```

**Cost**: $5/month for Eco dyno  
**Environment Variables**: None required! The app works out of the box.

---

### 2. **Railway** (Modern, fast deployment)

**Option 1: One-click deploy (if button works):**
Use the Railway button above.

**Option 2: Manual Railway deployment:**
1. Visit [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" 
3. Choose "Deploy from GitHub repo"
4. Connect your GitHub account if needed
5. Search for "SimpleMessenger" or paste: `https://github.com/SepehrMohammady/SimpleMessenger`
6. Select the repository
7. Railway will auto-detect settings and deploy!

**Railway will automatically:**
- Detect Python and install dependencies
- Use the correct start command from `railway.json`
- Provide a public URL
- Handle environment variables

**Build Command:** `pip install -r requirements.txt`  
**Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

### 3. **Render** (Free tier with SSL)

1. Visit [Render.com](https://render.com)
2. Connect GitHub and select this repo
3. Choose "Web Service"
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version:** 3.11.5

---

### 4. **Vercel** (Serverless)

**⚠️ Important:** Vercel doesn't support WebSockets due to its serverless architecture. The app will run in "polling mode" with limited real-time capabilities.

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Note:** For full WebSocket functionality, use Railway or Render instead.

---

### 5. **DigitalOcean App Platform**

1. Connect your GitHub repo
2. Select Python app
3. Use auto-detected settings
4. Deploy!

---

## 🔧 **VPS/Server Deployment**

### **With Docker** (Recommended)

```dockerfile
# Create Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t messenger .
docker run -p 8000:8000 messenger
```

### **With Nginx + Gunicorn**

```bash
# Install dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

# Configure Nginx (example config in nginx.conf)
sudo systemctl restart nginx
```

---

## 🌐 **Domain Setup**

### **Custom Domain Configuration**

1. **Purchase a domain** (Namecheap, GoDaddy, etc.)
2. **Update DNS records:**
   - Point A record to your server IP
   - Or use CNAME for platform domains
3. **Enable SSL:** Most platforms provide free SSL certificates

### **Subdomain Setup**
- `chat.yourdomain.com`
- `messenger.yourdomain.com`
- `talk.yourdomain.com`

---

## 🔒 **Production Security**

### **Environment Variables** (for production)
```bash
# Optional security enhancements
export CORS_ORIGINS="https://yourdomain.com"
export MAX_FILE_SIZE="10485760"  # 10MB
export DEBUG="false"
```

### **Recommended Security Headers**
The app includes basic CORS middleware. For production, consider:
- Rate limiting
- User authentication
- Message encryption
- File upload restrictions

---

## 📊 **Monitoring & Analytics**

### **Health Check Endpoint**
- `GET /` - Returns login page (health check)
- `GET /chat` - Chat interface
- WebSocket endpoint: `/ws/{username}`

### **Logs**
- Check platform logs for WebSocket connections
- Monitor file upload activities
- Track user connections

---

## 🎯 **Performance Optimization**

### **For High Traffic**
1. **Use Redis** for message persistence
2. **Enable database** for user management
3. **Add CDN** for static files
4. **Scale horizontally** with load balancers

### **File Upload Optimization**
- Consider cloud storage (AWS S3, Cloudinary)
- Implement image compression
- Add virus scanning

---

## 🆘 **Troubleshooting**

### **Common Issues**

**Railway Deploy Button 404 Error:**
If the Railway deploy button gives a 404 error:
1. Visit [Railway.app](https://railway.app) directly
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Search for and select your forked repository
5. Railway will auto-detect the Python app and deploy

**WebSocket Connection Failed:**
- Check HTTPS/WSS protocol matching
- Verify port configuration
- Check firewall settings

**File Upload Issues:**
- Verify file size limits
- Check MIME type restrictions
- Ensure proper base64 encoding

**Deployment Fails:**
- Check Python version (3.8+ required)
- Verify requirements.txt is complete
- Check platform-specific logs

### **Debug Mode**
```bash
# Run in debug mode locally
uvicorn main:app --reload --log-level debug
```

---

## 📱 **Mobile App Conversion**

This web app is PWA-ready! Users can:
1. Visit your deployed URL on mobile
2. Tap "Add to Home Screen"
3. Use like a native app

### **PWA Features Included:**
- ✅ Offline capability
- ✅ App-like interface
- ✅ Push notifications ready
- ✅ Responsive design

---

## 🔮 **Scaling for Production**

### **Database Integration**
```python
# Add to requirements.txt
sqlalchemy
alembic
asyncpg  # for PostgreSQL
```

### **User Authentication**
```python
# Add to requirements.txt
python-jose[cryptography]
passlib[bcrypt]
python-multipart
```

### **Message Persistence**
```python
# Add to requirements.txt
redis
celery
```

---

## 📞 **Support**

- **GitHub Issues:** Report bugs and feature requests
- **Documentation:** Check README.md for features
- **Community:** Fork and contribute!

---

**🎉 Happy Deploying!** Your messenger will be live in minutes!

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
