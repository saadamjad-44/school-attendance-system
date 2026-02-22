# PythonAnywhere Deployment Guide (No Credit Card Required)

## 🚀 Deploy on PythonAnywhere - 100% Free

### Step 1: Create Account
1. Go to **https://www.pythonanywhere.com**
2. Click **Start running Python online in less than a minute!**
3. Click **Create a Beginner account** (Free forever, no card needed)
4. Sign up with email

### Step 2: Upload Your Code
1. After login, go to **Files** tab
2. Click **Upload a file**
3. Upload your project as ZIP:
   - Download from GitHub: https://github.com/saadamjad-44/school-attendance-system/archive/refs/heads/main.zip
   - Upload to PythonAnywhere

OR use Git:
1. Go to **Consoles** tab
2. Start a **Bash console**
3. Run:
```bash
git clone https://github.com/saadamjad-44/school-attendance-system.git
cd school-attendance-system
```

### Step 3: Install Dependencies
In the Bash console:
```bash
cd school-attendance-system
pip3 install --user -r requirements.txt
python3 seed_data.py
```

### Step 4: Create Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click **Next**

### Step 5: Configure WSGI
1. In Web tab, find **WSGI configuration file** link
2. Click to edit
3. Replace ALL content with:

```python
import sys
import os

# Add your project directory
project_home = '/home/YOUR_USERNAME/school-attendance-system'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import FastAPI app
from main import app

# WSGI application
application = app
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

### Step 6: Set Working Directory
1. In Web tab, find **Working directory**
2. Set to: `/home/YOUR_USERNAME/school-attendance-system`

### Step 7: Enable Static Files
1. In Web tab, find **Static files** section
2. Add:
   - URL: `/static/`
   - Directory: `/home/YOUR_USERNAME/school-attendance-system/static/`

### Step 8: Reload & Access
1. Click **Reload** button (green button at top)
2. Your app will be live at:
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## ⚠️ Free Tier Limitations:
- One web app only
- Custom domain not available (use subdomain)
- 512MB storage
- Good enough for demo!

---

## 🎯 Easier Alternative: Replit (No Card, Instant Deploy)

### Replit Steps:
1. Go to **https://replit.com**
2. Sign up (no card needed)
3. Click **Create Repl**
4. Select **Import from GitHub**
5. Paste: `https://github.com/saadamjad-44/school-attendance-system`
6. Click **Import**
7. Replit will auto-detect and run!

Your app will be live at:
```
https://school-attendance-system.YOUR_USERNAME.repl.co
```

---

## 🎯 Simplest Option: Glitch (No Card, One Click)

### Glitch Steps:
1. Go to **https://glitch.com**
2. Sign up with GitHub (no card)
3. Click **New Project** → **Import from GitHub**
4. Paste: `https://github.com/saadamjad-44/school-attendance-system`
5. Done! Auto-deploys

---

## 📊 Comparison:

| Platform | Card Required? | Setup Time | Best For |
|----------|---------------|------------|----------|
| **Replit** | ❌ No | 2 min | Easiest |
| **Glitch** | ❌ No | 3 min | Simple |
| **PythonAnywhere** | ❌ No | 10 min | Most stable |
| Render | ✅ Yes | 5 min | Production |

---

## 🎯 My Recommendation:

**Try Replit first** - sabse aasan hai aur instantly deploy ho jata hai!

1. https://replit.com par jayen
2. GitHub se sign up karein
3. Import from GitHub
4. Done!

**Kaunsa option try karna chahte hain?**
