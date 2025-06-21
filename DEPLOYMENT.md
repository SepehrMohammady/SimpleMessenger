# 🚀 Simple Messenger - Deployment Guide

This project is ready for web deployment! Choose from reliable hosting options below.

## 🎯 **TL;DR - Best Options**

**🆓 Want FREE hosting with full functionality?**
→ Use **Render** (750 hours/month, WebSockets supported) ⭐ **RECOMMENDED**

**� Want global edge deployment?**  
→ Use **Fly.io** (generous free tier, excellent performance)

---

## 📋 Quick Deploy Options

### 🎯 **One-Click Deploy** (Recommended)

**🆓 FREE Options:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SepehrMohammady/SimpleMessenger)
*Render: 750 hours free per month - **RECOMMENDED FREE OPTION***

**Note**: Fly.io requires CLI deployment (see manual instructions below)

### 📁 **Configuration Files Included**

This project includes platform-specific configuration files for easy deployment:

- **`render.yaml`**: Render service configuration  
- **`Dockerfile`** & **`docker-compose.yml`**: Container deployment
- **`.env.example`**: Environment variables template

---

## 🆓 **Recommended FREE Hosting Platforms**

### **Render** (Most reliable free tier) ⭐ **RECOMMENDED**
- **Free Tier**: 750 hours/month, auto-sleep after 15min inactivity
- **Features**: Free SSL, auto-deployments, custom domains
- **Deploy**: One-click from GitHub
- **WebSocket Support**: ✅ Full real-time chat functionality
- **Video Calls**: ✅ Supported with TURN servers (configured)
- **Performance**: Excellent uptime and reliability

### **Fly.io** (Global edge deployment)
- **Free Tier**: Generous free allowance for small apps
- **Features**: Global edge network, excellent performance
- **Deploy**: CLI-based deployment
- **WebSocket Support**: ✅ Full real-time chat functionality  
- **Video Calls**: ✅ Supported with TURN servers (configured)
- **Performance**: Fast worldwide deployment

```bash
# Install Fly CLI and deploy
curl -L https://fly.io/install.sh | sh
fly launch
fly deploy
```

## 🛠️ **Manual Deployment Instructions**

### 1. **Render** (Free tier with SSL)

