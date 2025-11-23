# Quick Fix Guide

## Current Issues & Solutions

### Issue 1: ModuleNotFoundError for fastapi

**Problem:** Packages need to be installed in your current Python environment.

**Solution:**

```bash
cd backend

# Option A: Install globally (you're using conda base)
pip install --upgrade pip
pip install -r requirements.txt

# Option B: Use conda
conda install pip
pip install -r requirements.txt
```

### Issue 2: "Client.__init__() got an unexpected keyword argument 'proxies'"

**Problem:** Old version of anthropic package or incompatible version.

**Solution:**

```bash
# Upgrade anthropic package
pip install --upgrade anthropic

# Verify version (should be 0.40.0 or higher)
python3 -c "import anthropic; print(anthropic.__version__)"
```

### Issue 3: Backend won't start

**Quick Steps:**

1. **Install packages:**
```bash
cd /Users/darrenz/Documents/GitHub/claude-builder-hackathon-2025/backend
pip install --upgrade anthropic fastapi uvicorn PyGithub beautifulsoup4 requests python-dotenv pydantic pydantic-settings python-multipart
```

2. **Create .env file:**
```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_actual_api_key_here
GITHUB_TOKEN=optional_github_token
EOF
```

Replace `your_actual_api_key_here` with your real key from https://console.anthropic.com/

3. **Run the backend:**
```bash
python3 main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Issue 4: Still getting errors?

**Check your API key:**
```bash
cd backend
cat .env
```

Make sure it starts with `sk-ant-api03-`

**Test the installation:**
```bash
python3 -c "import fastapi, anthropic, github; print('All packages installed!')"
```

**Test Anthropic client:**
```bash
python3 << 'EOF'
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found!")

try:
    client = anthropic.Anthropic(api_key=api_key)
    print("✓ Anthropic client created successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
EOF
```

### Issue 5: Chrome Extension Errors

These errors are from browser extensions and can be **ignored**:
- `userReportLinkedCandidate.json:1 Failed to load resource`
- `ResumeSwitcher: Component mounted`
- `content-all.js:1 Uncaught (in promise) Error`

They don't affect your application.

## Complete Fresh Start

If nothing works, try this complete reset:

```bash
# 1. Navigate to backend
cd /Users/darrenz/Documents/GitHub/claude-builder-hackathon-2025/backend

# 2. Remove old venv if exists
rm -rf venv

# 3. Install packages globally (since you're using conda base)
pip3 install --upgrade pip
pip3 install --upgrade anthropic fastapi uvicorn PyGithub beautifulsoup4 requests python-dotenv pydantic pydantic-settings python-multipart

# 4. Create .env (edit with your actual key!)
nano .env

# Add this line (with your real key):
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx

# 5. Run the server
python3 main.py
```

## Verification Checklist

- [ ] Python 3.12 is installed: `python3 --version`
- [ ] Packages are installed: `pip list | grep anthropic`
- [ ] .env file exists: `ls -la backend/.env`
- [ ] API key is set: `cat backend/.env`
- [ ] Backend starts: `cd backend && python3 main.py`
- [ ] Health endpoint works: `curl http://localhost:8000/api/health`
- [ ] Frontend runs: `cd front_end && npm run dev`
- [ ] Frontend loads: Open `http://localhost:5173`

## Still Having Issues?

Run this diagnostic script:

```bash
cd backend

python3 << 'EOF'
import sys
print(f"Python version: {sys.version}")

try:
    import fastapi
    print(f"✓ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"✗ FastAPI: {e}")

try:
    import anthropic
    print(f"✓ Anthropic: {anthropic.__version__}")
except ImportError as e:
    print(f"✗ Anthropic: {e}")

try:
    import github
    print(f"✓ PyGithub: {github.__version__}")
except ImportError as e:
    print(f"✗ PyGithub: {e}")

try:
    import bs4
    print(f"✓ BeautifulSoup4: {bs4.__version__}")
except ImportError as e:
    print(f"✗ BeautifulSoup4: {e}")

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print(f"✓ ANTHROPIC_API_KEY: {api_key[:20]}...")
else:
    print("✗ ANTHROPIC_API_KEY: Not found in .env")

EOF
```

This will tell you exactly what's missing or misconfigured.

