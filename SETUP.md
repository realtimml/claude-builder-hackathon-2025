# Setup Instructions

## Quick Setup (5 minutes)

### 1. Get API Keys

#### Anthropic API Key (Required)
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-api03-...`)

#### GitHub Token (Optional - for higher rate limits)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Hackathon Presenter")
4. No special scopes needed for public repos
5. Click "Generate token"
6. Copy the token (starts with `ghp_...`)

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_anthropic_key_here
GITHUB_TOKEN=your_github_token_here
EOF

# Edit .env and replace with your actual keys
nano .env  # or vim .env, or use any text editor
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

### 3. Frontend Setup

```bash
# In a new terminal
cd front_end

# Install dependencies
npm install
```

### 4. Start Both Servers

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Terminal 2 - Frontend
```bash
cd front_end
npm run dev
```

You should see:
```
➜  Local:   http://localhost:5173/
```

### 5. Open in Browser

Go to `http://localhost:5173` and you're ready to generate presentations!

## Verify Installation

Run this quick test:

```bash
# Test backend health
curl http://localhost:8000/api/health
```

Expected response:
```json
{"status":"healthy","message":"API is running"}
```

## Troubleshooting Installation

### Python not found
Install Python 3.12+ from https://www.python.org/downloads/

### npm not found
Install Node.js 18+ from https://nodejs.org/

### Permission errors
Try using `sudo` (Linux/Mac) or run terminal as Administrator (Windows)

### Port already in use
- Backend (8000): Change port in `backend/main.py` at the bottom
- Frontend (5173): Vite will automatically try the next available port

### Dependencies won't install
```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
npm cache clean --force
npm install
```

## Next Steps

Once setup is complete, check out `TESTING.md` for testing instructions!