1. Visit [Render.com](https://render.com)
2. Connect GitHub and select this repo
3. Choose "Web Service"
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version:** 3.11.5

**Features**: 
- ✅ Free SSL certificates
- ✅ Auto-deployments from GitHub
- ✅ Custom domains support
- ✅ Full WebSocket support

---

### 2. **Fly.io** (Global edge deployment)

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Deploy using Fly CLI:
```bash
fly launch
fly deploy
```

**Features**:
- ✅ Global edge network
- ✅ Full WebSocket support  
- ✅ Excellent performance worldwide
- ✅ Generous free tier

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

### **Video Call Issues** 🎥

**The app includes comprehensive WebRTC diagnostics - click the "🔧 Diagnostics" button in the chat interface to run connectivity tests.**

#### **Common Video Call Problems:**

**1. "Video call connection failed" Error:**
- **Cause**: TURN servers are blocked or unreachable
- **Solution**: 
  - Try different network (mobile hotspot, VPN)
  - Check corporate firewall settings
  - Run diagnostics tool to identify specific issues
  - Use browsers like Chrome or Firefox (better WebRTC support)

**2. "Can't hear/see each other":**
- **Camera/Microphone Permissions**: Click the camera icon in browser address bar
- **Browser Compatibility**: Use Chrome, Firefox, or Safari
- **HTTPS Required**: Video calls only work on HTTPS (both Render and Fly.io provide SSL)
- **Firewall/NAT Issues**: The app now uses multiple TURN servers for better connectivity

**3. "Connection keeps dropping":**
- **Network Instability**: Check internet connection quality
- **TURN Server Issues**: App automatically retries with different servers
- **Corporate Networks**: May block WebRTC ports (80, 443, 3478)

#### **WebRTC Connection Monitoring** 📊

The app provides detailed logging in the browser console to help diagnose issues:

**Connection States to Look For:**
- `ICE gathering state: gathering` - Discovering connection paths
- `ICE connection state: checking` - Testing connectivity options
- `ICE connection state: connected` - Successful connection established
- `Connection state: connected` - Video call is working

**Warning Signs:**
- `TURN server test timeout` - TURN servers may be blocked
- `ICE connection state: failed` - Connection cannot be established
- `Connection state: failed` - Call has failed, will attempt restart

**Console Commands for Advanced Users:**
```javascript
// Check WebRTC statistics
window.pc.getStats().then(stats => console.log(stats));

// View current ICE candidates
console.log('Local candidates:', window.pc.localDescription);
console.log('Remote candidates:', window.pc.remoteDescription);

// Test specific TURN server
runWebRTCDiagnostics(); // Built-in diagnostics function
```

**Network Quality Indicators:**
- **Excellent**: Multiple TURN servers accessible, low latency
- **Good**: Some TURN servers working, stable connection
- **Poor**: Limited connectivity, may experience drops
- **Failed**: No TURN servers accessible, calls likely to fail

#### **WebRTC Technical Requirements:**

**Browser Support:**
- ✅ Chrome 23+ (recommended)
- ✅ Firefox 22+ (recommended)
- ✅ Safari 11+ (iOS Safari 11+)
- ✅ Edge 79+
- ❌ Internet Explorer (not supported)

**Network Requirements:**
- **HTTPS**: Required for camera/microphone access
- **WebSocket**: For signaling (wss://)
- **STUN/TURN**: For NAT traversal
  - Port 80 (HTTP/WebSocket)
  - Port 443 (HTTPS/WSS/TURN)
  - Port 3478 (TURN)

**Firewall Ports:**
- **Outbound**: 80, 443, 3478 (TCP/UDP)
- **RTP/SRTP**: Dynamic port range (typically 49152-65535)

#### **Advanced Troubleshooting:**

**Run Built-in Diagnostics:**
1. Open the chat interface
2. Click "🔧 Diagnostics" button
3. Review the connectivity report
4. Share results with network administrator if needed

**Manual Browser Tests:**
1. Open browser console (F12)
2. Check for WebRTC errors
3. Look for TURN server connectivity issues
4. Verify HTTPS certificate validity

**Corporate Network Solutions:**
- Contact IT department to whitelist WebRTC ports
- Use VPN to bypass restrictions
- Consider dedicated TURN server for organization

**Custom TURN Server Setup:**
If free TURN servers are consistently blocked, consider:
- [Coturn](https://github.com/coturn/coturn) (self-hosted)
- [Twilio STUN/TURN](https://www.twilio.com/stun-turn)
- [Xirsys](https://xirsys.com/) (commercial)

### **Deployment Issues**

**Render Deployment:**
- Check Python version (3.8+ required)
- Verify requirements.txt is complete
- Check Render dashboard for build logs
- Ensure environment variables are set

**Fly.io Deployment:**
- Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
- Check `fly logs` for runtime errors
- Verify Dockerfile configuration
- Ensure app listens on correct port

**WebSocket Connection Failed:**
- Check HTTPS/WSS protocol matching
- Verify platform WebSocket support
- Check CORS configuration
- Monitor connection logs

**File Upload Issues:**
- Verify file size limits (5MB default)
- Check MIME type restrictions
- Ensure proper base64 encoding
- Monitor network upload speeds

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

**🎉 Happy Deploying!** Your messenger will be live in minutes on Render or Fly.io!

## 🌐 Features Summary

✅ **Bilingual**: English/Farsi with RTL support
✅ **Real-time Chat**: Stable WebSocket connections  
✅ **Video Calls**: WebRTC with TURN servers for cloud deployment
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
