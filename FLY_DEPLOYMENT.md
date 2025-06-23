# 🚀 Fly.io Deployment Guide

## ✈️ **Deploy Simple Messenger to Fly.io**

### **📋 Prerequisites**

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS
   brew install fly
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up & Login:**
   ```bash
   fly auth signup  # Create account
   fly auth login   # Or login to existing account
   ```

### **🚀 Quick Deploy Steps**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SepehrMohammady/SimpleMessenger.git
   cd SimpleMessenger
   ```

2. **Deploy to Fly.io:**
   ```bash
   fly deploy
   ```

3. **Set your custom access key (optional):**
   ```bash
   fly secrets set ACCESS_KEY=YourSecureKey123
   ```

4. **Open your deployed app:**
   ```bash
   fly open
   ```

### **🔧 Configuration Details**

The repository includes a pre-configured `fly.toml` file:

```toml
app = "simple-messenger"
primary_region = "iad"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256

[env]
  PORT = "8000"
  ACCESS_KEY = "45000"
```

### **🔐 Security Setup**

#### **Change Default Access Key:**
```bash
# Set a secure access key
fly secrets set ACCESS_KEY=MySecureKey2024

# Verify secrets
fly secrets list
```

#### **View Application Logs:**
```bash
fly logs
```

### **🌍 Custom Domain (Optional)**

1. **Add your domain:**
   ```bash
   fly certs add yourdomain.com
   ```

2. **Add DNS records:**
   - **A record**: `@` → `[Fly.io IP]`
   - **AAAA record**: `@` → `[Fly.io IPv6]`

3. **Verify certificate:**
   ```bash
   fly certs check yourdomain.com
   ```

### **📊 Monitor Your App**

#### **Check Status:**
```bash
fly status
```

#### **View Metrics:**
```bash
fly dashboard
```

#### **Scale Resources (if needed):**
```bash
# Scale up memory
fly scale memory 512

# Scale to multiple machines
fly scale count 2
```

### **🔧 Advanced Configuration**

#### **Environment Variables:**
```bash
# Set multiple environment variables
fly secrets set ENVIRONMENT=production
fly secrets set DEBUG=false
fly secrets set MAX_CONNECTIONS=100
```

#### **Custom Regions:**
```bash
# Deploy to multiple regions
fly regions add fra  # Frankfurt
fly regions add nrt  # Tokyo
fly regions list
```

### **🐛 Troubleshooting**

#### **Common Issues:**

1. **App name already taken:**
   ```bash
   # Edit fly.toml and change app name
   app = "simple-messenger-yourname"
   ```

2. **Build failures:**
   ```bash
   # Check build logs
   fly logs --app simple-messenger
   
   # Force rebuild
   fly deploy --no-cache
   ```

3. **WebSocket issues:**
   ```bash
   # Check if WebSocket is working
   fly logs | grep -i websocket
   ```

4. **Memory issues:**
   ```bash
   # Increase memory
   fly scale memory 512
   ```

#### **Debug Commands:**
```bash
# SSH into your app
fly ssh console

# Check running processes
fly ssh console -C "ps aux"

# Check disk usage
fly ssh console -C "df -h"
```

### **💰 Cost Optimization**

#### **Free Tier Limits:**
- **CPU**: 1 shared vCPU
- **Memory**: 256MB RAM
- **Storage**: 3GB
- **Bandwidth**: Generous allowance

#### **Auto-scaling Settings:**
```toml
# In fly.toml
[http_service]
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0  # Saves costs when idle
```

### **🔄 Updates & Maintenance**

#### **Deploy Updates:**
```bash
git pull origin main
fly deploy
```

#### **Rollback:**
```bash
# List releases
fly releases

# Rollback to previous version
fly releases rollback
```

#### **Backup Configuration:**
```bash
# Export current configuration
fly config export > backup-fly.toml
```

### **📱 Testing Your Deployment**

1. **Get your app URL:**
   ```bash
   fly info
   ```

2. **Test features:**
   - ✅ **Login**: Use your access key
   - ✅ **Real-time chat**: Test with multiple browser tabs
   - ✅ **File upload**: Share images, documents
   - ✅ **Voice messages**: Record and playback
   - ✅ **Notifications**: Test browser notifications
   - ✅ **Mobile**: Test on smartphone

3. **Load testing:**
   ```bash
   # Test with multiple users simultaneously
   # Monitor performance with: fly dashboard
   ```

### **🎯 Production Checklist**

- ✅ **Custom access key set** (not default 45000)
- ✅ **HTTPS enabled** (automatic with Fly.io)
- ✅ **Monitoring setup** (fly dashboard)
- ✅ **Backup strategy** (git repository)
- ✅ **Domain configured** (optional)
- ✅ **Performance tested** with expected user load
- ✅ **Mobile compatibility** verified

### **🚨 Important Notes**

#### **Limitations:**
- **Free tier**: Limited resources (256MB RAM)
- **WebSocket**: Works perfectly on Fly.io
- **File uploads**: Limited by memory (5-20MB per file)
- **Concurrent users**: Depends on memory allocation

#### **Best Practices:**
- **Monitor logs** regularly: `fly logs`
- **Use secrets** for sensitive data: `fly secrets set`
- **Update regularly** to get latest features
- **Test thoroughly** before sharing with users

### **📞 Support**

- **Fly.io Docs**: https://fly.io/docs/
- **Fly.io Community**: https://community.fly.io/
- **GitHub Issues**: For app-specific problems

---

## 🎉 **Success!**

Your Simple Messenger is now deployed on Fly.io with:
- ✅ **Global CDN** for fast loading worldwide
- ✅ **Auto-scaling** to handle traffic spikes  
- ✅ **HTTPS** security built-in
- ✅ **WebSocket** support for real-time features
- ✅ **Mobile-optimized** interface
- ✅ **Notification system** for better UX

**Share your deployed URL with friends and family!** 🚀✨
