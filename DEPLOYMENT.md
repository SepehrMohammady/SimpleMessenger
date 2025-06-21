# 🚀 Simple Messenger - Deployment Guide

This project is ready for web deployment! Choose from multiple hosting options below.

> ⚠️ **Important Update**: Heroku discontinued their free tier in November 2022. We recommend **Railway** or **Render** for free hosting.

## 🎯 **TL;DR - Best Options by Use Case**

**🆓 Want FREE hosting with full functionality?**
→ Use **Render** (750 hours/month, WebSockets supported)

**🏃‍♂️ Want the fastest deployment?**  
→ Use **Vercel** (limited to polling mode, no real-time WebSockets)

**💰 Don't mind paying for premium features?**
→ Use **Railway** or **Heroku** ($5/month each, full functionality)

**🐳 Want to use Docker?**
→ Any VPS with Docker support or platforms like Fly.io

---

## 📋 Quick Deploy Options

### 🎯 **One-Click Deploy** (Recommended for beginners)

**🆓 FREE Options:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SepehrMohammady/SimpleMessenger)
*Render: 750 hours free per month - **RECOMMENDED FREE OPTION***

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/SepehrMohammady/SimpleMessenger)
*⚠️ Limited functionality - polling mode only (no real-time WebSockets)*

**💰 Paid Options:**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new?template=https://github.com/SepehrMohammady/SimpleMessenger)
*Railway: Starting at $5/month (no free app deployments)*

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

### **Render** (Most reliable free tier) ⭐ **RECOMMENDED**
- **Free Tier**: 750 hours/month, auto-sleep after 15min inactivity
- **Features**: Free SSL, auto-deployments, custom domains
- **Deploy**: Connect GitHub repo directly
- **WebSocket Support**: ✅ Full real-time chat functionality

### **Railway** (Now paid only)
- **⚠️ No Free Tier**: Requires paid plan starting at $5/month
- **Features**: Auto-deployments, custom domains, databases
- **Deploy**: One-click from GitHub (requires payment)

### **Vercel** (Limited functionality)
- **Free Tier**: Generous limits for hobby projects
- **⚠️ Limitation**: WebSockets not supported (uses polling mode instead)
- **Features**: Edge network, instant deployments
- **Deploy**: `npx vercel` or GitHub integration

### **Fly.io** (Another good free option)
- **Free Tier**: Generous free allowance for small apps
- **Features**: Full WebSocket support, auto-deployments
- **Deploy**: CLI-based deployment
- **WebSocket Support**: ✅ Full real-time chat functionality

```bash
# Install Fly CLI and deploy
curl -L https://fly.io/install.sh | sh
fly launch
fly deploy
```

### **PythonAnywhere** (Python-focused hosting)
- **Free Tier**: Limited but functional for small projects
- **Features**: Python-specific hosting, web-based console
- **WebSocket Support**: ⚠️ Limited on free tier
- **Deploy**: Upload files via web interface or git

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

### 2. **Railway** (Modern, fast deployment - PAID ONLY)

**⚠️ Important:** Railway no longer offers free app deployments. You need a paid plan starting at $5/month.

**Option 1: One-click deploy (requires payment):**
Use the Railway button above, but you'll need to add payment info.

**Option 2: Manual Railway deployment:**
1. Visit [Railway.app](https://railway.app) and sign up/login
2. **Add payment method** (required for app deployments)
3. Click "New Project" 
4. Choose "Deploy from GitHub repo"
5. Connect your GitHub account if needed
6. Search for "SimpleMessenger" or paste: `https://github.com/SepehrMohammady/SimpleMessenger`
7. Select the repository
8. Railway will auto-detect settings and deploy!

**Cost**: Starting at $5/month  
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

### 5. **Fly.io** (Another good free option)

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Deploy using Fly CLI:
```bash
fly launch
fly deploy
```

**WebSocket Support**: Full real-time chat functionality

---

### 6. **PythonAnywhere** (Python-focused hosting)

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create a new "Web app"
3. Choose "Manual configuration"
4. Select "Flask" and Python version
5. Upload your files via Files tab or git
6. Configure WSGI file to point to your FastAPI app

**Free Tier Limitations**: Limited CPU seconds, no custom domains on free tier

---

### 7. **Koyeb** (European alternative)

1. Visit [Koyeb.com](https://www.koyeb.com/)
2. Connect GitHub repository
3. Auto-detection will configure Python settings
4. Deploy with one click

**Features**: Global edge deployment, auto-scaling
**WebSocket Support**: ✅ Full functionality

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
⚠️ **Railway Update**: Railway no longer offers free app deployments. If you see "Limited Access" or "Requires paid plan" error:
1. **Free Alternative**: Use **Render** instead (recommended)
2. **Paid Option**: Upgrade Railway plan ($5/month) to deploy apps
3. **Manual Workaround**: Visit [Railway.app](https://railway.app) directly
   - Sign up/login with GitHub
   - Add payment method (required for apps)
   - Click "New Project" → "Deploy from GitHub repo"
   - Search for and select your forked repository

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
